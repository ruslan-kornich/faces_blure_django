from django.contrib import admin
from .models import Gallery, OriginalImage, BlurredImage


@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    list_display = ("name", "user")
    list_filter = ("user",)
    search_fields = ("name",)


@admin.register(OriginalImage)
class ImageAdmin(admin.ModelAdmin):
    list_display = ("gallery", "original_photo")
    list_filter = ("gallery",)
    search_fields = ("gallery__name",)


@admin.register(BlurredImage)
class BluredImageAdmin(admin.ModelAdmin):
    list_display = ("blured_photo",)
