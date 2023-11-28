

'''

'''

import apoplast.shows.essential_nutrients.land.add_measured_ingredient as add_measured_ingredient
import apoplast.shows.essential_nutrients.land.build as build_essential_nutrients_land
import apoplast.shows.essential_nutrients.grove.seek as grove_seek

import apoplast.shows.essential_nutrients.grove.has_uniters as has_uniters
import apoplast.shows.essential_nutrients.assertions.one as essentials_nutrients_assertions_one


import json	

	

def eloquently (
	measured_ingredients_list = [],
	identity = {}
):	
	land = build_essential_nutrients_land.eloquently ()
	grove = land ["grove"]
	natures = land ["natures"]
		
	natures.append ({
		"amount": "1",
		"identity": identity
	})	
		
	for measured_ingredient in measured_ingredients_list:
		add_measured_ingredient.beautifully (
			#
			#	This is a reference to the land.
			#
			land = land,
			
			amount = 1,
			source = identity,
			measured_ingredient = measured_ingredient
		)
		
	
		
	'''
		Make sure that all the story 2 and above "essentials",
		have a uniter that has "natures".
		
		That is make sure if "added, sugars" is listed,
		that "sugars, total" is listed.
	'''
	has_uniters.check (grove)
	essentials_nutrients_assertions_one.sweetly (
		essentials_nutrients = land
	)	
	
	return land;