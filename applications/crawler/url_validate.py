from urllib.parse import urlparse, urlunparse


def standardize_url(url):
    try:
        parsed_url = urlparse(url)

        # If the URL starts with 'www.', remove it
        if parsed_url.netloc.startswith('www.'):
            netloc = parsed_url.netloc[4:]
        else:
            netloc = parsed_url.netloc

        # Add 'https://' if no scheme is present
        if not parsed_url.scheme:
            scheme = 'https'
        else:
            scheme = parsed_url.scheme

        # Rebuild the URL
        standardized_url = urlunparse(
            (scheme, netloc, parsed_url.path, parsed_url.params, parsed_url.query, parsed_url.fragment))
        return standardized_url
    except Exception:
        return None
