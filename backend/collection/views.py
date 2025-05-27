from django.shortcuts import render

from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics

from .models import Anime, AnimeImage, Manga, MangaImage, MangaTitle, AnimeTitle, Scan, ScanImage, ScanTitle
from .serializers import AnimeSerializer, MangaSerializer, UnifiedTitleSerializer


# Create your views here.
class MangaListCreateAPIView(generics.ListCreateAPIView):
    queryset = Manga.objects.all()
    serializer_class = MangaSerializer


class GlobalTitleSearchAPIView(APIView):
    def get(self, request):
        query = request.query_params.get("search", "").strip()
        if not query:
            return Response([])

        results = []

        seen = set()

        # MangaTitle
        manga_titles = MangaTitle.objects.select_related("manga").filter(
            title__icontains=query
        )

        for t in manga_titles:

            manga = t.manga
            key = f"manga-{manga.id}"
            
            if key in seen:
                continue  # déjà traité
            try:
                main = manga.manga_titles.get(is_main=True)

                # Récupération de l’image principale associée
                image = MangaImage.objects.filter(manga=manga.id).first()

                results.append(
                    {"id": manga.id,
                    "main_title": main.title,
                    "format": None,
                    "image_url": image.image if image else None,
                    "type_support": "manga",
                    "year": manga.year_start_fr,
                    "slug": manga.slug,}
                    
                    
                )
                seen.add(key)
            except MangaTitle.DoesNotExisFFt:
                continue

        # AnimeTitle
        anime_titles = AnimeTitle.objects.select_related("anime").filter(
            title__icontains=query
        )

        for t in anime_titles:
            anime = t.anime
            key = f"anime-{anime.id}"
            if key in seen:
                continue
            try:
                main = anime.anime_titles.get(is_main=True)
                image = AnimeImage.objects.filter(anime=anime.id).first()
                print("test",image)
                
                results.append(
                    {"id": anime.id,
                    "main_title": main.title,
                    "format": anime.format,
                    "image_url": image.image if image else None,
                    "type_support": "anime",
                    "year": anime.season.year,
                    "slug": anime.slug,}
                )
                seen.add(key)
            except AnimeTitle.DoesNotExist:
                continue

        # ScanTitle
        scan_titles = ScanTitle.objects.select_related("scan").filter(
            title__icontains=query
        )

        for t in scan_titles:
            scan = t.scan
            key = f"scan-{scan.id}"
            if key in seen:
                continue
            try:
                main = scan.scan_titles.get(is_main=True)
                image = ScanImage.objects.filter(scan=scan.id).first()
                
                results.append(
                    {"id": scan.id,
                    "main_title": main.title,
                    "format": None,
                    "image_url": image.image if image else None,
                    "type_support": "scan",
                    "year": scan.year_start,
                    "slug": scan.slug,}
                )
                seen.add(key)
            except ScanTitle.DoesNotExist:
                continue

        # Sérialisation
        serializer = UnifiedTitleSerializer(results, many=True)
        return Response(serializer.data)


class AnimeViewSet(viewsets.ModelViewSet):
    queryset = Anime.objects.all()
    serializer_class = AnimeSerializer
    lookup_field = "slug"

    def get_queryset(self):
        slug = self.request.query_params.get("slug")
        if slug:
            return Anime.objects.filter(slug=slug)
        return Anime.objects.all()


class EntryCountView(APIView):
    def get(self, request):
        data = {
            "anime": Anime.objects.count(),
            "manga": Manga.objects.count(),
            "scan": Scan.objects.count(),
        }
        return Response(data)