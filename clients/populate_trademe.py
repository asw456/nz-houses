#!/usr/bin/env python

import json
import sys
import client_trademe_rauth as client_trademe
import insert_records_sqlite as dao_sqlite
import argparse
import sqlite3
import time
#import pandas as pd
#import pandasql.sqldf as sqldf

import numpy as np

def populate_residential_search_table(database_file):

	residential_json_pages = client_trademe.request_listings('Residential','2011-01-01','3')
	# second argument is region. 3 is Canterbury/Christchurch(?)

	#with open('/Users/james/development/code_personal/nz-houses/data/residential_pages.json', 'w') as json_f:
	#	json.dump(residential_json_pages, json_f)
	#with open('/Users/james/development/code_personal/nz-houses/data/residential_pages.json', 'r') as json_f:
	#	residential_json_pages = json.load(json_f)

	dao_sqlite.create_table_residential(database_file)
	dao_sqlite.insert_residential_json(residential_json_pages,database_file)

def populate_rental_search_table(database_file):

	rental_json_pages = client_trademe.request_listings('Rental','2011-01-01','3')
	# second argument is region. 3 is Canterbury/Christchurch(?)

	#with open('/Users/james/development/code_personal/nz-houses/data/rental_pages.json', 'w') as json_f:
	#	json.dump(rental_json_pages, json_f)
	#with open('/Users/james/development/code_personal/nz-houses/data/rental_pages.json', 'r') as json_f:
	#	rental_json_pages = json.load(json_f)

	dao_sqlite.create_table_rental(database_file)
	dao_sqlite.insert_rental_json(rental_json_pages,database_file)



def populate_trademe_listing_table(database_file):

	#api request limit 1000 requests / hour ??

	conn = sqlite3.connect(database_file)
	with conn:
		cur = conn.cursor()
		cur.execute('SELECT * FROM residential_listings')

		rows = cur.fetchall()

		ids = []
		for row in rows:
			ids.append(row[0])
		#print 'ids = ' + str(ids)

	number_of_hours = len(ids)/1000.0
	#print 'number of hours = ' + str(int(np.ceil(number_of_hours)))


	dao_sqlite.create_table_residential_listings_individual(database_file)

	k = 0
	for id in reversed(ids):
		result = client_trademe.retrieve_individual_listing(id)
		if 'ListingId' in result:
			dao_sqlite.insert_individual_listing(result,database_file)
			#print json.dumps(result, sort_keys=True, indent=4)
			k += 1
		if k % 800 == 0:
			print 'going to sleep, OK to terminate'
			time.sleep(3600.0 + 60)
			print 'waking up, don\'t terminate'

	print 'exit 0'


if __name__ == '__main__':

	parser = argparse.ArgumentParser(description='Pull Residential Listings from Trademe to sqlite3 database')

	parser.add_argument("-db", "--dbFilePath", \
		required=False, \
		default='/Users/james/development/personal/nz-houses/db/prod1.db', \
		help='sqlite3 database file path')

	parser.add_argument("-ed", "--endDate",
		required=False,
		help="stuff")

	args = parser.parse_args();

	populate_residential_search_table(args.dbFilePath)
	populate_rental_search_table(args.dbFilePath)
	populate_trademe_listing_table(args.dbFilePath)


