# isckonapp/forms.py

from django import forms
from .models import Event, GalleryImage, Album

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'date', 'month', 'link']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Event Name'}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }

class AlbumForm(forms.ModelForm):
    class Meta:
        model = Album
        fields = ['title', 'description', 'cover_image']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'e.g., Janmashtami 2025'}),
            'description': forms.Textarea(attrs={'rows': 3, 'placeholder': 'A short description of the album'}),
        }

class GalleryImageForm(forms.ModelForm):
    class Meta:
        model = GalleryImage
        fields = ['album', 'title', 'image', 'alt_text', 'show_in_homepage']

class MultipleImageUploadForm(forms.Form):
    album = forms.ModelChoiceField(
        queryset=Album.objects.all(),
        widget=forms.Select,
        label="Select Album"
    )
    images = forms.FileField(label="Select Images")