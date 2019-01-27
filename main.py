import datetime
import re

import geocoder
from daftlistings import Daft, RentType

date = str(datetime.datetime.today().strftime('%Y-%m-%d'))


def get_daft_listings(property_type, offset):
    daft = Daft()
    daft.set_county('Dublin')
    daft.set_listing_type(property_type)
    daft.set_min_price(200)
    daft.set_offset(offset)
    return daft.search()


def write_to_file(places, prices, locations, file_name_raw):
    filename = str(date) + str(file_name_raw) + '.csv'
    count = 0

    with open(filename.replace("/", ""), 'a', encoding='utf-8') as file:
        while count < len(places):
            file.write(places[count] + "," + prices[count] + "," + locations[count] + "," + filename.replace("/","") + "\n")
            count+=1
    file.close()


def get_geo_data(data):
    g = geocoder.bing(data, key="")
    return str(g._list[0].eastnorth).replace("[", "").replace("]", "")


def get_property_information(property_type):
    pages = True
    print("<--------------->")
    print(property_type)
    print("<--------------->")
    place_names = []
    prices = []
    locations = []
    offset = 0
    current_properties_in_catagory = 0

    while pages:
        listings = get_daft_listings(property_type, offset)

        if not listings:
            pages = False

        for listing in listings:
            priceRaw = str(listing.price)
            price = re.sub("[^\d]", "", str(priceRaw.split(" ")))
            if "week" in priceRaw.lower():
                price = str((int(price)) * 4)

            current_property_location = str(listing.formalised_address.replace(",", ""))

            if current_property_location not in place_names and (len(current_property_location) > 10):
                place_names.append(current_property_location)
                prices.append(price)

                locations.append(get_geo_data(current_property_location))

                current_properties_in_catagory += 1
                print(current_properties_in_catagory)

        offset += 10
        if current_properties_in_catagory >= 50:
            pages = False
    write_to_file(place_names, prices, locations,str(property_type))


def main():
    for property in RentType:
        get_property_information(property)


if __name__ == '__main__':
    print("START : " + str(datetime.datetime.now()))
    main()
    print("END : " + str(datetime.datetime.now()))
