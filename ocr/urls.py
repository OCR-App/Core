from django.urls import path
from .views import GetPhoto, ConfirmPhoto, TranslateText

app_name = "ocr"

urlpatterns = [
    path("get-photo/", GetPhoto.as_view(), name="get-photo"),
    path("confirm-photo/", ConfirmPhoto.as_view(), name="confirm-photo"),
    path("translate/", TranslateText.as_view(), name="translate"),
]
