import datetime
import os
import platform
from os import listdir
from os.path import isfile, join

import geocoder


def get_geo_data(input_property, todayfolder):
    output = []
    count = 0
    for property in input_property:
        print(str(count) + "/" + str(len(input_property)))
        try:
            g = geocoder.arcgis(property.split(",")[0])
            property = property + "," + str(g.geojson['features'][0]['properties']['lat']) + "," + \
                       str(g.geojson['features'][0]['properties']['lng'])
            output.append(property)
        except:
            output.append(property + ",NA,NA")
        count += 1

    with open(todayfolder + "/ total.csv", 'w', encoding='utf-8') as file:
        for line in output:
            file.write(line)
        file.close()


def read_files():
    allfilecontent = []
    today = str(datetime.datetime.today().strftime('%Y-%m-%d'))

    if platform.system() == 'Linux':
        todayFolder = os.getcwd() + "/" + today + "/"
    else:
        todayFolder = os.getcwd() + "\\" + today + "\\"

    # rooms-to-share and house-share are a lot of noise 3k + properties in comparison to others.
    # Until a better solution is in place they're removed.
    onlyfiles = [f for f in listdir(todayFolder) if
                 isfile(join(todayFolder, f)) and "rooms-to-share" not in f and "house-share" not in f]

    print(onlyfiles)

    for file in onlyfiles:
        with open(todayFolder + file) as f:
            content = f.readlines()
            for line in content:
                allfilecontent.append(line)

    get_geo_data(allfilecontent, todayFolder)


def main():
    read_files()


print("START : " + str(datetime.datetime.now()))
main()
print("END : " + str(datetime.datetime.now()))
