from rest_framework import serializers
from django.core.files.base import File
from AI.Segmentation_Module import segment
from AI.binary_module import black_and_white
from AI.Tesseract_Library import ocr_tesseract
from AI.ocr import OCR
from .models import ImageData, ImageLanguages
from .utils import str_generator
from googletrans import Translator
import uuid
import cv2
import os
from spellchecker import SpellChecker


class ImageDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageData
        fields = "__all__"


class GetPhotoSerializer(serializers.Serializer):
    image = serializers.ImageField()
    lang = serializers.CharField()

    def validate_lang(self, value):
        if value not in [ImageLanguages.ENGLISH, ImageLanguages.PERSIAN]:
            raise serializers.ValidationError(
                "You can choose persian or english.")
        return value

    def segment_process(self, image):
        image_data = segment(image)
        path = f"temp_{str_generator(4)}.png"
        cv2.imwrite(path, image_data)
        return os.path.abspath(path)

    def create(self, validated_data):
        obj = ImageData.objects.create(
            original_image=validated_data["image"],
            uuid=uuid.uuid4().hex[:15],
            lang=validated_data["lang"],
        )
        address = self.segment_process(obj.original_image.path)
        with open(address, 'rb') as f:
            image_file = File(f)
            obj.edited_image.save(
                f"image_{str_generator(4)}.jpg", image_file)
        obj.save()
        os.remove(address)
        return obj

    def save(self, **kwargs):
        return self.create(self.validated_data)


class ConfirmPhotoSerializer(serializers.Serializer):
    uuid = serializers.CharField(max_length=15)
    model = serializers.CharField(max_length=15)

    def validate_uuid(self, value):
        if not ImageData.objects.filter(uuid=value).exists():
            raise serializers.ValidationError("There is not exists.")
        return value

    def validate_model(self, value):
        if value not in ("custom", "tesseract"):
            raise serializers.ValidationError(
                "You can choose custom or tesseract.")
        return value

    def binary_image_process(self, image_path):
        image = cv2.imread(image_path)
        return black_and_white(image)

    def ocr_tesseract_process(self, image, lang):
        return ocr_tesseract(image, lang)

    def post_process(self, word: str, saved_words: str):
        spell = SpellChecker()
        spell.word_frequency.load_words(saved_words)
        misspelled = spell.unknown([word])
        data = None
        for item in misspelled:
            data = spell.candidates(item)
        if data is not None:
            if word in list(data):
                return word
            else:
                temp = list(
                    filter(lambda x: len(x) == len(word), list(data)))
                if len(temp) == 0:
                    return word
                else:
                    return self.string_similarity(word, list(data))
        else:
            return word

    def post_process_main(self, text: str):
        with open("cleaned_words.txt", 'r') as file:
            saved_words = file.read().splitlines()
        words = "".join(text).split(" ")
        for i, item in enumerate(words):
            new_word = self.post_process(item, saved_words)
            words[i] = new_word
        return words

    def string_similarity(self, str1, data: list):
        result = list()
        len_str1 = len(str1)
        for item in data:
            len_str2 = len(item)
            min_len = min(len_str1, len_str2)
            match_count = sum(c1 == c2 for c1, c2 in zip(str1, item))
            similarity_percentage = (match_count / min_len) * 100
            result.append((similarity_percentage, item))
        max_ = result[0][0]
        index = 0
        for i, item in enumerate(result):
            if item[0] > max_:
                max_ = item[0]
                index = i
        return result[index][1]

    def custom_model_process(self, path):
        image = cv2.imread(path)
        text = OCR(image)
        words = self.post_process_main(text)
        return " ".join(words)
        # return "".join(text)

    def save(self, **kwargs):
        obj = ImageData.objects.get(uuid=self.validated_data["uuid"])
        if self.validated_data["model"] == "custom":
            text = self.custom_model_process(obj.original_image.path)
        else:
            binary_img = self.binary_image_process(obj.original_image.path)
            text = self.ocr_tesseract_process(binary_img, obj.lang)
        return text


class TranslateTextSerializer(serializers.Serializer):
    text = serializers.CharField()

    def translate_to_persian(self, text: str):
        translator = Translator()
        translation = translator.translate(text, dest='fa')
        return translation.text

    def save(self, **kwargs):
        return self.translate_to_persian(self.validated_data["text"])
