from bs4 import BeautifulSoup
import requests
import re
import json
import os
import pickle

areas_file = "areas.pickle"

areas = {}
if os.path.isfile(areas_file):

    print("{} exists, skipping".format(areas_file))
    areas = pickle.load(open("areas.pickle", "rb"))

else: 

    area_codes = ["north", "matsu", "anch", "kenai", "kodiak", "pws", "south", "gulf"]
    area_url= "http://dnr.alaska.gov/parks/cabins/"

    for area_code in area_codes:
        print(area_code)

        r = requests.get(area_url + area_code)
        # TODO: use html5lib instead
        soup = BeautifulSoup(r.content, "lxml")
        elems = soup.find_all("input", {"name": "cabin_code"})

        cabins = []
        for elem in elems:
            code = int(elem["value"])
            name_text = elem.find_previous_siblings("strong")[0].text
            name = str(re.sub(u"(\u2018|\u2019)", "'", name_text))
            print("{}: {}: {}".format(area_code, name, code))
            cabins.append({"name": name, "code": code})

        areas[area_code] = cabins

    pickle.dump(areas, open( areas_file, "wb" ) )


areas_with_availability_file = "areas_with_availability.pickle"
areas_with_availability_json_file = "areas_with_availability.json"

availablility_url = "http://dnr.alaska.gov/projects/cabins/CabinAvailability.cfm"
possible_months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

availability = {}
for area in areas:

    cabins = areas[area]

    for cabin in cabins:

        print(cabin["name"])

        r = requests.post(availablility_url, data={"cabin_code": cabin["code"]})
        soup = BeautifulSoup(r.content, "lxml")

        # months listed
        elems = soup.find_all("span", {"class": "boldbodytext"})
        months = [str(elem.text.strip()) for elem in elems]
        months = [x for x in months if x in possible_months]

        # availability
        elems = soup.find_all("pre")
        assert len(months) == len(elems)
        availability = dict(zip(months, elems))

        for month in availability:
            print(month)
            print(availability[month])

        cabin["availability"] = availability
        
with open(areas_with_availability_json_file, 'w') as outfile:
    json.dump(areas, outfile)

pickle.dump(areas, open( areas_with_availability_file, "wb" ) )

