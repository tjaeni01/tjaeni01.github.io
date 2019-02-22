import csv
import tsv
import requests
import urllib

writer = tsv.TsvWriter(open("counties.tsv", "w"))
writer.line("FIPS", "state", "n_killed", "n_injured", "count", "county")

with open('incidents.tsv') as tsvfile:
	reader = csv.DictReader(tsvfile, dialect='excel-tab')
	for row in reader:
		fipsCD = row['FIPS']
		url = 'https://www.broadbandmap.gov/broadbandmap/census/county/fips/' + str(fipsCD) + '?format=json'
		response = requests.get(url)
		data = response.json()
		try:
			countyNM = data['Results']['county'][0]['name']
		except IndexError:
			fipsCD = '0' + fipsCD
			url = 'https://www.broadbandmap.gov/broadbandmap/census/county/fips/' + str(fipsCD) + '?format=json'
			response = requests.get(url)
			data = response.json()
			try:
				countyNM = data['Results']['county'][0]['name']
			except IndexError:
				print(fipsCD)
				print(data)
		writer.line(row['FIPS'], row['state'], row['n_killed'], row['n_injured'], row['count'], countyNM)

writer.close()
