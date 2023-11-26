

'''
	python3 insurance.py shows/essential_nutrients/land/build/status_1.py
'''

import apoplast.shows.essential_nutrients.land.build as build_essential_nutrients_land
import json

def check_1 ():
	land = build_essential_nutrients_land.eloquently ()

	print (json.dumps (land, indent = 4))

	return;
	
	
	
checks = {
	"check 1": check_1
}