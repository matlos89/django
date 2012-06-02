# Create your views here.
from django.views.generic import TemplateView, DetailView, ListView
from django.views.generic.edit import FormView
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.models import User
from rower.forms import *
from rower.models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
import datetime

#Usuwanie wycieczki
@login_required
def UsunWycieczke(request, pk):
  wycieczka_do_usuniecia = Wycieczka.objects.get(pk=pk)
  rower = Rower.objects.get(pk = wycieczka_do_usuniecia.rower.pk)
  rower.przebieg = rower.przebieg - wycieczka_do_usuniecia.km
  rower.save()
  wycieczka_do_usuniecia.delete()
  return HttpResponseRedirect('wycieczki')
  
#Funkcja edycji wycieczki
@login_required
def EdytujWycieczke(request, pk):
  if request.method == 'POST':
    form = DodajWycieczkeForm(request.POST)
    if form.is_valid():
      edytowana = Wycieczka.objects.get(pk=pk)
      rower = Rower.objects.get(pk = edytowana.rower.pk)
      dawny_przebieg = rower.przebieg
      dawne_km = edytowana.km
      edytowana.nazwa = form.cleaned_data['nazwa']
      edytowana.rower = form.cleaned_data['rower']
      edytowana.km = form.cleaned_data['km']
      edytowana.data = form.cleaned_data['data']
      edytowana.opis = form.cleaned_data['opis']
      edytowana.save()
      nowy = dawny_przebieg - dawne_km
      rower.przebieg = nowy + edytowana.km
      rower.save()
      return HttpResponseRedirect('wycieczki')
    else:
      return render_to_response('edytuj_wycieczke.html', {'form': form, 'pk': pk}, context_instance=RequestContext(request))
  else:
    edytowana = Wycieczka.objects.get(pk=pk)
    form = DodajWycieczkeForm({'nazwa': edytowana.nazwa, 'rower': edytowana.rower, 'km':edytowana.km, 'data': edytowana.data, 'opis': edytowana.opis})
    context = {'form': form}
    return render_to_response('edytuj_wycieczke.html', {'form': form}, context_instance=RequestContext(request))

#Funkcja dodawania wycieczki
@login_required
def DodajWycieczke(request):
  if request.method == 'POST':
    form = DodajWycieczkeForm(request.POST)
    if form.is_valid():
      nowa_wycieczka = Wycieczka(autor = Uzytkownik.objects.get(nick=request.user.username), rower=form.cleaned_data['rower'], km = form.cleaned_data['km'], nazwa = form.cleaned_data['nazwa'], data=form.cleaned_data['data'])
      nowa_wycieczka.save()
      #Dodawanie przebiegu do rowera
      rower = Rower.objects.get(pk = nowa_wycieczka.rower.pk)
      dawny = rower.przebieg
      rower.przebieg = dawny + form.cleaned_data['km']
      rower.save()
      #Dodawanie wpisu do glownej strony
      nowy_wpis = Wpis(tytul=nowa_wycieczka.nazwa, data=datetime.datetime.today(), opis='Uzytkownik '+request.user.username+' dodal nowa wycieczke: '+nowa_wycieczka.nazwa+', dystans: '+nowa_wycieczka.km)
      nowy_wpis.save()
      return HttpResponseRedirect('wycieczki')
    else:
      return render_to_response('dodaj_wycieczke.html', {'form': form}, context_instance=RequestContext(request))
  else:
    form = DodajWycieczkeForm()
    context = {'form': form}
    return render_to_response('dodaj_wycieczke.html', context, context_instance=RequestContext(request))

#Usuwanie rowera
@login_required
def UsunRower(request, pk):
  Rower.objects.get(pk=pk).delete()
  return HttpResponseRedirect('rowery')    
    
#Funkcja dodajaca rower
@login_required    
def DodajRower(request):
  if request.method == 'POST':
    form = DodajRowerForm(request.POST)
    if form.is_valid():
      nowy_rower = Rower(nazwa = form.cleaned_data['nazwa'], producent = form.cleaned_data['producent'], model = form.cleaned_data['model'], typ = form.cleaned_data['typ'], przebieg = form.cleaned_data['przebieg'], opis = form.cleaned_data['opis'], wlasciciel = Uzytkownik.objects.get(nick=request.user.username))
      nowy_rower.save()
      return HttpResponseRedirect('rowery')
    else:
      return render_to_response('dodaj_rower.html', {'form': form}, context_instance=RequestContext(request))
  else:
    form = DodajRowerForm()
    return render_to_response('dodaj_rower.html', {'form': form}, context_instance=RequestContext(request))

#Edycja roweru
@login_required
def EdytujRower(request, pk):
  if request.method == 'POST':
    form = DodajRowerForm(request.POST)
    if form.is_valid():
      edytowany = Rower.objects.get(pk=pk)
      edytowany.nazwa = form.cleaned_data['nazwa']
      edytowany.producent = form.cleaned_data['producent']
      edytowany.model = form.cleaned_data['model']
      edytowany.typ = form.cleaned_data['typ']
      edytowany.przebieg = form.cleaned_data['przebieg']
      edytowany.opis = form.cleaned_data['opis']
      edytowany.save()
      return HttpResponseRedirect('rowery')
    else:
      return render_to_response('edytuj_rower.html', {'form': form, 'pk': pk}, context_instance=RequestContext(request))
  else:
    edytowany = Rower.objects.get(pk=pk)
    form = DodajRowerForm({'nazwa': edytowany.nazwa, 'producent': edytowany.producent, 'model':edytowany.model, 'typ': edytowany.typ, 'opis': edytowany.opis, 'przebieg': edytowany.przebieg})
    context = {'form': form}
    return render_to_response('edytuj_rower.html', {'form': form}, context_instance=RequestContext(request))
        
    
#Funkcja do rejestracji uzytkownika
def UzytkownikRegistration(request):
  if request.user.is_authenticated():
    return HttpResponseRedirect('/profile/')
  if request.method == 'POST':
    form = RegistrationForm(request.POST)
    if form.is_valid():
      user = User.objects.create_user(username=form.cleaned_data['username'], email = form.cleaned_data['email'], password=form.cleaned_data['password'])
      user.save()
      uzytkownik = user.get_profile()
      uzytkownik.nick = form.cleaned_data['username']
      uzytkownik.plec = form.cleaned_data['plec']
      uzytkownik.email = form.cleaned_data['email']
      uzytkownik.save()
      return HttpResponseRedirect('registerSucc')
    else:
      return render_to_response('register.html', {'form': form}, context_instance=RequestContext(request))
      
      
  else:
    form = RegistrationForm()
    context = {'form': form}
    return render_to_response('register.html', context, context_instance=RequestContext(request))

#przekierowanie jesli rejestracja sie udala
def RegistrationSucc(request):
  return render_to_response('register_succ.html')
  
#Funkcja logowania    
def LoginRequest(request):
  if request.user.is_authenticated():
    return HttpResponseRedirect('index.html')
  if request.method == 'POST':
    form = LoginForm(request.POST)
    if form.is_valid():
      username=form.cleaned_data['username']
      password=form.cleaned_data['password']
      user = authenticate(username=username, password=password)
      if user is not None:
	login(request, user)
	return HttpResponseRedirect('index.html')
      else:
	return render_to_response('login.html', context, context_instance=RequestContext(request))
    else:
      return render_to_response('login.html', context, context_instance=RequestContext(request))
  else:
    form = LoginForm()
    context = {'form': form}
    return render_to_response('login.html', context, context_instance=RequestContext(request))
    
#Funkcja wylogowania
def LogoutRequest(request):
  logout(request)
  return HttpResponseRedirect('/')

#Funkcja glownej strony - wyswietla wszystkie newsy  
class IndexView(ListView):
  template_name="index.html"
  queryset = Wpis.objects.all().order_by('-data') 
  
  def dispatch(self, *args, **kwargs):
    return super(IndexView, self).dispatch(*args, **kwargs)

#Funkcja wyswietlania wycieczek zalogowanego usera    
class WycieczkiView(ListView):
  template_name="wycieczki.html"
  
  @method_decorator(login_required)
  def dispatch(self,request, *args, **kwargs):
    self.queryset = Wycieczka.objects.filter(autor=Uzytkownik.objects.get(nick=request.user.username))
    return super(WycieczkiView, self).dispatch(request, *args, **kwargs)

#Funkcja wyswietlania rowerow uzytkownika
class RoweryView(ListView):
  template_name="rowery.html"
  
  @method_decorator(login_required)
  def dispatch(self,request, *args, **kwargs):
    self.queryset = Rower.objects.filter(wlasciciel=Uzytkownik.objects.get(nick=request.user.username))
    return super(RoweryView, self).dispatch(request, *args, **kwargs)
