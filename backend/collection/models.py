from django.db import models
from slugify import slugify  # pip install python-slugify
import os

#genre et theme
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




# anime
class Anime(models.Model):
    ORIGIN_CHOICES = [
        ('original', '	Œuvre originale'),
        ('manga', 'Manga'),
        ('light-novel', 'Light Novel'),
        ('visual-novel', 'Visual Novel'),
        ('jeu-video', 'Jeu vidéo'),
        ('Jouets-/-figurines', 'Jouets / Figurines'),
        ('roman', 'Roman'),
        ('jeu-de-carte', 'Jeu de carte'),
        ('vocaloid', 'Vocaloid'),
        ('projet-transmedia', 'Projet transmédia'),
        ('autre', 'Autre'),
        ('anime', 'Anime'),
        ('doujinshi', 'Doujinshi'),
        ('film', 'Film'),
        ('chanson', 'Chanson'),
        ('vtuber', 'Vtuber'),
    ]
    
    FORMAT_CHOICES = [
        ('serie', 'Série'),
        ('oav', 'OAV'),
        ('film', 'Film'),
        ('special', 'Spécial'),
        ('musique', 'Musique'),
        ('animix-/-picture-drama', 'Animix / Picture drama'),
        ('court-metrage', 'Court-métrage'),
        ('publicité', 'Publicité'),
        ('inconnu', 'inconnu'),
        ('bonus', 'Bonus'),
    ]
    
    main_title = models.CharField(max_length=255)
    origin = models.CharField(max_length=50, choices=ORIGIN_CHOICES)
    synopsis = models.TextField()
    date_start = models.DateField(null=True, blank=True)
    date_end = models.DateField(null=True, blank=True)
    episode = models.IntegerField()
    duration = models.IntegerField(help_text="Durée moyenne d’un épisode en minutes")
    season = models.CharField(max_length=50, null=True, blank=True)
    studio = models.CharField(max_length=150, null=True, blank=True)
    studio_3D = models.CharField(max_length=150, null=True, blank=True)
    format = models.CharField(max_length=50, choices=FORMAT_CHOICES)
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
    CODE_CHOICES = [
        ('jp', 'jp'),
        ('en', 'en'),
        ('fr', 'fr'),
        ('ch', 'ch'),
    ]
    
    
    anime = models.ForeignKey(Anime, related_name='anime_titles', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    language_code = models.CharField(max_length=2, choices=CODE_CHOICES)  # Code de la langue (ex: 'en' pour anglais, 'ja' pour japonais)
    is_original = models.BooleanField(default=False)  # Indique si le titre est original (true) ou une version modifiée (false)
    is_nickname = models.BooleanField(default=False)  # Indique si le titre est un surnom ou un autre alias
    is_main = models.BooleanField(default=False)      # Indique si le titre celui que j'utiliserais principalement
    slug = models.CharField(max_length=255)  # Pour une URL simplifiée du titre, souvent utilisée pour les routes
    
    class Meta:
        # Contrainte d'unicité pour assurer qu'il n'y ait pas de doublon
        constraints = [
            models.UniqueConstraint(fields=['anime', 'title', 'language_code'], name='unique_anime_title_language')
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
        return f"Title: {self.title} ({self.language_code}) - Original: {self.is_original}"
    
class RelationAnime(models.Model):
    RELATION_CHOICES = [
        ('suite', 'Suite'),
        ('prequel', 'Préquelle'),
        ('spin-off', 'Spin-off'),
        ('remake', 'Remake'),
        ('histoire-supplémentaire', 'Histoire supplémentaire'),
        ('version-alternative', 'Version alternative'),
        ('compilation', 'Compilation'),
        ('parodie', 'Parodie'),
        ('pilote', 'Pilote')
        # Tu peux en ajouter d’autres ici
    ]

    INVERSE_RELATIONS = {
        'suite': 'prequel',
        'prequel': 'suite',
        'spin-off': 'origine-du-spin-off',
        'remake': 'origine-du-remake',  # symétrique
        'histoire-supplémentaire': 'histoire-d-origine',
        'version-alternative': 'version-alternative',
        'compilation': 'histoire-complete',
        'parodie': 'origine-de-la-parodie',
        'pilote': 'version-finale'
    }

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
    relation_type = models.CharField(max_length=50, choices=RELATION_CHOICES)

    class Meta:
        unique_together = ('anime_source', 'anime_target', 'relation_type')

    def __str__(self):
        return f"{self.anime_source} → {self.relation_type} → {self.anime_target}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        inverse_type = self.INVERSE_RELATIONS.get(self.relation_type)

        # Vérifie si l’inverse n’existe pas déjà
        if inverse_type and not RelationAnime.objects.filter(
            anime_source=self.anime_target,
            anime_target=self.anime_source,
            relation_type=inverse_type
        ).exists():
            RelationAnime.objects.create(
                anime_source=self.anime_target,
                anime_target=self.anime_source,
                relation_type=inverse_type
            )
            
    def delete(self, *args, **kwargs):
        inverse_type = self.INVERSE_RELATIONS.get(self.relation_type)
        # Supprime la relation inverse si elle existe
        if inverse_type:
            RelationAnime.objects.filter(
                anime_source=self.anime_target,
                anime_target=self.anime_source,
                relation_type=inverse_type
            ).delete()
        super().delete(*args, **kwargs)
        


#manga  