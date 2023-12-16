import json
import zipfile
import os
import io
from PIL import ImageOps
from PIL import Image as PILImage
from PIL import ImageFilter
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Count, Q
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.core.files import File

from .forms import ZipUploadForm
from .models import Gallery, OriginalImage, BlurredImage
from .utils import scale_coords


@login_required
@csrf_exempt
def blur_image(request):
    if request.method == "POST":
        try:
            print("Received POST request")
            blur_coords = json.loads(request.POST.get("coords"))
            original_image_id = request.POST.get("original_image_id")
            display_width = float(request.POST.get("display_width"))
            display_height = float(request.POST.get("display_height"))
            print(f"Coords: {blur_coords}")
            print(f"Original Image ID: {original_image_id}")
            if original_image_id:
                original_image_instance = OriginalImage.objects.get(
                    id=original_image_id
                )
                original_image_path = original_image_instance.original_photo.path

                print(f"Original image path: {original_image_path}")

                with PILImage.open(original_image_path) as image:
                    print(f"Original image size: {image.size}")
                    image = ImageOps.exif_transpose(image)

                    # Scaling coordinates
                    scaled_coords = scale_coords(
                        blur_coords, image.size, (display_width, display_height)
                    )
                    x, y, width, height = (
                        scaled_coords["x"],
                        scaled_coords["y"],
                        scaled_coords["width"],
                        scaled_coords["height"],
                    )

                    cropped_area = image.crop((x, y, x + width, y + height))
                    print(f"Cropped area size: {cropped_area.size}")

                    blurred_area = cropped_area.filter(
                        ImageFilter.GaussianBlur(radius=15)
                    )
                    image.paste(blurred_area, (x, y, x + width, y + height))

                    img_byte_arr = io.BytesIO()
                    image.save(img_byte_arr, format="JPEG", quality=95)
                    img_byte_arr.seek(0)

                new_image_name = f"blurred-{os.path.basename(original_image_instance.original_photo.name)}"
                print(f"New image name: {new_image_name}")

                blurred_image = BlurredImage(
                    original_image=original_image_instance,
                    blured_photo=File(
                        io.BytesIO(img_byte_arr.getvalue()), name=new_image_name
                    ),
                )
                blurred_image.save()
                original_image_instance.is_blurred = True
                original_image_instance.save()

                print("Image blurred and saved successfully")

                return JsonResponse({"message": "Image blurred successfully"})

        except Exception as e:
            print(f"Error: {e}")
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request"}, status=400)


@login_required
def upload_zip(request):
    if request.method == "POST":
        form = ZipUploadForm(request.POST, request.FILES)
        if form.is_valid():
            zip_file = request.FILES["zip_file"]
            gallery_name = os.path.splitext(zip_file.name)[0]
            gallery = Gallery.objects.create(name=gallery_name, user=request.user)

            with zipfile.ZipFile(zip_file, "r") as zip_ref:
                for file_name in zip_ref.namelist():
                    if file_name.lower().endswith((".png", ".jpg", ".jpeg")):
                        zip_ref.extract(file_name, settings.MEDIA_ROOT)
                        image_file_path = os.path.join(settings.MEDIA_ROOT, file_name)
                        OriginalImage.objects.create(
                            gallery=gallery, original_photo=image_file_path
                        )

            return redirect("gallery_list")
    else:
        form = ZipUploadForm()

    return render(request, "blur/upload_zip.html", {"form": form})


@login_required
def gallery_list(request):
    galleries = (
        Gallery.objects.filter(user=request.user)
        .annotate(
            total_images=Count("original_images"),
            not_blurred_images=Count(
                "original_images", filter=Q(original_images__is_blurred=False)
            ),
        )
        .order_by("-created_at")
    )
    return render(request, "blur/gallery_list.html", {"galleries": galleries})


@login_required
def gallery_detail(request, gallery_id):
    gallery = get_object_or_404(Gallery, id=gallery_id)

    # Filter to show only unblurred images
    show_unblurred = request.GET.get("show_unblurred", "false") == "true"
    images = gallery.original_images.all()
    if show_unblurred:
        images = images.filter(is_blurred=False)

    context = {"gallery": gallery, "original_images": images}
    return render(request, "blur/gallery_detail.html", context)


@login_required
def image_detail(request, image_id):
    image = get_object_or_404(OriginalImage, id=image_id)
    gallery = image.gallery
    images_in_gallery = list(gallery.original_images.all().order_by("id"))
    current_index = images_in_gallery.index(image)

    previous_image_id = None
    next_image_id = None
    show_modal = False

    if current_index > 0:
        previous_image_id = images_in_gallery[current_index - 1].id
    if current_index < len(images_in_gallery) - 1:
        next_image_id = images_in_gallery[current_index + 1].id
    else:
        show_modal = True

    return render(
        request,
        "blur/image_detail.html",
        {
            "image": image,
            "gallery": gallery,
            "previous_image_id": previous_image_id,
            "next_image_id": next_image_id,
            "show_modal": show_modal,
        },
    )


@login_required
def delete_gallery(request, gallery_id):
    if request.method == "POST":
        gallery = get_object_or_404(Gallery, id=gallery_id, user=request.user)
        gallery.delete()
        return JsonResponse({"success": True})

    return JsonResponse({"success": False})


@login_required
def download_blurred_images(request, gallery_id):
    gallery = get_object_or_404(Gallery, id=gallery_id)

    # Create archive
    response = HttpResponse(content_type="application/zip")
    zip_file = zipfile.ZipFile(response, "w")

    for image in gallery.original_images.filter(is_blurred=True):
        blurred_image = image.blurred_image.blured_photo
        file_path = os.path.join(settings.MEDIA_ROOT, blurred_image.name)

        # Remove the prefix 'blured-' from the file name
        original_file_name = os.path.basename(file_path).replace("blurred-", "")

        zip_file.write(file_path, original_file_name)

    zip_file.close()
    response["Content-Disposition"] = f"attachment; filename=Blured-{gallery.name}.zip"

    return response
