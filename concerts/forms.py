from .models import Comment, Concert, Band
from django import forms


class CommentForm(forms.ModelForm):
    """ Form for the Comment model """
    class Meta:
        model = Comment
        fields = ('sentence', 'photo',)


class ConcertForm(forms.ModelForm):
    """ Form for the Concert model """
    class Meta:
        model = Concert
        fields = ('date', 'country', 'city', )
        widgets = {'date': forms.TextInput(attrs={'type': 'date'})}


class BandForm(forms.ModelForm):
    """ Form for the Band model """
    class Meta:
        model = Band
        fields = ('name', )
        labels = {'name': 'Band', }
