# -*- coding: utf-8 -*-
"""
Created on Sat Mar 27 00:29:01 2021

@author: guang
"""

# Azadeh: wrote ScrapeClass.py
# This script is written using different methods for converting html to pd then save as CSV
# Purpose is to save scraped html tables as CSV for dataframes and plotting

import json
import pandas as pd
from bs4 import BeautifulSoup
from urllib.request import urlopen
import os
import codecs
#import lxml
#import html5lib
import csv
import requests
import urllib.error
import urllib.parse

class scrapping:
    def __init__(self):
        self.current_dir = os.getcwd()
        self.day = self.get_date()
        self.local_html = os.path.join('local_html', self.get_filename())
        self.file_dir = os.path.join(self.current_dir, self.local_html)
        self.scrapped = self.scrape_html()
        self.rows = self.get_rows()
        self.df = self.get_df()
    
    def get_date(self):
        response = int(input("Enter day only (1-31):\n"))
        return response
    
    def get_filename(self):
        # missing 2021-03-21 data
        if self.day>=15 and self.day<=17:
            return 'local_page2021-03-17.html'
        elif self.day >=18 and self.day <=20:
            return 'local_page2021-03-20.html'
        elif self.day >= 22 and self.day <=23:
            return 'local_page2021-03-24.html'
        elif self.day >=24 and self.day <=26:
            return 'local_page2021-03-26.html'
        elif self.day >=27 and self.day <=29:
            return 'local_page2021-03-29.html'
        else:
            print("Sorry, the day you enterred is not in the database")
    
    def scrape_html(self):
        file = codecs.open(self.file_dir, "r","utf-8")
        html = file.read()
        scrapped = BeautifulSoup(html, 'html.parser')
        return scrapped
    
    def get_tableid(self):
        if self.day == 17 or self.day == 20 or self.day==26 or self.day==29:
            return 'main_table_countries_today'
        elif self.day == 16 or self.day == 19 or self.day==25 or self.day==28 or self.day==23:
            return 'main_table_countries_yesterday'
        elif self.day == 15 or self.day == 18 or self.day==24 or self.day==27 or self.day==22:
            return 'main_table_countries_yesterday2'
        else:
            print("Interested date is not in stored in database")
    
    def get_rows(self):
        table = self.scrapped.find(id=self.get_tableid())
        rows = table.find_all('tr')
        return rows
    
    def get_df(self):
        try:
            table_data = []
            for row in self.rows:
                row_data = []
                for cell in row.findAll('td'):
                    row_data.append(cell.text)
                if(len(row_data) > 0):
                    data_item = {"Country": row_data[1],
                                 "TotalCases": row_data[2],
                                 "NewCases": row_data[3],
                                 "TotalDeaths": row_data[4],
                                 "NewDeaths": row_data[5],
                                 "TotalRecovered": row_data[6],
                                 "NewRecovered": row_data[7],
                                 "ActiveCases": row_data[8],
                                 "CriticalCases": row_data[9],
                                 "Totcase1M": row_data[10],
                                 "Totdeath1M": row_data[11],
                                 "TotalTests": row_data[12],
                                 "Tottest1M": row_data[13],
                                 "Population": row_data[14]
                    }
                    table_data.append(data_item)
            df = pd.DataFrame(table_data)
            df = df.drop(df[df.Population==''].index)
            df['NewCases']=df['NewCases'].str.strip('+')
            #df['NewCases']=df['NewCases'].replace(',','', regex=True).astype(float)
            #df['NewDeaths']=df['NewDeaths'].replace(',','', regex=True).astype(float)
            #df['NewRecovered']=df['NewRecovered'].replace(',','', regex=True).astype(float)
            #df['Totdeath1M']=df['Totdeath1M'].replace(',','', regex=True).astype(float)
            return df
        except:
            print('Error for converting to DataFrame')
    
    def save_df(self):
        csvName = 'corona2021-03-'+str(self.day)+'.csv'
        csvPath = os.path.join(self.current_dir, 'corona_tables')
        csv_dir = os.path.join(csvPath, csvName)
        self.df.to_csv(csv_dir, index=True)
        print("Saved to local csv file")
    
    
def main_save_localhtml(url, htmlname):
    response = requests.get(url)
    html = response.content
    html_path = os.path.join(os.getcwd(), 'local_html')
    html_name = os.path.join(html_path, htmlname)
    f = open(html_name, 'wb')
    f.write(html)
    f.close
        

