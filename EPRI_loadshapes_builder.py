#!/usr/bin/env python
# coding: utf-8


import pandas as pd
import csv


#See your choices for locations
def peek_locations(data):
    locations = set(data.columns.values)
    print(locations)
    return locations
    
#Create new DF with like locatios
def filter_location(data, location):
    data = data.filter(like=location)
    return data
    
#peek at your buildings
def peek_buildings(data):
    print(set(data.iloc[2].values))
    return list(set(data.iloc[2].values))

#Input a list of buildings you want to build loadshapes for
def make_buildings_df(data, buildings='All'):
    if buildings =='All':
        buildings = list(set(data.iloc[2].values))
    print(buildings)
    df_dict = {}
    for i in buildings:
        buildings = data.columns[data.iloc[2] == i]
        df = data[buildings]
        #only support electric for now, assume military bases are rural enough that they cannot support nat gas.
        source = df.columns[df.iloc[1]=='Electric']
        df = df[source].dropna()
        df_dict[i] = df
#     print(df_dict)
    return df_dict

#Data Transformer, this function take in a df, sums all hourly load of buildings in df for certain location
def sum_load(df):
    load_shape_arr = [0]*8760
    for building in df.values():
        idx = 0
        rows = len(building)
        cols = len(building.columns)

        for row in range(5,(rows)):
            for col in range((cols)):
    #             print(building.iloc[row,col])
                load_shape_arr[idx] = [building.iloc[row,col]]
                idx+=1
    return load_shape_arr





#Driver

data = pd.read_excel('WholePremise_LoadShapeDatav11.xlsx', skiprows=1)

print(data.columns)

place = 'SAN ANTONIO, TX'
locations = peek_locations(data)
data = filter_location(data, place)
buildings = peek_buildings(data)
df = make_buildings_df(data)


load_shape = sum_load(df)
print(load_shape)
raise Exception

#Save the loadshape as csv vector
with open('load_shape_'+str(place)+'_.csv', 'w', newline='') as outfile:
    wr = csv.writer(outfile)
    wr.writerows(load_shape)





