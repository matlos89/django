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
    url(r'register', 'rower.views.UzytkownikRegistration'),
    url(r'^wpis/(?P<pk>\d+)$', DetailView.as_view(model=Wpis, template_name='wpis.html')),
    url(r'^wycieczka/(?P<pk>\d+)$', DetailView.as_view(model=Wycieczka, template_name='wycieczka.html')),
    url(r'index', IndexView.as_view()),
    url(r'wycieczki', WycieczkiView.as_view()),
    url(r'logout', 'rower.views.LogoutRequest'),
    url(r'dodaj_wycieczke', 'rower.views.DodajWycieczke'),
    url(r'', 'rower.views.LoginRequest'),
    
)
