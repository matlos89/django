from django.conf.urls import patterns, include, url
from django.conf.urls import *
from django.conf.urls.defaults import *
from django.views.generic import *
from rower.views import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'projekt_django.views.home', name='home'),
    # url(r'^projekt_django/', include('projekt_django.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'registerSucc', 'rower.views.RegistrationSucc'),
    url(r'register', 'rower.views.UzytkownikRegistration'),
    url(r'^wpis/(?P<pk>\d+)$', DetailView.as_view(model=Wpis, template_name='wpis.html')),
    url(r'^wycieczka/(?P<pk>\d+)$', DetailView.as_view(model=Wycieczka, template_name='wycieczka.html')),
    url(r'^wycieczka/usun/(?P<pk>\d+)$', 'rower.views.UsunWycieczke'),
    url(r'^wycieczka/edycja/(?P<pk>\d+)$', 'rower.views.EdytujWycieczke'),
    url(r'wycieczki', WycieczkiView.as_view()),
    url(r'dodaj_wycieczke', 'rower.views.DodajWycieczke'),
    url(r'rowery', RoweryView.as_view()),
    url(r'dodaj_rower', 'rower.views.DodajRower'),   
    url(r'^rower/usun/(?P<pk>\d+)$', 'rower.views.UsunRower'),
    url(r'^rower/edycja/(?P<pk>\d+)$', 'rower.views.EdytujRower'),
    url(r'^rower/(?P<pk>\d+)$', DetailView.as_view(model=Rower, template_name='rower.html')),
    url(r'index', IndexView.as_view()),
    url(r'logout', 'rower.views.LogoutRequest'),
    url(r'', 'rower.views.LoginRequest'),
    
)
