from django.urls import path
from . import views

urlpatterns = [
    path("", views.upload_zip, name="index"),
    path("blur-image/", views.blur_image, name="blur"),
    path("galleries/", views.gallery_list, name="gallery_list"),
    path("galleries/<int:gallery_id>/", views.gallery_detail, name="gallery_detail"),
    path("images/<int:image_id>/", views.image_detail, name="original_image_detail"),
]
