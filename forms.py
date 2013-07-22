#coding=utf-8
from django import forms

class ContactForm(forms.Form):
    subject = forms.CharField(max_length=100, label='Наслов/цел на пораката')
    message = forms.CharField( label = 'Порака', widget=forms.Textarea )
    sender = forms.EmailField(label='Ваш email')
