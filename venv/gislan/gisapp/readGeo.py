from django.core.files.base import ContentFile
from gisapp.models import GeojsonDatua

def readGeo(datua):
	f = GeojsonDatua.objects.all().get(id=datua.id).datuak
	f.open(mode ='rb')
	geo = f.read()
	return geo