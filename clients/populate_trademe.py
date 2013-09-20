#!/usr/bin/env python

import json
import sys
import client_trademe_rauth as client_trademe
import dao_sqlite
import argparse 
import sqlite3
#import pandas as pd
#import pandasql.sqldf as sqldf

import numpy as np

def populate_trademe_search_table(database_file):

	propertyPages = client_trademe.retrieve_all_listings('2011-01-01','3')
	# second argument is region. 3 is Canterbury/Christchurch(?)
	
	
	#propertyPages = json.load(open('../data/propertyPages.json'))
	
	dao_sqlite.insert_search_results(propertyPages,database_file)
	

def populate_trademe_listing_table():
	
	#api request limit 1000 requests / hour ??

	conn = sqlite3.connect('/Users/james/development/resources/nz-houses/db/test.db')
	with conn:
		cur = conn.cursor()
		cur.execute('SELECT * FROM residential_listings')
		
		rows = cur.fetchall()

		ids = np.zeros([len(rows),1],dtype=int)
		i = 0
		for row in rows:#[:5]:
			ids[i] = row[0]
			i += 1
		#print ids[:10]

	number_of_hours = len(ids)/1000.0
	print int(np.ceil(number_of_hours))

	#for j in range(0,len(ids)):
	#	print ids[j]

if __name__ == '__main__':
	
	parser = argparse.ArgumentParser(description='Pull Residential Listings from Trademe to sqlite3 database')
    parser.add_argument("-db", "--dbFilePath", required=True, help="sqlite3 database file path")
    parser.add_argument("-ed", "--endDate", required=False, help="End date of data for copy job. Needs to be in the format yyyyMMdd. Date will be attached to end of source. E.g. -ed 20130513. Date needs to be represented in folder structure of the bucket. E.g. s3n://sourceBucket/20130513")
    args = parser.parse_args();
    

    database_file = '/Users/james/development/resources/nz-houses/db/test.db'

	populate_trademe_search_table(database_file)
	
	
	#populate_trademe_listing_table()

