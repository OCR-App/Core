from django.contrib import admin
from .models import ImageData


class ImageDataAdmin(admin.ModelAdmin):
    list_display = ("uuid",)


admin.site.register(ImageData, ImageDataAdmin)
