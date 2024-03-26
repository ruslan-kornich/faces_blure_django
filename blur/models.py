import os

from django.db import models
from django.utils.text import slugify
from accounts.models import CustomUser


def get_blurred_image_path(instance, filename):
    gallery_name_slug = slugify(instance.original_image.gallery.name)
    return os.path.join("photos", "blurred_images", gallery_name_slug, filename)


def get_original_image_path(instance, filename):
    gallery_name_slug = slugify(instance.gallery.name)
    return os.path.join("photos", "original_images", gallery_name_slug, filename)


class Gallery(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(
        CustomUser, related_name="galleries", on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f" {self.name} - {self.created_at}"


class OriginalImage(models.Model):
    gallery = models.ForeignKey(
        Gallery, related_name="original_images", on_delete=models.CASCADE
    )
    original_photo = models.ImageField(upload_to=get_original_image_path)
    is_blurred = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.gallery.name} - Original Image {self.id}"


class BlurredImage(models.Model):
    original_image = models.OneToOneField(
        OriginalImage, on_delete=models.CASCADE, related_name="blurred_image"
    )
    blured_photo = models.ImageField(upload_to=get_blurred_image_path)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.original_image.gallery.name} - Blurred Image {self.id}"
