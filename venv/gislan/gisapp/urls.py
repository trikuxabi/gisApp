from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^sartu/', auth_views.login, {'template_name': 'sartu.html'}, name='login'),
    url(r'^irten/', auth_views.logout, {'next_page': '/gisapp'}, name='logout'),
    url(r'^erregistratu/', views.register, name='register'),
    url(r'^konexioak/', views.konexioak, name='konexioak'),
    url(r'^konexioberria/', views.konexioBerria, name='konexioBerria'),
    url(r'^menua/(?P<gis_id>\d+)', views.menua, name='menua'),
    url(r'^mapa/(?P<gis_id>\d+)', views.mapa, name='mapa'),
	url(r'^dbkarga/(?P<gis_id>\d+)', views.dbkarga, name='dbkarga'),
	url(r'^fitxategi/(?P<gis_id>\d+)', views.fitxategi, name='fitxategi'),
	url(r'^ezabatu/(?P<gis_id>\d+)', views.ezabatu, name='ezabatu'),
]