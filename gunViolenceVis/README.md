Tucker Jaenicke
9/29/18

This folder creates a visualization of gun violence in America. It builds a choropleth 
map of America that shows the different levels of gun violence in every county since 
2013. The visualization can be run by setting up a python simple HTTP server:

python3 -m http.server 8000

and then running http://localhost:8000/FinalVis.html in a web browser.

The data from this visualization was downloaded from here:
https://www.kaggle.com/jameslko/gun-violence-data

The files in this folder are as follows:
FinalVis.html: Builds the visualization using incidents.tsv and the files in the folder js
gun_violence.py: Wrangles the data. The data was originally a csv with over 260,000 lines.
  Each line respresented one gun violence incident. I wanted the data as a tsv where every
  line was a different county with information on the gun violence in that county. 
  gun_violence.py wrangles the data into a form I could use: incidents.tsv
getCountyNames.py: To make the choropleth, I needed the name of the county each incident
  occurred in. The main data set states the location of each incident as either the city
  or county where it happened. If it says the county there was no issue, but for the 
  instances where it has the city instead of the county, I needed to get the county name.
  these county names were stored in counties.tsv.
js: a folder containing the d3 frameworks used in this project as well info on the counties
  and states of the US which were used to make the choropleth
