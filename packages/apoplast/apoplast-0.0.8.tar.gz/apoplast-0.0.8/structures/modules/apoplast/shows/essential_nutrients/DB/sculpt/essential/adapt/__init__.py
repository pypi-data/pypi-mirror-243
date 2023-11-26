

'''
	caution, not checked.

		import apoplast.shows.essential_nutrients.DB.access as access
		import apoplast.shows.essential_nutrients.DB.sculpt.adapt as adapt_essential_nutrient
		adapt_essential_nutrient.eloquently (
			essentials_DB = access.DB (),
			essential = {
				"region": 1,
				"names": [ "protein" ],
				"accepts": [],
				"includes": []			
			}
		)
'''

import apoplast.shows.essential_nutrients.DB.access as access
import apoplast.shows.essential_nutrients.DB.scan.seek_next_region as seek_next_region
import apoplast.shows.essential_nutrients.DB.scan.seek as seek_nutrient

from tinydb import TinyDB, Query

import json

def eloquently (
	essentials_DB = access.DB (),
	essential = {}
):
	region = essential ["region"]
	
	revenue = essentials_DB.update (
		essential, 
		Query ().region == region
	)
	
	print (revenue)
	
	nutrient = seek_nutrient.presently (
		for_each = lambda essential : True if essential ["region"] == region else False
	)
	
	print ("adapted version =", json.dumps (nutrient, indent = 4))
		