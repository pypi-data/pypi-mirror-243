


import apoplast.shows.essential_nutrients.land.add_measured_ingredient as add_measured_ingredient
import apoplast.shows.essential_nutrients.land.build as build_essential_nutrients_land
import apoplast.shows.essential_nutrients.grove.seek as grove_seek

import json	

	

def eloquently (
	measured_ingredients_list = [],
	identity = {}
):	
	land = build_essential_nutrients_land.eloquently ()
	grove = land ["grove"]
	
	
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
		
	return land;