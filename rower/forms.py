from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm
from rower.models import *

class RegistrationForm(ModelForm):
  username = forms.CharField(label=(u'Nazwa uzytkownika'))
  email = forms.EmailField(label=(u'Adres email'))
  password = forms.CharField(label=(u'Haslo'), widget=forms.PasswordInput(render_value=False))
  password1 = forms.CharField(label=(u'Potwierdz haslo'), widget=forms.PasswordInput(render_value=False))
  
  class Meta:
    model = Uzytkownik
    exclude = ('user', 'haslo', 'nick')
    
    def clean_username(self):
      username = self.cleaned_data['username']
      try:
	User.objects.get(username=username)
      except User.DoesNotExist:
	return username
      raise forms.ValidationError("Nazwa uzytkownika jest juz w uzyciu.")
    
    def clean_password(self):
      password = self.cleaned_data['password']
      password1 = self.cleaned_data['password']
      if password != password1:
	raise forms.ValidationError("Hasla roznia sie")
      return password
      
class LoginForm(forms.Form):
  username = forms.CharField(label=(u'Nazwa uzytkownika'))
  password = forms.CharField(label=(u'Haslo'), widget=forms.PasswordInput(render_value=False))
  
class DodajWycieczkeForm(ModelForm):
  opis = forms.CharField(label=(u'Opis'), widget=forms.Textarea)
  class Meta:
    model = Wycieczka
    exclude = ('autor',)

    
class DodajRowerForm(ModelForm):
  opis = forms.CharField(label=(u'Opis'), widget=forms.Textarea)
  class Meta:
    model = Rower
    exclude = ('wlasciciel', )
	 