import data_loader

# Input path is folder in current working directory creating relative paths to subfolders
import os
cwd = os.getcwd()
log_path = os.path.join(cwd, 'logs')

# Setting up logger for log/data_loader.log
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(name)s:%(message)s')

file_handler = logging.FileHandler(os.path.join(log_path,'cname_etl_module.log'))
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)

stream_handler = logging.StreamHandler()

logger.addHandler(file_handler)
logger.addHandler(stream_handler)

# Using data_loader model to load csv into dict generateor
dict_all = data_loader.pos_data_loader('posdata_test_small.csv')

# function creating a uid value pair dictionairy

def upsert_dict(key, value = 'uid'):
	# create sdict from linedict to iterate over (dictall is a generator creating linedicts)
	sdict = {}
	for line_dict in dict_all:
		sdict[line_dict[value]] = line_dict[key]
	# reversing key and value to create unique constraint on values
	udict = {}
	for k, v in sdict.iteritems():
		udict.setdefault(v,[]).append(k)
	return udict


# Creating a dictionairy with key: uid and value: customer name  by merging the line dictionairies	

customer_dict = upsert_dict('CustName')
print customer_dict


# from itertools import chain
# all = {}
# 	for k, v in chain(a.iteritems(), b.iteritems()):
# 	    all.setdefault(k, []).extend(v)


# for i in xrange(0,len(dict_cname)):
#  	print dict_cname['i']

# class Customer:
# 	def __init__(self, cname, clegelent, ccountry, ccity, czip):
# 		self.cname = cname
# 		self.cname = clegelent
# 		self.cname = ccountry
# 		self.cname = ccity
# 		self.cname = czip