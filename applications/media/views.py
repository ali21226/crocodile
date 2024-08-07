# media/views.py
import requests
from django.core.files.base import ContentFile
from django.utils.crypto import get_random_string
from .models import Photo, Audio
from io import BytesIO
from PIL import Image
from urllib.parse import urlparse
from django.shortcuts import render


def media_list(request):
    photos = Photo.objects.all()
    audios = Audio.objects.all()
    return render(request, 'media/templates/media/media_list.html', {'photos': photos, 'audios': audios})


def save_photo(url, path):
    response = requests.get(url)
    if response.status_code == 200:
        photo = Photo(
            url=url,
            size=len(response.content),
            path=path
        )
        photo.image.save(f'{generate_unique_filename(url)}.jpg', ContentFile(response.content))

        # Create and save avatar
        avatar_io = BytesIO()
        image = Image.open(BytesIO(response.content))
        image.thumbnail((50, 50))
        image.save(avatar_io, format='JPEG')
        avatar_io.seek(0)
        photo.avatar.save(f'avatar_{generate_unique_filename(url)}.jpg', ContentFile(avatar_io.read()))

        photo.save()


def generate_unique_filename(url):
    return get_random_string(10)


def extract_website_name(url):
    parsed_url = urlparse(url)
    return parsed_url.netloc
