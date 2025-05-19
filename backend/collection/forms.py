from django import forms
from .models import Anime

class AnimeForm(forms.ModelForm):
        
    date_start = forms.DateField(
        input_formats=['%d/%m/%Y'],  # format de saisie attendu
    )
    
    date_end = forms.DateField(
        input_formats=['%d/%m/%Y'],
    )
    
    class Meta:
        model = Anime
        fields = ['main_title', 'format', 'origin', 'synopsis', 'date_start', 'date_end', 'episode', 'duration', 'season', 'studio', 'studio_3D', 'url_nautiljon', 'url_mal', 'genres', 'themes', 'slug']


