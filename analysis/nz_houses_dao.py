
import pandas.io.sql
import sqlite3


def read_residential_table(dbFilePath):
	
	conn = sqlite3.connect(dbFilePath)
	with conn:
		cur = conn.cursor()
		cur.execute('SELECT * FROM residential_listings')
		rows = cur.fetchall()
	return rows		

def read_residential_table_pandas(dbFilePath):
	
	with sqlite3.connect(dbFilePath, detect_types=sqlite3.PARSE_DECLTYPES) as conn:
		return pandas.io.sql.frame_query('select * from residential_listings', conn)


def read_listing_table(dbFilePath):
	
	conn = sqlite3.connect(dbFilePath)
	with conn:
		cur = conn.cursor()
		cur.execute('SELECT * FROM residential_individual_listings')
		rows = cur.fetchall()
	return rows		

def read_listing_table_pandas(dbFilePath):
	
	with sqlite3.connect(dbFilePath, detect_types=sqlite3.PARSE_DECLTYPES) as conn:
		return pandas.io.sql.frame_query('select * from residential_individual_listings', conn)
