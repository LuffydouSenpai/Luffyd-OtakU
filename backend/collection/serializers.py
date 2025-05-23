from rest_framework import serializers
from .models import Manga

class MangaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manga
        fields = '__all__'  # ou liste explicite ['title', 'author', 'release_date']
        

class UnifiedTitleSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    main_title = serializers.CharField()
    type = serializers.CharField()