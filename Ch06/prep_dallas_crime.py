

import pandas as pd

df = pd.read_csv('dallasdata.csv.zip')

nibr_num = {'LARCENY/ THEFT OFFENSES': 0, 
            'MOTOR VEHICLE THEFT': 1, 
            'DESTRUCTION/ DAMAGE/ VANDALISM OF PROPERTY': 2, 
            'ASSAULT OFFENSES': 3, 
            'DRUG/ NARCOTIC VIOLATIONS': 4, 
            'BURGLARY/ BREAKING & ENTERING': 5, 
            'ALL OTHER OFFENSES': 6, 
            'TRAFFIC VIOLATION - HAZARDOUS': 7, 
            'ROBBERY': 8, 
            'PUBLIC INTOXICATION': 9, 
            'WEAPON LAW VIOLATIONS': 10, 
            'FRAUD OFFENSES': 11, 
            'DRIVING UNDER THE INFLUENCE': 12, 
            'TRESPASS OF REAL PROPERTY': 13, 
            'FAMILY OFFENSES, NONVIOLENT': 14, 
            'STOLEN PROPERTY OFFENSES': 15, 
            'EMBEZZELMENT': 16, 
            'COUNTERFEITING / FORGERY': 17}


nibr_lab = {v:k for k,v in nibr_num.items()}

loc_label = {0: 'Street',
             1: 'Apartment/Residence',
             2: 'Bar/Restaurant',
             3: 'Commercial',
             4: 'Gas/Convenience',
             5: 'Hotel/Motel',
             6: 'Other',
             7: 'Outdoor',
             8: 'Parking Lot',
             9: 'Store',
            10: 'School'}


# convert dates, have month-year
df['nibrs'] = df['nibrs_cat'].replace(nibr_lab)
df['location'] = df['location'].replace(loc_label)

bdate = pd.to_datetime(df['begin'])
df['Month'] = bdate.dt.month
df['Year'] = bdate.dt.year

df = df[df['Year'] > 2022].copy()

df_sub = df[['Year','Month','nibrs','location','address']]
df_sub.to_csv('DallasCrime.csv.zip',index=False)

gb = df_sub.groupby(['Year','Month'],as_index=False).size()
pb = gb.pivot(index='Month',columns='Year',values='size')
print(pb.to_markdown())





