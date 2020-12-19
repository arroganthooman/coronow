from django import forms
from covidblog.models import Blog
from ckeditor.widgets import CKEditorWidget

class BlogForm(forms.ModelForm):
    title = forms.CharField(required=True)
    # image = forms.ImageField()
    body = forms.CharField(required=True, widget=CKEditorWidget())
    snippet = forms.CharField(required=True)


    title.widget.attrs.update({'class':'form-control'})
    # image.widget.attrs.update({'class':'form-control'})
    body.widget.attrs.update({'class':'form-control', 'style':'width:100%'})
    snippet.widget.attrs.update({'class':'form-control'})

    class Meta:
        model = Blog
        fields = ['title','image', 'snippet', 'body']

