import folium
import pandas
import COVID19Py

covid19 = COVID19Py.COVID19()
locations = covid19.getLocations()
map = folium.Map(location = [44.196037, 17.918107], zoom_start=7, tiles = "Stamen Terrain")

htmls = """<h4>Statistika:</h4>
 Lokacija: <b> %s </b> <br>
 Zaraženih: %s <br> 
 Umrlih: %s <br>
 Ozdravilo: %s
 """
#print(locations)
lat, lon, loc, confirm, death, recover = [], [], [], [], [], []
for temp in locations:
    lat.append(temp["coordinates"]["latitude"])
    lon.append(temp["coordinates"]["longitude"])
    loc.append(temp["country"] + " " + temp["province"])
    confirm.append(temp["latest"]["confirmed"])
    death.append(temp["latest"]["deaths"])
    recover.append(temp["latest"]["recovered"])

def putColor(confirm):
    if confirm < 200:
        return 'green'
    elif 200 <= confirm < 600:
        return 'orange'
    else:
        return 'red'

fgv = folium.FeatureGroup(name = "CoVID2019") #feature Group for corona 

for latX, lonY, locZ, confirmW, deathU, recoverV in zip(lat, lon, loc, confirm, death, recover):
    iframe = folium.IFrame(html=htmls % (locZ, confirmW, deathU, recoverV), width=250, height=150)
    fgv.add_child(folium.Marker(location = [latX, lonY], popup=folium.Popup(iframe),
    icon = folium.Icon(color = putColor(confirmW), icon = 'ambulance', prefix = 'fa' )))

fgp = folium.FeatureGroup(name = "Smrtnost")


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
else 'yellow' if 10 <= number_of_deaths(locations, x["properties"]["NAME"]) < 80 else 'red' }))


map.add_child(fgv)
map.add_child(fgp)
map.add_child(folium.LayerControl())
map.save(r"Map1.html")