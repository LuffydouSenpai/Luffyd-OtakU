from django.db import models
from slugify import slugify  # pip install python-slugify
import os

#table unique
class Genre(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.CharField(max_length=50)
    
    def save(self, *args, **kwargs):
        original_slug = slugify(f"{self.name}")
        slug = original_slug
        self.slug = slug
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name
      
class Theme(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.CharField(max_length=50)
    
    def save(self, *args, **kwargs):
        original_slug = slugify(f"{self.name}")
        slug = original_slug
        self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    
class Publisher(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.CharField(max_length=50)
    
    def save(self, *args, **kwargs):
        original_slug = slugify(f"{self.name}")
        slug = original_slug
        self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class TypeManga(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.CharField(max_length=50)
    
    def save(self, *args, **kwargs):
        original_slug = slugify(f"{self.name}")
        slug = original_slug
        self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    
class Language(models.Model):
    code = models.CharField(max_length=5, unique=True)  # 'jp'
    name = models.CharField(max_length=50)  # 'Japonais'
    native_name = models.CharField(max_length=50)  # '日本語'

    def __str__(self):
        return self.name

class RelationType(models.Model):
    code = models.CharField(max_length=50, unique=True)
    label = models.CharField(max_length=100)
    inverse = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='inverse_of'
    )

    def __str__(self):
        return self.label
    
class Origin(models.Model):
    code = models.CharField(max_length=50, unique=True)
    label = models.CharField(max_length=100)
    
    def __str__(self):
        return self.label
    
class Format(models.Model):
    code = models.CharField(max_length=50, unique=True)
    label = models.CharField(max_length=100)
    
    def __str__(self):
        return self.label

class Season(models.Model):
    SEASON_CHOICES = [
        ('winter', 'Hiver'),
        ('spring', 'Printemps'),
        ('summer', 'Été'),
        ('autumn', 'Automne'),
    ]

    season = models.CharField(max_length=10, choices=SEASON_CHOICES)
    year = models.PositiveIntegerField()

    class Meta:
        unique_together = ('season', 'year')

    def __str__(self):
        return f"{dict(self.SEASON_CHOICES).get(self.season)} {self.year}"

# anime
class Anime(models.Model):
    
    main_title = models.CharField(max_length=255)
    origin = models.ForeignKey(Origin, null=True, on_delete=models.CASCADE, related_name='animes')
    synopsis = models.TextField()
    date_start = models.DateField(null=True, blank=True)
    date_end = models.DateField(null=True, blank=True)
    episode = models.IntegerField()
    duration = models.IntegerField(help_text="Durée moyenne d’un épisode en minutes")
    season = models.CharField(max_length=50, null=True, blank=True)
    studio = models.CharField(max_length=150, null=True, blank=True)
    studio_3D = models.CharField(max_length=150, null=True, blank=True)
    format = models.ForeignKey(Format, null=True, on_delete=models.CASCADE, related_name='animes')
    url_nautiljon = models.TextField()
    url_mal = models.TextField()
    genres = models.ManyToManyField('Genre', related_name='animes')
    themes = models.ManyToManyField('Theme', related_name='animes')
    slug = models.CharField(max_length=255, null=True)  # Pour une URL simplifiée du titre, souvent utilisée pour les routes

    def save(self, *args, **kwargs):
        if not self.slug:
            original_slug = slugify(f"{self.main_title}")
            slug = original_slug
            counter = 1

            # Si le slug existe déjà, ajouter un compteur
            while AnimeTitle.objects.filter(slug=slug).exists():
                slug = f"{original_slug}-{counter}"
                counter += 1

            self.slug = slug

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.main_title}"
    
class AnimeImage(models.Model):
    anime = models.ForeignKey(Anime, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='anime_images/')
    description = models.CharField(max_length=255, blank=True)
    
    def save(self, *args, **kwargs):
        # Générer le nom de fichier basé sur le slug de l'anime
        anime_slug = slugify(self.anime.slug)
        base_filename = f"{anime_slug}"

        # Vérifier s'il existe déjà une image avec ce nom (pour ajouter un suffixe)
        count = 1
        while AnimeImage.objects.filter(image__startswith=base_filename).exists():
            base_filename = f"{anime_slug}-{count}"
            count += 1
        
        # Renommer l'image avant de la sauvegarder
        if self.image:
            # Récupérer le nom de fichier original (extension)
            ext = os.path.splitext(self.image.name)[1]
            # Créer un nouveau chemin pour l'image
            new_image_name = f"{base_filename}{ext}"
            self.image.name = new_image_name  # Mettre à jour le nom du fichier

        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"Image de {self.anime.main_title}"
    
class AnimeTitle(models.Model):
    
    anime = models.ForeignKey(Anime, related_name='anime_titles', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    language = models.ForeignKey(Language, null=True, on_delete=models.PROTECT)
    is_original = models.BooleanField(default=False)  # Indique si le titre est original (true) ou une version modifiée (false)
    is_nickname = models.BooleanField(default=False)  # Indique si le titre est un surnom ou un autre alias
    is_main = models.BooleanField(default=False)      # Indique si le titre celui que j'utiliserais principalement
    slug = models.CharField(max_length=255)  # Pour une URL simplifiée du titre, souvent utilisée pour les routes
    
    class Meta:
        # Contrainte d'unicité pour assurer qu'il n'y ait pas de doublon
        constraints = [
            models.UniqueConstraint(fields=['anime', 'title', 'language'], name='unique_anime_title_language')
        ]
        
        
    def save(self, *args, **kwargs):
        if not self.slug:
            original_slug = slugify(f"{self.title}")
            slug = original_slug
            counter = 1

            # Si le slug existe déjà, ajouter un compteur
            while AnimeTitle.objects.filter(slug=slug).exists():
                slug = f"{original_slug}-{counter}"
                counter += 1

            self.slug = slug

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Title: {self.title} ({self.language}) - Original: {self.is_original}"
    
class RelationAnime(models.Model):

    anime_source = models.ForeignKey(
        'Anime',
        on_delete=models.CASCADE,
        related_name='relations_as_source'
    )
    anime_target = models.ForeignKey(
        'Anime',
        on_delete=models.CASCADE,
        related_name='relations_as_target'
    )
    relation_type = models.ForeignKey(
        RelationType,
        on_delete=models.CASCADE
    )

    class Meta:
        unique_together = ('anime_source', 'anime_target')

    def __str__(self):
        return f"{self.anime_source} → {self.relation_type} → {self.anime_target}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        inverse_type = self.relation_type.inverse

        if inverse_type and not RelationAnime.objects.filter(
            anime_source=self.anime_target,
            manga_target=self.anime_source,
            relation_type=inverse_type
        ).exists():
            RelationAnime.objects.create(
                anime_source=self.anime_target,
                anime_target=self.anime_source,
                relation_type=inverse_type
            )

    def delete(self, *args, **kwargs):
        inverse_type = self.relation_type.inverse
        if inverse_type:
            RelationAnime.objects.filter(
                anime_source=self.anime_target,
                anime_target=self.anime_source,
                relation_type=inverse_type
            ).delete()
        super().delete(*args, **kwargs)
        


#manga  
class Manga(models.Model):
    
    main_title = models.CharField(max_length=255)
    type = models.ForeignKey(TypeManga, null=True, on_delete=models.CASCADE, related_name='mangas')
    synopsis = models.TextField()
    year_start_jp = models.PositiveIntegerField()
    year_start_fr = models.PositiveIntegerField()
    publisher = models.ForeignKey(Publisher, null=True, on_delete=models.CASCADE, related_name='mangas')
    author = models.CharField(max_length=150, null=True, blank=True)
    scenariste = models.CharField(max_length=150, null=True, blank=True)
    designer = models.CharField(max_length=150, null=True, blank=True)
    chara_designer = models.CharField(max_length=150, null=True, blank=True)
    storage = models.CharField(max_length=50)
    url_nautiljon = models.TextField()
    url_mal = models.TextField()
    genres = models.ManyToManyField('Genre', related_name='mangas')
    themes = models.ManyToManyField('Theme', related_name='mangas')
    slug = models.CharField(max_length=255)  # Pour une URL simplifiée du titre, souvent utilisée pour les routes
    
    def save(self, *args, **kwargs):
        if not self.slug:
            original_slug = slugify(f"{self.main_title}")
            slug = original_slug
            counter = 1

            # Si le slug existe déjà, ajouter un compteur
            while AnimeTitle.objects.filter(slug=slug).exists():
                slug = f"{original_slug}-{counter}"
                counter += 1

            self.slug = slug

        super().save(*args, **kwargs)
        
    def __str__(self):
        return f"{self.main_title}"
       
class MangaImage(models.Model):
    manga = models.ForeignKey(Manga, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='manga_images/')
    description = models.CharField(max_length=255, blank=True)
    
    def save(self, *args, **kwargs):
        # Générer le nom de fichier basé sur le slug de l'anime
        manga_slug = slugify(self.manga.slug)
        base_filename = f"{manga_slug}"

        # Vérifier s'il existe déjà une image avec ce nom (pour ajouter un suffixe)
        count = 1
        while AnimeImage.objects.filter(image__startswith=base_filename).exists():
            base_filename = f"{manga_slug}-{count}"
            count += 1
        
        # Renommer l'image avant de la sauvegarder
        if self.image:
            # Récupérer le nom de fichier original (extension)
            ext = os.path.splitext(self.image.name)[1]
            # Créer un nouveau chemin pour l'image
            new_image_name = f"{base_filename}{ext}"
            self.image.name = new_image_name  # Mettre à jour le nom du fichier

        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"Image de {self.manga.main_title}"
    
class MangaTitle(models.Model):
    
    manga = models.ForeignKey(Manga, related_name='manga_titles', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    language = models.ForeignKey(Language, null=True, on_delete=models.PROTECT)
    is_original = models.BooleanField(default=False)  # Indique si le titre est original (true) ou une version modifiée (false)
    is_nickname = models.BooleanField(default=False)  # Indique si le titre est un surnom ou un autre alias
    is_main = models.BooleanField(default=False)      # Indique si le titre celui que j'utiliserais principalement
    slug = models.CharField(max_length=255)  # Pour une URL simplifiée du titre, souvent utilisée pour les routes
    
    class Meta:
        # Contrainte d'unicité pour assurer qu'il n'y ait pas de doublon
        constraints = [
            models.UniqueConstraint(fields=['manga', 'title', 'language'], name='unique_manga_title_language')
        ]
        
    def save(self, *args, **kwargs):
        if not self.slug:
            original_slug = slugify(f"{self.title}")
            slug = original_slug
            counter = 1

            # Si le slug existe déjà, ajouter un compteur
            while MangaTitle.objects.filter(slug=slug).exists():
                slug = f"{original_slug}-{counter}"
                counter += 1

            self.slug = slug

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Title: {self.title} ({self.language}) - Original: {self.is_original}"
      
class RelationManga(models.Model):
    
    manga_source = models.ForeignKey(
        'Manga',
        on_delete=models.CASCADE,
        related_name='relations_as_source'
    )
    manga_target = models.ForeignKey(
        'Manga',
        on_delete=models.CASCADE,
        related_name='relations_as_target'
    )
    relation_type = models.ForeignKey(
        RelationType,
        on_delete=models.CASCADE
    )
    
    class Meta:
        unique_together = ('manga_source', 'manga_target')
        
    def __str__(self):
        return f"{self.manga_source} → {self.relation_type} → {self.manga_target}"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        inverse_type = self.relation_type.inverse

        if inverse_type and not RelationManga.objects.filter(
            manga_source=self.manga_target,
            manga_target=self.manga_source,
            relation_type=inverse_type
        ).exists():
            RelationManga.objects.create(
                manga_source=self.manga_target,
                manga_target=self.manga_source,
                relation_type=inverse_type
            )

    def delete(self, *args, **kwargs):
        inverse_type = self.relation_type.inverse
        if inverse_type:
            RelationManga.objects.filter(
                manga_source=self.manga_target,
                manga_target=self.manga_source,
                relation_type=inverse_type
            ).delete()
        super().delete(*args, **kwargs)
    
    