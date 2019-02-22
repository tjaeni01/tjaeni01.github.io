import csv
import tsv
import addfips
import geocoder
import numpy as np
from collections import Counter
from collections import namedtuple
from datetime import datetime

API_KEY = "YOUR_GOOGLE_API_KEY"
af = addfips.AddFIPS() #initialize 
writer = tsv.TsvWriter(open("counties.tsv", "w"))
countyDict = np.load('countyDict.npy').item() #initialize dictionary
incidents = 'gun-violence-data_01-2013_03-2018.csv'

fields = ("incident_id", "date", "state", "city_or_county", "address", "n_killed", 
	"n_injured", "incedent_url", "source_url", "incident_url_fields_missing",
	"congressional_district", "gun_stolen", "gun_type", 
	"incident_characteristics", "latitude", "location_description", "longitude",
	"n_guns_involved", "notes", "participant_age", "participant_age_group",
	"participant_gender", "participant_name", "participant_relationship", 
	"participant_status", "participant_type", "sources", "state_house_district",
	"state_senate_district")

GunRecord = namedtuple('GunRecord', fields)

class GunRecord(namedtuple('GunRecord_', fields)):

    @classmethod
    def parse(klass, row):
        row = list(row)             # Make row mutable
        row[0] = int(row[0])      	# Convert "incident_id" to an integer
        row[1] = datetime.strptime(row[1], "%Y-%m-%d") # Parse the "date"
        row[5] = int(row[5])	# Convert "n_killed" to an integer
        row[6] = int(row[6])    # Convert "n_injured" to an integer
        row[10] = int(row[10]) if row[10] else None # Convert "congressional_district" to an integer
        row[14] = float(row[14]) if row[14] else None # Convert "latitude" to an integer
        row[16] = float(row[16]) if row[16] else None # Convert "longitude" to an integer
        row[27] = int(row[27]) if row[27] else None  # Convert "state_house_district" to an integer
        row[28] = int(row[28]) if row[28] else None # Convert "state_senate_district" to an integer
        return klass(*row)

# parse the data, yielding the info one line at a time
def read_gun_data(path):
    with open(path, 'rU') as data:
        data.readline()       # Skip the header
        reader = csv.reader(data)  # Create a regular tuple reader
        for row in map(GunRecord.parse, reader):
            yield row

# def save_obj(obj, name ):
#     with open('obj/'+ name + '.pkl', 'wb') as f:
#         pickle.dump(obj, f)

if __name__ == "__main__":
    for idx, row in enumerate(read_gun_data(incidents)):
        # since the data set was very large, I parsed it in chunks to check
        # if any errors were occuring. I could then single out the line of data
        # that was causing the error without going through the entire dataset
        # everytime. This was the last iteration that looked at the lines 
        # 200,000 - 240,000 in the dataset
        if idx >= 200000:
            fips = af.get_county_fips(row[3], state=row[2])
            # fips sometimes failed because the data gave the location of the 
            # incident as either a city or a county. If the locations was given
            # as acity, have to first find the county the city is in, then get
            # the fips of the county
            if fips == None:
                try:
                    g = geocoder.here(row[3] + ", " + row[2], app_id='gX8AbnhufJGb7RUSz7u7', app_code='H2YD2J8mZzr8MjSxV6XfAw')
                except IndexError:
                    print (idx)
                    print("Index Error!")
                    continue
                # if still getting an error, skip that line of data
                if g == None:
                    continue
                else:
                    # get fips now that we have the name of the county
                    try: 
                        fips =af.get_county_fips(g.json['county'], state=row[2])
                    except (KeyError, TypeError):
                        print(g.json)
                        continue
            existingEnt = countyDict.setdefault(fips, [row[2], 0, 0, 0])
            # {county: [state, n_killed, n_injured, counter]}
            countyDict[fips] = [existingEnt[0], existingEnt[1] + row[5], existingEnt[2] + row[6], existingEnt[3] + 1]
    print("dict filled")
    np.save('countyDict.npy', countyDict)
    writer.line("FIPS", "state", "n_killed", "n_injured", "count")
    for key, value in countyDict.items():
        writer.line(key, value[0], value[1], value[2], value[3])
    print("tsv filled")
    writer.close()

data = read_gun_data(incidents)
print(repr(data))
