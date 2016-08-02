import pandas as pd
import datetime

# change to the date you want
d = datetime.date(2016,8,6)

cabins = pd.read_pickle('cabin_db.pickle')
a = pd.read_pickle('availability_db.pickle')
available = a[(a['date']==d) & (a['available']==True)]

available_cabins = pd.merge(available, cabins, how='left', left_on='cabin_code', right_index=True)

print(available_cabins)

