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
    }

    input_attrs_email = {
        'type' : 'text',
        'placeholder' : 'Email Address',
        'class' : 'inputbox',
    }

    input_attrs_isi = {
        'type' : 'text',
        'placeholder' : 'Isi',
        'class' : 'inputbox',
    }

    nama = forms.CharField(label='', required=True, max_length=50, widget=forms.TextInput(attrs=input_attrs_nama))
    email = forms.CharField(label='', required=True, max_length=50, widget=forms.TextInput(attrs=input_attrs_email))
    isi = forms.CharField(label='', required=True, widget=forms.Textarea(attrs=input_attrs_isi))