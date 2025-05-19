from django.db import migrations

def create_initial_genres(apps, schema_editor):
    TypeManga = apps.get_model('collection', 'TypeManga')
    TypeManga.objects.bulk_create([
        TypeManga(name='Seinen', slug='seinen'),
        TypeManga(name='Shojo', slug='shojo'),
        TypeManga(name='Shonen', slug='shonen'),
        TypeManga(name='Yuri', slug='yuri'),
    ]),
    Language = apps.get_model('collection', 'Language')
    Language.objects.bulk_create([
        Language(code='jp', name='Japonais', native_name='日本語'),
        Language(code='fr', name='Français', native_name='Français'),
        Language(code='en', name='Anglais', native_name='English'),
    ]),
    RelationType = apps.get_model('collection', 'RelationType')

    # Étape 1 : On crée les objets sans inverse
    relations = {
        'suite': RelationType.objects.create(code='suite', label='Suite'),
        'prequel': RelationType.objects.create(code='prequel', label='Préquelle'),
        'spin_off': RelationType.objects.create(code='spin_off', label='Spin-off'),
        'origin_of_the_spin_off': RelationType.objects.create(code='origin_of_the_spin_off', label='Origine du spin-off'),
        'origin_story': RelationType.objects.create(code='origin_story', label="Histoire d'origine"),
        'additional_story': RelationType.objects.create(code='additional_story', label='Histoire supplémentaire'),
        'alternative': RelationType.objects.create(code='alternative', label='Version alternative'),
        'origine_of_adaptation': RelationType.objects.create(code='origine_of_adaptation', label="Origine de l'adaptation"),
        'adaptation': RelationType.objects.create(code='adaptation', label='Adaptation'),
    }

    # Étape 2 : On met à jour les relations inverses
    relations['suite'].inverse = relations['prequel']
    relations['prequel'].inverse = relations['suite']
    relations['spin_off'].inverse = relations['origin_of_the_spin_off']
    relations['origin_of_the_spin_off'].inverse = relations['spin_off']
    relations['origin_story'].inverse = relations['additional_story']
    relations['additional_story'].inverse = relations['origin_story']
    relations['alternative'].inverse = relations['alternative']  # auto-inverse
    relations['origine_of_adaptation'].inverse = relations['adaptation']
    relations['adaptation'].inverse = relations['origine_of_adaptation']

    # Save des mises à jour
    for r in relations.values():
        r.save()
    
    Origin = apps.get_model('collection', 'Origin')
    Origin.objects.bulk_create([
        Origin(name='Œuvre originale', slug='oeuvre-originale'),
        Origin(name='Light Novel', slug='light-novel'),
        Origin(name='Visual Novel', slug='visual-novel'),
        Origin(name='Jeu vidéo', slug='jeu-video'),
        Origin(name='Jouets / Figurines', slug='jouets-figurines'),
    ]),
    
    Format = apps.get_model('collection', 'Format')
    Format.objects.bulk_create([
        Format(name='Série', slug='serie'),
        Format(name='OAV', slug='oav'),
        Format(name='Film', slug='film'),
        Format(name='Spécial', slug='special'),
    ]),
    
    Role = apps.get_model('collection', 'Role')
    Role.objects.bulk_create([
        Role(code='author', label='Author'),
        Role(code='scenariste', label='Scenariste'),
        Role(code='designer', label='Designer'),
        Role(code='chara_designer', label='Chara_designer'),
    ]),
    
    StudioRole = apps.get_model('collection', 'StudioRole')
    StudioRole.objects.bulk_create([
        StudioRole(code='studio', label='Studio'),
        StudioRole(code='studio_3d', label='Studio_3d'),
    ]),
    
    Status = apps.get_model('collection', 'Status')
    Status.objects.bulk_create([
        Status(name='En cours', slug='en-cours'),
        Status(name='Terminé', slug='termine'),
        Status(name='Abandonné', slug='abandonne'),
    ]),
    

class Migration(migrations.Migration):

    dependencies = [
        ('collection', '0042_alter_origin_slug'),
    ]

    operations = [
        migrations.RunPython(create_initial_genres),
    ]