#!/usr/bin/env python

import json
import sys
import client_trademe
import dao_sqlite

import sqlite3
import pandas as pd
import pandasql.sqldf as sqldf

import numpy as np

def populate_trademe_search_table():

	#propertyPages = client_trademe.retrieve_all_listings('2011-01-01','1')
	propertyPages = json.load(open('../json/propertyPages.json'))
	
	dao_sqlite.insert_search_results(propertyPages,'/Users/alanw/development/resources/nz-houses/db/test.db')
	

def populate_trademe_listing_table():
	
	#api request limit 1000 requests / hour ??

	conn = sqlite3.connect('/Users/alanw/development/resources/nz-houses/db/test.db')
	with conn:
		cur = conn.cursor()
		cur.execute('SELECT * FROM residential_listings')
		
		rows = cur.fetchall()

		ids = np.zeros([len(rows),1],dtype=int)
		i = 0
		for row in rows[:5]:
			ids[i] = row[0]
			i += 1
		
		print ids[:5]

if __name__ == '__main__':
	
	#populate_trademe_search_table()
	populate_trademe_listing_table()

