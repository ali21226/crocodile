import re
import requests
from django.core.files.base import ContentFile
from django.shortcuts import render
from django.http import JsonResponse
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from .models import CrawledImage

def index(request):
    return render(request, 'crawler/index.html')

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
                            img_response = requests.get(img_url)
                            img_response.raise_for_status()  # Check if the request was successful
                            img_name = urlparse(img_url).path.split("/")[-1]
                            img = CrawledImage(url=img_url)
                            img.image.save(img_name, ContentFile(img_response.content), save=True)
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
