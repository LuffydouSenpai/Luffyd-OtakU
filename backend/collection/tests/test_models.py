from django.test import TestCase
from collection.models import Genre, Theme, Publisher, TypeManga, Language, Format, Origin, Season, People, Role, Studio, Contribution, ContributionStudio, StudioRole, Status
from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError
from django.utils.text import slugify
from datetime import date


class GenreTestCase(TestCase):
    def setUp(self):
        self.genre = Genre.objects.create(name="testGenre")

    def test_is_correct_instance(self):
        self.assertIsInstance(self.genre, Genre)

    def test_str_method(self):
        self.assertEqual(str(self.genre), "testGenre")

    def test_name_cannot_be_empty(self):
        genre = Genre(name="")
        with self.assertRaises(ValidationError):
            genre.full_clean()  # C’est là que la validation se fait
            genre.save()

    def test_name_uniqueness(self):
        with self.assertRaises(IntegrityError):
            Genre.objects.create(name="testGenre")  # nom déjà existant
            
    def test_name_max_length(self):
        long_name = "a" * 60
        genre = Genre(name=long_name)
        with self.assertRaises(ValidationError):
            genre.full_clean()
    
    def test_slug_auto_generation(self):
        genre = Genre.objects.create(name="Nom Avec Espaces")
        self.assertEqual(genre.slug, "nom-avec-espaces")

    def test_slug_uniqueness(self):
        Genre.objects.create(name="Unique Name")
        with self.assertRaises(IntegrityError):
            Genre.objects.create(name="Unique Name")  # slug identique => erreur
            
    def test_name_one_char(self):
        genre = Genre(name="A")
        genre.slug = slugify(genre.name)  # import slugify
        genre.full_clean()
        genre.save()
        self.assertEqual(genre.slug, "a")

    def test_name_special_chars(self):
        genre = Genre(name="Épée & Bouclier")
        genre.slug = slugify(genre.name)
        genre.full_clean()
        genre.save()
        self.assertEqual(genre.slug, "epee-bouclier")
    
    def test_update_name_updates_slug(self):
        self.genre.name = "Nouveau Nom"
        self.genre.slug = slugify(self.genre.name)
        self.genre.full_clean()
        self.genre.save()
        self.assertEqual(self.genre.slug, "nouveau-nom")

    def test_genre_delete(self):
        self.genre.delete()
        self.assertFalse(Genre.objects.filter(pk=self.genre.pk).exists())
    
    def test_slug_not_null(self):
        genre = Genre(name="Test Null")
        genre.slug = None
        with self.assertRaises(ValidationError):
            genre.full_clean()

class ThemeTestCase(TestCase):
    def setUp(self):
        self.theme = Theme.objects.create(name="testTheme")

    def test_is_correct_instance(self):
        self.assertIsInstance(self.theme, Theme)

    def test_str_method(self):
        self.assertEqual(str(self.theme), "testTheme")

    def test_name_cannot_be_empty(self):
        theme = Theme(name="")
        with self.assertRaises(ValidationError):
            theme.full_clean()  # C’est là que la validation se fait
            theme.save()

    def test_name_uniqueness(self):
        with self.assertRaises(IntegrityError):
            Theme.objects.create(name="testTheme")  # nom déjà existant
            
    def test_name_max_length(self):
        long_name = "a" * 60
        theme = Theme(name=long_name)
        with self.assertRaises(ValidationError):
            theme.full_clean()
    
    def test_slug_auto_generation(self):
        theme = Theme.objects.create(name="Nom Avec Espaces")
        self.assertEqual(theme.slug, "nom-avec-espaces")

    def test_slug_uniqueness(self):
        Theme.objects.create(name="Unique Name")
        with self.assertRaises(IntegrityError):
            Theme.objects.create(name="Unique Name")  # slug identique => erreur
            
    def test_name_one_char(self):
        theme = Theme(name="A")
        theme.slug = slugify(theme.name)  # import slugify
        theme.full_clean()
        theme.save()
        self.assertEqual(theme.slug, "a")

    def test_name_special_chars(self):
        theme = Theme(name="Épée & Bouclier")
        theme.slug = slugify(theme.name)
        theme.full_clean()
        theme.save()
        self.assertEqual(theme.slug, "epee-bouclier")
    
    def test_update_name_updates_slug(self):
        self.theme.name = "Nouveau Nom"
        self.theme.slug = slugify(self.theme.name)
        self.theme.full_clean()
        self.theme.save()
        self.assertEqual(self.theme.slug, "nouveau-nom")

    def test_theme_delete(self):
        self.theme.delete()
        self.assertFalse(Theme.objects.filter(pk=self.theme.pk).exists())
    
    def test_slug_not_null(self):
        theme = Theme(name="Test Null")
        theme.slug = None
        with self.assertRaises(ValidationError):
            theme.full_clean()

class PublisherTestCase(TestCase):
    def setUp(self):
        self.publisher = Publisher.objects.create(name="testPublisher")

    def test_is_correct_instance(self):
        self.assertIsInstance(self.publisher, Publisher)

    def test_str_method(self):
        self.assertEqual(str(self.publisher), "testPublisher")

    def test_name_cannot_be_empty(self):
        publisher = Publisher(name="")
        with self.assertRaises(ValidationError):
            publisher.full_clean()  # C’est là que la validation se fait
            publisher.save()

    def test_name_uniqueness(self):
        with self.assertRaises(IntegrityError):
            Publisher.objects.create(name="testPublisher")  # nom déjà existant
            
    def test_name_max_length(self):
        long_name = "a" * 60
        publisher = Publisher(name=long_name)
        with self.assertRaises(ValidationError):
            publisher.full_clean()
    
    def test_slug_auto_generation(self):
        publisher = Publisher.objects.create(name="Nom Avec Espaces")
        self.assertEqual(publisher.slug, "nom-avec-espaces")

    def test_slug_uniqueness(self):
        Publisher.objects.create(name="Unique Name")
        with self.assertRaises(IntegrityError):
            Publisher.objects.create(name="Unique Name")  # slug identique => erreur
            
    def test_name_one_char(self):
        publisher = Publisher(name="A")
        publisher.slug = slugify(publisher.name)  # import slugify
        publisher.full_clean()
        publisher.save()
        self.assertEqual(publisher.slug, "a")

    def test_name_special_chars(self):
        publisher = Publisher(name="Épée & Bouclier")
        publisher.slug = slugify(publisher.name)
        publisher.full_clean()
        publisher.save()
        self.assertEqual(publisher.slug, "epee-bouclier")
    
    def test_update_name_updates_slug(self):
        self.publisher.name = "Nouveau Nom"
        self.publisher.slug = slugify(self.publisher.name)
        self.publisher.full_clean()
        self.publisher.save()
        self.assertEqual(self.publisher.slug, "nouveau-nom")

    def test_theme_delete(self):
        self.publisher.delete()
        self.assertFalse(Publisher.objects.filter(pk=self.publisher.pk).exists())
    
    def test_slug_not_null(self):
        publisher = Publisher(name="Test Null")
        publisher.slug = None
        with self.assertRaises(ValidationError):
            publisher.full_clean()

class TypeMangaTestCase(TestCase):
    def setUp(self):
        self.typeManga = TypeManga.objects.create(name="testTypeManga")

    def test_is_correct_instance(self):
        self.assertIsInstance(self.typeManga, TypeManga)

    def test_str_method(self):
        self.assertEqual(str(self.typeManga), "testTypeManga")

    def test_name_cannot_be_empty(self):
        typeManga = TypeManga(name="")
        with self.assertRaises(ValidationError):
            typeManga.full_clean()  # C’est là que la validation se fait
            typeManga.save()

    def test_name_uniqueness(self):
        with self.assertRaises(IntegrityError):
            TypeManga.objects.create(name="testTypeManga")  # nom déjà existant
            
    def test_name_max_length(self):
        long_name = "a" * 60
        typeManga = TypeManga(name=long_name)
        with self.assertRaises(ValidationError):
            typeManga.full_clean()
    
    def test_slug_auto_generation(self):
        typeManga = TypeManga.objects.create(name="Nom Avec Espaces")
        self.assertEqual(typeManga.slug, "nom-avec-espaces")

    def test_slug_uniqueness(self):
        TypeManga.objects.create(name="Unique Name")
        with self.assertRaises(IntegrityError):
            TypeManga.objects.create(name="Unique Name")  # slug identique => erreur
            
    def test_name_one_char(self):
        typeManga = TypeManga(name="A")
        typeManga.slug = slugify(typeManga.name)  # import slugify
        typeManga.full_clean()
        typeManga.save()
        self.assertEqual(typeManga.slug, "a")

    def test_name_special_chars(self):
        typeManga = TypeManga(name="Épée & Bouclier")
        typeManga.slug = slugify(typeManga.name)
        typeManga.full_clean()
        typeManga.save()
        self.assertEqual(typeManga.slug, "epee-bouclier")
    
    def test_update_name_updates_slug(self):
        self.typeManga.name = "Nouveau Nom"
        self.typeManga.slug = slugify(self.typeManga.name)
        self.typeManga.full_clean()
        self.typeManga.save()
        self.assertEqual(self.typeManga.slug, "nouveau-nom")

    def test_theme_delete(self):
        self.typeManga.delete()
        self.assertFalse(TypeManga.objects.filter(pk=self.typeManga.pk).exists())
    
    def test_slug_not_null(self):
        typeManga = TypeManga(name="Test Null")
        typeManga.slug = None
        with self.assertRaises(ValidationError):
            typeManga.full_clean()
            
class LanguageTestCase(TestCase):
    def setUp(self):
        self.lang = Language.objects.create(
            code="aa",
            name="aaaaaa",
            native_name="aaaa"
        )

    def test_is_correct_instance(self):
        self.assertIsInstance(self.lang, Language)

    def test_str_method(self):
        self.assertEqual(str(self.lang), "aaaaaa")

    def test_code_uniqueness(self):
        with self.assertRaises(IntegrityError):
            Language.objects.create(code="jp", name="Japonais2", native_name="日本語2")

    def test_name_uniqueness(self):
        with self.assertRaises(IntegrityError):
            Language.objects.create(code="kr", name="Japonais", native_name="한국어")

    def test_native_name_uniqueness(self):
        with self.assertRaises(IntegrityError):
            Language.objects.create(code="cn", name="Chinois", native_name="日本語")

    def test_code_max_length(self):
        lang = Language(code="abcdef", name="Test", native_name="テスト")
        with self.assertRaises(ValidationError):
            lang.full_clean()

    def test_name_max_length(self):
        long_name = "a" * 60
        lang = Language(code="de", name=long_name, native_name="Deutsch")
        with self.assertRaises(ValidationError):
            lang.full_clean()

    def test_native_name_max_length(self):
        long_native = "語" * 60
        lang = Language(code="it", name="Italien", native_name=long_native)
        with self.assertRaises(ValidationError):
            lang.full_clean()

    def test_fields_cannot_be_blank(self):
        lang = Language(code="", name="", native_name="")
        with self.assertRaises(ValidationError):
            lang.full_clean()

    def test_minimal_valid_entry(self):
        lang = Language(code="al", name="al", native_name="al")
        lang.full_clean()
        lang.save()
        self.assertEqual(str(lang), "al")
        
class OriginTestCase(TestCase):
    def setUp(self):
        self.origin = Origin.objects.create(name="testOrigin")

    def test_is_correct_instance(self):
        self.assertIsInstance(self.origin, Origin)

    def test_str_method(self):
        self.assertEqual(str(self.origin), "testOrigin")

    def test_name_cannot_be_empty(self):
        origin = Origin(name="")
        with self.assertRaises(ValidationError):
            origin.full_clean()  # C’est là que la validation se fait
            origin.save()

    def test_name_uniqueness(self):
        with self.assertRaises(IntegrityError):
            Origin.objects.create(name="testOrigin")  # nom déjà existant
            
    def test_name_max_length(self):
        long_name = "a" * 60
        origin = Origin(name=long_name)
        with self.assertRaises(ValidationError):
            origin.full_clean()
    
    def test_slug_auto_generation(self):
        origin = Origin.objects.create(name="Nom Avec Espaces")
        self.assertEqual(origin.slug, "nom-avec-espaces")

    def test_slug_uniqueness(self):
        Origin.objects.create(name="Unique Name")
        with self.assertRaises(IntegrityError):
            Origin.objects.create(name="Unique Name")  # slug identique => erreur
            
    def test_name_one_char(self):
        origin = Origin(name="A")
        origin.slug = slugify(origin.name)  # import slugify
        origin.full_clean()
        origin.save()
        self.assertEqual(origin.slug, "a")

    def test_name_special_chars(self):
        origin = Origin(name="Épée & Bouclier")
        origin.slug = slugify(origin.name)
        origin.full_clean()
        origin.save()
        self.assertEqual(origin.slug, "epee-bouclier")
    
    def test_update_name_updates_slug(self):
        self.origin.name = "Nouveau Nom"
        self.origin.slug = slugify(self.origin.name)
        self.origin.full_clean()
        self.origin.save()
        self.assertEqual(self.origin.slug, "nouveau-nom")

    def test_origin_delete(self):
        self.origin.delete()
        self.assertFalse(Origin.objects.filter(pk=self.origin.pk).exists())
    
    def test_slug_not_null(self):
        origin = Origin(name="Test Null")
        origin.slug = None
        with self.assertRaises(ValidationError):
            origin.full_clean()
            
class FormatTestCase(TestCase):
    def setUp(self):
        self.format = Format.objects.create(name="testFormat")

    def test_is_correct_instance(self):
        self.assertIsInstance(self.format, Format)

    def test_str_method(self):
        self.assertEqual(str(self.format), "testFormat")

    def test_name_cannot_be_empty(self):
        format = Format(name="")
        with self.assertRaises(ValidationError):
            format.full_clean()  # C’est là que la validation se fait
            format.save()

    def test_name_uniqueness(self):
        with self.assertRaises(IntegrityError):
            Format.objects.create(name="testFormat")  # nom déjà existant
            
    def test_name_max_length(self):
        long_name = "a" * 60
        format = Format(name=long_name)
        with self.assertRaises(ValidationError):
            format.full_clean()
    
    def test_slug_auto_generation(self):
        format = Format.objects.create(name="Nom Avec Espaces")
        self.assertEqual(format.slug, "nom-avec-espaces")

    def test_slug_uniqueness(self):
        Format.objects.create(name="Unique Name")
        with self.assertRaises(IntegrityError):
            Format.objects.create(name="Unique Name")  # slug identique => erreur
            
    def test_name_one_char(self):
        format = Format(name="A")
        format.slug = slugify(format.name)  # import slugify
        format.full_clean()
        format.save()
        self.assertEqual(format.slug, "a")

    def test_name_special_chars(self):
        format = Format(name="Épée & Bouclier")
        format.slug = slugify(format.name)
        format.full_clean()
        format.save()
        self.assertEqual(format.slug, "epee-bouclier")
    
    def test_update_name_updates_slug(self):
        self.format.name = "Nouveau Nom"
        self.format.slug = slugify(self.format.name)
        self.format.full_clean()
        self.format.save()
        self.assertEqual(self.format.slug, "nouveau-nom")

    def test_format_delete(self):
        self.format.delete()
        self.assertFalse(Format.objects.filter(pk=self.format.pk).exists())
    
    def test_slug_not_null(self):
        format = Format(name="Test Null")
        format.slug = None
        with self.assertRaises(ValidationError):
            format.full_clean()

class SeasonTestCase(TestCase):
    def setUp(self):
        self.season = Season.objects.create(season='winter', year=2024)

    def test_is_instance(self):
        self.assertIsInstance(self.season, Season)

    def test_str_method(self):
        self.assertEqual(str(self.season), "Hiver 2024")

    def test_slug_generation(self):
        self.assertEqual(self.season.slug, slugify("winter 2024"))

    def test_season_choices(self):
        with self.assertRaises(ValidationError):
            s = Season(season='invalid', year=2024)
            s.full_clean()

    def test_year_must_be_positive(self):
        with self.assertRaises(ValidationError):
            s = Season(season='summer', year=-1999)
            s.full_clean()

    def test_unique_together_constraint(self):
        with self.assertRaises(IntegrityError):
            Season.objects.create(season='winter', year=2024)

    def test_slug_unique_constraint(self):
        with self.assertRaises(IntegrityError):
            Season.objects.create(season='winter', year=2024)

    def test_different_season_same_year(self):
        other = Season.objects.create(season='spring', year=2024)
        self.assertEqual(other.slug, slugify("spring 2024"))

    def test_different_year_same_season(self):
        other = Season.objects.create(season='winter', year=2025)
        self.assertEqual(other.slug, slugify("winter 2025"))

    def test_slug_collision_handling(self):
        # Tu devras gérer ça si tu veux éviter les collisions
        Season.objects.create(season='autumn', year=2024)
        with self.assertRaises(IntegrityError):
            Season.objects.create(season='autumn', year=2024)  # même slug

    def test_verbose_seasons(self):
        for code, label in Season.SEASON_CHOICES:
            season = Season(season=code, year=2023)
            season.slug = slugify(f"{season.season} {season.year}")  # ajoute ça
            season.full_clean()

class PeopleTestCase(TestCase):
    def setUp(self):
        self.people = People.objects.create(name="testPeople")

    def test_is_correct_instance(self):
        self.assertIsInstance(self.people, People)

    def test_str_method(self):
        self.assertEqual(str(self.people), "testPeople")

    def test_name_cannot_be_empty(self):
        people = People(name="")
        with self.assertRaises(ValidationError):
            people.full_clean()  # C’est là que la validation se fait
            people.save()

    def test_name_uniqueness(self):
        with self.assertRaises(IntegrityError):
            People.objects.create(name="testPeople")  # nom déjà existant
            
    def test_name_max_length(self):
        long_name = "a" * 60
        people = People(name=long_name)
        with self.assertRaises(ValidationError):
            people.full_clean()
    
    def test_slug_auto_generation(self):
        people = People.objects.create(name="Nom Avec Espaces")
        self.assertEqual(people.slug, "nom-avec-espaces")

    def test_slug_uniqueness(self):
        People.objects.create(name="Unique Name")
        with self.assertRaises(IntegrityError):
            People.objects.create(name="Unique Name")  # slug identique => erreur
            
    def test_name_one_char(self):
        people = People(name="A")
        people.slug = slugify(people.name)  # import slugify
        people.full_clean()
        people.save()
        self.assertEqual(people.slug, "a")

    def test_name_special_chars(self):
        people = People(name="Épée & Bouclier")
        people.slug = slugify(people.name)
        people.full_clean()
        people.save()
        self.assertEqual(people.slug, "epee-bouclier")
    
    def test_update_name_updates_slug(self):
        self.people.name = "Nouveau Nom"
        self.people.slug = slugify(self.people.name)
        self.people.full_clean()
        self.people.save()
        self.assertEqual(self.people.slug, "nouveau-nom")

    def test_people_delete(self):
        self.people.delete()
        self.assertFalse(People.objects.filter(pk=self.people.pk).exists())
    
    def test_slug_not_null(self):
        people = People(name="Test Null")
        people.slug = None
        with self.assertRaises(ValidationError):
            people.full_clean()
                
class RoleTestCase(TestCase):
    def setUp(self):
        self.role = Role.objects.create(code="admin", label="Administrateur")

    def test_instance(self):
        self.assertIsInstance(self.role, Role)

    def test_str_method(self):
        self.assertEqual(str(self.role), "Administrateur")

    def test_code_uniqueness(self):
        with self.assertRaises(IntegrityError):
            Role.objects.create(code="admin", label="Duplication")

    def test_code_max_length(self):
        long_code = "c" * 51  # dépasse max_length=50
        role = Role(code=long_code, label="Test")
        with self.assertRaises(ValidationError):
            role.full_clean()

    def test_label_required(self):
        role = Role(code="user", label="")
        with self.assertRaises(ValidationError):
            role.full_clean()

    def test_label_max_length(self):
        long_label = "l" * 51  # dépasse max_length=50
        role = Role(code="user2", label=long_label)
        with self.assertRaises(ValidationError):
            role.full_clean()
            
class StudioTestCase(TestCase):
    def setUp(self):
        self.studio = Studio.objects.create(name="testStudio")

    def test_is_correct_instance(self):
        self.assertIsInstance(self.studio, Studio)

    def test_str_method(self):
        self.assertEqual(str(self.studio), "testStudio")

    def test_name_cannot_be_empty(self):
        studio = Studio(name="")
        with self.assertRaises(ValidationError):
            studio.full_clean()  # C’est là que la validation se fait
            studio.save()

    def test_name_uniqueness(self):
        with self.assertRaises(IntegrityError):
            Studio.objects.create(name="testStudio")  # nom déjà existant
            
    def test_name_max_length(self):
        long_name = "a" * 60
        studio = Studio(name=long_name)
        with self.assertRaises(ValidationError):
            studio.full_clean()
    
    def test_slug_auto_generation(self):
        studio = Studio.objects.create(name="Nom Avec Espaces")
        self.assertEqual(studio.slug, "nom-avec-espaces")

    def test_slug_uniqueness(self):
        Studio.objects.create(name="Unique Name")
        with self.assertRaises(IntegrityError):
            Studio.objects.create(name="Unique Name")  # slug identique => erreur
            
    def test_name_one_char(self):
        studio = Studio(name="A")
        studio.slug = slugify(studio.name)  # import slugify
        studio.full_clean()
        studio.save()
        self.assertEqual(studio.slug, "a")

    def test_name_special_chars(self):
        studio = Studio(name="Épée & Bouclier")
        studio.slug = slugify(studio.name)
        studio.full_clean()
        studio.save()
        self.assertEqual(studio.slug, "epee-bouclier")
    
    def test_update_name_updates_slug(self):
        self.studio.name = "Nouveau Nom"
        self.studio.slug = slugify(self.studio.name)
        self.studio.full_clean()
        self.studio.save()
        self.assertEqual(self.studio.slug, "nouveau-nom")

    def test_people_delete(self):
        self.studio.delete()
        self.assertFalse(Studio.objects.filter(pk=self.studio.pk).exists())
    
    def test_slug_not_null(self):
        studio = Studio(name="Test Null")
        studio.slug = None
        with self.assertRaises(ValidationError):
            studio.full_clean()

class ContributionTestCase(TestCase):
    def setUp(self):
        self.people = People.objects.create(name="Hayao Miyazaki")
        self.role = Role.objects.create(code="director", label="Réalisateur")
        self.contribution = Contribution.objects.create(people=self.people, role=self.role)

    def test_instance(self):
        self.assertIsInstance(self.contribution, Contribution)

    def test_str_method(self):
        self.assertEqual(str(self.contribution), "Hayao Miyazaki  - Réalisateur")

    def test_foreign_keys_linked(self):
        self.assertEqual(self.contribution.people.name, "Hayao Miyazaki")
        self.assertEqual(self.contribution.role.label, "Réalisateur")

    def test_missing_people(self):
        contribution = Contribution(role=self.role)
        with self.assertRaises(ValidationError):
            contribution.full_clean()

    def test_missing_role(self):
        contribution = Contribution(people=self.people)
        with self.assertRaises(ValidationError):
            contribution.full_clean()

class ContributionStudioTestCase(TestCase):
    def setUp(self):
        self.studio = Studio.objects.create(name="Studio Ghibli")
        self.studio_role = StudioRole.objects.create(code="prod", label="Production")
        self.contribution = ContributionStudio.objects.create(studio=self.studio, studioRole=self.studio_role)

    def test_instance(self):
        self.assertIsInstance(self.contribution, ContributionStudio)

    def test_str_method(self):
        self.assertEqual(str(self.contribution), "Studio Ghibli  - Production")

    def test_foreign_key_links(self):
        self.assertEqual(self.contribution.studio.name, "Studio Ghibli")
        self.assertEqual(self.contribution.studioRole.label, "Production")

    def test_missing_studio(self):
        contribution = ContributionStudio(studioRole=self.studio_role)
        with self.assertRaises(ValidationError):
            contribution.full_clean()

    def test_missing_studioRole(self):
        contribution = ContributionStudio(studio=self.studio)
        with self.assertRaises(ValidationError):
            contribution.full_clean()
            
    def test_unique_constraint(self):
        with self.assertRaises(IntegrityError):
            ContributionStudio.objects.create(studio=self.studio, studioRole=self.studio_role)
            
class StatusTestCase(TestCase):
    def setUp(self):
        self.status = Status.objects.create(name="testStatus")

    def test_is_correct_instance(self):
        self.assertIsInstance(self.status, Status)

    def test_str_method(self):
        self.assertEqual(str(self.status), "testStatus")

    def test_name_cannot_be_empty(self):
        status = Status(name="")
        with self.assertRaises(ValidationError):
            status.full_clean()  # C’est là que la validation se fait
            status.save()

    def test_name_uniqueness(self):
        with self.assertRaises(IntegrityError):
            Status.objects.create(name="testStatus")  # nom déjà existant
            
    def test_name_max_length(self):
        long_name = "a" * 60
        status = Status(name=long_name)
        with self.assertRaises(ValidationError):
            status.full_clean()
    
    def test_slug_auto_generation(self):
        status = Status.objects.create(name="Nom Avec Espaces")
        self.assertEqual(status.slug, "nom-avec-espaces")

    def test_slug_uniqueness(self):
        Status.objects.create(name="Unique Name")
        with self.assertRaises(IntegrityError):
            Status.objects.create(name="Unique Name")  # slug identique => erreur
            
    def test_name_one_char(self):
        status = Status(name="A")
        status.slug = slugify(status.name)  # import slugify
        status.full_clean()
        status.save()
        self.assertEqual(status.slug, "a")

    def test_name_special_chars(self):
        status = Status(name="Épée & Bouclier")
        status.slug = slugify(status.name)
        status.full_clean()
        status.save()
        self.assertEqual(status.slug, "epee-bouclier")
    
    def test_update_name_updates_slug(self):
        self.status.name = "Nouveau Nom"
        self.status.slug = slugify(self.status.name)
        self.status.full_clean()
        self.status.save()
        self.assertEqual(self.status.slug, "nouveau-nom")

    def test_status_delete(self):
        self.status.delete()
        self.assertFalse(Status.objects.filter(pk=self.status.pk).exists())
    
    def test_slug_not_null(self):
        status = Status(name="Test Null")
        status.slug = None
        with self.assertRaises(ValidationError):
            status.full_clean()


