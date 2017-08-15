from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.forms import ModelForm
from gisapp.models import Konexioa, GeojsonDatua
from gisapp.forms import KonexioFormularioa, fitxategiaKargatu
import gisapp.postgis2geojson
import gisapp.readGeo
import psycopg2

def index(request):
	view = "index"
	return render(request, "hasiera.html")

def login(request):
	view = "login"
	return render(request, "sartu.html")

def logout(request):
	view = "logout"
	return render(request, "irten.html")

def register(request):
	if request.method == 'POST':
		form = UserCreationForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			raw_password = form.cleaned_data.get('password1')
			user = authenticate(username=username, password=raw_password)
			login(request)
			return redirect('index')
	else:
		form = UserCreationForm()
	return render(request, 'erregistratu.html', {'form': form})

@login_required
def konexioak(request):

	konexioZerrenda = Konexioa.objects.filter(jabea = request.user).order_by('konexio_izena').distinct()

	return render(request, "konexioak.html", {'konexioak': konexioZerrenda} )


@login_required
def konexioBerria(request):
	if request.method == 'POST':
		form = KonexioFormularioa(request.POST)
		if form.is_valid():
			kon = form.save(commit=False)
			kon.jabea = request.user
			kon.save()
			return redirect('konexioak')
	else:
		form = KonexioFormularioa()
	return render(request, 'konexioBerria.html', {'form': form})


@login_required
def menua(request, gis_id):
	gis_obj = Konexioa.objects.get(id=gis_id)
	try:
		badaudeDatuak = GeojsonDatua.objects.get(konexioa = gis_obj)
	except GeojsonDatua.DoesNotExist:
		badaudeDatuak = False
	except GeojsonDatua.MultipleObjectsReturned:
		badaudeDatuak = True
	view = "menua"
	return render(request, "menua.html", {'gaitu': badaudeDatuak, 'konexioa': gis_obj})


@login_required
def mapa(request, gis_id):
	gis_obj = Konexioa.objects.get(id=gis_id)
	if request.user == gis_obj.jabea:
		datuak = GeojsonDatua.objects.filter(konexioa = gis_obj).order_by('datu_izena')
		#lista = []
		# for d in datuak:
		# 	geostr = gisapp.readGeo.readGeo(d)
		# 	lista.append(geostr)
		view = "mapa"
		return render(request, "mapa.html", {'geojsonDatuak': datuak})
	else:
		return redirect('index')


@login_required
def dbkarga(request, gis_id):
	gis_obj = Konexioa.objects.get(id=gis_id)
	if request.user == gis_obj.jabea:
		db_izena = gis_obj.konexio_izena
		db_helb = gis_obj.helbidea
		db_portua = gis_obj.portua
		db_erab = gis_obj.erabiltzailea
		db_pasahitza = gis_obj.pasahitza
		taulak = gisapp.postgis2geojson.getTables(db_izena, db_erab, db_pasahitza, db_helb, db_portua)
		print(len(taulak))
		for t in taulak:
			if not t.endswith("_audit"):
				gisapp.postgis2geojson.getData(gis_id, db_izena, db_erab, db_pasahitza, db_helb, db_portua, t)
				print(t)
		view = "mapa"
		return redirect("mapa", gis_id)
	else:
		return redirect('index')


@login_required
def fitxategi(request, gis_id):
	gis_obj = Konexioa.objects.get(id=gis_id)
	if request.user == gis_obj.jabea:
		if request.method == 'POST':
			form = fitxategiaKargatu(request.POST, request.FILES)
			if form.is_valid():
				datua=form.save(commit=False)
				datua.konexioa=gis_obj
				datua.save()
				#testua = open(request.FILES['fitxategia'], 'r').read()
				#izena = form.cleaned_data['izena']
				#datua = GeojsonDatua(izena, gis_obj, testua)
				#datua.save()
				return redirect('menua', gis_id)
		else:
			form = fitxategiaKargatu()
	else:
		return redirect('index')
	return render(request, 'fitxategi.html', {'form': form})

@login_required
def ezabatu(request, gis_id):
	gis_obj = Konexioa.objects.get(id=gis_id)
	if request.user == gis_obj.jabea:
		view = "ezabatu"
		datuak = GeojsonDatua.objects.filter(konexioa = gis_obj).order_by('datu_izena')
		return render(request, "ezabatu.html", {'konexioa': gis_obj, 'datuak': datuak})
	else:
		return redirect('index')