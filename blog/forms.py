from django import forms

from .models import Post, Comment

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'text',)
    
    helper = FormHelper()
    helper.form_method = 'POST'
    helper.add_input(Submit('submit', 'Enviar'))


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('author', 'text',)
    
    helper = FormHelper()
    helper.form_method = 'POST'
    helper.add_input(Submit('submit', 'Enviar'))