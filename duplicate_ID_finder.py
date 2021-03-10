#!/usr/bin/env python3

import sys,os
from random import seed
from random import randint

bcg_path="/home/webstejo/bin/UBCG/bcg/"

def parser(dir):
	bcg_ids=[]
	for file in os.listdir(dir):
		with open(os.path.join("bcg",file)) as fh:
			filedata=fh.read()
			bcg_ids.append(filedata[9:22])
	return(set([x for x in bcg_ids if bcg_ids.count(x) > 1]))

def find_and_replace(list):
	for file in os.listdir(bcg_path):
		for ID in list:
			new_ID=randint(1614740000000,1614750000000)
			with open(os.path.join(bcg_path,file), 'r') as fh:
				filedata=fh.read()
				if ID in filedata:
					print("duplicate ID in file {} with ID {}. Replaced with ID {}".format(file,ID,new_ID))
					filedata=filedata.replace(str(ID),str(new_ID))
					with open(os.path.join(bcg_path,file), 'w') as fh:
						fh.write(filedata)

find_and_replace(parser(bcg_path))
