from .models import Comment, Concert, Band
from django import forms


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('sentence', 'photo',)


class ConcertForm(forms.ModelForm):
    class Meta:
        model = Concert
        fields = ('date', 'country', 'city', 'slug', )
        widgets = {'date': forms.TextInput(attrs={'type': 'date'})}


class BandForm(forms.ModelForm):
    class Meta:
        model = Band
        fields = ('name', )
        labels = {'name': 'Band', } 
