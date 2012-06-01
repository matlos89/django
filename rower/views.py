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
  Wycieczka.objects.get(pk=pk).delete()
  return HttpResponseRedirect('wycieczki')
  
@login_required
def EdytujWycieczke(request, pk):
  return HttpResponseRedirect('wycieczki')
  
#Funkcja dodawania wycieczki
@login_required
def DodajWycieczke(request):
  if request.method == 'POST':
    form = DodajWycieczkeForm(request.POST)
    if form.is_valid():
      nowa_wycieczka = Wycieczka(autor = Uzytkownik.objects.get(nick=request.user.username), rower=form.cleaned_data['rower'], km = form.cleaned_data['km'], nazwa = form.cleaned_data['nazwa'], data=form.cleaned_data['data'])
      nowa_wycieczka.save()
      #mozna dorobic dopisywanie wpisow po wpisaniu nowej wycieczki
      #problem - jak nadac format zwracanej daty z now() ?
      #nowy_wpis = Wpis(tytul=nowa_wycieczka.nazwa, data=datetime.datetime.now('YYYY-MM-DD'), opis='Uzytkownik '+request.user.username+' dodal nowa wycieczke')
      #nowy_wpis.save()
      return HttpResponseRedirect('wycieczki')
    else:
      return render_to_response('dodaj_wycieczke.html', {'form': form}, context_instance=RequestContext(request))
  else:
    form = DodajWycieczkeForm()
    context = {'form': form}
    return render_to_response('dodaj_wycieczke.html', context, context_instance=RequestContext(request))

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
  
  @method_decorator(login_required)
  def dispatch(self, *args, **kwargs):
    return super(IndexView, self).dispatch(*args, **kwargs)

#Fukcja wyswietlania wycieczek zalogowanego usera    
class WycieczkiView(ListView):
  template_name="wycieczki.html"
  
  @method_decorator(login_required)
  def dispatch(self,request, *args, **kwargs):
    self.queryset = Wycieczka.objects.filter(autor=Uzytkownik.objects.get(nick=request.user.username))
    return super(WycieczkiView, self).dispatch(request, *args, **kwargs)

