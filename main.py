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


def write_to_file(property_information, file_name_raw):
    filename = str(date) + str(file_name_raw) + '.csv'
    count = 0

    print(len(property_information))
    property_information = remove_duplicate_properties(property_information)
    print(len(property_information))

    with open(filename.replace("/", ""), 'a', encoding='utf-8') as file:
        for line in property_information:
            print(len(property_information))
            string_to_write = line['address'] + "," + line['price'] + "," + line['long'] + "," + line[
                'lat'] + "," + filename.replace("/", "") + "\n"
            file.write(string_to_write)
            count += 1
    file.close()


def build_dict(seq, key):
    return dict((d[key], dict(d, index=index)) for (index, d) in enumerate(seq))


def get_geo_data(property_information, property_type):
    information_by_address = build_dict(property_information, key="address")
    data = [x['address'] for x in property_information]

    g = geocoder.bing(data, method='batch', key="AtV8eTK7ZuP0D1ZE0Nr_Y00AGQsy7vewgt5IwH3Vw8s4kPv5zqIQuBYCnUtmJ9JO")

    g_count = 0
    output = []
    while g_count < len(g):
        output.append({
            "address": g.location[g_count],
            "price": information_by_address.get(g.location[g_count])['price'],
            "lat": str(g._list[g_count].lat),
            "long": str(g._list[g_count].lng)
        })
        g_count += 1

    write_to_file(output, property_type)
    print("GET GEO DONE")


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
    get_geo_data(property_information)


def get_property_as_dict(current_property_location, price):
    return {
        "address": current_property_location,
        "price": get_propety_price(price)
    }


def remove_duplicate_properties(contents):
    return [i for n, i in enumerate(contents) if i not in contents[n + 1:]]


def validate_listings(listings, property_information, property_type):
    for listing in listings:

        current_property_location = str(listing.formalised_address.replace(",", ""))

        if len(current_property_location) > 10:
            property_information.append(get_property_as_dict(current_property_location, listing.price))

            # Remove duplicates at each interval of 25 items being added to it.
            if len(property_information) % 10 == 0:
                property_information = remove_duplicate_properties(property_information)
            if len(property_information) >= 50:
                get_geo_data(remove_duplicate_properties(property_information), property_type)
                property_information = []
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
        property_information = validate_listings(listings, property_information, property_type)

        offset += 10


def main():
    for property in RentType:
        get_property_information(property)


if __name__ == '__main__':
    print("START : " + str(datetime.datetime.now()))
    main()
    print("END : " + str(datetime.datetime.now()))
