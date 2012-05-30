# Create your views here.
from django.views.generic import TemplateView, DetailView, ListView
from django.views.generic.edit import FormView
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from rower.forms import *
from rower.models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


def DodajWycieczke(request):
  if request.method == 'POST':
    form = DodajWycieczkeForm(request.POST)
    if form.is_valid():
      pass
    else:
      return render_to_response('dodaj_wycieczke.html', {'form': form}, context_instance=RequestContext(request))
  else:
    form = DodajWycieczkeForm()
    context = {'form': form}
    return render_to_response('dodaj_wycieczke.html', context, context_instance=RequestContext(request))
  
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
      return HttpResponseRedirect('/profile/')
    else:
      return render_to_response('register.html', {'form': form}, context_instance=RequestContext(request))
      
      
  else:
    form = RegistrationForm()
    context = {'form': form}
    return render_to_response('register.html', context, context_instance=RequestContext(request))

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
    
def LogoutRequest(request):
  logout(request)
  return HttpResponseRedirect('/')

class IndexView(ListView):
  template_name="index.html"
  queryset = Wpis.objects.all().order_by('-data') 
  
  @method_decorator(login_required)
  def dispatch(self, *args, **kwargs):
    return super(IndexView, self).dispatch(*args, **kwargs)

class WycieczkiView(ListView):
  template_name="wycieczki.html"
  queryset = Wycieczka.objects.all().order_by('-data')
  
  @method_decorator(login_required)
  def dispatch(self, *args, **kwargs):
    return super(WycieczkiView, self).dispatch(*args, **kwargs)
    
  
