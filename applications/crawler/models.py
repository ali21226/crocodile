from django.db import models

class CrawledImage(models.Model):
    url = models.URLField(max_length=200, null=False, blank=False)
    image = models.ImageField(upload_to=f'images/')
