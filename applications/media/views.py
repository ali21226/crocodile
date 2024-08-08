# media/views.py
import requests
from django.core.files.base import ContentFile
from django.utils.crypto import get_random_string
from .models import Photo, Audio
from io import BytesIO
from PIL import Image
from urllib.parse import urlparse
from django.shortcuts import render
from django.http import JsonResponse

def media_list(request):
    photos = Photo.objects.all()
    audios = Audio.objects.all()
    return render(request, 'media/media_list.html', {'photos': photos, 'audios': audios})

def save_photo(url, path, unique_photos):
    response = requests.get(url)
    if response.status_code == 200:
        if unique_photos:
            photo, created = Photo.objects.get_or_create(
                url=url,
                defaults={
                    'size': len(response.content),
                    'path': path,
                }
            )

            if created:
                save_photo_file(photo, response.content)
        else:
            photo = Photo.objects.create(
                url=url,
                size=len(response.content),
                path=path
            )
            save_photo_file(photo, response.content)

def save_photo_file(photo, content):
    photo.image.save(f'{generate_unique_filename(photo.url)}.jpg', ContentFile(content))

    avatar_io = BytesIO()
    image = Image.open(BytesIO(content))
    image.thumbnail((50, 50))
    image.save(avatar_io, format='JPEG')
    avatar_io.seek(0)
    photo.avatar.save(f'avatar_{generate_unique_filename(photo.url)}.jpg', ContentFile(avatar_io.read()))

    photo.save()

def generate_unique_filename(url):
    return get_random_string(10)

def extract_website_name(url):
    parsed_url = urlparse(url)
    return parsed_url.netloc

def crawl(request):
    url = request.GET.get('url')
    unique_photos = request.GET.get('unique_photos') == 'true'
    type = request.GET.get('type')
    pattern = request.GET.get('pattern')

    results = crawl_website(url, type, pattern, unique_photos)

    return JsonResponse({'results': results})

def crawl_website(url, type, pattern, unique_photos):
    return ['example_image_url_1', 'example_image_url_2']
