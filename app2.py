import folium
import pandas
import COVID19Py
from datetime import datetime

try:
    covid19 = COVID19Py.COVID19()
    locations = covid19.getLocations()
except:
    covid19 = COVID19Py.COVID19(data_source="csbs")
    locations = covid19.getLocations()
    
map = folium.Map(location = [44.196037, 17.918107], zoom_start=7, tiles = "Stamen Terrain")

htmls = """<h4>Statistics:</h4>
 Location: <b> %s </b> <br>
 Confirmed (recovered included): %s <br> 
 Deaths: %s <br>
 Last updated: %s
 
 """
#print(locations)
lat, lon, loc, confirm, death, update = [], [], [], [], [], []
for temp in locations:
    lat.append(temp["coordinates"]["latitude"])
    lon.append(temp["coordinates"]["longitude"])
    loc.append(temp["country"] + " " + temp["province"])
    confirm.append(temp["latest"]["confirmed"])
    death.append(temp["latest"]["deaths"])
    t = datetime.strptime(temp["last_updated"][:19], "%Y-%m-%dT%H:%M:%S")
    update.append(t.strftime("%d/%m/%Y %H:%M:%S"))

def putColor(confirm):
    if confirm < 200:
        return 'green'
    elif 200 <= confirm < 600:
        return 'orange'
    else:
        return 'red'

fgv = folium.FeatureGroup(name = "CoVID2019") #feature Group for corona 

for latX, lonY, locZ, confirmW, deathU, updateV in zip(lat, lon, loc, confirm, death, update):
    iframe = folium.IFrame(html=htmls % (locZ, confirmW, deathU, updateV), width=300, height=150)
    fgv.add_child(folium.Marker(location = [latX, lonY], popup=folium.Popup(iframe),
    icon = folium.Icon(color = putColor(confirmW), icon = 'ambulance', prefix = 'fa' )))

fgp = folium.FeatureGroup(name = "Red = Deaths>100")


def number_of_deaths(dataB, country):
   
    d = 0
    for temp in dataB:
        if (temp["country"] == country and temp["province"] != "" or (country == "United States" and temp["country"] == "US")):
            d = d + (temp["latest"]["deaths"])
        elif temp["country"] == country:
            return temp["latest"]["deaths"]
    return d



fgp.add_child(folium.GeoJson(data = open('world.json', 'r', encoding='utf-8-sig').read(),
style_function = lambda x: {'fillColor' : 'green' if number_of_deaths(locations, x["properties"]["NAME"]) < 10
else 'orange' if 30 <= number_of_deaths(locations, x["properties"]["NAME"]) < 100 else 'red' }))


map.add_child(fgv)
map.add_child(fgp)
map.add_child(folium.LayerControl())
map.save(r"Map1.html")