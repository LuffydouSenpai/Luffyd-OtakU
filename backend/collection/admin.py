from django.contrib import admin
from django.utils.html import format_html
from .models import (
    Anime, Genre, Theme, AnimeImage, AnimeTitle, RelationAnime,
    Manga, MangaImage, MangaTitle, RelationManga, Publisher,
    TypeManga, Language, RelationType, Origin, Format, Season,
    People, Role, Contribution, Studio, StudioRole, ContributionStudio,
    AnimeEpisode, TomeManga, ChapterManga, TomeMangaImage, Scan,
    ScanImage, ScanTitle, RelationScan, TomeScan, ChapterScan,
    TomeScanImage, RelationAnimeManga, RelationAnimeScan,
    RelationMangaScan, Status
)
from .forms import AnimeForm
from .admin_forms import MangaAdminForm, AnimeAdminForm, ScanAdminForm



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
    
@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)
    exclude = ('slug',)  # Exclut le champ 'slug' du formulaire
    
@admin.register(TypeManga)
class TypeMangaAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)
    exclude = ('slug',)  # Exclut le champ 'slug' du formulaire
    
@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'native_name')
    search_fields = ('name',)
    
@admin.register(RelationType)
class RelationTypeAdmin(admin.ModelAdmin):
    list_display = ('code', 'label', 'inverse')  # visible dans la liste
    search_fields = ('code', 'label')            # champ de recherche
    list_filter = ('inverse',)                   # filtre latéral
    
@admin.register(Origin)
class OriginAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')  # visible dans la liste
    search_fields = ('name', 'slug')            # champ de recherche
    exclude = ('slug',)  # Exclut le champ 'slug' du formulaire
    
@admin.register(Format)
class FormatAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')  # visible dans la liste
    search_fields = ('name', 'slug')  # champ de recherche
    exclude = ('slug',)  # Exclut le champ 'slug' du formulaire

@admin.register(Season)
class SeasonAdmin(admin.ModelAdmin):
    list_display = ('season', 'year', 'slug')  # visible dans la liste
    search_fields = ('season', 'year', 'slug')            # champ de recherche
    exclude = ('slug',)  # Exclut le champ 'slug' du formulaire

@admin.register(People)
class PeopleAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)
    exclude = ('slug',)  # Exclut le champ 'slug' du formulaire

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('code', 'label')  # visible dans la liste
    search_fields = ('code', 'label')            # champ de recherche

@admin.register(Contribution)
class ContributionAdmin(admin.ModelAdmin):
    autocomplete_fields = ['people']
    list_display = ('people', 'role')  # visible dans la liste
    search_fields = ('people', 'role')            # champ de recherche
    list_filter = ('people',)
    
@admin.register(Studio)
class PeopleAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)
    exclude = ('slug',)  # Exclut le champ 'slug' du formulaire

@admin.register(StudioRole)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('code', 'label')  # visible dans la liste
    search_fields = ('code', 'label')            # champ de recherche

@admin.register(ContributionStudio)
class ContributionAdmin(admin.ModelAdmin):
    autocomplete_fields = ['studio']
    list_display = ('studio', 'studioRole')  # visible dans la liste
    search_fields = ('studio', 'studioRole')            # champ de recherche
    list_filter = ('studio',)

@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)
    exclude = ('slug',)  # Exclut le champ 'slug' du formulaire

# anime
@admin.register(Anime)
class AnimeAdmin(admin.ModelAdmin):

    form = AnimeForm  # Associe le formulaire personnalisé à l'admin
    
    autocomplete_fields = ['season']
    list_display = ('id', 'main_title', 'image_previews', 'slug')
    search_fields = ['main_title']
    list_filter = ('genres', 'themes', 'studio', 'studio_3D', 'season')
    filter_horizontal = ('genres', 'themes', 'studio', 'studio_3D')  # meilleure UX pour les ManyToMany
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
    
    list_display = ('anime', 'title', 'language', 'is_original', 'is_nickname','is_main')
    search_fields = ('title', 'language', 'slug')
    list_filter = ('is_original', 'is_nickname', 'language')
    
@admin.register(AnimeEpisode)
class AnimeEpisodeAdmin(admin.ModelAdmin):
    autocomplete_fields = ['anime']
    search_fields = ['anime__main_title']
    list_display = ['anime', 'number', 'title']
    ordering = ['anime', 'number']


#manga
@admin.register(Manga)
class MangaAdmin(admin.ModelAdmin):
    form = MangaAdminForm
    
    autocomplete_fields = ['publisher']
    list_display = ('id', 'main_title', 'image_previews', 'slug')
    search_fields = ['main_title']
    list_filter = ('genres', 'themes', 'author', 'designer', 'scenariste', 'chara_designer', 'publisher')
    filter_horizontal = ('genres', 'themes', 'author', 'designer', 'scenariste', 'chara_designer')  # meilleure UX pour les ManyToMany
    exclude = ('slug',)  # Exclut le champ 'slug' du formulaire
    
    def save_model(self, request, obj, form, change):
    # Sauvegarde de l'objet Manga
        super().save_model(request, obj, form, change)

        # Crée un MangaTitle automatiquement si on est en création et qu'un titre est fourni
        if not change and 'main_title' in form.cleaned_data:
            try:
                lang_fr = Language.objects.get(code='fr')  # Récupère la langue 'fr'
            except Language.DoesNotExist:
                lang_fr = None  # Ou gérer autrement si c’est bloquant

            if lang_fr:  # On ne crée que si la langue existe
                MangaTitle.objects.create(
                    manga=obj,
                    title=form.cleaned_data['main_title'],
                    language=lang_fr,
                    is_main=True  # Si le champ existe
                )
        
    def image_previews(self, obj):
        images = obj.images.all()  # Récupère toutes les images de cet anime
        preview_html = ''
        for image in images:
            preview_html += f'<img src="{image.image.url}" width="75" height="100" style="margin-right:5px;" />'
        return format_html(preview_html) if images else 'Aucune image'
        
    image_previews.allow_tags = True  # Permet d'afficher le HTML dans l'admin
    image_previews.short_description = 'Aperçu des images'  # Titre de la colonne

@admin.register(MangaImage)
class MangaImageAdmin(admin.ModelAdmin):
    autocomplete_fields = ['manga']
    list_display = ('manga', 'description', 'image_preview')
    search_fields = ('manga__main_title', 'description')
    list_filter = ('manga',)

    def image_preview(self, obj):
        return format_html(
                '<img src="{}" width="75" height="100" style="margin-right:5px;" />',
                obj.image.url
            )
    image_preview.allow_tags = True  # Permet d'afficher le HTML dans l'admin
    image_preview.short_description = 'Aperçu de l\'image'

@admin.register(MangaTitle)
class MangaTitleAdmin(admin.ModelAdmin):
    autocomplete_fields = ['manga']
    search_fields = ['manga__main_title']
    
    def get_search_results(self, request, queryset, search_term):
        print(f"Recherche avec le terme : {search_term}")
        return super().get_search_results(request, queryset, search_term)
    
    list_display = ('manga', 'title', 'language', 'is_original', 'is_nickname','is_main')
    search_fields = ('title', 'language', 'slug')
    list_filter = ('is_original', 'is_nickname', 'language')

@admin.register(TomeManga)
class TomeMangaAdmin(admin.ModelAdmin):
    list_display = ['manga', 'number', 'date_publication_jp', 'date_publication_fr']
    search_fields = ['manga__main_title']
    autocomplete_fields = ['manga']  
    
@admin.register(ChapterManga)
class ChapterMangaAdmin(admin.ModelAdmin):
    list_display = ['tome_manga', 'number', 'title']
    list_filter = ['tome_manga']
    search_fields = ['title', 'tome_manga__manga__main_title']
    autocomplete_fields = ['tome_manga']

@admin.register(TomeMangaImage)
class TomeMangaImageAdmin(admin.ModelAdmin):
    autocomplete_fields = ['tome_manga']
    list_display = ('tome_manga', 'description', 'image_preview')
    search_fields = ('manga__main_title', 'description')
    list_filter = ('tome_manga',)

    def image_preview(self, obj):
        return format_html(
                '<img src="{}" width="75" height="100" style="margin-right:5px;" />',
                obj.image.url
            )
    image_preview.allow_tags = True  # Permet d'afficher le HTML dans l'admin
    image_preview.short_description = 'Aperçu de l\'image'



#scan
@admin.register(Scan)
class ScanAdmin(admin.ModelAdmin):
    form = ScanAdminForm
    
    list_display = ('id', 'main_title', 'image_previews', 'slug')
    search_fields = ['main_title']
    list_filter = ('genres', 'themes', 'author', 'designer', 'scenariste', 'chara_designer')
    filter_horizontal = ('genres', 'themes', 'author', 'designer', 'scenariste', 'chara_designer')  # meilleure UX pour les ManyToMany
    exclude = ('slug',)  # Exclut le champ 'slug' du formulaire
    
    def save_model(self, request, obj, form, change):
    # Sauvegarde de l'objet Scan
        super().save_model(request, obj, form, change)

        # Crée un ScanTitle automatiquement si on est en création et qu'un titre est fourni
        if not change and 'main_title' in form.cleaned_data:
            try:
                lang_jp = Language.objects.get(code='jp')  # Récupère la langue 'fr'
            except Language.DoesNotExist:
                lang_jp = None  # Ou gérer autrement si c’est bloquant

            if lang_jp:  # On ne crée que si la langue existe
                ScanTitle.objects.create(
                    scan=obj,
                    title=form.cleaned_data['main_title'],
                    language=lang_jp,
                    is_main=True  # Si le champ existe
                )
        
    def image_previews(self, obj):
        images = obj.images.all()  # Récupère toutes les images de cet anime
        preview_html = ''
        for image in images:
            preview_html += f'<img src="{image.image.url}" width="75" height="100" style="margin-right:5px;" />'
        return format_html(preview_html) if images else 'Aucune image'
        
    image_previews.allow_tags = True  # Permet d'afficher le HTML dans l'admin
    image_previews.short_description = 'Aperçu des images'  # Titre de la colonne
    
@admin.register(ScanImage)
class ScanImageAdmin(admin.ModelAdmin):
    autocomplete_fields = ['scan']
    list_display = ('scan', 'description', 'image_preview')
    search_fields = ('scan__main_title', 'description')
    list_filter = ('scan',)
    
    def image_preview(self, obj):
        return format_html(
                '<img src="{}" width="75" height="100" style="margin-right:5px;" />',
                obj.image.url
            )
    image_preview.allow_tags = True  # Permet d'afficher le HTML dans l'admin
    image_preview.short_description = 'Aperçu de l\'image'

@admin.register(ScanTitle)
class ScanTitleAdmin(admin.ModelAdmin):
    autocomplete_fields = ['scan']
    search_fields = ['scan__main_title']
    
    def get_search_results(self, request, queryset, search_term):
        print(f"Recherche avec le terme : {search_term}")
        return super().get_search_results(request, queryset, search_term)
    
    list_display = ('scan', 'title', 'language', 'is_original', 'is_nickname','is_main')
    search_fields = ('title', 'language', 'slug')
    list_filter = ('is_original', 'is_nickname', 'language')

@admin.register(TomeScan)
class TomeScanAdmin(admin.ModelAdmin):
    list_display = ['scan', 'number', 'date_publication_jp']
    search_fields = ['scan__main_title']
    autocomplete_fields = ['scan']

@admin.register(ChapterScan)
class ChapterScanAdmin(admin.ModelAdmin):
    list_display = ['tome_scan', 'number', 'title']
    list_filter = ['tome_scan']
    search_fields = ['title', 'tome_scan__scan__main_title']
    autocomplete_fields = ['tome_scan']

@admin.register(TomeScanImage)
class TomeScanImageAdmin(admin.ModelAdmin):
    autocomplete_fields = ['tome_scan']
    list_display = ('tome_scan', 'description', 'image_preview')
    search_fields = ('scan__main_title', 'description')
    list_filter = ('tome_scan',)

    def image_preview(self, obj):
        return format_html(
                '<img src="{}" width="75" height="100" style="margin-right:5px;" />',
                obj.image.url
            )
    image_preview.allow_tags = True  # Permet d'afficher le HTML dans l'admin
    image_preview.short_description = 'Aperçu de l\'image'


#relation

@admin.register(RelationAnime)
class RelationAnimeAdmin(admin.ModelAdmin):
    list_display = ('anime_source', 'relation_type', 'anime_target')
    search_fields = (
        'anime_source__title',
        'anime_target__title',
        'relation_type',
    )
    autocomplete_fields = ('anime_source', 'anime_target')

@admin.register(RelationManga)
class RelationMangaAdmin(admin.ModelAdmin):
    list_display = ('manga_source', 'relation_type', 'manga_target')
    search_fields = (
        'manga_source__title',
        'manga_target__title',
        'relation_type',
    )
    autocomplete_fields = ('manga_source', 'manga_target')

@admin.register(RelationScan)
class RelationScanAdmin(admin.ModelAdmin):
    list_display = ('scan_source', 'relation_type', 'scan_target')
    search_fields = (
        'scan_source__title',
        'scan_target__title',
        'relation_type',
    )
    autocomplete_fields = ('scan_source', 'scan_target')

@admin.register(RelationAnimeManga)
class RelationAnimeMangaAdmin(admin.ModelAdmin):
    list_display = ('get_source', 'relation_type', 'get_target', 'source_type')
    search_fields = (
        'anime__title',
        'manga__title',
        'relation_type__label',
    )
    autocomplete_fields = ('anime', 'manga', 'relation_type')

    def get_source(self, obj):
        return obj.anime if obj.source_type == 'anime' else obj.manga
    get_source.short_description = 'Source'

    def get_target(self, obj):
        return obj.manga if obj.source_type == 'anime' else obj.anime
    get_target.short_description = 'Cible'
    

@admin.register(RelationAnimeScan)
class RelationAnimeScanAdmin(admin.ModelAdmin):
    list_display = ('get_source', 'relation_type', 'get_target', 'source_type')
    search_fields = (
        'anime__title',
        'scan__title',
        'relation_type__label',
    )
    autocomplete_fields = ('anime', 'scan', 'relation_type')

    def get_source(self, obj):
        return obj.anime if obj.source_type == 'anime' else obj.scan
    get_source.short_description = 'Source'

    def get_target(self, obj):
        return obj.scan if obj.source_type == 'anime' else obj.anime
    get_target.short_description = 'Cible'

@admin.register(RelationMangaScan)
class RelationMangaScanAdmin(admin.ModelAdmin):
    list_display = ('get_source', 'relation_type', 'get_target', 'source_type')
    search_fields = (
        'manga__title',
        'scan__title',
        'relation_type__label',
    )
    autocomplete_fields = ('manga', 'scan', 'relation_type')

    def get_source(self, obj):
        return obj.manga if obj.source_type == 'manga' else obj.scan
    get_source.short_description = 'Source'

    def get_target(self, obj):
        return obj.sacn if obj.source_type == 'manga' else obj.manga
    get_target.short_description = 'Cible'