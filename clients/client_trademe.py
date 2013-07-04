#!/usr/bin/env python
#http://api.trademe.co.nz/v1/Listings/553527490.json

import oauth2 as oauth
import time
import urllib2
import json
import datetime

def retrieve_all_listings():

	## api parameters
	# file_format	= 'json'
	adjacent_suburbs = 'false'	
	# bathrooms_max = None	
	# bathrooms_min = None	
	# bedrooms_max = None	
	# bedrooms_min = None	
	date_from = '2011-01-01' # time.strftime("%Y-%m-%d", time.localtime())	
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
	region = '1'	
	# rows = '500'	
	# search_string = 'million dollar views'	
	# sort_order = 'PriceAsc'	
	# suburb = None

	# url = "https://api.trademe.co.nz/v1/Search/Property/Residential.json?adjacent_suburbs=false&date_from=2011-01-01T00%3A00&photo_size=FullSize&region=1&rows=500&sort_order=PriceAsc HTTP/1.1"

	url = 'https://api.trademe.co.nz/v1/Search/Property/Residential.json?adjacent_suburbs=' + adjacent_suburbs + '&date_from=' + date_from + 'T00%3A00&photo_size=FullSize&region=' + region + '&rows=500&sort_order=PriceAsc HTTP/1.1'

	params = {
	    'oauth_version': "1.0",
	    'oauth_nonce': oauth.generate_nonce(),
	    'oauth_timestamp': int(time.time())
	}

	with open('./tmapikeys.txt') as fileObject:
		KEYHERE = fileObject.readline().strip()
		SECRETHERE = fileObject.readline().strip()
		CONSUMERKEYHERE = fileObject.readline().strip()
		CONSUMERSECRETHERE = fileObject.readline().strip()

	# Token.key and Token.secret are obtained after three-legged authentication.
	token = oauth.Token(key=KEYHERE, secret=SECRETHERE)
	consumer = oauth.Consumer(key=CONSUMERKEYHERE, secret=CONSUMERSECRETHERE)

	params['oauth_token'] = token.key
	params['oauth_consumer_key'] = consumer.key

	req = oauth.Request(method="GET", url=url, parameters=params)

	signature_method = oauth.SignatureMethod_HMAC_SHA1()
	req.sign_request(signature_method, consumer, token)

	rs = urllib2.urlopen(req.to_url())
	result_string = rs.read()
	
	# save result_string to disk here for backup?
	propertyPages = []
	propertyPages.append(json.loads(result_string))

	pages = propertyPages[0].get('TotalCount')/500

	for j in range(0,pages):
		#apiRequest = "https://api.trademe.co.nz/v1/Search/Property/Residential.json?adjacent_suburbs=false&date_from=2011-01-01T00%3A00&page="
		#apiRequest += str(j)
		#apiRequest += "&photo_size=FullSize&region=1&rows=500&sort_order=PriceAsc HTTP/1.1"

		apiRequest = 'https://api.trademe.co.nz/v1/Search/Property/Residential.json?adjacent_suburbs=' + adjacent_suburbs + '&date_from=' + date_from + 'T00%3A00&page=' + str(j) + '&photo_size=FullSize&region=' + region + '&rows=500&sort_order=PriceAsc HTTP/1.1'

		req = oauth.Request(method="GET", url=apiRequest, parameters=params)
		req.sign_request(signature_method, consumer, token)
		rs = urllib2.urlopen(req.to_url())
		
		result_string = rs.read()
		# save result_string to disk here for backup?
		propertyPages.append(json.loads(result_string))

	print len(propertyPages)
	return propertyPages

def retrieve_individual_listing(listingid):

	url = "http://api.trademe.co.nz/v1/Listings/"
	url += str(listingid) 
	url += ".json"

	params = {
	    'oauth_version': "1.0",
	    'oauth_nonce': oauth.generate_nonce(),
	    'oauth_timestamp': int(time.time())
	}

	with open('./tmapikeys.txt') as fileObject:
		KEYHERE = fileObject.readline().strip()
		SECRETHERE = fileObject.readline().strip()
		CONSUMERKEYHERE = fileObject.readline().strip()
		CONSUMERSECRETHERE = fileObject.readline().strip()

	# Token.key and Token.secret are obtained after three-legged authentication.
	token = oauth.Token(key=KEYHERE, secret=SECRETHERE)
	consumer = oauth.Consumer(key=CONSUMERKEYHERE, secret=CONSUMERSECRETHERE)

	params['oauth_token'] = token.key
	params['oauth_consumer_key'] = consumer.key

	req = oauth.Request(method="GET", url=url, parameters=params)

	signature_method = oauth.SignatureMethod_HMAC_SHA1()
	req.sign_request(signature_method, consumer, token)

	rs = urllib2.urlopen(req.to_url())
	result_string = rs.read()
	return result_string


if __name__ == '__main__':
    #retrieve_individual_listing(593811323)
    #retrieve_individual_listing(606638189)
	retrieve_all_listings()