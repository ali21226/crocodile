# Crawl/models.py
from django.db import models
from urllib.parse import urlparse

class Photo(models.Model):
    id = models.AutoField(primary_key=True)
    url = models.URLField()
    size = models.PositiveIntegerField()
    path = models.CharField(max_length=255, null=True)
    website_name = models.CharField(max_length=255)
    image = models.ImageField(upload_to=f'images/')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    insert_time = models.DateTimeField(auto_now_add=True)  # Add this field

    def save(self, *args, **kwargs):
        if not self.website_name:
            self.website_name = self.extract_website_name(self.url)
        super().save(*args, **kwargs)

    @staticmethod
    def extract_website_name(url):
        parsed_url = urlparse(url)
        return parsed_url.netloc

class Email(models.Model):
    id = models.AutoField(primary_key=True)
    email = models.EmailField(unique=True)
    url = models.URLField()
    path = models.CharField(max_length=255, null=True)
    website_name = models.CharField(max_length=255)
    insert_time = models.DateTimeField(auto_now_add=True)  # Add this field

    def save(self, *args, **kwargs):
        if not self.website_name:
            self.website_name = self.extract_website_name(self.url)
        super().save(*args, **kwargs)

    @staticmethod
    def extract_website_name(url):
        parsed_url = urlparse(url)
        return parsed_url.netloc

class Audio(models.Model):
    id = models.AutoField(primary_key=True)
    url = models.URLField()
    size = models.PositiveIntegerField()
    path = models.CharField(max_length=255, null=True, blank=True)
    website_name = models.CharField(max_length=255)
    audio = models.FileField(upload_to='audios/')
    insert_time = models.DateTimeField(auto_now_add=True)  # Add this field

    def save(self, *args, **kwargs):
        if not self.website_name:
            self.website_name = self.extract_website_name(self.url)
        super().save(*args, **kwargs)

    @staticmethod
    def extract_website_name(url):
        parsed_url = urlparse(url)
        return parsed_url.netloc
