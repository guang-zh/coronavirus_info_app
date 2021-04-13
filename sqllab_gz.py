# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.

"""
# Written by Azadeh, then edited by Guang

import os
import mysql.connector
from ScrapeClass_test import Scrape
from pandas.io import sql
from sqlalchemy import create_engine
#import pymysql
#from file import FILEIO

class SQLOBJ:
    def __init__(self, host, usr, passwd):
        self.host = host
        self.usr = usr
        self.passwd = passwd
        self.conn = self.connection_db()
        self.cursor = self.conn.cursor()
    
    def connection_db (self):
        try:
            conn = mysql.connector.connect(host=self.host,user=self.usr,password=self.passwd)
            return conn
        except mysql.connector.Error as err:
            print('some problem here with db connection: {}'.format(err) )

    def create_db(self, db_name):
        self.cursor.execute('Create Database '+db_name)
    
    def select_db(self,db_name):
        self.cursor.execute('use '+db_name)
    
    def create_table(self,table_name ,schema):
        self.cursor.execute('create table '+table_name+ schema+';')

    def select_data_from_table(self,table_name, columns_str, criteria_str):
        self.cursor.execute('select '+columns_str+' from '+table_name+' where '+criteria_str +';')

    def populate_table(self , table_name,lst_field,lst_value,format_str):
        insert_stm=('insert into '+table_name +lst_field+ 'Values' +format_str+';')
        self.cursor.executemany(insert_stm,lst_value)
        self.cursor.fetchall()

    def create_db_corona(self, databasename):
        self.create_db(databasename)
    
    '''
    def save_df_mysql(self, tablename, df):
        try:
            df.to_sql(tablename, con=self.engine, index=True, if_exists='fail')
        except ValueError as vx:
            print(vx)
        except Exception as ex:
            print(ex)
        #sql.write_frame(df, con=self.conn, name=tablename, if_exists='replace', flavor='mysql')
   '''     
   
  
'''
scrapeobj=Scrape(" file:///C:\\users\\Admin\\Downloads\\2021-03-17.html")
webscrape=scrapeobj.bsomaker()

scrapeobj.firstrow=scrapeobj.firstrow(webscrape)
finallis=scrapeobj.rows(webscrape)
scrapeobj.tuplerow(finallis)
   
tuple1=scrapeobj.finallis
   
lst_field1='(Scrapedate , ranking,Country_Other ,Total_Case,New_Cases , Total_Death , New_Deaths  ,Total_Recovered  ,Active_Cases ,Serious_Critical ,Tot_Cases_1M_pop ,Deaths_1M_pop, Total_Tests, Tests_1m_pop ,Population )'
format_str1='("2021-03-17",%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'

    
schema2='(Scrapedate date  NOT NULL ,ranking  int(5) NOT NULL,\
  Country_Other varchar(30) NOT NULL,Total_Case int(15) ,\
  New_Cases int(15) , Total_Death int(15), New_Deaths int(15) ,Total_Recovered int(15) ,Active_cases int(15),Serious_Critical int(15),\
  Tot_Cases_1M_pop int(15),Deaths_1M_pop int(15), Total_Tests int(15), Tests_1m_pop int(15),Population int(15),PRIMARY KEY (Scrapedate ,Country_Other));'
select_db(crs,'covid_corona_db_ahma_zhan')
create_table(crs,'corona_table ',schema2)
populate_table(crs , 'corona_table  ',lst_field1,tuple1,format_str1 )
   
js=FILEIO("country_neighbour_dist_file.json") 
js.readFromFile() 
js.readvalue()
   
newlist=[]
for i in js.list:       
    newlist.append(i)
    if ' ' in newlist[i]:
        newlist[i].replace(' ','_')
         
       
       
crs.commit()
conn.close()
'''