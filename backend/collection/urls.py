from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import (
    EntryCountView,
    MangaListCreateAPIView,
    GlobalTitleSearchAPIView,
    AnimeViewSet,
)

# Router pour les ViewSet
router = DefaultRouter()
router.register(r'animes', AnimeViewSet)  # /api/animes/

urlpatterns = [
    path('mangas/', MangaListCreateAPIView.as_view(), name='manga-list'),
    path('entry_count/', EntryCountView.as_view(), name='entry-count'),
    path('titres/', GlobalTitleSearchAPIView.as_view()), 
]

# Ajoute les routes du router à urlpatterns
urlpatterns += router.urls