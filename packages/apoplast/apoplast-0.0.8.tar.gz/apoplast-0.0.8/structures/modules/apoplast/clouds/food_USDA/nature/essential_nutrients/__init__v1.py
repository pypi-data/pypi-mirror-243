


"""
	essentials nutrients grove
"""

'''
	priorities:
		steps:
			1.  build the essential nutrients structure
			
			2.  loop through the measured ingredient list and
				merge any essentials found into the essential 
				nutrients structure.grove

					if an ingredient is not found in the ENSG, 
					then raise an alarm about it.
'''

import apoplast.shows.essential_nutrients.land.build as build_essential_nutrients_land
import apoplast.shows.essential_nutrients.grove.seek as grove_seek
import json	
import apoplast.shows.essential_nutrients.grove.measures.add as add_grove_measures

	
	

'''
	This finds the entry in the grove
	that has the name of the 
	measured ingredient.
'''
def seek_measured_ingredient_name (
	measured_ingredient_name = "",
	grove = []
):
	checked = []
	def for_each (entry):		
		accepts = []
		if ("accepts" in entry ["essential"]):
			accepts = entry ["essential"] ["accepts"]
	
		patterns = [
			* entry ["essential"] ["names"],
			* accepts
		]	
		
		checked.append (patterns)
			
		for name in patterns:
			if (measured_ingredient_name == name.lower ().strip ()):			
				return True;
			
		return False

	entry = grove_seek.beautifully (
		grove = grove,
		for_each = for_each
	)
	if (type (entry) != dict):
		print (entry)
		#print (checked)
		raise Exception ("A measured ingredient was not found.")

	return entry
	
def eloquently (
	measured_ingredients_list = [],
	identity = {}
):
	land = build_essential_nutrients_land.eloquently ()
	grove = land ["grove"]


	
		
	'''
		Add each measured_ingredient to the grove.
	'''
	for measured_ingredient in measured_ingredients_list:
		measured_ingredient_name = measured_ingredient ["name"].lower ().strip ()
	
		#print (f"measured_ingredient_name: '{ measured_ingredient_name }'")
		
		'''
		entry = seek_measured_ingredient_name (
			measured_ingredient_name,
			grove
		)
		'''
				
		def for_each (entry):
			names = entry ["essential"] ["names"]
			accepts = []
			if ("accepts" in entry ["essential"]):
				accepts = entry ["essential"] ["accepts"]
			
			monikers = [
				* names,
				* accepts
			]
			for moniker in monikers:			
				if (moniker.lower () == measured_ingredient_name):
					return True
					
			return False
			
		essential_nutrient = grove_seek.beautifully (
			grove = grove,
			for_each = for_each
		)

		assert (type (essential_nutrient) == dict), measured_ingredient_name
		
			
		print (json.dumps ({
			"measured_ingredient": measured_ingredient,
			"entry": essential_nutrient
		}, indent = 4))
		
		add_grove_measures.beautifully (
			#
			#	This is a reference to the essential ingredient.
			#
			entry = essential_nutrient,
			amount = 1,
			source = identity,
			measured_ingredient = measured_ingredient
		)
		
		#return;

	return land;