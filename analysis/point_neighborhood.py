
import nz_houses_dao as dao
import pandas
import math


def distance_on_unit_sphere(lat1, long1, lat2, long2):

    # Convert latitude and longitude to 
    # spherical coordinates in radians.
    degrees_to_radians = math.pi/180.0
        
    # phi = 90 - latitude
    phi1 = (90.0 - lat1)*degrees_to_radians
    phi2 = (90.0 - lat2)*degrees_to_radians
        
    # theta = longitude
    theta1 = long1*degrees_to_radians
    theta2 = long2*degrees_to_radians
        
    # Compute spherical distance from spherical coordinates.
        
    # For two locations in spherical coordinates 
    # (1, theta, phi) and (1, theta, phi)
    # cosine( arc length ) = 
    #    sin phi sin phi' cos(theta-theta') + cos phi cos phi'
    # distance = rho * arc length
    
    cos = (math.sin(phi1)*math.sin(phi2)*math.cos(theta1 - theta2) + 
           math.cos(phi1)*math.cos(phi2))
    arc = math.acos( cos )

    # Remember to multiply arc by the radius of the earth 
    # in your favorite set of units to get length.
    # meters = *6373000 
    return arc*6373000 


if __name__ == '__main__':

	dbFilePath 				= '/Users/james/development/code_personal/nz-houses/db/prod1.db'
	
	query_result = dao.read_residential_table(dbFilePath)
	
	#query_result = dao.read_residential_table_pandas(dbFilePath)
	#print query_result.head()
	#print query_result.describe()
	#df_1 = df_sqlite[df_sqlite['ListingId'] > 641386568]
	#a = df_1[-1:]['Body']
	#print a.to_string()

	home_lat  = -43.510946
	home_long = 172.546268
	
	results = []
	for row in query_result:
		if distance_on_unit_sphere(home_lat,home_long,row[19],row[20]) < 2001 and row[3] != -99:
			results.append(row)
		
	for row in results:
		print 'listingid =\t' + str(row[0]) + '\t' + str(row[3])