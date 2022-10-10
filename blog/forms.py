from .models import Comment
from django import forms


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        # comma after 'body' is important to add or else python will read
        # it as a string rather than a tuple which will cause an error.
        fields = ('body',)
