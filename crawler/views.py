from django.shortcuts import render
from django.http import JsonResponse
import requests
from bs4 import BeautifulSoup
import re

def index(request):
    return render(request, 'crawler/index.html')

def crawl(request):
    url = request.GET.get('url')
    crawl_type = request.GET.get('type')
    data = {
        'url': url,
        'type': crawl_type,
        'results': []
    }

    if url:
        # Check and prepend "https://" if necessary
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url

        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.content, 'html.parser')

            if crawl_type == 'photos':
                images = [img['src'] for img in soup.find_all('img', src=True)]
                if not images:
                    images = ['/static/images/not_found.png']
                data['results'] = images
            elif crawl_type == 'voices':
                data['results'] = [audio['src'] for audio in soup.find_all('audio', src=True)]
                if not data['results']:
                    data['results'] = ['/static/images/not_found.png']
            elif crawl_type == 'emails':
                data['results'] = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', soup.get_text())
                if not data['results']:
                    data['results'] = ['/static/images/not_found.png']
            elif crawl_type == 'regex':
                pattern = request.GET.get('pattern')
                data['results'] = re.findall(pattern, soup.get_text())
                if not data['results']:
                    data['results'] = ['/static/images/not_found.png']
        except requests.RequestException as e:
            # Handle the case where the URL is invalid or the request fails
            data['results'] = ['/static/images/not_found.png']

    return JsonResponse(data)
