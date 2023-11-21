from rest_framework import serializers
from django.core.files.base import File
from AI.Segmentation_Module import segment
from AI.binary_module import black_and_white
from AI.Tesseract_Library import ocr_tesseract
from .models import ImageData, ImageLanguages
from .utils import str_generator
import uuid
import cv2
import os


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

    def validate_uuid(self, value):
        if not ImageData.objects.filter(uuid=value).exists():
            raise serializers.ValidationError("There is not exists.")
        return value

    def binary_image_process(self, image_path):
        image = cv2.imread(image_path)
        return black_and_white(image)

    def ocr_tesseract_process(self, image, lang):
        return ocr_tesseract(image, lang)

    def save(self, **kwargs):
        obj = ImageData.objects.get(uuid=self.validated_data["uuid"])
        binary_img = self.binary_image_process(obj.original_image.path)
        text = self.ocr_tesseract_process(binary_img, obj.lang)
        return text
