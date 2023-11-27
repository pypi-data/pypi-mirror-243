

'''
	import apoplast.shows.essential_nutrients.grove.nurture as grove_nurture
	grove = grove_nurture.beautifully ()
'''

'''
	"grove": [{
		#
		#	The essential nutrient from the
		#	essential nutrient grove DB.
		#
		"essential": {
			"names": [ "vitamin b", "cobalamin" ],
			"includes": []
		},
		
		#
		#	The ingredient from either:
		#
		#		USDA:
		#			foodNutrients (flat list)
		#
		#		NIH:
		#			ingredientRows (tree)
		#				nestedRows
		#					nestedRows
		#
		"natures": [{
			"identity": {
				"name": "",
				"UPC": "",
				"DSLD ID": "",
				"FDC ID": ""
			}
		}],
		
		"unites": [{
			"essential": {},
			"ingredients": [],			
			"unites": []
		}]
	}]
'''

import apoplast.shows.essential_nutrients.DB.scan.list as essentials_list

import json
import copy


def nutrient ():
	return {
		"essential": {},
		"measures": {},
		"natures": [],
		"unites": []
	}

def beautifully (
	essentials_DB_list = None,
	records = 0
):
	this_grove = []

	if (essentials_DB_list == None):
		essentials_DB_list = essentials_list.retrieve ()
		essentials_DB_list.sort (key = lambda essential : essential ["region"])
		essentials_DB_list_size = len (essentials_DB_list)

	'''
		Add "unites" to each essential.
	'''
	for essential in essentials_DB_list:		
		this_grove.append ({
			"essential": essential,
			"measures": {},
			"natures": [],
			"unites": []
		})

	'''
		This is a "recursive" loop through 
		the list,
		that constructs this_grove.
	'''
	def find_region (list, region):
		for entry in list:		
			if (entry ["essential"] ["region"] == region):
				return entry;
				
			if (len (entry ["unites"]) >= 1):
				found = find_region (entry ["unites"], region)
				if (type (found) == dict):
					return found;
					
		return False
	
	
	def add_inclusions (entry, the_list):
		nonlocal this_grove;
	
		for region in entry ["essential"] ["includes"]:
			physical = find_region (this_grove, region)
			
			copy_of_physical = copy.deepcopy (physical)
			this_grove.remove (physical)
			
			entry ["unites"].append (copy_of_physical)
			
			if (records >= 1):
				print ()
				print ("for:", entry ["essential"] ["names"])
				print ("found:", copy_of_physical ["essential"] ["names"])
	
	def build_grove (the_list):
		for entry in the_list:		
			if (len (entry ["essential"] ["includes"]) >= 1):
				add_inclusions (entry, the_list)
								
				build_grove (entry ["unites"])
			

	build_grove (this_grove)

	return this_grove