#!/usr/bin/env python
#http://api.trademe.co.nz/v1/Listings/553527490.json

import oauth2 as oauth
import time
import urllib2
import json

def retrieve_school_zone():

  with open('./kdapikeys.txt') as fileObject:
    KEYHERE = fileObject.readline().strip()

	#school zone request
	apiRequest = 'http://api.koordinates.com/api/vectorQuery.json/?key=' + KEYHERE + '&layer=743&x='
	apiRequest += str(174.6964)
	apiRequest += '&y='
	apiRequest += str(-36.9246)
	apiRequest += '&radius=0'

	rs = urllib2.urlopen(apiRequest)	
	result_string = rs.read()

	results = json.loads(result_string)

	features = results.get('vectorQuery').get('layers').get('743').get('features')

	for i in range(0,len(features)):
		distance = features[i].get('properties').get('distance')
		schoolID = features[i].get('properties').get('SchoolID')
		schoolName = features[i].get('properties').get('SchoolName')
		effectiveDate = features[i].get('properties').get('EffectiveDate')
		iNSTTYPE = features[i].get('properties').get('INSTTYPE')
		# create tuple and append to tuples

def retrieve_elevation():

  with open('./kdapikeys.txt') as fileObject:
    KEYHERE = fileObject.readline().strip()

	#apiRequest = 'http://api.koordinates.com/api/vectorQuery.json?key=' + KEYHERE + '&layer=1165&x=174.7254467010498&y=-36.871106809995844&max_results=3&radius=10000&geometry=true&with_field_names=true'
	#apiRequest = 'http://api.koordinates.com/api/vectorQuery.json?key=' + KEYHERE + '&layer=281&x=174.7254467010498&y=-36.871106809995844&max_results=3&radius=10000&geometry=true&with_field_names=true'
	apiRequest = 'http://api.koordinates.com/api/vectorQuery.json?key=' + KEYHERE + '&layer=1066&x=174.7254467010498&y=-36.871106809995844&max_results=3&radius=0&geometry=true&with_field_names=true'

	rs = urllib2.urlopen(apiRequest)
	result_string = rs.read()

	results = json.loads(result_string)

	print results


if __name__ == '__main__':
	retrieve_school_zone()
	retrieve_elevation()


