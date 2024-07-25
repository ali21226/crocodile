from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('crawler.urls')),  # This should route the root URL to crawler.urls
]
    