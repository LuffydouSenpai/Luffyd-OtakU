from django import forms
from .models import Manga, Scan, Contribution, Role, Anime, ContributionStudio, StudioRole

class MangaAdminForm(forms.ModelForm):
    class Meta:
        model = Manga
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        try:
            role_author = Role.objects.get(code="author")
            self.fields['author'].queryset = Contribution.objects.filter(role=role_author)
        except Role.DoesNotExist:
            self.fields['author'].queryset = Contribution.objects.none()
        
        try:
            role_scenariste = Role.objects.get(code="scenariste")
            self.fields['scenariste'].queryset = Contribution.objects.filter(role=role_scenariste)
        except Role.DoesNotExist:
            self.fields['scenariste'].queryset = Contribution.objects.none()
            
        try:
            role_designer = Role.objects.get(code="designer")
            self.fields['designer'].queryset = Contribution.objects.filter(role=role_designer)
        except Role.DoesNotExist:
            self.fields['designer'].queryset = Contribution.objects.none()
            
            
        try:
            role_chara_designer = Role.objects.get(code="chara_designer")
            self.fields['chara_designer'].queryset = Contribution.objects.filter(role=role_chara_designer)
        except Role.DoesNotExist:
            self.fields['chara_designer'].queryset = Contribution.objects.none()
            
        try:
            role_illustrator = Role.objects.get(code="illustrator")
            self.fields['illustrator'].queryset = Contribution.objects.filter(role=role_illustrator)
        except Role.DoesNotExist:
            self.fields['illustrator'].queryset = Contribution.objects.none()
            
            
            
class ScanAdminForm(forms.ModelForm):
    class Meta:
        model = Scan
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        try:
            role_author = Role.objects.get(code="author")
            self.fields['author'].queryset = Contribution.objects.filter(role=role_author)
        except Role.DoesNotExist:
            self.fields['author'].queryset = Contribution.objects.none()
        
        try:
            role_scenariste = Role.objects.get(code="scenariste")
            self.fields['scenariste'].queryset = Contribution.objects.filter(role=role_scenariste)
        except Role.DoesNotExist:
            self.fields['scenariste'].queryset = Contribution.objects.none()
            
        try:
            role_designer = Role.objects.get(code="designer")
            self.fields['designer'].queryset = Contribution.objects.filter(role=role_designer)
        except Role.DoesNotExist:
            self.fields['designer'].queryset = Contribution.objects.none()
            
            
        try:
            role_chara_designer = Role.objects.get(code="chara_designer")
            self.fields['chara_designer'].queryset = Contribution.objects.filter(role=role_chara_designer)
        except Role.DoesNotExist:
            self.fields['chara_designer'].queryset = Contribution.objects.none()
            
        try:
            role_illustrator = Role.objects.get(code="illustrator")
            self.fields['illustrator'].queryset = Contribution.objects.filter(role=role_illustrator)
        except Role.DoesNotExist:
            self.fields['illustrator'].queryset = Contribution.objects.none()  

class AnimeAdminForm(forms.ModelForm):
    
    date_start = forms.DateField(
        input_formats=['%d/%m/%Y'],  # format de saisie attendu
    )
    
    date_end = forms.DateField(
        input_formats=['%d/%m/%Y'],
    )
    class Meta:
        model = Anime
        fields = '__all__'

    def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            try:
                role_studio = StudioRole.objects.get(code="studio")
                self.fields['studio'].queryset = ContributionStudio.objects.filter(studioRole=role_studio)
            except StudioRole.DoesNotExist:
                self.fields['studio'].queryset = ContributionStudio.objects.none()
            
            try:
                role_studio3d = StudioRole.objects.get(code="studio_3d")
                self.fields['studio_3D'].queryset = ContributionStudio.objects.filter(studioRole=role_studio3d)
            except StudioRole.DoesNotExist:
                self.fields['studio_3D'].queryset = ContributionStudio.objects.none()
            

class TomeMangaAdminForm(forms.ModelForm):
    date_publication_jp = forms.DateField(
        input_formats=['%d/%m/%Y'],  # format de saisie attendu
    )
    
    date_publication_fr = forms.DateField(
        input_formats=['%d/%m/%Y'],
    )


class TomeScanAdminForm(forms.ModelForm):
    date_publication_jp = forms.DateField(
        input_formats=['%d/%m/%Y'],  # format de saisie attendu
    )