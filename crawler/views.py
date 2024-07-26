from django.shortcuts import render
from django.http import JsonResponse
from django.core.exceptions import ValidationError
import requests
from bs4 import BeautifulSoup
import re
from .url_validate import standardize_url  # Import your URL validation function


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

    # Validate and standardize the URL
    standardized_url = standardize_url(url)

    if standardized_url is None:
        return JsonResponse({'error': 'URL invalid'}, status=400)

    if url:
        try:
            response = requests.get(standardized_url)
            soup = BeautifulSoup(response.content, 'html.parser')

            if crawl_type == 'photos':
                data['results'] = [img['src'] for img in soup.find_all('img', src=True)]
            elif crawl_type == 'voices':
                data['results'] = [audio['src'] for audio in soup.find_all('audio', src=True)]
            elif crawl_type == 'emails':
                data['results'] = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', soup.get_text())
            elif crawl_type == 'regex':
                pattern = request.GET.get('pattern')
                data['results'] = re.findall(pattern, soup.get_text())

        except requests.RequestException as e:
            return JsonResponse({'error': 'Failed to fetch the URL'}, status=500)

    return JsonResponse(data)
