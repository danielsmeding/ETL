import csv
from datetime import datetime

# Input path is folder in current working directory creating relative paths to subfolders
import os
cwd = os.getcwd()
input_path = os.path.join(cwd, 'input')
log_path = os.path.join(cwd, 'logs')

# Setting up logger for log/data_loader.log
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(name)s:%(message)s')

file_handler = logging.FileHandler(os.path.join(log_path,'data_loader.log'))
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)

stream_handler = logging.StreamHandler()

logger.addHandler(file_handler)
logger.addHandler(stream_handler)


# Loading data out of replacable csv file. File will get a unique id (uid) added and copied into the 'indexed_workfile.csv file'
def pos_data_loader(filename):
	# Locating inport file relative to current working directory
	input_file = os.path.join(input_path, filename)
	output_file = os.path.join(input_path, 'indexed_workfile.csv')
	# retrieving size and last modification time
	file_size = os.stat(input_file).st_size
	mod_time = os.stat(input_file).st_mtime

	# opening file and adding adding a unique key column 'uid' in workfile.csv
	import uuid
	with open(input_file,'r') as csvinput, open(output_file, 'w') as csvoutput:
	    reader = csv.reader(csvinput)
	    # writing indexed_workfile.csv with header and uid 
	    writer = csv.writer(csvoutput, lineterminator='\n')
	    i = 1
	    for row in csv.reader(csvinput):
	    	if i == 1:
	    		writer.writerow(row+['uid'])
	    	else:
	        	writer.writerow(row+[uuid.uuid4()])
	    	i = i + 1
	# Reading indexed_workfile with dict Generator
	csv_dict = csv.DictReader(open(output_file,'r'))
	
	# console out message on file size and modification date
	logger.info('Imported {} Size: {} MB last modified date: {}.'.format(filename, (file_size/1048576), datetime.fromtimestamp(mod_time)))
	# Returing dict generator
	return csv_dict

# Loading data out of legal_entity.csv 
def legal_entity(filename = 'legal_entity.csv'):
	# Locating inport file relative to current working directory
	legent_file = os.path.join(input_path, filename)
	with open(legent_file, 'r') as csvinput:
		legent_reader = csv.reader(csvinput)
		next(legent_reader, None)  # skip the headers
		legal_list = []
		for row in legent_reader:
			legal_list.append(row[0])
	return legal_list
