#!/usr/bin/env python

import json
import sys
import apiTrademe
import daoSqlite

def populate_trademe_search_table():

	#propertyPages = json.load(open('../json/propertyPages.json'))
	
    columns = ['ListingId','Title','Category','StartPrice','StartDate','EndDate','IsFeatured','HasGallery','IsBold','IsHighlighted','AsAt','CategoryPath','PictureHref','RegionId','Region','SuburbId','Suburb','ReserveState','IsClassified','Latitude','Longitude','Northing','Easting','Accuracy','PriceDisplay','Address','District','AgencyReference','LandArea','Bathrooms','Bedrooms','ListingGroup','Parking','PropertyType','PropertyId','DistrictId','AgencyId','AgencyName','AgencyPhoneNumber','AgencyWebsite','IsRealEstateAgnecy','IsLicensedPropertyAgency']

	#print len(columns)
	x = propertyPages[0]['List'][0]
	tuple = (x['Title'].encode('ascii'),x['ListingId'])
	#print tuple

	y=x

	print 'hello'
	print y.get('AgencyReference')
	print y.get('GeographicLocation').get('Latitude')

	property_tuple2 = (y['ListingId'],y['Title'].encode['ascii'],y['Category'].encode['ascii'],y['StartPrice'],y['StartDate'],y['EndDate'],y['IsFeatured'],y['HasGallery'],y['IsBold'],y['IsHighlighted'],y['AsAt'],y['CategoryPath'].encode['ascii'],y['PictureHref'].encode['ascii'],y['RegionId'],y['Region'],y['SuburbId'],y['Suburb'].encode['ascii'],y['ReserveState'],y['IsClassified'],y['Latitude'],y['Longitude'],y['Northing'],y['Easting'],y['Accuracy'],y['PriceDisplay'].encode['ascii'],y['Address'].encode['ascii'],y['District'].encode['ascii'],y['AgencyReference'].encode['ascii'] if y['AgencyReference'] else None)
	print property_tuple2

	'''
	property_tuple2 = (y['ListingId'],y['Title'].encode['ascii'],y['Category'].encode['ascii'],y['StartPrice'],y['StartDate'],y['EndDate'],y['IsFeatured'],y['HasGallery'],y['IsBold'],y['IsHighlighted'],y['AsAt'],y['CategoryPath'].encode['ascii'],y['PictureHref'].encode['ascii'],y['RegionId'],y['Region'],y['SuburbId'],y['Suburb'].encode['ascii'],y['ReserveState'],y['IsClassified'],y['Latitude'],y['Longitude'],y['Northing'],y['Easting'],y['Accuracy'],y['PriceDisplay'].encode['ascii'],y['Address'].encode['ascii'],y['District'].encode['ascii'],y['AgencyReference'].encode['ascii'] if y['AgencyReference'] else None,y['LandArea'],y['Bathrooms'],y['Bedrooms'],y['ListingGroup'].encode['ascii'],y['Parking'].encode['ascii'],y['PropertyType'].encode['ascii'],y['PropertyId'].encode['ascii'],y['DistrictId'],y['AgencyId'],y['AgencyName'].encode['ascii'],y['AgencyPhoneNumber'].encode['ascii'],y['AgencyWebsite'].encode['ascii'],y['IsRealEstateAgnecy'],y['IsLicensedPropertyAgency'])
	print property_tuple2
	'''

def populate_trademe_listing_table():
	
	# api request limit 1000 requests / hour
	pass


if __name__ == '__main__':
	populate_trademe_search_table()


