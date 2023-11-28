
'''
	import apoplast.clouds.supp_NIH.nature.essential_nutrients as calculate_essential_nutrients
	calculate_essential_nutrients.eloquently (
		measured_ingredients_grove
	)
'''

import apoplast.clouds.supp_NIH.nature.measured_ingredients.seek as seek
import apoplast.shows.essential_nutrients.land.build as build_essential_nutrients_land
import apoplast.shows.essential_nutrients.land.add_measured_ingredient as add_measured_ingredient
	
import apoplast.shows.essential_nutrients.grove.has_uniters as has_uniters
import apoplast.shows.essential_nutrients.assertions.one as essentials_nutrients_assertions_one	

import json

def eloquently (
	measured_ingredients_grove,
	identity
):
	essential_nutrients_land = build_essential_nutrients_land.eloquently ()
	essential_nutrients_grove = essential_nutrients_land ["grove"]
	essential_nutrients_natures = essential_nutrients_land ["natures"]
		
	essential_nutrients_natures.append ({
		"amount": "1",
		"identity": identity
	})	

	print ()
	print ("essential nutrients")
	print ()

	#print (json.dumps (essential_nutrients_land, indent = 4))

	not_found = []

	def for_each (
		measured_ingredient, 
		indent = 0, 
		parent_measured_ingredient = None
	):
		found = add_measured_ingredient.beautifully (
			#
			#	This is a reference to the land.
			#
			land = essential_nutrients_land,
			
			amount = 1,
			source = identity,
			measured_ingredient = measured_ingredient,
			
			return_False_if_not_found = True
		)
		if (not found):
			not_found.append (measured_ingredient ["name"])
		
		#print (measured_ingredient ["name"], f"? found = ", found)
		
		return False;

	seek.beautifully (
		measured_ingredients = measured_ingredients_grove,
		for_each = for_each
	)
	
	has_uniters.check (essential_nutrients_grove)
	essentials_nutrients_assertions_one.sweetly (
		essentials_nutrients = essential_nutrients_land
	)	
	
	
	print ("These ingredients were not found:", not_found)

	return essential_nutrients_land