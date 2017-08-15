from django.forms import ModelForm
from django import forms
from gisapp.models import Konexioa, GeojsonDatua

class KonexioFormularioa(ModelForm):
	class Meta:
		model = Konexioa
		fields = ['konexio_izena', 'helbidea', 'portua', 'erabiltzailea', 'pasahitza']


class fitxategiaKargatu(ModelForm):
	class Meta:
		model=GeojsonDatua
		fields=['datu_izena', 'datuak']