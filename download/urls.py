from django.urls import path
from . import views

urlpatterns = [
    path('', views.downloader_home, name='downloader_home'),
    path('download-stream/', views.processing_download, name='processing_download'),
]
