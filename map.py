import folium
import pandas

map = folium.Map(location = [38.58, -99.09], zoom_start = 4)

data = pandas.read_csv("volcanoes.txt")
lat = list(data["LAT"])
long = list(data["LON"])
elev = list(data["ELEV"])
name = list(data["NAME"])

html = """
Volcano Name: 
<a href="https://www.google.com/search?q=%%22%s%%22" target="_blank">%s</a><br>
Height: %s m
"""

def colour_producer(elvation):
    if elvation <= 1500:
        return 'green'
    elif elvation <= 3000:
        return 'orange'
    else:
        return 'red'

volcanoes = folium.FeatureGroup(name = "Volcanoes")

for lt, ln, el, nm in zip(lat, long, elev, name):
    iframe = folium.IFrame(html = html % (nm, nm, el), width = 240, height = 64)
    colour = colour_producer(el)
    volcanoes.add_child(folium.CircleMarker(location = [lt, ln], radius = 8, popup = folium.Popup(iframe), fill_color = colour, color = colour, fill_opacity = 0.7))

population = folium.FeatureGroup(name = "Population")

population.add_child(folium.GeoJson(data=open('population.json', 'r', encoding = 'utf-8-sig').read(),
style_function = lambda x: {'fillColor':'green' if x['properties']['POP2005'] < 15000000
else 'orange' if 15000000 <= x['properties']['POP2005'] < 30000000 else 'red',
'color':'blank'}))

map.add_child(volcanoes)
map.add_child(population)
map.add_child(folium.LayerControl())
map.save("Map.html", tiles = "Stamen Terrain")
