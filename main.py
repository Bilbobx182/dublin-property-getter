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
            file.write(
                places[count] + "," + prices[count] + "," + locations[count] + "," + filename.replace("/", "") + "\n")
            count += 1
    file.close()


def get_geo_data(data):
    g = geocoder.bing(data, key="")
    return str(g._list[0].eastnorth).replace("[", "").replace("]", "")


def print_header(property_type):
    print("<--------------->")
    print(property_type)
    print("<--------------->")


def get_propety_price(price_input):
    priceRaw = str(price_input)
    price = re.sub("[^\d]", "", str(priceRaw.split(" ")))
    if "week" in priceRaw.lower():
        price = str((int(price)) * 4)
    return price


def get_batch_address(property_information):
    for item in property_information:
        print(item['address'])


def get_property_as_dict(current_property_location, price):
    return {
        "address": current_property_location,
        "price": get_propety_price(price)
    }


def remove_duplicate_properties(contents):
    return [i for n, i in enumerate(contents) if i not in contents[n + 1:]]


def validate_listings(listings, property_information):
    for listing in listings:

        current_property_location = str(listing.formalised_address.replace(",", ""))

        if len(current_property_location) > 10:
            property_information.append(get_property_as_dict(current_property_location, listing.price))

            # Remove duplicates at each interval of 25 items being added to it.
            if len(property_information) % 10 == 0:
                property_information = remove_duplicate_properties(property_information)
            if len(property_information) >= 50:
                get_batch_address(property_information)
    return property_information


def get_property_information(property_type):
    property_information = []
    pages = True
    offset = 0

    print_header(property_type)

    while pages:
        listings = get_daft_listings(property_type, offset)

        if not listings:
            pages = False

        property_information = validate_listings(listings, property_information)
        offset += 10


def main():
    for property in RentType:
        get_property_information(property)


if __name__ == '__main__':
    print("START : " + str(datetime.datetime.now()))
    main()
    print("END : " + str(datetime.datetime.now()))
