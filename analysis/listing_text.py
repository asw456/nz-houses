
import cPickle
import nz_houses_dao as dao
from nltk.corpus import stopwords
import re
import gzip

class Residential:
	
	distionary
	
	def 
	
	def __init__():
		pass
		
	

def generate_word_lists(descriptions):
	descriptions_features = {}
	
	i = 0
	for listingId in descriptions.keys():
		
		a = descriptions[listingId].lower()
		a = re.sub(r'\d+',r'',a)
		a = re.sub(r'sqm',r'',a)
		a = re.sub(r'm2',r'',a)
		a_words = re.findall(r'\w+',a)  #,flags = re.UNICODE | re.LOCALE)
		a_words = filter(lambda x: x not in stopwords.words('english'), a_words)
		
		descriptions_features[listingId] = a_words
		if i % 50 == 0:
			print i
		i += 1
	
	return descriptions_features


def print_words(a_words):
	b = ''
	for word in a_words:
		b = b + str(word) + ' '
	print b	

if __name__ == '__main__':

	dbFilePath 				= '/Users/james/development/code_personal/nz-houses/db/prod1.db'
	
	#df_1 = read_listing_table(dbFilePath)
	#df_1 = df_sqlite[df_sqlite['ListingId'] > 641386568]
	#print df_1.describe()
	#a = df_1[-1:]['Body']
	#print a.to_string()


	query_result = dao.read_listing_table(dbFilePath)

	pickle_flag = 1
	if pickle_flag == 0:
		descriptions = {}
		for row in query_result:
			descriptions[row[0]] = row[1]
		descriptions_features 	= generate_word_lists(descriptions)
		with gzip.open('/Users/james/development/code_personal/nz-houses/db/descriptions_features.pkl.gz', 'wb') as f:
			cPickle.dump(descriptions_features, f, protocol=2)
	if pickle_flag == 1:
		with gzip.open('/Users/james/development/code_personal/nz-houses/db/descriptions_features.pkl.gz', 'rb') as f:
			descriptions_features = cPickle.load(f)
	
	
	i = 0
	for listingId in reversed(descriptions_features.keys()):
		print listingId
		print_words(descriptions_features[listingId])
		print '-----------'
		i += 1
		if i == 10:
			break

	
	
	
	
	
	
	