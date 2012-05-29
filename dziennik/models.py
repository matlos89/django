from django.db import models

# Create your models here.
class Klasa(models.Model):
  nazwa = models.CharField(max_length=2)
  profil = models.CharField(max_length=30)
  
  def __unicode__(self):
    return self.nazwa

class Uczen(models.Model):
  imie = models.CharField(max_length=30)
  nazwisko = models.CharField(max_length=30)
  klasa = models.ForeignKey('Klasa')
  
  def __unicode__(self):
    return self.imie+' '+self.nazwisko
  
class Przedmiot(models.Model):
  nazwa = models.CharField(max_length=20)
  
  def __unicode__(self):
    return self.nazwa
    
class Wyniki(models.Model):
  przedmiot = models.ForeignKey('Przedmiot')
  uczen = models.ForeignKey('Uczen')
  ocena = models.IntegerField(max_length=1)
  
  def __unicode__(self):
    return self.uczen+' '+self.przedmiot
