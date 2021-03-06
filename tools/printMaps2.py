# -*- coding: utf-8 -*-

import gmplot

##################### Ferramenta Stand Alone para plotar resultados obtidos em um HTML com o mapa do Google #############################

# Referência: https://manojsaha.com/2017/03/08/drawing-locations-google-maps-python/

# Fetch all the data returned by the database query as a list
lat_long = [(-22.86985120,-43.1051227),(-22.86983310,-43.1051285),(-22.86984080,-43.1051355),(-22.86983130,-43.1051311),(-22.86984440,-43.1051408),(-22.86987940,-43.1051325),(-22.86986800,-43.1051353),(-22.86986740,-43.1051099),(-22.86982530,-43.1051313),(-22.86986990,-43.1051268),(-22.86987800,-43.1051076),(-22.86984740,-43.1051061),(-22.86984480,-43.1051351),(-22.86984460,-43.1051185),(-22.86986010,-43.1051341),(-22.86987300,-43.1051315),(-22.86985720,-43.1051022),(-22.86986560,-43.1051251),(-22.86986950,-43.1051279),(-22.86987230,-43.1051344),(-22.86984940,-43.1051007),(-22.86984500,-43.1051201),(-22.86992110,-43.1050613),(-22.86984650,-43.1050980),(-22.86997450,-43.1050409),(-22.86984980,-43.1050972),(-22.86989680,-43.1050272),(-22.86984260,-43.1050673),(-22.86982940,-43.1050112),(-22.86996080,-43.1050254)]
dist_wf = (0.000251189,0.000271227,0.000292864,0.000316228,0.000316228,0.000398107,0.000398107,0.000398107,0.000398107,0.000429866,0.000429866,0.000464159,0.000464159,0.000501187,0.000681292,0.000735642,0.000926119,0.001000000,0.001079775,0.001165914,0.001165914,0.001847850,0.001847850,0.002712273,0.002712273,0.002928645,0.002928645,0.003162278,0.003981072,0.005843414)

# Initialize two empty lists to hold the latitude and longitude values
latitude = []
longitude = []

# Transform the the fetched latitude and longitude data into two separate lists
for i in range(len(lat_long)):
	latitude.append(lat_long[i][0])
	longitude.append(lat_long[i][1])

# Initialize the map to the first location in the list
gmap = gmplot.GoogleMapPlotter(latitude[0],longitude[0],20)

# Draw the points on the map. I created my own marker for '#FF66666'.
# You can use other markers from the available list of markers.
# Another option is to place your own marker in the folder -
# /usr/local/lib/python3.5/dist-packages/gmplot/markers/

#gmap.scatter(latitude, longitude, '#FF6666', size=4, marker=False)
#gmap.scatter(latitude, longitude, 'k', marker=True)
#gmap.plot(latitude, longitude, 'cornflowerblue', edge_width=3)
#gmap.heatmap(latitude, longitude, radius=100)

for n in range(len(latitude)):
    gmap.marker(latitude[n], longitude[n], '#FF0000', title='Ponto%03i'%n)
    gmap.circle(latitude[n], longitude[n], radius=dist_wf[n]*1000, color='#FF6666')


# Write the map in an HTML file
gmap.draw('mapa.html')
