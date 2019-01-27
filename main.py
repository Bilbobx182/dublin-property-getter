import datetime
import re
from multiprocessing.pool import Pool

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
                lat = str(g.geojson['features'][0]['geometry']['coordinates'][0])
                long = str(g.geojson['features'][0]['geometry']['coordinates'][1])
                line = location + " ," + lat + "," + long + "," + price + "," + str(property_type) + str(date)
                print(line)
                csvData.append(line)
            except:
                csvData.append(location + " ," + price + "," + (str(property_type) + " ERROR") + str(date))
        offset += 10


def main():
    pool = Pool(processes=8)
    pool.map(get_property_information, RentType)
    pool.close()
    pool.join()


if __name__ == '__main__':
    print("START : " + str(datetime.datetime.now()))
    main()
    print("END : " + str(datetime.datetime.now()))
