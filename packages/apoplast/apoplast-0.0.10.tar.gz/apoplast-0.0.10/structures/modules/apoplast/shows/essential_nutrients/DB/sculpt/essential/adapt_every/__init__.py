

'''
	caution, not checked.

		import apoplast.shows.essential_nutrients.DB.access as access
		import apoplast.shows.essential_nutrients.DB.sculpt.essential.adapt_every as adapt_every_essential_nutrient
	
		def for_each (essential):
			return essential

		adapt_every_essential_nutrient.eloquently (
			essentials_DB = access.DB (),
			for_each = for_each
		)
'''

import apoplast.shows.essential_nutrients.DB.access as access

import apoplast.shows.essential_nutrients.DB.scan.seek_next_region as seek_next_region
import apoplast.shows.essential_nutrients.DB.scan.seek as seek_nutrient
import apoplast.shows.essential_nutrients.DB.scan.list as essentials_list

from tinydb import TinyDB, Query

import json

def for_each ():
	return;

def eloquently (
	essentials_DB = access.DB (),
	for_each = for_each
):
	
	import apoplast.shows.essential_nutrients.DB.access as access
	essentials = essentials_list.retrieve (
		essentials_DB = access.DB ()
	)

	for essential in essentials:
		essential = for_each (essential)
		region = essential ["region"]

		updated = essentials_DB.update (
			essential, 
			Query ().region == region
		)
		
		#print ("updated:", updated)
	

		