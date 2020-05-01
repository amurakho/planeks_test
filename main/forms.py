from django import forms
from ckeditor.widgets import CKEditorWidget

from main import models


class PubCreationForm(forms.ModelForm):
    text = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = models.Pub
        exclude = ('is_pub', 'slug', 'author')


class CommentForm(forms.ModelForm):
    class Meta:
        model = models.Comment
        exclude = ('author', 'created_date', 'pub')