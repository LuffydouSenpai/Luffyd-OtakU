from django import forms
from .models import Manga, Scan, Contribution, Role, Anime, ContributionStudio, StudioRole

class MangaAdminForm(forms.ModelForm):
    class Meta:
        model = Manga
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        try:
            role_author = Role.objects.get(code="mangas_author")
            self.fields['author'].queryset = Contribution.objects.filter(role=role_author)
        except Role.DoesNotExist:
            self.fields['author'].queryset = Contribution.objects.none()
        
        try:
            role_scenariste = Role.objects.get(code="mangas_scenariste")
            self.fields['scenariste'].queryset = Contribution.objects.filter(role=role_scenariste)
        except Role.DoesNotExist:
            self.fields['scenariste'].queryset = Contribution.objects.none()
            
        try:
            role_designer = Role.objects.get(code="mangas_designer")
            self.fields['designer'].queryset = Contribution.objects.filter(role=role_designer)
        except Role.DoesNotExist:
            self.fields['designer'].queryset = Contribution.objects.none()
            
            
        try:
            role_chara_designer = Role.objects.get(code="mangas_chara_designer")
            self.fields['chara_designer'].queryset = Contribution.objects.filter(role=role_chara_designer)
        except Role.DoesNotExist:
            self.fields['chara_designer'].queryset = Contribution.objects.none()
            
            
            
class ScanAdminForm(forms.ModelForm):
    class Meta:
        model = Scan
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        try:
            role_author = Role.objects.get(code="scan_author")
            self.fields['author'].queryset = Contribution.objects.filter(role=role_author)
        except Role.DoesNotExist:
            self.fields['author'].queryset = Contribution.objects.none()
        
        try:
            role_scenariste = Role.objects.get(code="scan_scenariste")
            self.fields['scenariste'].queryset = Contribution.objects.filter(role=role_scenariste)
        except Role.DoesNotExist:
            self.fields['scenariste'].queryset = Contribution.objects.none()
            
        try:
            role_designer = Role.objects.get(code="scan_designer")
            self.fields['designer'].queryset = Contribution.objects.filter(role=role_designer)
        except Role.DoesNotExist:
            self.fields['designer'].queryset = Contribution.objects.none()
            
            
        try:
            role_chara_designer = Role.objects.get(code="scan_chara_designer")
            self.fields['chara_designer'].queryset = Contribution.objects.filter(role=role_chara_designer)
        except Role.DoesNotExist:
            self.fields['chara_designer'].queryset = Contribution.objects.none()
            
            

class AnimeAdminForm(forms.ModelForm):
    class Meta:
        model = Anime
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        try:
            role_studio = StudioRole.objects.get(code="studio")
            self.fields['studio'].queryset = ContributionStudio.objects.filter(role=role_studio)
        except StudioRole.DoesNotExist:
            self.fields['studio'].queryset = ContributionStudio.objects.none()
        
        try:
            role_studio3d = StudioRole.objects.get(code="role_studio3d")
            self.fields['role_studio3d'].queryset = ContributionStudio.objects.filter(role=role_studio3d)
        except StudioRole.DoesNotExist:
            self.fields['role_studio3d'].queryset = ContributionStudio.objects.none()
         