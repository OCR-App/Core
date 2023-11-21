from django.urls import path
from .views import GetPhoto, ConfirmPhoto

app_name = "ocr"

urlpatterns = [
    path("get-photo/", GetPhoto.as_view(), name="get-photo"),
    path("confirm-photo/", ConfirmPhoto.as_view(), name="confirm-photo"),
]
