import psycopg2
import json
import subprocess
from django.core.files.base import ContentFile
from gisapp.models import Konexioa, GeojsonDatua

def getTables(dbizena, dberab, dbpasahitza, dbhelb, dbportua):
	try:
		conn = psycopg2.connect("dbname=" + dbizena + " user=" + dberab + " host=" + dbhelb + " port=" + dbportua + " password=" + dbpasahitza)
	except:
		print ("Ezin izan da datu-basera konektatu.")
		return

	cursor = conn.cursor()
	cursor.execute("select nspname||'.'||relname from pg_class join pg_namespace on relnamespace = pg_namespace.oid where relkind='r' and relname !~ '^(pg_|sql_)';")
	taulak = cursor.fetchall()
	taulaZerrenda = ["%s" % x for x in taulak ]
	geomZerrenda = []
	for elem in taulaZerrenda:
		banatuta = elem.split(".")
		sententzia = "SELECT attname FROM pg_attribute WHERE attrelid = (SELECT oid FROM pg_class WHERE relname = '" + banatuta[1] + "') AND attname = 'geom';"
		cursor.execute(sententzia)
		emaitza = cursor.fetchall()
		if len(emaitza) > 0:
			geomZerrenda.append(elem)
	conn.close()
	return geomZerrenda


def getData(gis_id, dbizena, dberab, dbpasahitza, dbhelb, dbportua, dbtaula, eremuak="*", geometria="geom", non="", irteera="data", srid="4326"):
	
	print("DATA SCRIPTA " + dbtaula)


	# Connect to the database
	try:
		conn = psycopg2.connect("dbname=" + dbizena + " user=" + dberab + " host=" + dbhelb + " port=" + dbportua + " password=" + dbpasahitza)
	except:
		print ("Ezin izan da datu-basera konektatu.")
		return

	# Create a cursor for executing queries
	cur = conn.cursor()




	query = "SELECT " + eremuak
	#transformazioa sartu!!
	query += ", ST_AsGeoJSON(ST_transform(" + geometria + ", " + srid + ")) AS geojson FROM " + dbtaula

	
	if non != "":
		query += " WHERE " + non + ";"
	else:
		query += ";"

	# Execute the query
	try:
		print(query)
		cur.execute(query)
	except:
		print ("Kontsulta ez da zuzena izan.")
		return


	# Retrieve the results of the query
	rows = cur.fetchall();



	# Get the column names returned
	colnames = [desc[0] for desc in cur.description]

	# Find the index of the column that holds the geometry
	geomIndex = colnames.index(geometria)

	# output is the main content, rowOutput is the content from each record returned
	output = ""
	rowOutput = ""
	i = 0
		# For each row returned...
	while i < len(rows):
		# Make sure the geometry exists
		if rows[i][geomIndex] is not None:
			# If it's the first record, don't add a comma
			comma = "," if i > 0 else ""
			rowOutput =  comma + '{"type": "Feature", "geometry": ' + rows[i][geomIndex] + ', "properties": {'
			properties = ""
			
			j = 0
			# For each field returned, assemble the properties object
			while j < len(colnames):
				if colnames[j] != 'geometry':
					comma = "," if j > 0 else ""
					properties +=  comma + '"' + colnames[j] + '":"' + str(rows[i][j]) + '"'

				j += 1

			rowOutput += properties + '}'
			rowOutput += '}'

			output += rowOutput

		# start over
		rowOutput = ""
		i += 1

	dbtaulaizena = dbtaula.replace(".","_")

	# Assemble the GeoJSON
	totalOutput = 'var ' + dbtaulaizena + ' = { "type": "FeatureCollection", "features": [ ' + output + ' ]};'
	#with open(dbtaula + '.geojson', 'w') as outfile:
	#	outfile.write(totalOutput)

	

	kon = Konexioa.objects.get(id = gis_id)
	gj = GeojsonDatua(datu_izena = dbtaulaizena + '.geojson', konexioa = kon, datuak = totalOutput)
	gj.save()

	#outfile.close()
	conn.close()