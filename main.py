import datetime
import re
from multiprocessing.pool import Pool
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

    with open(filename.replace("/", ""), 'a', encoding='utf-8') as file:
        for line in property_information:
            string_to_write = line['address'] + "," + line['price'] +  "," + filename.replace("/", "") + "\n"
            file.write(string_to_write)
            count += 1
    file.close()


def build_dict(seq, key):
    return dict((d[key], dict(d, index=index)) for (index, d) in enumerate(seq))



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

    return property_information


def get_property_information(property_type):
    property_information = []
    pages = True
    offset = 0

    while pages:
        listings = get_daft_listings(property_type, offset)
        if not listings:
            pages = False
        property_information = validate_listings(listings, property_information, property_type)
        offset += 10

    write_to_file(remove_duplicate_properties(property_information), property_type)

def main():
    pool = Pool(processes=24)
    pool.map(get_property_information, RentType)
    pool.close()
    pool.join()


if __name__ == '__main__':
    print("START : " + str(datetime.datetime.now()))
    main()
    print("END : " + str(datetime.datetime.now()))
