from bs4 import BeautifulSoup
import requests
import re
import os
import calendar
import jsonpickle
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
import pandas as pd


area_db = pd.DataFrame(columns=['name'])
area_db.index.name = 'area_code'
cabin_db = pd.DataFrame(columns=['area_code', 'name'])
cabin_db.index.name = 'cabin_code'
availability_db = pd.DataFrame(columns=['date', 'cabin_code', 'available'])

area_codes = ["north", "matsu", "anch", "kenai", "kodiak", "pws", "south", "gulf"]
area_names = ["Northern", "Mat-Su", "Anchorage", "Kenai", "Kodiak", "Prince William Sound", "Southeast", "Gulf Coast"]
areas = {}
for i in range(0, len(area_codes)):
    area_code = area_codes[i] 
    area_name = area_names[i] 
    areas[area_code] = { "name": area_name }
    area_db.loc[area_code] = [area_name]

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

    areas[area_code]["cabins"] = cabins


availablility_url = "http://dnr.alaska.gov/projects/cabins/CabinAvailability.cfm"
possible_months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

calendar.setfirstweekday(calendar.SUNDAY)

availability = {}
for area in areas:

    area_code = area
    cabins = areas[area]["cabins"]

    for cabin in cabins:

        print(cabin["name"])

        cabin_code = cabin['code']
        cabin_db.loc[cabin_code] = [area_code, cabin['name']]

        r = requests.post(availablility_url, data={"cabin_code": cabin_code})
        soup = BeautifulSoup(r.content, "lxml")

        # months listed
        month_names = soup.find_all("span", {"class": "boldbodytext"})
        month_names = [str(elem.text.strip()) for elem in month_names]
        month_names = [x for x in month_names if x in possible_months]

        # availability
        month_dates = soup.find_all("pre")

        # make sure data makes sense
        assert len(month_names) == len(month_dates), "month names and dates should line up"
        assert len(month_names) == 8, "should have 8 months"
        starting_month = datetime.strptime(month_names[0], "%B").replace(year=datetime.now().year)
        assert starting_month.month == datetime.now().month, "should start on this month"

        # convert raw data to datetimes
        months = {}
        current_month = starting_month
        for i in range(0, len(month_names)):

            num_days = calendar.monthrange(current_month.year, current_month.month)[1]
            possible_days = [d for d in range(1, num_days + 1)]

            available_days = re.findall(re.compile('\d\d'), month_dates[i].text)
            available_days = [int(d) for d in available_days]
            reserved_days = list(set(possible_days).difference(available_days))
            assert (len(available_days) + len(reserved_days)) == num_days, \
                "total number of days should equal number of days in month"

            availability = {date(current_month.year, current_month.month, day): True for day in available_days}
            availability.update({date(current_month.year, current_month.month, day): False for day in reserved_days})

            for a in availability:
                availability_db.loc[len(availability_db.index)] = [a, cabin_code, availability[a]]

            months[month_names[i]] = availability
            current_month = current_month + relativedelta(months=1)

        for month in months:
            print(month)
            print(months[month])

        cabin["availability"] = months

jsonpickle.set_encoder_options('simplejson', indent=4)
with open('cabins.json', 'w') as f:
    j = jsonpickle.encode(areas)
    f.write(j)

area_db.to_pickle('area_db.pickle')
cabin_db.to_pickle('cabin_db.pickle')
availability_db.to_pickle('availability_db.pickle')


