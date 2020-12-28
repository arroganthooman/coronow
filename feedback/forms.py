from django import forms
from .models import Feedback

class Form_Feedback(forms.ModelForm) :
    class Meta:
        model = Feedback
        fields = ['nama', 'email', 'isi']

    error_messages = {
        'required': 'Tolong diisi'
    }

    input_attrs_nama = {
        'type' : 'text',
        'placeholder' : 'Nama',
        'class' : 'inputbox',
        'id' : 'nama',
    }

    input_attrs_email = {
        'type' : 'email',
        'placeholder' : 'Email Address',
        'class' : 'inputbox',
        'id' : 'email',
    }

    input_attrs_isi = {
        'type' : 'text',
        'placeholder' : 'Isi',
        'class' : 'inputbox',
        'id' : 'isi',
    }

    nama = forms.CharField(label='', required=True, max_length=50, widget=forms.TextInput(attrs=input_attrs_nama))
    email = forms.CharField(label='', required=True, max_length=50, widget=forms.TextInput(attrs=input_attrs_email))
    isi = forms.CharField(label='', required=True, widget=forms.Textarea(attrs=input_attrs_isi))