from django.db import models
from . import models
from django import forms


class PostForm(forms.ModelForm):
    class Meta:
        model = models.Tweet
        fields = ['image', 'content']

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.fields['image'].required = False




# class CommentForm(forms.ModelForm):
#      class Meta:
#          model = models.Comment
#          fields = ['image', 'content']

#      def __init__(self, *args, **kwargs):
#          super(CommentForm, self).__init__(*args, **kwargs)
#          self.fields['image'].required = False  