# crawler/views.py
import re
import requests
from django.core.files.base import ContentFile
from django.shortcuts import render
from django.http import JsonResponse
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from media.models import Photo

def index(request):
    return render(request, 'crawler/index.html')

def generate_unique_id():
    import uuid
    return str(uuid.uuid4())

def generate_unique_filename(url):
    import hashlib
    return hashlib.sha256(url.encode('utf-8')).hexdigest()

def save_photo(url, path):
    response = requests.get(url)
    if response.status_code == 200:
        photo = Photo(
            url=url,
            size=len(response.content),
            path=path,
            unique_id=generate_unique_id()
        )
        photo.image.save(f'{generate_unique_filename(url)}.jpg', ContentFile(response.content))
        photo.save()
        return photo
    return None

def crawl(request):
    url = request.GET.get('url')
    crawl_type = request.GET.get('type')
    pattern = request.GET.get('pattern', '')  # Default to empty string if pattern is not provided
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
                data['results'] = [audio['src'] for audio in soup.find_all('audio', src=True)]
                if not data['results']:
                    data['results'] = ['/static/images/notfound.png']
            elif crawl_type == 'emails':
                data['results'] = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', soup.get_text())
                if not data['results']:
                    data['results'] = ['/static/images/notfound.png']
            elif crawl_type == 'regex':
                data['results'] = re.findall(pattern, soup.get_text())
                if not data['results']:
                    data['results'] = ['/static/images/notfound.png']
        except requests.RequestException as e:
            print(f"Error fetching URL {url}: {e}")
            data['results'] = ['/static/images/notfound.png']

    return JsonResponse(data)
