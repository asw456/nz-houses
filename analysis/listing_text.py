
import pandas.io.sql
import sqlite3
import nltk


def read_listing_table1(dbFilePath):

	conn = sqlite3.connect(dbFilePath)
	with conn:
		cur = conn.cursor()
		cur.execute('SELECT * FROM residential_individual_listings')
		rows = cur.fetchall()
		descriptions = []
		for row in rows:
			descriptions.append(row[1])
		return descriptions
		
	#with sqlite3.connect(dbFilePath, detect_types=sqlite3.PARSE_DECLTYPES) as conn:
	#	return pandas.io.sql.frame_query('select * from residential_individual_listings limit 100', conn)

def remove_stop_words(descriptions):
	
	# ================= nltk ========================
	
	
	
	
	# ================= custom regexp ========================
	
	re.sub(r'.*\$(.*) ',r'\1',string)
    re.sub(r',',r'',string)



if __name__ == '__main__':

	dbFilePath = '/Users/james/development/resources/nz-houses/db/prod1_listings.db'
	
	#df_1 = read_listing_table(dbFilePath)
	#df_1 = df_sqlite[df_sqlite['ListingId'] > 641386568]
	#print df_1.describe()
	#a = df_1[-1:]['Body']
	#print a.to_string()

	descriptions = read_listing_table1(dbFilePath)
	for i in range(0,3):
		print descriptions[i]