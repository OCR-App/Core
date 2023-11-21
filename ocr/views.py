from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import GetPhotoSerializer, ImageDataSerializer, ConfirmPhotoSerializer


class GetPhoto(APIView):
    def post(self, request):
        serializer = GetPhotoSerializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid(raise_exception=True):
            obj = serializer.save()
            data = ImageDataSerializer(obj).data
            return Response(data, status=status.HTTP_200_OK)


class ConfirmPhoto(APIView):
    def post(self, request):
        serializer = ConfirmPhotoSerializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid(raise_exception=True):
            response = {"text": serializer.save()}
            return Response(response, status=status.HTTP_200_OK)
