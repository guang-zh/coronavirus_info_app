# coronavirus_info_app
The pandemic COVID not only brings people fear, but also leads to increasing data, which should be more accessible and easily visualized for the public.

1. Web scrapping directly from Worldometers https://www.worldometers.info/coronavirus/
2. Scrape from local saved html pages from Worldometers
3. Save to MySQL Database and as CSV files
4. Data Exploration and Visualization: User choose interested Country, check Graphs for new cases, new deaths, new recovered, and neighbouring countries by border distances

Note: Application will be done using Django, and still in progress.

To run the Python coding:
Main Driver: mainGZ.py

Make sure you have the following modules installed:
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

If you don't have above modules, use _pip install module_name_
