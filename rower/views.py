# Create your views here.
from django.views.generic import TemplateView, DetailView, ListView
from django.views.generic.edit import FormView
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from rower.forms import *
from rower.models import *
from django.contrib.auth import *

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
    return HttpResponseRedirect('/profile/')
  if request.method == 'POST':
    form = LoginForm(request.POST)
    if form.is_valid():
      username=form.cleaned_data['username']
      password=form.cleaned_data['password']
      user = authenticate(username=username, password=password)
      if user is not None:
	login(request, user)
	return HttpResponseRedirect('/profile/')
      else:
	return HttpResponseRedirect('/login/')
    else:
      return render_to_response('index.html', context, context_instance=RequestContext(request))
  else:
    form = LoginForm()
    context = {'form': form}
    return render_to_response('index.html', context, context_instance=RequestContext(request))
    
class IndexView(ListView):
  template_name="index.html"
  queryset = Wpis.objects.all().order_by('-data')    

    
  
