# -*- coding: utf-8 -*-
"""
Created on Tue Mar 23 02:48:52 2021

@author: Guang
"""

# Convert JSON file to DataFrame

import json
import pandas as pd
from pandas.io.json import json_normalize

class JSONTable:
    def __init__(self, json_dir, countryname):
        self.json_dir = json_dir
        self.json_data = self.load_json()
        self.json_df = self.normalize_json()
        self.country_data = self.process_country_data(countryname)
        
    
    def load_json(self):
        if self.json_dir == None:
            with open ('countries_json/country_neighbour_dist_file.json','r') as f:
                json_data = json.loads(f.read())
                return json_data
        elif self.json_dir != None:
            with open(self.json_dir) as f:
                json_data = json.loads(f.read())
                return json_data
    
    def normalize_json(self):
        # flatten the json data to the DataFrame format
        json_df = pd.json_normalize(self.json_data)
        return json_df
    
    def get_country_df(self, countryname):
        json_df = pd.DataFrame(self.json_data)
        country_df = json_df[[countryname]]
        #country_df = pd.json_normalize(self.json_data, record_path=[countryname])
        country_df = country_df.dropna()
        return country_df
        
    def save_df_to_csv(self, csvName):
        # Save DataFrame to CSV
        if csvName == None:
            self.json_df.to_csv('country_neighbour_dist.csv', index=True)
        elif csvName != None:
            self.json_df.to_csv(csvName, index=True)
    
    def process_country_data(self, countryname):
        # input the interested country name
        country_data = []
        country_name = countryname.capitalize()
        country_lst = self.json_df.head()
        matching = [s for s in country_lst if country_name in s]
        for mt in matching:
            mt_str = mt.split('.')
            if mt_str[0] == country_name:
                col_mt = self.json_df.loc[:, [mt]]
                mt_value = col_mt.dropna()
                country_data.append(mt_value)
        print(country_data)
        return country_data
    
    def plot_lst(self):
        df = pd.DataFrame(self.country_data)
        df.plot.bar()
                
        #for country_str in country_lst:
         #   country_strlst = country_str.split('.')
          #  if country_strlst[0] == country_name:
              #     print(country_name)
