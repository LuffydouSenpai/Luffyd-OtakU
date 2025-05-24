from rest_framework import serializers
from .models import Manga, Anime, AnimeImage, AnimeTitle


class AnimeTitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnimeTitle
        fields = ["title", "is_main", "is_original", "is_nickname"]


class AnimeImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnimeImage
        fields = ["image", "description"]

class AnimeSerializer(serializers.ModelSerializer):

    titles = AnimeTitleSerializer(source="anime_titles", many=True, read_only=True)
    images = AnimeImageSerializer(source="animeImage", many=True, read_only=True)

    class Meta:
        model = Anime
        fields = "__all__"  #for development and explicit list for production ['title', 'author', 'release_date']







class MangaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manga
        fields = "__all__"  # ou liste explicite ['title', 'author', 'release_date']


class UnifiedTitleSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    main_title = serializers.CharField()
    type = serializers.CharField()
