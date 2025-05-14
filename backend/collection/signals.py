import os
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver
from .models import AnimeImage

@receiver(post_delete, sender=AnimeImage)
def delete_image_file(sender, instance, **kwargs):
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)

@receiver(pre_save, sender=AnimeImage)
def delete_old_image_on_update(sender, instance, **kwargs):
    if not instance.pk:
        return  # Création, rien à faire

    try:
        old_instance = sender.objects.get(pk=instance.pk)
    except sender.DoesNotExist:
        return

    if old_instance.image and old_instance.image != instance.image:
        if os.path.isfile(old_instance.image.path):
            os.remove(old_instance.image.path)