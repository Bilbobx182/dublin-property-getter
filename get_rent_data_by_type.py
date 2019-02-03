import os
from os import listdir
from os.path import isfile, join


def write_to_group(data, property_type):
    with open(property_type + "master.csv", mode='w') as csv_file:
        csv_file.write("Location,Price,X,Y,META\n")
        for line in data:
            csv_file.write(line)
    csv_file.close()


def get_property_by_catagory(property_type):
    cwd = os.getcwd()
    path = cwd + "\\data"
    allfiles = [f for f in listdir(path) if isfile(join(path, f))]
    files_of_property_type = [f for f in allfiles if property_type in f]

    data = []

    for file in files_of_property_type:
        with open(path + "\\" + file, mode='r') as csv_file:
            for line in csv_file.readlines():
                data.append(line)
    write_to_group(data, property_type)


property_types = ["apartment-share", "flats-for-rent", "flat-to-share", "apartments-for-rent",
                  "studio-apartment-for-rent", "houses-for-rent"]

for property in property_types:
    get_property_by_catagory(property)
