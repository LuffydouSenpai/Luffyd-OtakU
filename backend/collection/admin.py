from django.contrib import admin
from django.utils.html import format_html
from .models import Anime, Genre, Theme, AnimeImage, AnimeTitle, RelationAnime
from .forms import AnimeForm



#genre et theme
@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)
    exclude = ('slug',)  # Exclut le champ 'slug' du formulaire

@admin.register(Theme)
class ThemeAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)
    exclude = ('slug',)  # Exclut le champ 'slug' du formulaire
    
    

# anime
@admin.register(Anime)
class AnimeAdmin(admin.ModelAdmin):

    form = AnimeForm  # Associe le formulaire personnalisé à l'admin
    
    
    list_display = ('id', 'main_title', 'image_previews', 'slug')
    search_fields = ['main_title']
    list_filter = ('genres', 'themes')
    filter_horizontal = ('genres', 'themes')  # meilleure UX pour les ManyToMany
    exclude = ('slug',)  # Exclut le champ 'slug' du formulaire
    
    def save_model(self, request, obj, form, change):
        # Sauvegarde de l'objet Anime
        super().save_model(request, obj, form, change)

        # Crée un AnimeTitle automatiquement si on est en création et qu'un titre est fourni
        if not change and 'main_title' in form.cleaned_data:
            AnimeTitle.objects.create(
                anime=obj,
                title=form.cleaned_data['main_title'],
                language_code='jp',
                is_main=True  # si tu as ce champ, sinon enlève cette ligne
            )
     
    def image_previews(self, obj):
        images = obj.images.all()  # Récupère toutes les images de cet anime
        preview_html = ''
        for image in images:
            preview_html += f'<img src="{image.image.url}" width="75" height="100" style="margin-right:5px;" />'
        return format_html(preview_html) if images else 'Aucune image'
    
    image_previews.allow_tags = True  # Permet d'afficher le HTML dans l'admin
    image_previews.short_description = 'Aperçu des images'  # Titre de la colonne

@admin.register(AnimeImage)
class AnimeImageAdmin(admin.ModelAdmin):
    autocomplete_fields = ['anime']
    list_display = ('anime', 'description', 'image_preview')
    search_fields = ('anime__main_title', 'description')
    list_filter = ('anime',)

    def image_preview(self, obj):
        return format_html(
                '<img src="{}" width="75" height="100" style="margin-right:5px;" />',
                obj.image.url
            )
    image_preview.allow_tags = True  # Permet d'afficher le HTML dans l'admin
    image_preview.short_description = 'Aperçu de l\'image'
     
@admin.register(AnimeTitle)
class AnimeTitleAdmin(admin.ModelAdmin):
    autocomplete_fields = ['anime']
    search_fields = ['anime__main_title']
    
    def get_search_results(self, request, queryset, search_term):
        print(f"Recherche avec le terme : {search_term}")
        return super().get_search_results(request, queryset, search_term)
    
    list_display = ('anime', 'title', 'language_code', 'is_original', 'is_nickname','is_main', 'slug')
    search_fields = ('title', 'language_code', 'slug')
    list_filter = ('is_original', 'is_nickname', 'language_code')
    exclude = ('slug',)  # Exclut le champ 'slug' du formulaire
    
@admin.register(RelationAnime)
class RelationAnimeAdmin(admin.ModelAdmin):
    list_display = ('anime_source', 'relation_type', 'anime_target')
    search_fields = (
        'anime_source__title',
        'anime_target__title',
        'relation_type',
    )
    autocomplete_fields = ('anime_source', 'anime_target')
    


#manga
