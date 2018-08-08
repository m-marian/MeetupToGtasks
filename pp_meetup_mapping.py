import csv

#read mapping of csv file as dictionary
def read_mapping(inpath):
	with open(inpath, mode = 'r') as infile:
		inreader = csv.reader(infile)
		mapping = {rows[0]:rows[1] for rows in inreader}
	return mapping
