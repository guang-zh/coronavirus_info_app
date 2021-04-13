# -*- coding: utf-8 -*-
"""
Created on Mon Mar 29 11:59:17 2021

@author: Guang
"""


# Module for Data Science: data_explore_analyse
# Read data, storing in dataframes, and make plots

import pandas as pd
import mysql.connector
import numpy as np
import matplotlib.pyplot as plt

class DataExplore():
    
    def __init__(self, country):
        self.country=country
        self.conn = self.get_SQLconnection()
        self.df_dist = self.get_dfDist()
        self.df_corona = self.get_dfCorona()
        self.maxborder_country = self.get_maxBorderCountry()
        self.df_lst = self.get_dfList()
        self.country_newcases = self.get_countryNewcases()
        self.country_newdeaths = self.get_countryNewdeaths()
        self.country_newrecovered = self.get_countryNewRecovered()
        self.index=['03-15','03-16','03-17','03-18','03-19','03-20','03-22','03-23','03-24','03-25','03-26','03-27','03-28','03-29']
        self.country_totdeath1M = self.get_Totdeath1M()
        self.bcountries_lst = self.get_NeighbourCountries()
        self.df3neighbours = self.get_Totdeath1M()
    
    def get_SQLconnection(self):
        # connection to mysql; modify user, password, host as needed
        db_name = 'covid_corona_db_ahma_zhan'
        conn = mysql.connector.connect(user='admin', password='password',
                              host='localhost',
                              database= db_name)
        return conn
    
    
    def get_df_fromSQL(self, table_name):
        sql_str = 'select * from '+table_name+';'
        df = pd.read_sql(sql_str, self.conn)
        return df
    
    def get_dfDist(self):
        table_name='countries_border'
        sql_str = 'select * from '+ table_name+' where Country_Other='+ '\''+str(self.country)+'\''+';'
        df_dist = pd.read_sql(sql_str, self.conn)
        return df_dist
    
    def get_dfCorona(self):
        table_name = 'corona_table'
        sql_str = 'select * from '+ table_name+' where Country_Other='+ '\''+str(self.country)+'\''+';'
        df_corona = pd.read_sql(sql_str, self.conn)
        return df_corona
        
    def saveDF_toCSV(self, df, csvName):
        df.to_csv(csvName)
    
    def get_maxBorderCountry(self):
        df_dist = self.df_dist
        maxborder_distance=(max(df_dist['Distance']))
        maxborder_country=df_dist.loc[df_dist['Distance']==maxborder_distance, 'Neigbour'].item()
        print("Longest bordered neighbour country for "+ self.country+': '+maxborder_country)
        return maxborder_country
    
    def cleanDF(self, df): # clean data frames from loaded CSV files
        df['NewCases']=df['NewCases'].str.strip('+')
        df['NewCases']=(df['NewCases'].replace(',','', regex=True).astype(float))
        df['NewDeaths']=(df['NewDeaths'].replace(',','', regex=True).astype(float))
        df['NewRecovered']=(df['NewRecovered'].replace(',','', regex=True).astype(float))
        df['Totdeath1M']=(df['Totdeath1M'].replace(',','', regex=True).astype(float))
        return df
    
    def get_countryNewcases(self):
        country_newcases = []
        for cdf in self.df_lst:
            cnewcase = cdf.loc[cdf['Country']==self.country,'NewCases'].item()
            country_newcases.append(cnewcase)
        return country_newcases
    
    def get_countryNewdeaths(self):
        country_newdeaths = []
        for cdf in self.df_lst:
            cnewdeath = cdf.loc[cdf['Country']==self.country,'NewDeaths'].item()
            country_newdeaths.append(cnewdeath)
        return country_newdeaths
    
    def get_countryNewRecovered(self):
      country_newrecovered = []
      for cdf in self.df_lst:  
          cnewrecovered = cdf.loc[cdf['Country']==self.country,'NewRecovered'].item()
          country_newrecovered.append(cnewrecovered)
      return country_newrecovered
    
    def plot_BarCountry(self):
        newcases_name = 'Newcases-'+self.country
        newdeaths_name = 'Newdeaths-'+self.country
        newrecovered_name = 'Newrecovered-'+self.country
        plot_title = '14-days key indicators evolution '+self.country
        newdata_df = pd.DataFrame({newcases_name:self.country_newcases,newdeaths_name:self.country_newdeaths,newrecovered_name:self.country_newrecovered}, index=self.index)
        ax1 = newdata_df.plot.bar(rot=0, fontsize=7, title=plot_title)
        ax1.set_xlabel("date")
        ax1.set_ylabel("3-main indicators")
    
    def plot_HistCountry(self):
        # Histograpm: NewCases, NewDeaths, NewRecovered
        newcases_name = 'Newcases-'+self.country
        newdeaths_name = 'Newdeaths-'+self.country
        newrecovered_name = 'Newrecovered-'+self.country
        plot_title = '14-days key indicators evolution '+self.country
        newdata_df = pd.DataFrame({newcases_name:self.country_newcases,newdeaths_name:self.country_newdeaths,newrecovered_name:self.country_newrecovered}, index=self.index)
        newdata_df.hist(alpha=0.5,layout=(3,1), figsize=(20,10))
    
    def plot_BarMaxBorder(self, bordercountry_newcases):
        # Second plot: 'NewCases' for interested country vs longest border neighbour country
        country_newcases = self.country_newcases
        newcases_country = 'Newcases-'+self.country
        newcases_maxcountry = 'Newcases-'+self.maxborder_country
        newcases_df = pd.DataFrame({newcases_country:self.country_newcases,newcases_maxcountry:bordercountry_newcases}, index=self.index)
        ax2 = newcases_df.plot.bar(rot=0, fontsize=7, title='14-day Newcases comparison-Italy with neighbour France')
        ax2.set_xlabel("date")
        ax2.set_ylabel("Newcases")
    
    def plot_ScatterMaxBorder(self, bordercountry_newcases):
        xlab = 'NewCases-'+self.country
        ylab = 'NewCases-'+self.maxborder_country
        df = pd.DataFrame({xlab:self.country_newcases, ylab:bordercountry_newcases})
        df.plot(xlab, ylab, kind='scatter')
    
    def get_NeighbourCountries(self):
        # find 3 neighbour countries with longest borders
        df_dist=self.df_dist.sort_values(by='Distance', ascending=False)
        bcountries = []
        for i in range(0, 3):
            bc=df_dist.iloc[i][2]
            bcountries.append(bc)
        print(self.country+' three neighbour countries with longest border distances: ')
        for i in range(0, len(bcountries)):
            print(bcountries[i])
        return bcountries
    
    def get_Totdeath1M(self):
        country_totdeath1M = []
        for cdf in self.df_lst:
            ctotdeath1M = cdf.loc[cdf['Country']==self.country,'Totdeath1M'].item()
            country_totdeath1M.append(ctotdeath1M)
        return country_totdeath1M
    
    def get_bTotdeath1M(self, bcountry):
        country_totdeath1M = []
        for cdf in self.df_lst:
            ctotdeath1M = cdf.loc[cdf['Country']==bcountry,'Totdeath1M'].item()
            country_totdeath1M.append(ctotdeath1M)
        return country_totdeath1M
    
    def get_df3neighbours(self):
        data3neighbours = []
        data3neighbours.append(self.get_Totdeath1M())
        for c in self.bcountries_lst:
            name = c + '_totdeath1M'
            globals()[name] = self.get_bTotdeath1M(c)
            data3neighbours.append(globals()[name])
        df3neighbours = pd.DataFrame(data3neighbours)
        return df3neighbours
    
    def plot_Bar3Neighbours(self):
        country_totdeath1M = self.country_totdeath1M
        bcountry1_totdeath1M = self.df3neighbours[1]
        bcountry2_totdeath1M = self.df3neighbours[2]
        bcountry3_totdeath1M = self.df3neighbours[3]
        l1 = 'Deaths/1M pop-'+self.country
        l2 = 'Deaths/1M pop-'+self.bcountries_lst[0]
        l3 = 'Deaths/1M pop-'+self.bcountries_lst[1]
        l4 = 'Deaths/1M pop-'+self.bcountries_lst[2]
        indices=[]
        indices.append(self.country)
        for c in self.bcountries_lst:
            indices.append(c)
        totdeath1M_df = pd.DataFrame({l1:country_totdeath1M,l2:bcountry1_totdeath1M,l3:bcountry2_totdeath1M,l4:bcountry3_totdeath1M}, index=indices)

        ax3 = totdeath1M_df.plot.bar(rot=0, fontsize=7, width=0.8, title='14-days Deaths/1M pop comparison-Italy with 3 neighbour countries')
        ax3.set_xlabel("date")
        ax3.set_ylabel("Deaths/1M pop")
        ax3.set_ylim([0,2500])
        ax3.legend(loc=2, prop={'size':7})
    
    def get_dfList(self): # read list of CSV files as df
        days = ['15','16','17','18','19','20','22','23','24','25','26','27','28','29']
        for d in days:
            csv_dir='corona_tables/corona2021-03-'+d+'.csv'
            if d=='15':
                df_0315 = pd.read_csv(csv_dir)
                df_0315 = self.cleanDF(df_0315)
            elif d=='16':
                df_0316 = pd.read_csv(csv_dir)
                df_0316 = self.cleanDF(df_0316)
            elif d=='17':
                df_0317 = pd.read_csv(csv_dir)
                df_0317 = self.cleanDF(df_0317)
            elif d=='18':
                df_0318 = pd.read_csv(csv_dir)
                df_0318 = self.cleanDF(df_0318)
            elif d=='19':
                df_0319 = pd.read_csv(csv_dir)
                df_0319 = self.cleanDF(df_0319)
            elif d=='20':
                df_0320 = pd.read_csv(csv_dir)
                df_0320 = self.cleanDF(df_0320)
            elif d=='22':
                df_0322 = pd.read_csv(csv_dir)
                df_0322 = self.cleanDF(df_0322)
            elif d=='23':
                df_0323 = pd.read_csv(csv_dir)
                df_0323 = self.cleanDF(df_0323)
            elif d=='24':
                df_0324 = pd.read_csv(csv_dir)
                df_0324 = self.cleanDF(df_0324)
            elif d=='25':
                df_0325 = pd.read_csv(csv_dir)
                df_0325 = self.cleanDF(df_0325)
            elif d=='26':
                df_0326 = pd.read_csv(csv_dir)
                df_0326 = self.cleanDF(df_0326)
            elif d=='27':
                df_0327 = pd.read_csv(csv_dir)
                df_0327 = self.cleanDF(df_0327)
            elif d=='28':
                df_0328 = pd.read_csv(csv_dir)
                df_0328 = self.cleanDF(df_0328)
            elif d=='29':
                df_0329 = pd.read_csv(csv_dir)
                df_0329 = self.cleanDF(df_0329)
            else: 
                print('Day is not in stored database')

        # df list for all DataFrames
        df_lst = [df_0315, df_0316, df_0317, df_0318, df_0319, df_0320, df_0322, df_0323, df_0324, df_0325, df_0326, df_0327, df_0328, df_0329]
        return df_lst
        

# asks user to enter the interested country and make 14-days trends plots
def main_datascience():
    country = input('Enter country interested: ')
    country = country.capitalize()
    data_obj = DataExplore(country)
    maxborder_country = data_obj.get_maxBorderCountry()
    
    # Bar plot for Newcases, Newdeaths, Newrecovered
    data_obj.plot_BarCountry()
    # Histogram for Newcases, Newdeaths, 
    data_obj.plot_HistCountry()
    
    # Get neighbour country with max border distance
    bordercountry_newcases = []
    for cdf in data_obj.df_lst:
        bcnewcase = cdf.loc[cdf['Country']==data_obj.maxborder_country,'NewCases'].item()
        bordercountry_newcases.append(bcnewcase)
    # Bar plot for Newcases comparison for country vs max bordered country
    data_obj.plot_BarMaxBorder(bordercountry_newcases)
    # Scatterplot for Newcases comparison for country vs max bordered country
    data_obj.plot_ScatterMaxBorder(bordercountry_newcases)
    
    # Find 3 neighbour countries with longest border distances
    bcountries_lst=data_obj.get_NeighbourCountries()
    
    df_corona = pd.read_csv('corona_table.csv')
    df_c = df_corona[df_corona['Country_Other']==country]
    c_death1M=df_c['Deaths_1M_pop']
    
    df_bc1 = df_corona[df_corona['Country_Other']==bcountries_lst[0]]
    bc1_death1M=df_bc1['Deaths_1M_pop']
    df_bc2 = df_corona[df_corona['Country_Other']==bcountries_lst[1]]
    bc2_death1M=df_bc2['Deaths_1M_pop']
    df_bc3 = df_corona[df_corona['Country_Other']==bcountries_lst[2]]
    bc3_death1M=df_bc3['Deaths_1M_pop']
    c_name = 'Deaths/1M pop-'+country
    bc1_name = 'Deaths/1M pop-'+bcountries_lst[0]
    bc2_name = 'Deaths/1M pop-'+bcountries_lst[1]
    bc3_name = 'Deaths/1M pop-'+bcountries_lst[2]
    #indices = []
    #indices.append(country)
    #for i in range(0, len(bcountries_lst)):
     #   indices.append(bcountries_lst[i])
    totdeath1M_df = pd.DataFrame({c_name:c_death1M.values.tolist(),bc1_name:bc1_death1M.values.tolist(),bc2_name:bc2_death1M.values.tolist(),bc3_name:bc3_death1M.values.tolist()})
    ax3 = totdeath1M_df.plot.bar(rot=0, fontsize=7, width=0.8, title='14-days Deaths/1M pop comparison-Italy with 3 neighbour countries')
    ax3.set_xlabel("date")
    ax3.set_ylabel("Deaths/1M pop")
    ax3.set_ylim([0,2500])
    ax3.legend(loc=2, prop={'size':7})
    # Histograpm: Deaths/1M pop for Italy, France, Austria, Slovenia
    totdeath1M_df.hist(alpha=0.5,layout=(4,1), figsize=(20,20))


    
# Codes for testing
'''
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
'''