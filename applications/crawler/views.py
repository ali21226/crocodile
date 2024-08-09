# crawler/views.py
import re
import os
from django.conf import settings
from django.core.files.base import ContentFile
from django.shortcuts import render
from django.http import JsonResponse
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import requests
from django.utils.crypto import get_random_string
from applications.Crawl.models import Photo, Email, Audio
from io import BytesIO


def index(request):
    return render(request, '../../../applications/crawler/templates/crawler/index.html')


def save_photo(url, path):
    response = requests.get(url)
    if response.status_code == 200:
        photo = Photo(
            url=url,
            size=len(response.content),
            path=path,
            website_name=extract_website_name(url),
        )
        photo.image.save(f'{generate_unique_filename(url)}.jpg', ContentFile(response.content))

        # Create and save avatar
        avatar_io = BytesIO()
        # image = Image.open(BytesIO(response.content))
        # image.thumbnail((50, 50))
        # image.save(avatar_io, format='JPEG')
        avatar_io.seek(0)
        photo.avatar.save(f'avatar_{generate_unique_filename(url)}.jpg', ContentFile(avatar_io.read()))

        photo.save()
        return photo


def save_email_to_db(email, url, website_name):
    Email.objects.get_or_create(
        email=email,
        url=url,
        website_name=website_name
    )


def save_emails_to_file(emails, website_name):
    directory = os.path.join(settings.MEDIA_ROOT, 'Email')
    if not os.path.exists(directory):
        os.makedirs(directory)
    filename = f"{website_name}.txt"
    file_path = os.path.join(directory, filename)
    with open(file_path, 'w') as f:
        for email in emails:
            f.write(f"{email}\n")
    return file_path


def generate_unique_filename(url):
    return get_random_string(10)


def extract_website_name(url):
    parsed_url = urlparse(url)
    return parsed_url.netloc

def save_audio(url, path):
    response = requests.get(url)
    if response.status_code == 200:
        file_name = generate_unique_filename(url) + os.path.splitext(url)[1]  # Use original file extension
        audio = Audio(
            url=url,
            size=len(response.content),
            path=path,
            website_name=extract_website_name(url),
        )
        audio.audio.save(file_name, ContentFile(response.content))
        audio.save()
        return audio
    return None



def crawl(request):
    url = request.GET.get('url')
    crawl_type = request.GET.get('type')
    pattern = request.GET.get('pattern', '')
    data = {
        'url': url,
        'type': crawl_type,
        'results': []
    }

    if url:
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url

        try:
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            website_name = extract_website_name(url)

            if crawl_type == 'photos':
                images = [img['src'] for img in soup.find_all('img', src=True)]
                if images:
                    for img_url in images:
                        img_url = urljoin(url, img_url)  # Ensure the image URL is absolute
                        try:
                            img = save_photo(img_url, url)
                            if img:
                                data['results'].append(img.image.url)
                        except requests.RequestException as e:
                            print(f"Error fetching image {img_url}: {e}")
                if not data['results']:
                    data['results'] = ['/static/images/notfound.png']

            elif crawl_type == 'voices':
                audio_urls = [audio['src'] for audio in soup.find_all('audio', src=True)]
                audio_urls += [source['src'] for source in soup.find_all('source', src=True)]
                if audio_urls:
                    for audio_url in audio_urls:
                        audio_url = urljoin(url, audio_url)
                        try:
                            audio = save_audio(audio_url, url)
                            if audio:
                                data['results'].append(audio.audio.url)
                        except requests.RequestException as e:
                            print(f"Error fetching audio {audio_url}: {e}")
                if not data['results']:
                    data['results'] = ['/static/images/notfound.png']

            elif crawl_type == 'emails':
                emails = re.findall(r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}', soup.get_text())
                if emails:
                    for email in emails:
                        save_email_to_db(email, url, website_name)
                    file_path = save_emails_to_file(emails, website_name)
                    data['results'] = emails
                    data['file_path'] = file_path
                else:
                    data['results'] = ['/static/images/notfound.png']

            elif crawl_type == 'regex':
                data['results'] = re.findall(pattern, soup.get_text())
                if not data['results']:
                    data['results'] = ['/static/images/notfound.png']

        except requests.RequestException as e:
            print(f"Error fetching URL {url}: {e}")
            data['results'] = ['/static/images/notfound.png']

    return JsonResponse(data)
