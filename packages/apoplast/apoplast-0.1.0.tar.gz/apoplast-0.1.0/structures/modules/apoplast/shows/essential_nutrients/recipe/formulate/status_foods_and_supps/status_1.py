



'''
	python3 insurance.py shows/essential_nutrients/recipe/formulate/status_foods_and_supps/status_1.py
'''




import apoplast.clouds.food_USDA.deliveries.one.assertions.foundational as assertions_foundational
import apoplast.clouds.food_USDA.examples as USDA_examples	
import apoplast.clouds.food_USDA.nature as food_USDA_nature
import apoplast.insure.equality as equality

import apoplast.shows.essential_nutrients.recipe.formulate as formulate_recipe
import apoplast.shows.essential_nutrients.grove.seek_name_or_accepts as grove_seek_name_or_accepts

import apoplast.clouds.supp_NIH.nature as supp_NIH_nature
import apoplast.clouds.supp_NIH.examples as NIH_examples

from fractions import Fraction
from copy import deepcopy
import json

def find_grams (measures):
	return Fraction (
		measures ["mass + mass equivalents"] ["per recipe"] ["grams"] ["fraction string"]
	)
	

def check_1 ():
	def retrieve_supp (supp_path):
		return supp_NIH_nature.create (
			NIH_examples.retrieve (supp_path) 
		) ["essential nutrients"]
	
	def retrieve_food (food_path):
		return food_USDA_nature.create (
			USDA_examples.retrieve (food_path)
		) ["essential nutrients"]
	
	print (json.dumps (retrieve_food ("branded/beet_juice_2412474.JSON"), indent = 4))
	
	recipe = formulate_recipe.adroitly ([
		[ retrieve_supp ("coated tablets/multivitamin_276336.JSON"), 10 ],
		[ retrieve_supp ("other/chia_seeds_214893.JSON"), 20 ],
		
		[ retrieve_food ("branded/beet_juice_2412474.JSON"), 20 ],
		[ retrieve_food ("branded/beet_juice_2642759.JSON"), 20 ],
		[ retrieve_food ("branded/Gardein_f'sh_2664238.JSON"), 20 ],
		[ retrieve_food ("branded/impossible_beef_2664238.JSON"), 80 ],
	])
	
	def add (path, data):
		import pathlib
		from os.path import dirname, join, normpath
		this_directory = pathlib.Path (__file__).parent.resolve ()
		example_path = normpath (join (this_directory, path))
		FP = open (example_path, "w")
		FP.write (data)
		FP.close ()
		
	add ("status_1.JSON", json.dumps (recipe, indent = 4))
	
	assert (len (recipe ["natures"]) == 6)
	
	'''
		These amounts are calculcated another way.
	'''
	assert (
		recipe ["measures"] ==
		{
			"mass + mass equivalents": {
				"per recipe": {
					"grams": {
						"fraction string": "5139137410365247955069599/225179981368524800000"
					}
				}
			},
			"energy": {
				"per recipe": {
					"food calories": {
						"fraction string": "438088/5"
					}
				}
			}
		}
	)

	
checks = {
	"check 1": check_1
}