# -*- coding: utf-8 -*-
"""
Created on Wed Mar 24 14:02:26 2021

@author: Guang
"""

# written modules
from scrape_module import scrapping
from scrape_module import main_save_localhtml
from data_explore_module import DataExplore
from data_explore_module import main_datascience

# built-in modules
import json
import matplotlib
import pandas as pd
from bs4 import BeautifulSoup
from urllib.request import urlopen
import requests
import os
import mysql.connector as myc
import html5lib
import codecs
import lxml
import csv


def main_project():
    # Ask Users to Scrape or Save to local files
    response = int(input("""
    Please enter your choice:
    1. save to local web file
    2. scrape from a saved local file
    3. data science
    """))
    print("User enters "+str(response))
    
    # Based on the choice by User
    if response == 1:
        url = 'https://www.worldometers.info/coronavirus/'
        filename = input("Enter html name you want to save as:")
        # function for scrapping from URL
        main_save_localhtml(url, filename)
    elif response == 2:
        # scrape_module Object
        scrapped = scrapping()
        scrapped.save_df()
    elif response == 3:
        main_datascience()
    elif response != 1 or response != 2:
        print("Enterred option is not valid")

         
main_project()    

