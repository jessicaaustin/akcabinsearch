from bs4 import BeautifulSoup
import requests
import re
import os
import pickle
import calendar
from datetime import datetime, date
from dateutil.relativedelta import relativedelta

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

calendar.setfirstweekday(calendar.SUNDAY)

availability = {}
for area in areas:

    cabins = areas[area]

    for cabin in cabins:

        print(cabin["name"])

        r = requests.post(availablility_url, data={"cabin_code": cabin["code"]})
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

            months[month_names[i]] = availability
            current_month = current_month + relativedelta(months=1)

        for month in months:
            print(month)
            print(months[month])

        cabin["availability"] = months

pickle.dump(areas, open( areas_with_availability_file, "wb" ) )

