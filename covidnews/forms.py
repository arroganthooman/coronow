from django import forms
from covidnews.models import News
from ckeditor.widgets import CKEditorWidget

class NewsForm(forms.ModelForm):
    Judul= forms.CharField(required=True)
    description= forms.CharField(required=True)
    isi= forms.CharField(required=True, widget=CKEditorWidget())
    Foto=forms.URLField(required=True)
    Sumber= forms.CharField(required=True)

    isi.widget.attrs.update({'class':'form-control', 'style':'width:100%'})

    class Meta:
        model = News
        fields=['Judul','description','isi','Foto','Sumber']

