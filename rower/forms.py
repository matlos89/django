from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm
from rower.models import *
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect

GENDER_CHOICES = (
  ('M', 'Mezczyzna'),
  ('F', 'Kobieta'),
)

#class RegistrationForm(ModelForm):
class RegistrationForm(forms.Form):
  username = forms.CharField(label=(u'Nazwa uzytkownika'))
  email = forms.EmailField(label=(u'Adres email'))
  password = forms.CharField(label=(u'Haslo'), widget=forms.PasswordInput(render_value=False))
  password1 = forms.CharField(label=(u'Potwierdz haslo'), widget=forms.PasswordInput(render_value=False))
  plec = forms.ChoiceField(choices=GENDER_CHOICES)
    
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
      if len(password) < 5:
	raise forms.ValidationError("Haslo musi miec wiecej niz 5 liter")
      return password
      
class LoginForm(forms.Form):
  username = forms.CharField(label=(u'Nazwa uzytkownika'))
  password = forms.CharField(label=(u'Haslo'), widget=forms.PasswordInput(render_value=False))
  
class DodajWycieczkeForm(ModelForm):
  rower = forms.ModelChoiceField(queryset = Rower.objects.all(), label= (u'Rower'))
  opis = forms.CharField(label=(u'Opis'), widget=forms.Textarea)
  class Meta:
    model = Wycieczka
    exclude = ('autor', 'rower',)

  def __init__(self, *args, **kwargs):
    self.request = kwargs.pop('request', None)
    super(DodajWycieczkeForm, self).__init__(*args, **kwargs)
    #Aby wyswietlac rowery tylko zalogowane uzytkownika
    self.fields['rower'].queryset = Rower.objects.filter(wlasciciel=Uzytkownik.objects.get(user=self.request.user))
   
    
class DodajRowerForm(ModelForm):
  opis = forms.CharField(label=(u'Opis'), widget=forms.Textarea)
  class Meta:
    model = Rower
    exclude = ('wlasciciel', )
	 