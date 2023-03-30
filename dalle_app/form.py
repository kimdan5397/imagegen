from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms

class ContactForm(forms.Form):
    name = forms.CharField(label='Name', max_length=100)
    email = forms.EmailField(label='email')
    subject = forms.CharField(label='Subject', max_length=100)
    message = forms.CharField(label='content', widget=forms.Textarea)