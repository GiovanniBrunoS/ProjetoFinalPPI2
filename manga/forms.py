from django import forms

from .models import Manga, MangaChapter, Author, Artist

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

class AuthorForm(forms.ModelForm):

    class Meta:
        model = Author
        fields = ('name',)

    helper = FormHelper()
    helper.form_method = 'POST'
    helper.add_input(Submit('submit', 'Enviar'))

class ArtistForm(forms.ModelForm):

    class Meta:
        model = Artist
        fields = ('name',)

    helper = FormHelper()
    helper.form_method = 'POST'
    helper.add_input(Submit('submit', 'Enviar'))

class MangaForm(forms.ModelForm):

    class Meta:
        model = Manga
        fields = ('author', 'artist', 'title', 'description')
    
    helper = FormHelper()
    helper.form_method = 'POST'
    helper.add_input(Submit('submit', 'Enviar'))

class ChapterForm(forms.ModelForm):

    class Meta:
        model = MangaChapter
        fields = ('chapter_number', 'title', 'language', 'chapter')
    
    helper = FormHelper()
    helper.form_method = 'POST'
    helper.add_input(Submit('submit', 'Enviar'))