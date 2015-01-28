# Script to take random unique variables from mapped files
# RUN:
# python take_unique.py ../data/dbGaP.datJuly1_2013.1_cat_HealthcareEncounter  > ../data/HealcareEncounter_unique_random500

import os,sys
import random

def main():

	Dict = {}
	f1=open(sys.argv[1],'r')
	
	for line in f1.readlines():
		line1 = line.split(':::')

		if not Dict.has_key(line1[5]):
			Dict[line1[5].strip()] = [line1]
		else:
			Dict[line1[5].strip()].append(line1)
	f1.close()


	# Random select key from Dict
	
	count = 0
	List1 = []
	while count < 500:
		key = random.choice(Dict.keys())
		if not key in List1:
			List1.append(key) 
			count = count + 1

	#print List1

	# Print N random keys from Dict

	for item in List1:
		print ':::'.join(Dict[item][0]).strip()

if __name__=="__main__":
	main()

