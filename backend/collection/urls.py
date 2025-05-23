from django.urls import path
from .views import MangaListCreateAPIView, GlobalTitleSearchAPIView

urlpatterns = [
    path('mangas/', MangaListCreateAPIView.as_view(), name='manga-list'),
    path('titres/', GlobalTitleSearchAPIView.as_view()),
]