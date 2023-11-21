from rest_framework import serializers
from django.core.files.base import File
import uuid
import os
from .models import ImageData
from .image_processing import segment, binary_image, ocr_tesseract
from .utils import str_generator


class ImageDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageData
        fields = "__all__"


class GetPhotoSerializer(serializers.Serializer):
    image = serializers.ImageField()

    def segment_process(self, image):
        return segment(image)

    def create(self, validated_data):
        obj = ImageData.objects.create(
            original_image=validated_data["image"],
            uuid=uuid.uuid4().hex[:15],
        )
        address = self.segment_process(obj.original_image.path)
        with open(address, 'rb') as f:
            image_file = File(f)
            obj.edited_image.save(
                f"image_{str_generator(4)}.jpg", image_file)
        os.remove(address)
        obj.save()
        return obj

    def save(self, **kwargs):
        return self.create(self.validated_data)


class ConfirmPhotoSerializer(serializers.Serializer):
    uuid = serializers.CharField(max_length=15)

    def validate_uuid(self, value):
        if not ImageData.objects.filter(uuid=value).exists():
            raise serializers.ValidationError("There is not exists.")
        return value

    def binary_image_process(self, image):
        return binary_image(image)

    def save(self, **kwargs):
        obj = ImageData.objects.get(uuid=self.validated_data["uuid"])
        binary_img = self.binary_image_process(obj.original_image)
        response = {"text": ocr_tesseract(binary_img)}
        return response
