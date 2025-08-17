from django.db import models

# Create your models here.
from django.db.models.signals import post_delete
from django.dispatch import receiver
import os

from django.conf import settings


class Musique(models.Model):
    titre = models.CharField(max_length=100)
    artiste = models.CharField(max_length=100)
    duree = models.DurationField()
    style = models.CharField(max_length=50)
    date_ajout = models.DateField(auto_now_add=True)
    fichier = models.FileField(upload_to='musiques/', blank=False, null=False)
    publique = models.BooleanField(default=False, help_text="Accessible à tous les utilisateurs")
    utilisateurs_autorises = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='musiques_autorisees')

# Supprimer le fichier du disque quand une musique est supprimée
@receiver(post_delete, sender=Musique)
def delete_musique_file(sender, instance, **kwargs):
    if instance.fichier:
        if os.path.isfile(instance.fichier.path):
            os.remove(instance.fichier.path)

