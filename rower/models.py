from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
# Create your models here.

ROWER_CHOICES = (
  ('BMX', 'Rower BMX'),
  ('MTB', 'Rower gorski'),
  ('SZO', 'Rower szosowy'),
  ('TRE', 'Rower trekingowy'),
  ('DWH', 'Rower downhillowy'),
)
GENDER_CHOICES = (
  ('M', 'Mezczyzna'),
  ('F', 'Kobieta'),
)


class Rower(models.Model):
  nazwa = models.CharField(max_length=20)
  producent = models.CharField(max_length=30)
  model = models.CharField(max_length=30)
  typ = models.CharField(max_length=3, choices=ROWER_CHOICES)
  przebieg = models.IntegerField()
  wlasciciel = models.ForeignKey('Uzytkownik')
  opis = models.CharField(max_length=200)
  
  class Meta:
    verbose_name = "Rower"
    verbose_name_plural = "Rowery"
  
  def __unicode__(self):
    return self.nazwa
    
class Wycieczka(models.Model):
  nazwa = models.CharField(max_length=50)
  autor = models.ForeignKey('Uzytkownik')
  rower = models.ForeignKey('Rower')
  km = models.IntegerField()
  data = models.DateField()
  opis = models.TextField(max_length=200, blank=True)
  
  class Meta:
    verbose_name = "Wycieczka"
    verbose_name_plural = "Wycieczki"
  
  def __unicode__(self):
    return self.nazwa
  
class Uzytkownik(models.Model):
  user = models.OneToOneField(User)
  nick = models.CharField(max_length=20)
  plec = models.CharField(max_length=1, choices=GENDER_CHOICES)
  email = models.EmailField()
  
  class Meta:
    verbose_name = "Uzytkownik"
    verbose_name_plural = "Uzytkownicy"
  
  def __unicode__(self):
    return self.nick

class Wpis(models.Model):
  tytul = models.CharField(max_length=40)
  data = models.DateField()
  opis = models.CharField(max_length=500)
  
  class Meta:
    verbose_name = "Wiadomosc"
    verbose_name_plural = "Wiadomosci"
  
  def __unicode__(self):
    return self.tytul
    
def create_uzytkownik_user_callback(sender, instance, **kwargs):
  uzytkownik, new = Uzytkownik.objects.get_or_create(user=instance)
post_save.connect(create_uzytkownik_user_callback, User)