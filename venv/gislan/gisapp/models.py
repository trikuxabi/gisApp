from django.db import models
from django.contrib.auth.models import User


class Konexioa(models.Model):
	konexio_izena = models.CharField(max_length=100, unique=True)
	helbidea = models.CharField(max_length=100)
	portua = models.CharField(max_length=10)
	erabiltzailea = models.CharField(max_length=100)
	pasahitza = models.CharField(max_length=100)
	jabea = models.ForeignKey(User, related_name='User', default=1)
	readonly_fields=('id',)
	def __str__(self):
		return self.konexio_izena

class GeojsonDatua(models.Model):
	datu_izena = models.CharField(max_length=2000, unique=True)
	konexioa = models.ForeignKey(Konexioa, related_name='Konexioa', default=1)
	#datuak = models.FileField(upload_to='datuak/konexioak')
	datuak = models.TextField()
	def __str__(self):
		return self.datu_izena
	