#!/usr/bin/env python
#http://api.trademe.co.nz/v1/Listings/553527490.json

from rauth.service import OAuth1Service
import time
import urllib2
import json
import datetime
import math

def request_listings(listing_type,date_from,region):

	# file_format	= 'json'
	# adjacent_suburbs = 'false'
	# bathrooms_max = None	
	# bathrooms_min = None	
	# bedrooms_max = None	
	# bedrooms_min = None	
	# date_from = '2011-01-01' # time.strftime("%Y-%m-%d", time.localtime())	
	# district = '1'	
	# latitude_max = None	
	# latitude_min = None	
	# longitude_max =	None
	# longitude_min =	None
	# page = '1'	
	# photo_size = 'FullSize'	
	# price_max = None
	# price_min = None	
	# property_type = None
	# region = '1'	
	# rows = '500'	
	# search_string = 'million dollar views'	
	# sort_order = 'PriceAsc'	
	# suburb = None

	# Location hierarchy is Region/Locality, District, Suburb (+ adjacent Suburbs)

	# simple api request
	# 'https://api.trademe.co.nz/v1/Search/Property/Residential.json?adjacent_suburbs=false&date_from=2011-01-01T00%3A00&photo_size=FullSize&region=1&rows=500&sort_order=PriceAsc HTTP/1.1'
	# more complex request 
	# 'https://api.tmsandbox.co.nz/v1/Search/Property/Residential.json?adjacent_suburbs=false&date_from=2011-01-01T00%3A00&district=1&latitude_max=12&latitude_min=13&longitude_max=14&longitude_min=15&page=1&photo_size=FullSize&property_type=House%2CSection%2CTownhouse%2CUnit&region=2&rows=500&search_string=searchstring&sort_order=PriceAsc&suburb=1 HTTP/1.1'

	residential_json_pages = []
	
	# url = 'https://api.trademe.co.nz/v1/Search/Property/Residential.json?adjacent_suburbs=' + adjacent_suburbs + '&date_from=' + date_from + 'T00%3A00&photo_size=FullSize&region=' + region + '&rows=500&sort_order=PriceAsc HTTP/1.1'
	# url = 'https://api.trademe.co.nz/v1/Search/Property/' + listing_type + '.json?adjacent_suburbs=' + adjacent_suburbs + '&date_from=' + date_from + 'T00%3A00&photo_size=FullSize&region=' + region + '&rows=500&sort_order=PriceAsc HTTP/1.1'
	url = 'https://api.trademe.co.nz/v1/Search/Property/' + listing_type + '.json?date_from=' + date_from + 'T00%3A00&photo_size=FullSize&region=' + region + '&district=60' + '&rows=500&sort_order=PriceAsc HTTP/1.1'
	print url

	with open('./tmapikeys.txt') as fileObject:
		KEYHERE = fileObject.readline().strip()
		SECRETHERE = fileObject.readline().strip()
		CONSUMERKEYHERE = fileObject.readline().strip()
		CONSUMERSECRETHERE = fileObject.readline().strip()

	service = OAuth1Service(name='service', consumer_key = KEYHERE, consumer_secret = SECRETHERE)
	session = service.get_session((CONSUMERKEYHERE, CONSUMERSECRETHERE))
	
	r = session.get(url)
	residential_json_pages.append(r.json())

	print 'TotalCount = ' + str(residential_json_pages[0].get('TotalCount'))
	pages = int(math.ceil(residential_json_pages[0].get('TotalCount')/500.0))

	for j in range(2,pages+1):
		# apiRequest = 'https://api.trademe.co.nz/v1/Search/Property/Residential.json?adjacent_suburbs=false&date_from=2011-01-01T00%3A00&page=' + str(j) + '&photo_size=FullSize&region=1&rows=500&sort_order=PriceAsc HTTP/1.1'
		# apiRequest = 'https://api.trademe.co.nz/v1/Search/Property/' + listing_type + '.json?adjacent_suburbs=' + adjacent_suburbs + '&date_from=' + date_from + 'T00%3A00&page=' + str(j) + '&photo_size=FullSize&region=' + region + '&rows=500&sort_order=PriceAsc HTTP/1.1'
		apiRequest = 'https://api.trademe.co.nz/v1/Search/Property/' + listing_type + '.json?date_from=' + date_from + 'T00%3A00&page=' + str(j) + '&photo_size=FullSize&region=' + region + '&district=60' + '&rows=500&sort_order=PriceAsc HTTP/1.1'
		print apiRequest

		r = session.get(apiRequest)
		residential_json_pages.append(r.json())	
	
	print 'residential_json_pages structure length is ' + str(len(residential_json_pages))
	return residential_json_pages
	
	
	
def retrieve_individual_listing(listingid):

	url = "http://api.trademe.co.nz/v1/Listings/"
	url += str(listingid) 
	url += ".json"

	with open('./tmapikeys.txt') as fileObject:
		KEYHERE = fileObject.readline().strip()
		SECRETHERE = fileObject.readline().strip()
		CONSUMERKEYHERE = fileObject.readline().strip()
		CONSUMERSECRETHERE = fileObject.readline().strip()

	service = OAuth1Service(name='service', consumer_key = KEYHERE, consumer_secret = SECRETHERE)
	session = service.get_session((CONSUMERKEYHERE, CONSUMERSECRETHERE))
	
	r = session.get(url)
	#print url
	return r.json()


if __name__ == '__main__':
    
    print retrieve_individual_listing(593811323)
	#retrieve_all_listings()