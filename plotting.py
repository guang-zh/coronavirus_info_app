# -*- coding: utf-8 -*-
"""
Created on Mon Mar 29 11:59:17 2021

@author: Guang
"""


# Plotting
# Data_explore_analyse (dataScience), reading tables and stored in dataframes, then plots

import pandas as pd
import mysql.connector
import numpy as np
import matplotlib.pyplot as plt

# connection to mysql; modify user, password, host as needed
db_name = 'covid_corona_db_ahma_zhan'
conn = mysql.connector.connect(user='admin', password='password',
                              host='localhost',
                              database= db_name)
crs=conn.cursor()


# Ask User to enter the interested country
# read from database with mysql connection, and save to dataframe
country = input("Enter country interested: ")
sql_str = 'select * from countries_border where Country_Other='+ '\''+str(country)+'\''
df_dist = pd.read_sql(sql_str, conn)


# Find the neighbour country with longest borders
maxborder_distance=(max(df_dist['Distance']))
maxborder_country=df_dist.loc[df_dist['Distance']==maxborder_distance, 'Neigbour'].item()
print("Longest bordered neighbour country for "+ country+': '+maxborder_country)


# Read CSV files as dataframes
def cleanDF(df):
    df['NewCases']=df['NewCases'].str.strip('+')
    df['NewCases']=(df['NewCases'].replace(',','', regex=True).astype(float))
    df['NewDeaths']=(df['NewDeaths'].replace(',','', regex=True).astype(float))
    df['NewRecovered']=(df['NewRecovered'].replace(',','', regex=True).astype(float))
    df['Totdeath1M']=(df['Totdeath1M'].replace(',','', regex=True).astype(float))
    return df

# Read CSV to df and clean the df
# note 2021-03-21 is missing due to lack of data from saved html
days = ['15','16','17','18','19','20','22','23','24','25','26','27','28','29']
for d in days:
    csv_dir='corona_tables/corona2021-03-'+d+'.csv'
    if d=='15':
        df_0315 = pd.read_csv(csv_dir)
        df_0315 = cleanDF(df_0315)
    elif d=='16':
        df_0316 = pd.read_csv(csv_dir)
        df_0316 = cleanDF(df_0316)
    elif d=='17':
        df_0317 = pd.read_csv(csv_dir)
        df_0317 = cleanDF(df_0317)
    elif d=='18':
        df_0318 = pd.read_csv(csv_dir)
        df_0318 = cleanDF(df_0318)
    elif d=='19':
        df_0319 = pd.read_csv(csv_dir)
        df_0319 = cleanDF(df_0319)
    elif d=='20':
        df_0320 = pd.read_csv(csv_dir)
        df_0320 = cleanDF(df_0320)
    elif d=='22':
        df_0322 = pd.read_csv(csv_dir)
        df_0322 = cleanDF(df_0322)
    elif d=='23':
        df_0323 = pd.read_csv(csv_dir)
        df_0323 = cleanDF(df_0323)
    elif d=='24':
        df_0324 = pd.read_csv(csv_dir)
        df_0324 = cleanDF(df_0324)
    elif d=='25':
        df_0325 = pd.read_csv(csv_dir)
        df_0325 = cleanDF(df_0325)
    elif d=='26':
        df_0326 = pd.read_csv(csv_dir)
        df_0326 = cleanDF(df_0326)
    elif d=='27':
        df_0327 = pd.read_csv(csv_dir)
        df_0327 = cleanDF(df_0327)
    elif d=='28':
        df_0328 = pd.read_csv(csv_dir)
        df_0328 = cleanDF(df_0328)
    elif d=='29':
        df_0329 = pd.read_csv(csv_dir)
        df_0329 = cleanDF(df_0329)
    else: 
        print('Day is not in stored database')

# df list for all DataFrames
df_lst = [df_0315, df_0316, df_0317, df_0318, df_0319, df_0320, df_0322, df_0323, df_0324, df_0325, df_0326, df_0327, df_0328, df_0329]


# First plot: 'NewCases', 'NewDeaths', 'NewRecovered' for the interested country
country_newcases = []
country_newdeaths = []
country_newrecovered = []
for cdf in df_lst:
    cnewcase = cdf.loc[cdf['Country']==country,'NewCases'].item()
    country_newcases.append(cnewcase)
    cnewdeath = cdf.loc[cdf['Country']==country,'NewDeaths'].item()
    country_newdeaths.append(cnewdeath)
    cnewrecovered = cdf.loc[cdf['Country']==country,'NewRecovered'].item()
    country_newrecovered.append(cnewrecovered)

index=['03-15','03-16','03-17','03-18','03-19','03-20','03-22','03-23','03-24','03-25','03-26','03-27','03-28','03-29']
if country=='Italy':
    newdata_df = pd.DataFrame({'Newcases-Italy':country_newcases,'Newdeaths-Italy':country_newdeaths,'Newrecovered-Italy':country_newrecovered}, index=index)
    ax1 = newdata_df.plot.bar(rot=0, fontsize=7, title='14-days key indicators evolution Italy')
    ax1.set_xlabel("date")
    ax1.set_ylabel("3-main indicators")

# Histograpm: Italy NewCases, NewDeaths, NewRecovered
newdata_df.hist(alpha=0.5,layout=(3,1), figsize=(20,10))

# Second plot: 'NewCases' for interested country vs longest border neighbour country
country_newcases = []
bordercountry_newcases = []
for cdf in df_lst:
    cnewcase = cdf.loc[cdf['Country']==country,'NewCases'].item()
    country_newcases.append(cnewcase)
    bcnewcase = cdf.loc[cdf['Country']==maxborder_country,'NewCases'].item()
    bordercountry_newcases.append(bcnewcase)

index=['03-15','03-16','03-17','03-18','03-19','03-20','03-22','03-23','03-24','03-25','03-26','03-27','03-28','03-29']
if country=='Italy':
    newcases_df = pd.DataFrame({'Newcases-Italy':country_newcases,'Newcases-France':bordercountry_newcases}, index=index)
    ax2 = newcases_df.plot.bar(rot=0, fontsize=7, title='14-day Newcases comparison-Italy with neighbour France')
    ax2.set_xlabel("date")
    ax2.set_ylabel("Newcases")

# Scatterplot: Italy and France for NewCases
plt.scatter(x=country_newcases, y=bordercountry_newcases, alpha=0.5)
plt.xlabel("NewCases - Italy")
plt.ylabel("NewCases - France")
plt.show()

# Third plot: Deaths/1M pop comparison for Italy with 3 neighbour countries with longer border distances
# find 3 neighbour countries with longest borders
df_dist=df_dist.sort_values(by='Distance', ascending=False)
bcountries = []
for i in range(0, 3):
    bc=df_dist.iloc[i][2]
    bcountries.append(bc)
print('Italy three neighbour countries with longest border distances: ')
for i in range(0, len(bcountries)):
    print(bcountries[i])
# bcountries: ['France', 'Austria', 'Slovenia']

# Italy (interested country) 
country_totdeath1M = []
for cdf in df_lst:
    ctotdeath1M = cdf.loc[cdf['Country']==country,'Totdeath1M'].item()
    country_totdeath1M.append(ctotdeath1M)

# France
france_totdeath1M = []
for cdf in df_lst:    
    bctotdeath1M = cdf.loc[cdf['Country']=='France','Totdeath1M'].item()
    france_totdeath1M.append(bctotdeath1M)

# Austria
austria_totdeath1M = []
for cdf in df_lst:    
    bctotdeath1M = cdf.loc[cdf['Country']=='Austria','Totdeath1M'].item()
    austria_totdeath1M.append(bctotdeath1M)

# Solovenia
slovenia_totdeath1M = []
for cdf in df_lst:    
    bctotdeath1M = cdf.loc[cdf['Country']=='Slovenia','Totdeath1M'].item()
    slovenia_totdeath1M.append(bctotdeath1M)

totdeath1M_df = pd.DataFrame({'Deaths/1M pop-Italy':country_totdeath1M,'Deaths/1M pop-France':france_totdeath1M,'Deaths/1M pop-Austria':austria_totdeath1M,'Deaths/1M pop-Slovenia':slovenia_totdeath1M}, index=index)
ax3 = totdeath1M_df.plot.bar(rot=0, fontsize=7, width=0.8, title='14-days Deaths/1M pop comparison-Italy with 3 neighbour countries')
ax3.set_xlabel("date")
ax3.set_ylabel("Deaths/1M pop")
ax3.set_ylim([0,2500])
ax3.legend(loc=2, prop={'size':7})

# Histograpm: Deaths/1M pop for Italy, France, Austria, Slovenia
totdeath1M_df.hist(alpha=0.5,layout=(4,1), figsize=(20,20))