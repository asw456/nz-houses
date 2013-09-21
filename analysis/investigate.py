
import pandas.io.sql as psql
import sqlite3



def read_db_table_to_dataframe(dbFilePath):

    with sqlite3.connect(dbFilePath, detect_types=sqlite3.PARSE_DECLTYPES) as conn:
        return psql.frame_query('select * from residential_listings limit 1000', conn)
    
    
    
    

if __name__ == '__main__':

	dbFilePath = '/Users/james/development/resources/nz-houses/db/test.db'
	
	df_sqlite = read_db_table_to_dataframe(dbFilePath)
	df_1 = df_sqlite[df_sqlite['ListingId'] > 641386568]
	
	
	print df_1.describe()
	print df_1


