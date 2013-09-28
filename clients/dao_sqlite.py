import json
import sqlite3
import sys
import re
import dateutil.parser
import datetime

# API Reference is at 
# http://developer.trademe.co.nz/api-reference/search-methods/residential-search/

def create_table_residential(dbPath):
  
    conn = sqlite3.connect(dbPath)
    with conn:
        cur = conn.cursor()
        #cur.execute("DROP TABLE IF EXISTS residential_listings")
        cur.execute("CREATE TABLE IF NOT EXISTS residential_listings (ListingId INTEGER,Title VARCHAR(100),Category VARCHAR(50),StartPrice REAL,StartDate INTEGER,EndDate INTEGER,IsFeatured INTEGER,HasGallery INTEGER,IsBold INTEGER,IsHighlighted INTEGER,AsAt INTEGER,CategoryPath VARCHAR(100),PictureHref VARCHAR(100),RegionId INTEGER,Region VARCHAR(50),SuburbId INTEGER,Suburb VARCHAR(100),ReserveState INTEGER,IsClassified VARCHAR(5),Latitude REAL,Longitude REAL,Northing INTEGER,Easting INTEGER,Accuracy INTEGER,PriceDisplay VARCHAR(100),Address VARCHAR(100),District VARCHAR(100),AgencyReference VARCHAR(10),LandArea INTEGER,Bathrooms INTEGER,Bedrooms INTEGER,ListingGroup VARCHAR(100),Parking VARCHAR(100),PropertyType VARCHAR(50),PropertyId VARCHAR(50),DistrictId INTEGER,AgencyId INTEGER,AgencyName VARCHAR(255),AgencyPhoneNumber VARCHAR(20),IsRealEstateAgnecy VARCHAR(6),IsLicensedPropertyAgency VARCHAR(6), UNIQUE(ListingId) ON CONFLICT REPLACE)")

def create_table_rental(dbPath):
  
    conn = sqlite3.connect(dbPath)
    with conn:
        cur = conn.cursor()
        #cur.execute("DROP TABLE IF EXISTS rental_listings")
        cur.execute("CREATE TABLE IF NOT EXISTS rental_listings (ListingId INTEGER,Title VARCHAR(100),Category VARCHAR(50),RentPerWeek INTEGER,SmokersOkay VARCHAR(5),StartDate INTEGER,EndDate INTEGER,IsFeatured INTEGER,HasGallery INTEGER,IsBold INTEGER,IsHighlighted INTEGER,AsAt INTEGER,CategoryPath VARCHAR(100),PictureHref VARCHAR(100),RegionId INTEGER,Region VARCHAR(50),SuburbId INTEGER,Suburb VARCHAR(100),ReserveState INTEGER,IsClassified VARCHAR(5),Latitude REAL,Longitude REAL,Northing INTEGER,Easting INTEGER,Accuracy INTEGER,PriceDisplay VARCHAR(100),Address VARCHAR(100),District VARCHAR(100),AgencyReference VARCHAR(10),LandArea INTEGER,Bathrooms INTEGER,Bedrooms INTEGER,ListingGroup VARCHAR(100),Parking VARCHAR(100),PropertyType VARCHAR(50),PropertyId VARCHAR(50),DistrictId INTEGER,AgencyId INTEGER,AgencyName VARCHAR(255),AgencyPhoneNumber VARCHAR(20),IsRealEstateAgnecy VARCHAR(6),IsLicensedPropertyAgency VARCHAR(6), UNIQUE(ListingId) ON CONFLICT REPLACE)")        
        
def create_table_schools(dbPath):

    conn = sqlite3.connect(dbPath)
    with conn:
        cur = conn.cursor()
        cur.execute("DROP TABLE IF EXISTS schools")
        cur.execute("CREATE TABLE schools (id INTEGER, name VARCHAR(255), decile INTEGER)")


def insert_residential_json(residential_json_pages, dbPath):

    property_tuple_all = []
    num_records = 0
    
    #for x in residential_json_pages:  #[:1]:    
    for i in range(0,len(residential_json_pages)):
    
        x = residential_json_pages[i]
        print 'starting page ' + str(i)
        #if i == 1:
        #print 'x on following line'
        #print type(x)
        #print x[u'Page']
        #print x[u'PageSize']
    
        for y in x[u'List']:  #[:20]:    
            ListingId = y.get('ListingId') if y.get('ListingId') else -99
            Title = y.get('Title') if y.get('Title') else ''
            Category = y.get('Category') if y.get('Category') else ''
            StartPrice = y.get('StartPrice') if y.get('StartPrice') else -99
            
            if (y.get('StartDate')):
                StartDate = re.sub(r'\/Date\(([0-9]*)\)\/',r'd\1',y.get('StartDate'))
                #StartDate = datetime.datetime.fromtimestamp(int(StartDate)/1000.0)
            else:
                StartDate = -99
            
            if (y.get('EndDate')):
                EndDate = re.sub(r'\/Date\(([0-9]*)\)\/',r'd\1',y.get('EndDate'))
                #EndDate = datetime.datetime.fromtimestamp(int(EndDate)/1000.0)
            else:
                EndDate = -99
            
            IsFeatured = y.get('IsFeatured') if y.get('IsFeatured') else -99
            HasGallery = y.get('HasGallery') if y.get('HasGallery') else -99
            IsBold = y.get('IsBold') if y.get('IsBold') else -99
            IsHighlighted = y.get('IsHighlighted') if y.get('IsHighlighted') else -99
            AsAt = y.get('AsAt') if y.get('AsAt') else -99
            CategoryPath = y.get('CategoryPath') if y.get('CategoryPath') else ''
            PictureHref = y.get('PictureHref') if y.get('PictureHref') else ''
            RegionId = y.get('RegionId') if y.get('RegionId') else -99
            Region = y.get('Region') if y.get('Region') else ''
            SuburbId = y.get('SuburbId') if y.get('SuburbId') else -99
            Suburb = y.get('Suburb') if y.get('Suburb') else ''
            ReserveState = y.get('ReserveState') if y.get('ReserveState') else -99
            IsClassified = y.get('IsClassified') if y.get('IsClassified') else ''
            Latitude = y.get('GeographicLocation').get('Latitude') if (y.get('GeographicLocation') and y.get('GeographicLocation').get('Latitude')) else -99
            Longitude = y.get('GeographicLocation').get('Longitude') if (y.get('GeographicLocation') and y.get('GeographicLocation').get('Longitude')) else -99
            Northing = y.get('GeographicLocation').get('Northing') if (y.get('GeographicLocation') and y.get('GeographicLocation').get('Northing')) else -99
            Easting = y.get('GeographicLocation').get('Easting') if (y.get('GeographicLocation') and y.get('GeographicLocation').get('Easting')) else -99
            Accuracy = y.get('GeographicLocation').get('Accuracy') if (y.get('GeographicLocation') and y.get('GeographicLocation').get('Accuracy')) else -99
            PriceDisplay = y.get('PriceDisplay') if y.get('PriceDisplay') else ''
            
            if ('$' in y.get('PriceDisplay')):
                StartPrice = re.sub(r'.*\$(.*)',r'\1',y.get('PriceDisplay'))
                StartPrice = re.sub(r',',r'',StartPrice) # re-use StartPrice field as it seems unused

            Address = y.get('Address') if y.get('Address') else ''
            District = y.get('District') if y.get('District') else ''
            AgencyReference = y.get('AgencyReference') if y.get('AgencyReference') else ''
            LandArea = y.get('LandArea') if y.get('LandArea') else -99
            Bathrooms = y.get('Bathrooms') if y.get('Bathrooms') else -99
            Bedrooms = y.get('Bedrooms') if y.get('Bedrooms') else -99
            ListingGroup = y.get('ListingGroup') if y.get('ListingGroup') else ''
            Parking = y.get('Parking') if y.get('Parking') else ''
            PropertyType = y.get('PropertyType') if y.get('PropertyType') else ''
            PropertyId = y.get('PropertyId') if y.get('PropertyId') else ''
            DistrictId = y.get('DistrictId') if y.get('DistrictId') else -99
                        
            AgencyId                    = y.get('Agency').get('Id')                         if (y.get('Agency') and y.get('Agency').get('Id')) else -99
            AgencyName                  = y.get('Agency').get('Name')                       if (y.get('Agency') and y.get('Agency').get('Name')) else ''
            AgencyPhoneNumber           = y.get('Agency').get('PhoneNumber')                if (y.get('Agency') and y.get('Agency').get('PhoneNumber')) else ''
            IsRealEstateAgency          = y.get('Agency').get('IsRealEstateAgency')         if (y.get('Agency') and y.get('Agency').get('IsRealEstateAgency')) else ''
            IsLicensedPropertyAgency    = y.get('Agency').get('IsLicensedPropertyAgency')   if (y.get('Agency') and y.get('Agency').get('IsLicensedPropertyAgency')) else ''

            property_tuple = (ListingId,Title,Category,StartPrice,StartDate,EndDate,IsFeatured,HasGallery,IsBold,IsHighlighted,AsAt,CategoryPath,PictureHref,RegionId,Region,SuburbId,Suburb,ReserveState,IsClassified,Latitude,Longitude,Northing,Easting,Accuracy,PriceDisplay,Address,District,AgencyReference,LandArea,Bathrooms,Bedrooms,ListingGroup,Parking,PropertyType,PropertyId,DistrictId,AgencyId,AgencyName,AgencyPhoneNumber,IsRealEstateAgency,IsLicensedPropertyAgency)
            num_records += 1
            property_tuple_all.append(property_tuple)

        print 'finished page'

    print 'number of records by counter ' + str(num_records)
    print 'length of property_tuple     ' + str(len(property_tuple_all))
    print 'starting database entry'
    
    conn = sqlite3.connect(dbPath) #conn = sqlite3.connect(":memory:")
    with conn:
        cur = conn.cursor()
        #cur.execute("INSERT INTO Cars VALUES(1,'Audi',52642)")
        cur.executemany("INSERT INTO residential_listings VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", property_tuple_all)
    
    print 'finished residential database entry'




def insert_rental_json(rental_json_pages, dbPath):

    property_tuple_all = []
    num_records = 0
    
    #for x in rental_json_pages:  #[:1]:    
    for i in range(0,len(rental_json_pages)):
    
        x = rental_json_pages[i]
        print 'starting page ' + str(i)
        #if i == 1:
        #print 'x on following line'
        #print type(x)
        #print x[u'Page']
        #print x[u'PageSize']
    
        for y in x[u'List']:  #[:20]:    
            ListingId = y.get('ListingId') if y.get('ListingId') else -99
            Title = y.get('Title') if y.get('Title') else ''
            Category = y.get('Category') if y.get('Category') else ''
            RentPerWeek = y.get('RentPerWeek') if y.get('RentPerWeek') else -99
            SmokersOkay = y.get('SmokersOkay') if y.get('SmokersOkay') else ''
            
            if (y.get('StartDate')):
                StartDate = re.sub(r'\/Date\(([0-9]*)\)\/',r'd\1',y.get('StartDate'))
                #StartDate = datetime.datetime.fromtimestamp(int(StartDate)/1000.0)
            else:
                StartDate = -99
            
            if (y.get('EndDate')):
                EndDate = re.sub(r'\/Date\(([0-9]*)\)\/',r'd\1',y.get('EndDate'))
                #EndDate = datetime.datetime.fromtimestamp(int(EndDate)/1000.0)
            else:
                EndDate = -99
            
            IsFeatured = y.get('IsFeatured') if y.get('IsFeatured') else -99
            HasGallery = y.get('HasGallery') if y.get('HasGallery') else -99
            IsBold = y.get('IsBold') if y.get('IsBold') else -99
            IsHighlighted = y.get('IsHighlighted') if y.get('IsHighlighted') else -99
            AsAt = y.get('AsAt') if y.get('AsAt') else -99
            CategoryPath = y.get('CategoryPath') if y.get('CategoryPath') else ''
            PictureHref = y.get('PictureHref') if y.get('PictureHref') else ''
            RegionId = y.get('RegionId') if y.get('RegionId') else -99
            Region = y.get('Region') if y.get('Region') else ''
            SuburbId = y.get('SuburbId') if y.get('SuburbId') else -99
            Suburb = y.get('Suburb') if y.get('Suburb') else ''
            ReserveState = y.get('ReserveState') if y.get('ReserveState') else -99
            IsClassified = y.get('IsClassified') if y.get('IsClassified') else ''
            Latitude = y.get('GeographicLocation').get('Latitude') if (y.get('GeographicLocation') and y.get('GeographicLocation').get('Latitude')) else -99
            Longitude = y.get('GeographicLocation').get('Longitude') if (y.get('GeographicLocation') and y.get('GeographicLocation').get('Longitude')) else -99
            Northing = y.get('GeographicLocation').get('Northing') if (y.get('GeographicLocation') and y.get('GeographicLocation').get('Northing')) else -99
            Easting = y.get('GeographicLocation').get('Easting') if (y.get('GeographicLocation') and y.get('GeographicLocation').get('Easting')) else -99
            Accuracy = y.get('GeographicLocation').get('Accuracy') if (y.get('GeographicLocation') and y.get('GeographicLocation').get('Accuracy')) else -99
            PriceDisplay = y.get('PriceDisplay') if y.get('PriceDisplay') else ''

            Address = y.get('Address') if y.get('Address') else ''
            District = y.get('District') if y.get('District') else ''
            AgencyReference = y.get('AgencyReference') if y.get('AgencyReference') else ''
            LandArea = y.get('LandArea') if y.get('LandArea') else -99
            Bathrooms = y.get('Bathrooms') if y.get('Bathrooms') else -99
            Bedrooms = y.get('Bedrooms') if y.get('Bedrooms') else -99
            ListingGroup = y.get('ListingGroup') if y.get('ListingGroup') else ''
            Parking = y.get('Parking') if y.get('Parking') else ''
            PropertyType = y.get('PropertyType') if y.get('PropertyType') else ''
            PropertyId = y.get('PropertyId') if y.get('PropertyId') else ''
            DistrictId = y.get('DistrictId') if y.get('DistrictId') else -99
                        
            AgencyId                    = y.get('Agency').get('Id')                         if (y.get('Agency') and y.get('Agency').get('Id')) else -99
            AgencyName                  = y.get('Agency').get('Name')                       if (y.get('Agency') and y.get('Agency').get('Name')) else ''
            AgencyPhoneNumber           = y.get('Agency').get('PhoneNumber')                if (y.get('Agency') and y.get('Agency').get('PhoneNumber')) else ''
            IsRealEstateAgency          = y.get('Agency').get('IsRealEstateAgency')         if (y.get('Agency') and y.get('Agency').get('IsRealEstateAgency')) else ''
            IsLicensedPropertyAgency    = y.get('Agency').get('IsLicensedPropertyAgency')   if (y.get('Agency') and y.get('Agency').get('IsLicensedPropertyAgency')) else ''

            property_tuple = (ListingId,Title,Category,RentPerWeek,SmokersOkay,StartDate,EndDate,IsFeatured,HasGallery,IsBold,IsHighlighted,AsAt,CategoryPath,PictureHref,RegionId,Region,SuburbId,Suburb,ReserveState,IsClassified,Latitude,Longitude,Northing,Easting,Accuracy,PriceDisplay,Address,District,AgencyReference,LandArea,Bathrooms,Bedrooms,ListingGroup,Parking,PropertyType,PropertyId,DistrictId,AgencyId,AgencyName,AgencyPhoneNumber,IsRealEstateAgency,IsLicensedPropertyAgency)
            num_records += 1
            property_tuple_all.append(property_tuple)

        print 'finished page'

    print 'number of records by counter ' + str(num_records)
    print 'length of property_tuple     ' + str(len(property_tuple_all))
    print 'starting database entry'
    
    conn = sqlite3.connect(dbPath) #conn = sqlite3.connect(":memory:")
    with conn:
        cur = conn.cursor()
        #cur.execute("INSERT INTO Cars VALUES(1,'Audi',52642)")
        cur.executemany("INSERT INTO rental_listings VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", property_tuple_all)
    
    print 'finished rental database entry'
    
    
    