import datetime
import re

import geocoder
from daftlistings import Daft, RentType

date = str(datetime.datetime.today().strftime('%Y-%m-%d'))


def write_to_file(data, file_name_raw):
    filename = str(date) + str(file_name_raw) + '.csv'
    with open(filename.replace("/", ""), 'w', encoding='utf-8') as file:
        for row in data:
            file.write(str(row) + "\n")
        file.close()


def get_daft_listings(property_type, offset):
    daft = Daft()
    daft.set_county('Dublin')
    daft.set_listing_type(property_type)
    daft.set_min_price(200)
    daft.set_offset(offset)
    return daft.search()


def get_property_information(property_type):
    pages = True
    print("<--------------->")
    print(property_type)
    print("<--------------->")
    csvData = []
    offset = 0

    while pages:
        listings = get_daft_listings(property_type, offset)

        if not listings:
            pages = False

        for listing in listings:
            priceRaw = str(listing.price)
            price = re.sub("[^\d]", "", str(priceRaw.split(" ")))
            if "week" in priceRaw.lower():
                price = str((int(price)) * 4)

            location = str(listing.formalised_address.replace(",", ""))

            try:
                g = geocoder.arcgis(location)
                print(location + " ," + str(g.geojson['features'][0]['geometry']['coordinates'][0]) + "," + str(
                    g.geojson['features'][0]['geometry']['coordinates'][1]) + "," + price + "," + str(date))

                csvData.append(
                    location + " ," + str(g.geojson['features'][0]['geometry']['coordinates'][0]) + "," + str(
                        g.geojson['features'][0]['geometry']['coordinates'][1]) + "," + price + "," + str(date))
            except:
                csvData.append(location + " ," + price + "," + str(date))
                print("ERROR")

        offset += 10


for type in RentType:
    get_property_information(type)
