from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about', views.about, name='about'),
    path('identify-emotion', views.identifyEmotion, name='identify-emotion'),
    path('speech-emotion', views.speechEmotion, name='speech-emotion'),
    path('facial-emotion', views.facialEmotion, name='facial-emotion'),
    path('recommend-genres', views.recGenres, name='recommend-genres'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
