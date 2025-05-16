from django.db import models
from slugify import slugify  # pip install python-slugify
import os

#table unique
class Genre(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.CharField(max_length=50, unique=True)
    
    def save(self, *args, **kwargs):
        original_slug = slugify(f"{self.name}")
        slug = original_slug
        self.slug = slug
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name
      
class Theme(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.CharField(max_length=50, unique=True)
    
    def save(self, *args, **kwargs):
        original_slug = slugify(f"{self.name}")
        slug = original_slug
        self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    
class Publisher(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.CharField(max_length=50, unique=True)
    
    def save(self, *args, **kwargs):
        original_slug = slugify(f"{self.name}")
        slug = original_slug
        self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class TypeManga(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.CharField(max_length=50, unique=True)
    
    def save(self, *args, **kwargs):
        original_slug = slugify(f"{self.name}")
        slug = original_slug
        self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    
class Language(models.Model):
    code = models.CharField(max_length=5, unique=True)  # 'jp'
    name = models.CharField(max_length=50, unique=True)  # 'Japonais'
    native_name = models.CharField(max_length=50, unique=True)  # '日本語'

    def __str__(self):
        return self.name

class RelationType(models.Model):
    code = models.CharField(max_length=50, unique=True)
    label = models.CharField(max_length=50)
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
    label = models.CharField(max_length=50)
    
    def __str__(self):
        return self.label
    
class Format(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.CharField(max_length=50, unique=True)
    
    def save(self, *args, **kwargs):
        original_slug = slugify(f"{self.name}")
        slug = original_slug
        self.slug = slug
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name

class Season(models.Model):
    SEASON_CHOICES = [
        ('winter', 'Hiver'),
        ('spring', 'Printemps'),
        ('summer', 'Été'),
        ('autumn', 'Automne'),
    ]

    season = models.CharField(max_length=10, choices=SEASON_CHOICES)
    year = models.PositiveIntegerField()
    slug = models.CharField(max_length=50, unique=True)
    
    def save(self, *args, **kwargs):
        original_slug = slugify(f"{self.season} {self.year}")
        slug = original_slug
        self.slug = slug
        super().save(*args, **kwargs)

    class Meta:
        unique_together = ('season', 'year')

    def __str__(self):
        return f"{dict(self.SEASON_CHOICES).get(self.season)} {self.year}"

class People(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.CharField(max_length=100, unique=True)
        
    def save(self, *args, **kwargs):
        original_slug = slugify(f"{self.name}")
        slug = original_slug
        self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Role(models.Model):
    code = models.CharField(max_length=50, unique=True)
    label = models.CharField(max_length=50)
    
    def __str__(self):
        return self.label

class Studio(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.CharField(max_length=100, unique=True)
        
    def save(self, *args, **kwargs):
        original_slug = slugify(f"{self.name}")
        slug = original_slug
        self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class StudioRole(models.Model):
    code = models.CharField(max_length=50, unique=True)
    label = models.CharField(max_length=50)
    
    def __str__(self):
        return self.label

class Contribution(models.Model):
    people = models.ForeignKey(People, on_delete=models.CASCADE, related_name='contribution')
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name='contribution')
    
    def __str__(self):
        return f"{self.people}  - {self.role}"
    
class ContributionStudio(models.Model):
    studio = models.ForeignKey(Studio, on_delete=models.CASCADE, related_name='contributionStudio')
    studioRole = models.ForeignKey(StudioRole, on_delete=models.CASCADE, related_name='contributionStudio')
    
    def __str__(self):
        return f"{self.studio}  - {self.studioRole}"
    


# anime
class Anime(models.Model):
    
    main_title = models.CharField(max_length=255, unique=True)
    origin = models.ForeignKey(Origin, on_delete=models.CASCADE, related_name='anime')
    synopsis = models.TextField()
    date_start = models.DateField(null=True, blank=True)
    date_end = models.DateField(null=True, blank=True)
    episode = models.IntegerField(null=True, blank=True)
    duration = models.IntegerField(help_text="Durée moyenne d’un épisode en minutes", null=True, blank=True)
    season = models.ForeignKey(Season, on_delete=models.CASCADE, related_name='anime')
    studio = models.ManyToManyField('ContributionStudio', related_name='anime_studio', blank=True)
    studio_3D = models.ManyToManyField('ContributionStudio', related_name='anime_studio3d', blank=True)
    format = models.ForeignKey(Format, on_delete=models.CASCADE, related_name='anime')
    url_nautiljon = models.URLField(max_length=500, blank=True)
    url_mal = models.URLField(max_length=500, blank=True)
    genres = models.ManyToManyField('Genre', related_name='anime', blank=True)
    themes = models.ManyToManyField('Theme', related_name='anime', blank=True)
    slug = models.CharField(max_length=255, unique=True)  # Pour une URL simplifiée du titre, souvent utilisée pour les routes

    def save(self, *args, **kwargs):
        original_slug = slugify(f"{self.main_title}")
        slug = original_slug
        self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.main_title}"
    
class AnimeImage(models.Model):
    anime = models.ForeignKey(Anime, related_name='animeImage', on_delete=models.CASCADE)
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
    language = models.ForeignKey(Language, on_delete=models.PROTECT)
    is_original = models.BooleanField(default=False)  # Indique si le titre est original (true) ou une version modifiée (false)
    is_nickname = models.BooleanField(default=False)  # Indique si le titre est un surnom ou un autre alias
    is_main = models.BooleanField(default=False)      # Indique si le titre celui que j'utiliserais principalement
    
    class Meta:
        # Contrainte d'unicité pour assurer qu'il n'y ait pas de doublon
        constraints = [
            models.UniqueConstraint(fields=['anime', 'title', 'language'], name='unique_anime_title_language')
        ]
        
    def __str__(self):
        return f"Title: {self.title} ({self.language}) - Original: {self.is_original}"
       
class AnimeEpisode(models.Model):
    anime = models.ForeignKey(Anime, related_name='anime_episode', on_delete=models.CASCADE)
    number = models.PositiveIntegerField()
    title = models.CharField(max_length=255)
    
    class Meta:
        # Contrainte d'unicité pour assurer qu'il n'y ait pas de doublon
        constraints = [
            models.UniqueConstraint(fields=['anime', 'number'], name='unique__episode_number')
        ]
        
    def __str__(self):
        return f"{self.anime.main_title} – Épisode {self.number}: {self.title}"


#manga  
class Manga(models.Model):
    
    main_title = models.CharField(max_length=255, unique=True)
    type = models.ForeignKey(TypeManga, on_delete=models.CASCADE, related_name='mangas')
    synopsis = models.TextField()
    year_start_jp = models.PositiveIntegerField()
    year_start_fr = models.PositiveIntegerField()
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE, related_name='mangas')
    author = models.ManyToManyField('Contribution', related_name='mangas_author', blank=True)
    scenariste = models.ManyToManyField('Contribution', related_name='mangas_scenariste', blank=True)
    designer = models.ManyToManyField('Contribution', related_name='mangas_designer', blank=True)
    chara_designer = models.ManyToManyField('Contribution', related_name='mangas_chara_designer', blank=True)
    storage = models.CharField(max_length=50, null=True)
    url_nautiljon = models.URLField(max_length=500, blank=True)
    url_mal = models.URLField(max_length=500, blank=True)
    genres = models.ManyToManyField('Genre', related_name='mangas', blank=True)
    themes = models.ManyToManyField('Theme', related_name='mangas', blank=True)
    slug = models.CharField(max_length=255, unique=True)  # Pour une URL simplifiée du titre, souvent utilisée pour les routes
    
    def save(self, *args, **kwargs):
        original_slug = slugify(f"{self.main_title}")
        slug = original_slug
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
        while MangaImage.objects.filter(image__startswith=base_filename).exists():
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
    language = models.ForeignKey(Language, on_delete=models.PROTECT)
    is_original = models.BooleanField(default=False)  # Indique si le titre est original (true) ou une version modifiée (false)
    is_nickname = models.BooleanField(default=False)  # Indique si le titre est un surnom ou un autre alias
    is_main = models.BooleanField(default=False)      # Indique si le titre celui que j'utiliserais principalement
    
    class Meta:
        # Contrainte d'unicité pour assurer qu'il n'y ait pas de doublon
        constraints = [
            models.UniqueConstraint(fields=['manga', 'title', 'language'], name='unique_manga_title_language')
        ]
        

    def __str__(self):
        return f"Title: {self.title} ({self.language}) - Original: {self.is_original}"
      
class TomeManga(models.Model):
    
    manga = models.ForeignKey(
        'Manga',
        on_delete=models.CASCADE,
        related_name='tomes'
    )
    number = models.PositiveIntegerField()
    date_publication_jp = models.DateField(null=True, blank=True)
    date_publication_fr = models.DateField(null=True, blank=True)
    back_cover = models.TextField()
    slug = models.CharField(max_length=255,null=True)
    
    def save(self, *args, **kwargs):
        original_slug = slugify(f"{self.manga.main_name} Tome {self.number}")
        slug = original_slug
        self.slug = slug
        super().save(*args, **kwargs)
    
    class Meta:
        unique_together = ['manga', 'number']

    def __str__(self):
        return f"{self.manga.main_title} – Tome {self.number}"

class ChapterManga(models.Model):
    tome_manga = models.ForeignKey(
        TomeManga,
        on_delete=models.CASCADE,
        related_name='chapters'
    )
    number = models.PositiveIntegerField()
    title = models.CharField(max_length=255)

    class Meta:
        unique_together = ['tome_manga', 'number']

    def __str__(self):
        return f"Chapitre {self.number} : {self.title}"

class TomeMangaImage(models.Model):
    tome_manga = models.ForeignKey(TomeManga, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='manga_images/')
    description = models.CharField(max_length=255, blank=True)
    
    def save(self, *args, **kwargs):
        # Générer le nom de fichier basé sur le slug de l'anime
        manga_slug = slugify(self.manga.slug)
        base_filename = f"{manga_slug}"

        # Vérifier s'il existe déjà une image avec ce nom (pour ajouter un suffixe)
        count = 1
        while TomeMangaImage.objects.filter(image__startswith=base_filename).exists():
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



#scan
class Scan(models.Model):
    
    main_title = models.CharField(max_length=255, unique=True)
    type = models.ForeignKey(TypeManga, on_delete=models.CASCADE, related_name='scan')
    synopsis = models.TextField()
    year_start_jp = models.PositiveIntegerField()
    author = models.ManyToManyField('Contribution', related_name='scan_author', blank=True)
    scenariste = models.ManyToManyField('Contribution', related_name='scan_scenariste', blank=True)
    designer = models.ManyToManyField('Contribution', related_name='scan_designer', blank=True)
    chara_designer = models.ManyToManyField('Contribution', related_name='scan_chara_designer', blank=True)
    url_nautiljon = models.URLField(max_length=500, blank=True)
    url_mal = models.URLField(max_length=500, blank=True)
    genres = models.ManyToManyField('Genre', related_name='scan', blank=True)
    themes = models.ManyToManyField('Theme', related_name='scan', blank=True)
    slug = models.CharField(max_length=255, unique=True)  # Pour une URL simplifiée du titre, souvent utilisée pour les routes
    
    def save(self, *args, **kwargs):
        original_slug = slugify(f"{self.main_title}")
        slug = original_slug
        self.slug = slug
        super().save(*args, **kwargs)
        
    def __str__(self):
        return f"{self.main_title}"
       
class ScanImage(models.Model):
    scan = models.ForeignKey(Scan, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='scan_images/')
    description = models.CharField(max_length=255, blank=True)
    
    def save(self, *args, **kwargs):
        # Générer le nom de fichier basé sur le slug de l'anime
        scan_slug = slugify(self.scan.slug)
        base_filename = f"{scan_slug}"

        # Vérifier s'il existe déjà une image avec ce nom (pour ajouter un suffixe)
        count = 1
        while ScanImage.objects.filter(image__startswith=base_filename).exists():
            base_filename = f"{scan_slug}-{count}"
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
        return f"Image de {self.scan.main_title}"
    
class ScanTitle(models.Model):
    
    scan = models.ForeignKey(Scan, related_name='scan_titles', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    language = models.ForeignKey(Language, on_delete=models.PROTECT)
    is_original = models.BooleanField(default=False)  # Indique si le titre est original (true) ou une version modifiée (false)
    is_nickname = models.BooleanField(default=False)  # Indique si le titre est un surnom ou un autre alias
    is_main = models.BooleanField(default=False)      # Indique si le titre celui que j'utiliserais principalement
    
    class Meta:
        # Contrainte d'unicité pour assurer qu'il n'y ait pas de doublon
        constraints = [
            models.UniqueConstraint(fields=['scan', 'title', 'language'], name='unique_scan_title_language')
        ]
        

    def __str__(self):
        return f"Title: {self.title} ({self.language}) - Original: {self.is_original}"
      
class TomeScan(models.Model):
    
    scan = models.ForeignKey(
        'Scan',
        on_delete=models.CASCADE,
        related_name='tomes'
    )
    number = models.PositiveIntegerField()
    date_publication_jp = models.DateField(null=True, blank=True)
    back_cover = models.TextField(null=True)
    slug = models.CharField(max_length=255,null=True)
    
    def save(self, *args, **kwargs):
        original_slug = slugify(f"{self.scan.main_name} Tome {self.number}")
        slug = original_slug
        self.slug = slug
        super().save(*args, **kwargs)
    
    class Meta:
        unique_together = ['scan', 'number']

    def __str__(self):
        return f"{self.scan.main_title} – Tome {self.number}"

class ChapterScan(models.Model):
    tome_scan = models.ForeignKey(
        TomeScan,
        on_delete=models.CASCADE,
        related_name='scan_chapters'
    )
    number = models.PositiveIntegerField()
    title = models.CharField(max_length=255)

    class Meta:
        unique_together = ['tome_scan', 'number']

    def __str__(self):
        return f"Chapitre {self.number} : {self.title}"

class TomeScanImage(models.Model):
    tome_scan = models.ForeignKey(TomeScan, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='scan_images/')
    description = models.CharField(max_length=255, blank=True)
    
    def save(self, *args, **kwargs):
        # Générer le nom de fichier basé sur le slug de l'anime
        scan_slug = slugify(self.scan.slug)
        base_filename = f"{scan_slug}"

        # Vérifier s'il existe déjà une image avec ce nom (pour ajouter un suffixe)
        count = 1
        while TomeScanImage.objects.filter(image__startswith=base_filename).exists():
            base_filename = f"{scan_slug}-{count}"
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
        return f"Image de {self.scan.main_title}"


#relation

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

class RelationScan(models.Model):
    
    scan_source = models.ForeignKey(
        'Scan',
        on_delete=models.CASCADE,
        related_name='relations_as_source'
    )
    scan_target = models.ForeignKey(
        'Scan',
        on_delete=models.CASCADE,
        related_name='relations_as_target'
    )
    relation_type = models.ForeignKey(
        RelationType,
        on_delete=models.CASCADE
    )
    
    class Meta:
        unique_together = ('scan_source', 'scan_target')
        
    def __str__(self):
        return f"{self.scan_source} → {self.relation_type} → {self.scan_target}"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        inverse_type = self.relation_type.inverse

        if inverse_type and not RelationScan.objects.filter(
            scan_source=self.scan_target,
            scan_target=self.scan_source,
            relation_type=inverse_type
        ).exists():
            RelationScan.objects.create(
                scan_source=self.scan_target,
                scan_target=self.scan_source,
                relation_type=inverse_type
            )

    def delete(self, *args, **kwargs):
        inverse_type = self.relation_type.inverse
        if inverse_type:
            RelationScan.objects.filter(
                scan_source=self.scan_target,
                scan_target=self.scan_source,
                relation_type=inverse_type
            ).delete()
        super().delete(*args, **kwargs)

class RelationAnimeManga(models.Model):
    SOURCE_TYPE_CHOICES = [
        ('anime', 'Anime'),
        ('manga', 'Manga'),
    ]
    
    anime = models.ForeignKey(
        'Anime',
        on_delete=models.CASCADE,
        related_name='relations_as_anime_manga'
    )
    manga = models.ForeignKey(
        'Manga',
        on_delete=models.CASCADE,
        related_name='relations_as_anime_manga'
    )
    relation_type = models.ForeignKey(
        RelationType,
        on_delete=models.CASCADE
    )
    source_type = models.CharField(max_length=10, choices=SOURCE_TYPE_CHOICES)
    
    class Meta:
        unique_together = ('anime', 'manga', 'source_type')
    
    def __str__(self):
        if source_type == 'anime':
            return f"{self.anime} → {self.relation_type} → {self.manga}"
        else:
            return f"{self.manga} → {self.relation_type} → {self.anime}"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        inverse_type = self.relation_type.inverse

        if not inverse_type:
            return

        # Détermine les valeurs inversées
        inverse_source_type = 'manga' if self.source_type == 'anime' else 'anime'
        inverse_anime = self.anime
        inverse_manga = self.manga

        # Vérifie si la relation inverse existe déjà
        if not RelationAnimeManga.objects.filter(
            anime=inverse_anime,
            manga=inverse_manga,
            relation_type=inverse_type,
            source_type=inverse_source_type
        ).exists():
            RelationAnimeManga.objects.create(
                anime=inverse_anime,
                manga=inverse_manga,
                relation_type=inverse_type,
                source_type=inverse_source_type
            )

    def delete(self, *args, **kwargs):
        inverse_type = self.relation_type.inverse
        if inverse_type:
            inverse_source_type = 'manga' if self.source_type == 'anime' else 'anime'
            RelationAnimeManga.objects.filter(
                anime=self.anime,
                manga=self.manga,
                relation_type=inverse_type,
                source_type=inverse_source_type
            ).delete()

        super().delete(*args, **kwargs)

class RelationAnimeScan(models.Model):
    SOURCE_TYPE_CHOICES = [
        ('anime', 'Anime'),
        ('scan', 'Scan'),
    ]
    
    anime = models.ForeignKey(
        'Anime',
        on_delete=models.CASCADE,
        related_name='relations_as_anime_scan'
    )
    scan = models.ForeignKey(
        'Scan',
        on_delete=models.CASCADE,
        related_name='relations_as_anime_scan'
    )
    relation_type = models.ForeignKey(
        RelationType,
        on_delete=models.CASCADE
    )
    source_type = models.CharField(max_length=10, choices=SOURCE_TYPE_CHOICES)
    
    class Meta:
        unique_together = ('anime', 'scan', 'source_type')
    
    def __str__(self):
        if source_type == 'anime':
            return f"{self.anime} → {self.relation_type} → {self.scan}"
        else:
            return f"{self.scan} → {self.relation_type} → {self.anime}"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        inverse_type = self.relation_type.inverse

        if not inverse_type:
            return

        # Détermine les valeurs inversées
        inverse_source_type = 'scan' if self.source_type == 'anime' else 'anime'
        inverse_anime = self.anime
        inverse_scan = self.scan

        # Vérifie si la relation inverse existe déjà
        if not RelationAnimeScan.objects.filter(
            anime=inverse_anime,
            scan=inverse_scan,
            relation_type=inverse_type,
            source_type=inverse_source_type
        ).exists():
            RelationAnimeScan.objects.create(
                anime=inverse_anime,
                scan=inverse_scan,
                relation_type=inverse_type,
                source_type=inverse_source_type
            )

    def delete(self, *args, **kwargs):
        inverse_type = self.relation_type.inverse
        if inverse_type:
            inverse_source_type = 'scan' if self.source_type == 'anime' else 'anime'
            RelationAnimeScan.objects.filter(
                anime=self.anime,
                scan=self.scan,
                relation_type=inverse_type,
                source_type=inverse_source_type
            ).delete()

        super().delete(*args, **kwargs)

class RelationMangaScan(models.Model):
    SOURCE_TYPE_CHOICES = [
        ('manga', 'Manga'),
        ('scan', 'Scan'),
    ]
    
    manga = models.ForeignKey(
        'Manga',
        on_delete=models.CASCADE,
        related_name='relations_as_manga_scan'
    )
    scan = models.ForeignKey(
        'Scan',
        on_delete=models.CASCADE,
        related_name='relations_as_manga_scan'
    )
    relation_type = models.ForeignKey(
        RelationType,
        on_delete=models.CASCADE
    )
    source_type = models.CharField(max_length=10, choices=SOURCE_TYPE_CHOICES)
    
    class Meta:
        unique_together = ('manga', 'scan', 'source_type')
    
    def __str__(self):
        if source_type == 'manga':
            return f"{self.manga} → {self.relation_type} → {self.scan}"
        else:
            return f"{self.scan} → {self.relation_type} → {self.manga}"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        inverse_type = self.relation_type.inverse

        if not inverse_type:
            return

        # Détermine les valeurs inversées
        inverse_source_type = 'scan' if self.source_type == 'manga' else 'manga'
        inverse_manga = self.manga
        inverse_scan = self.scan

        # Vérifie si la relation inverse existe déjà
        if not RelationMangaScan.objects.filter(
            manga=inverse_manga,
            scan=inverse_scan,
            relation_type=inverse_type,
            source_type=inverse_source_type
        ).exists():
            RelationMangaScan.objects.create(
                manga=inverse_manga,
                scan=inverse_scan,
                relation_type=inverse_type,
                source_type=inverse_source_type
            )

    def delete(self, *args, **kwargs):
        inverse_type = self.relation_type.inverse
        if inverse_type:
            inverse_source_type = 'scan' if self.source_type == 'manga' else 'manga'
            RelationMangaScan.objects.filter(
                manga=self.manga,
                scan=self.scan,
                relation_type=inverse_type,
                source_type=inverse_source_type
            ).delete()

        super().delete(*args, **kwargs)