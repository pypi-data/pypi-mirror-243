

'''
	import apoplast.shows.essential_nutrients.recipe.formulate as formulate_recipe
	recipe = formulate_recipe.adroitly ([
		[ land_1, amount_1 ],
		[ land_2, amount_2 ]
	])
'''

'''
	description:
		This merges the land measures into the recipe measures.
	
	
	priorities:
		merge the land { ingredient } measures into the recipe ingredient measures. 
'''

import json
import apoplast.shows.essential_nutrients.land.multiply_amount as multiply_land_amount
import apoplast.shows.essential_nutrients.land.build.measures as build_land_measures
import apoplast.shows.essential_nutrients.measures.merge as merge_measures
import apoplast.shows.essential_nutrients.grove.seek as grove_seek
import apoplast.shows.essential_nutrients.grove.nurture as grove_nurture
import apoplast.shows.essential_nutrients.grove.seek_name_or_accepts as grove_seek_name_or_accepts
	
	
def adroitly (lands):
	recipe = {
		"natures": [],
		"measures": build_land_measures.quickly (),
		"grove": grove_nurture.beautifully ()		
	}


	for land_list in lands:
		land_amount = land_list [1];
		land = land_list [0]
		land_measures = land ["measures"]
		land_grove = land ["grove"]
		
		recipe ["natures"].append (
			land ["natures"] [0]
		)
		
		print ("land:", land_amount)
		
		'''
			This multiplies the land measures 
			and the land grove measures, then
			adds them to the recipe measures.
		'''
		multiply_land_amount.smoothly (
			amount = land_amount,
			land = land
		)
		merge_measures.calc (
			recipe ["measures"],
			land ["measures"]
		)
		
		'''
			priorities:
				for each in the land grove:
					1. merge the treasure measures into the recipe ingredient measures
					2. append the treasure nautres to the recipe ingredient natures
		'''
		def for_each (treasure_ingredient):
			recipe_grove_ingredient = grove_seek_name_or_accepts.politely (
				grove = recipe ["grove"],
				name_or_accepts = treasure_ingredient ["essential"]["names"][0]
			)
			merge_measures.calc (
				recipe_grove_ingredient ["measures"],
				treasure_ingredient ["measures"]
			)
			
			assert (len (treasure_ingredient ["natures"]) <= 1);
			
			if (len (treasure_ingredient ["natures"]) == 1):
				recipe_grove_ingredient ["natures"].append (
					treasure_ingredient ["natures"][0]
				) 
					
			return False		
		
		grove_seek.beautifully (
			grove = land ["grove"],
			for_each = for_each
		)
		
	'''
		For a second check, could loop through the ingredients
		in the grove to make sure that their ingredient amounts sum
		equals the recipe amount sum.
	'''
	
	
	
		

	return recipe