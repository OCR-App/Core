from django.db import models
from django.utils.translation import gettext_lazy as _


class ImageLanguages(models.TextChoices):
    NONE = ("none", "None")
    PERSIAN = ("persian", "Persian")
    ENGLISH = ("english", "English")


class ImageData(models.Model):
    original_image = models.ImageField(
        _("Original Image"), upload_to="original_image/")
    edited_image = models.ImageField(
        _("Edited Image"), upload_to="edited_image/", null=True, blank=True)
    uuid = models.CharField(_("Uuid"), max_length=15)
    result = models.TextField(_("Result"), null=True, blank=True)
    lang = models.CharField(max_length=7, verbose_name=_(
        "Language"), choices=ImageLanguages.choices, default=ImageLanguages.NONE)

    def __str__(self) -> str:
        return self.uuid
