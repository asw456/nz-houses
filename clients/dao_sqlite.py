import json
import sqlite3
import sys
import re
import dateutil.parser
import datetime

def create_table_residential_listings(dbPath):

    conn = sqlite3.connect(dbPath)
    with conn:
        cur = conn.cursor()
        cur.execute("DROP TABLE IF EXISTS residential_listings")
        cur.execute("CREATE TABLE residential_listings (ListingId INTEGER,Title VARCHAR(100),Category VARCHAR(50),StartPrice REAL,StartDate INTEGER,EndDate INTEGER,IsFeatured INTEGER,HasGallery INTEGER,IsBold INTEGER,IsHighlighted INTEGER,AsAt INTEGER,CategoryPath VARCHAR(100),PictureHref VARCHAR(100),RegionId INTEGER,Region VARCHAR(50),SuburbId INTEGER,Suburb VARCHAR(100),ReserveState INTEGER,IsClassified INTEGER,Latitude REAL,Longitude REAL,Northing INTEGER,Easting INTEGER,Accuracy INTEGER,PriceDisplay VARCHAR(100),Address VARCHAR(100),District VARCHAR(100),AgencyReference VARCHAR(10),LandArea INTEGER,Bathrooms INTEGER,Bedrooms INTEGER,ListingGroup VARCHAR(100),Parking VARCHAR(100),PropertyType VARCHAR(50),PropertyId VARCHAR(50),DistrictId INTEGER,AgencyId INTEGER,AgencyName VARCHAR(255),AgencyPhoneNumber VARCHAR(20),AgencyWebsite VARCHAR(100),IsRealEstateAgnecy INTEGER,IsLicensedPropertyAgency INTEGER)")
    
def create_table_schools(dbPath):

    conn = sqlite3.connect(dbPath)
    with conn:
        cur = conn.cursor()
        cur.execute("DROP TABLE IF EXISTS schools")
        cur.execute("CREATE TABLE schools (id INTEGER, name VARCHAR(255), decile INTEGER)")
    
    


def insert_search_results(propertyPages, dbPath):

    columns = ['ListingId','Title','Category','StartPrice','StartDate','EndDate','IsFeatured','HasGallery','IsBold','IsHighlighted','AsAt','CategoryPath','PictureHref','RegionId','Region','SuburbId','Suburb','ReserveState','IsClassified','Latitude','Longitude','Northing','Easting','Accuracy','PriceDisplay','Address','District','AgencyReference','LandArea','Bathrooms','Bedrooms','ListingGroup','Parking','PropertyType','PropertyId','DistrictId','AgencyId','AgencyName','AgencyPhoneNumber','AgencyWebsite','IsRealEstateAgnecy','IsLicensedPropertyAgency']

    property_tuple_all = []
    
    for x in propertyPages:#[:1]:    
        print 'starting page'
        
        for y in x['List']:#[:20]:    
            ListingId = y.get('ListingId') if y.get('ListingId') else -99
            Title = y.get('Title') if y.get('Title') else ''
            Category = y.get('Category') if y.get('Category') else ''
            StartPrice = y.get('StartPrice') if y.get('StartPrice') else -99
            
            if (y.get('StartDate')):
                sdate = re.sub(r'\/Date\(([0-9]*)\)\/',r'd\1',y.get('StartDate'))
                #sdate = datetime.datetime.fromtimestamp(int(sdate)/1000.0)
            else:
                sdate = -99
            StartDate = sdate 
            #StartDate = y.get('StartDate') if y.get('StartDate') else ''
            
            if (y.get('EndDate')):
                edate = re.sub(r'\/Date\(([0-9]*)\)\/',r'd\1',y.get('EndDate'))
                #edate = datetime.datetime.fromtimestamp(int(edate)/1000.0)
            else:
                edate = -99
            EndDate = edate
            #EndDate = y.get('EndDate') if y.get('EndDate') else ''

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
            IsClassified = y.get('IsClassified') if y.get('IsClassified') else -99
            Latitude = y.get('GeographicLocation').get('Latitude') if y.get('GeographicLocation').get('Latitude') else -99
            Longitude = y.get('GeographicLocation').get('Longitude') if y.get('GeographicLocation').get('Longitude') else -99
            Northing = y.get('GeographicLocation').get('Northing') if y.get('GeographicLocation').get('Northing') else -99
            Easting = y.get('GeographicLocation').get('Easting') if y.get('GeographicLocation').get('Easting') else -99
            Accuracy = y.get('GeographicLocation').get('Accuracy') if y.get('GeographicLocation').get('Accuracy') else -99
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
            AgencyId = y.get('AgencyId') if y.get('AgencyId') else -99
            AgencyName = y.get('AgencyName') if y.get('AgencyName') else ''
            AgencyPhoneNumber = y.get('AgencyPhoneNumber') if y.get('AgencyPhoneNumber') else ''
            AgencyWebsite = y.get('AgencyWebsite') if y.get('AgencyWebsite') else ''
            IsRealEstateAgnecy = y.get('IsRealEstateAgnecy') if y.get('IsRealEstateAgnecy') else -99
            IsLicensedPropertyAgency = y.get('IsLicensedPropertyAgency') if y.get('IsLicensedPropertyAgency') else -99

            property_tuple = (ListingId,Title,Category,StartPrice,StartDate,EndDate,IsFeatured,HasGallery,IsBold,IsHighlighted,AsAt,CategoryPath,PictureHref,RegionId,Region,SuburbId,Suburb,ReserveState,IsClassified,Latitude,Longitude,Northing,Easting,Accuracy,PriceDisplay,Address,District,AgencyReference,LandArea,Bathrooms,Bedrooms,ListingGroup,Parking,PropertyType,PropertyId,DistrictId,AgencyId,AgencyName,AgencyPhoneNumber,AgencyWebsite,IsRealEstateAgnecy,IsLicensedPropertyAgency)
            property_tuple_all.append(property_tuple)

        print 'finished page'

    print 'starting database'
    #conn = sqlite3.connect(":memory:")
    conn = sqlite3.connect(dbPath)
    with conn:
        cur = conn.cursor()
        #cur.execute("DROP TABLE IF EXISTS residential_listings")
        #cur.execute("CREATE TABLE residential_listings (ListingId INTEGER,Title VARCHAR(100),Category VARCHAR(50),StartPrice REAL,StartDate INTEGER,EndDate INTEGER,IsFeatured INTEGER,HasGallery INTEGER,IsBold INTEGER,IsHighlighted INTEGER,AsAt INTEGER,CategoryPath VARCHAR(100),PictureHref VARCHAR(100),RegionId INTEGER,Region VARCHAR(50),SuburbId INTEGER,Suburb VARCHAR(100),ReserveState INTEGER,IsClassified INTEGER,Latitude REAL,Longitude REAL,Northing INTEGER,Easting INTEGER,Accuracy INTEGER,PriceDisplay VARCHAR(100),Address VARCHAR(100),District VARCHAR(100),AgencyReference VARCHAR(10),LandArea INTEGER,Bathrooms INTEGER,Bedrooms INTEGER,ListingGroup VARCHAR(100),Parking VARCHAR(100),PropertyType VARCHAR(50),PropertyId VARCHAR(50),DistrictId INTEGER,AgencyId INTEGER,AgencyName VARCHAR(255),AgencyPhoneNumber VARCHAR(20),AgencyWebsite VARCHAR(100),IsRealEstateAgnecy INTEGER,IsLicensedPropertyAgency INTEGER)")
        #cur.execute("INSERT INTO Cars VALUES(1,'Audi',52642)")

        cur.executemany("INSERT INTO residential_listings VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", property_tuple_all)

'''
def insert_listing_result():

    propertyPages = json.load(open('../json/propertyPages.json'))
    columns = ['ListingId','Title','Category','StartPrice','StartDate','EndDate','IsFeatured','HasGallery','IsBold','IsHighlighted','AsAt','CategoryPath','PictureHref','RegionId','Region','SuburbId','Suburb','ReserveState','IsClassified','Latitude','Longitude','Northing','Easting','Accuracy','PriceDisplay','Address','District','AgencyReference','LandArea','Bathrooms','Bedrooms','ListingGroup','Parking','PropertyType','PropertyId','DistrictId','AgencyId','AgencyName','AgencyPhoneNumber','AgencyWebsite','IsRealEstateAgnecy','IsLicensedPropertyAgency']

    property_tuple_all = []

    for x in propertyPages[:1]:
        print 'starting page'

        for y in x['List'][:1]:
            ListingId = y.get('ListingId') if y.get('ListingId') else -99
            Title = y.get('Title').encode('ascii') if y.get('Title') else ''
            Category = y.get('Category').encode('ascii') if y.get('Category') else ''
            StartPrice = y.get('StartPrice') if y.get('StartPrice') else -99
            StartDate = y.get('StartDate').encode('ascii') if y.get('StartDate') else ''
            EndDate = y.get('EndDate').encode('ascii') if y.get('EndDate') else ''
            ListingLength
            HasGallery = y.get('HasGallery') if y.get('HasGallery') else -99
            AsAt = y.get('AsAt') if y.get('AsAt').encode('ascii') else -99
            CategoryPath = y.get('CategoryPath').encode('ascii') if y.get('CategoryPath') else ''
            RegionId = y.get('RegionId') if y.get('RegionId') else -99
            Region = y.get('Region').encode('ascii') if y.get('Region') else ''
            SuburbId = y.get('SuburbId') if y.get('SuburbId') else -99
            Suburb = y.get('Suburb').encode('ascii') if y.get('Suburb') else ''
            ViewCount = 
            NoteDate = 
            ReserveState = y.get('ReserveState') if y.get('ReserveState') else -99
            
            Bedrooms 




            IsClassified = y.get('IsClassified') if y.get('IsClassified') else -99
            OpenHomes = []
            PriceDisplay = y.get('PriceDisplay').encode('ascii') if y.get('PriceDisplay') else ''
            PriceDisplayParsed = re.    \$([0-9,][0-9]*)\   $1 # *** added ***
            
            MemberId
            Nickname
            DateAddressVerified
            DateJoined
            UniqueNegative
            UniquePositive
            FeedbackCount
            IsAddressVerified
            IsAuthenticated
            
            Body
            
            Latitude = y.get('GeographicLocation').get('Latitude') if y.get('GeographicLocation').get('Latitude') else -99
            Longitude = y.get('GeographicLocation').get('Longitude') if y.get('GeographicLocation').get('Longitude') else -99
            Northing = y.get('GeographicLocation').get('Northing') if y.get('GeographicLocation').get('Northing') else -99
            Easting = y.get('GeographicLocation').get('Easting') if y.get('GeographicLocation').get('Easting') else -99
            Accuracy = y.get('GeographicLocation').get('Accuracy') if y.get('GeographicLocation').get('Accuracy') else -99
            
            AgencyId = y.get('Agency').get('AgencyId') if y.get('AgencyId') else -99
            AgencyName = y.get('Agency').get('AgencyName').encode('ascii') if y.get('AgencyName') else ''
            AgencyPhoneNumber = y.get('Agency').get('AgencyPhoneNumber').encode('ascii') if y.get('AgencyPhoneNumber') else ''
            AgencyWebsite = y.get('Agency').get('AgencyWebsite').encode('ascii') if y.get('AgencyWebsite') else ''
            NumberOfAgents
            Agent1FullName
            Agent1Mobile
            Agent1Office
            Agent2FullName
            Agent2Mobile
            Agent2Office
            IsRealEstateAgnecy = y.get('IsRealEstateAgnecy') if y.get('IsRealEstateAgnecy') else -99
            IsLicensedPropertyAgency = y.get('IsLicensedPropertyAgency') if y.get('IsLicensedPropertyAgency') else -99

            property_tuple = (ListingId,Title,Category,StartPrice,StartDate,EndDate,IsFeatured,HasGallery,IsBold,IsHighlighted,AsAt,CategoryPath,PictureHref,RegionId,Region,SuburbId,Suburb,ReserveState,IsClassified,Latitude,Longitude,Northing,Easting,Accuracy,PriceDisplay,Address,District,AgencyReference,LandArea,Bathrooms,Bedrooms,ListingGroup,Parking,PropertyType,PropertyId,DistrictId,AgencyId,AgencyName,AgencyPhoneNumber,AgencyWebsite,IsRealEstateAgnecy,IsLicensedPropertyAgency)

            property_tuple_all.append(property_tuple)
        
        print 'finished page'


    print property_tuple
    print 'starting database'
    conn = sqlite3.connect(":memory:")
    with conn:
        cur = conn.cursor()
        cur.execute("DROP TABLE IF EXISTS residential_listings")
        cur.execute("CREATE TABLE residential_listings (ListingId INTEGER,Title VARCHAR(100),Category VARCHAR(50),StartPrice REAL,StartDate INTEGER,EndDate INTEGER,IsFeatured INTEGER,HasGallery INTEGER,IsBold INTEGER,IsHighlighted INTEGER,AsAt INTEGER,CategoryPath VARCHAR(100),PictureHref VARCHAR(100),RegionId INTEGER,Region VARCHAR(50),SuburbId INTEGER,Suburb VARCHAR(100),ReserveState INTEGER,IsClassified INTEGER,Latitude REAL,Longitude REAL,Northing INTEGER,Easting INTEGER,Accuracy INTEGER,PriceDisplay VARCHAR(100),Address VARCHAR(100),District VARCHAR(100),AgencyReference VARCHAR(10),LandArea INTEGER,Bathrooms INTEGER,Bedrooms INTEGER,ListingGroup VARCHAR(100),Parking VARCHAR(100),PropertyType VARCHAR(50),PropertyId VARCHAR(50),DistrictId INTEGER,AgencyId INTEGER,AgencyName VARCHAR(255),AgencyPhoneNumber VARCHAR(20),AgencyWebsite VARCHAR(50),IsRealEstateAgnecy INTEGER,IsLicensedPropertyAgency INTEGER)")
        #cur.execute("INSERT INTO Cars VALUES(1,'Audi',52642)")

        cur.executemany("INSERT INTO residential_listings VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", property_tuple_all)


'''



if __name__ == '__main__':
    insert_search_results()

