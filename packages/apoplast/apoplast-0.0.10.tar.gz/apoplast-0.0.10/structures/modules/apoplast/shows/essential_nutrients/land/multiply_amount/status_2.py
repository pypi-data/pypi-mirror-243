


'''
	python3 insurance.py shows/essential_nutrients/land/multiply_amount/status_2.py
'''

import apoplast.clouds.food_USDA.deliveries.one.assertions.foundational as assertions_foundational
import apoplast.clouds.food_USDA.examples as USDA_examples	
import apoplast.clouds.food_USDA.nature as food_USDA_nature
import apoplast.insure.equality as equality

import apoplast.shows.essential_nutrients.land.multiply_amount as multiply_land_amount
import apoplast.shows.essential_nutrients.grove.seek_name_or_accepts as grove_seek_name_or_accepts

from fractions import Fraction

import json	

def check_1 ():
	nature = food_USDA_nature.create (
		USDA_examples.retrieve ("branded/walnuts_1882785.JSON")
	)

	essential_nutrients = nature ["essential nutrients"];
	grove = essential_nutrients ["grove"]
	essential_nutrient_measures = essential_nutrients ["measures"]

	amount = 9;

	'''
		60.018288 = 1351491697361075527451/22517998136852480000
		131.35 = 2627/20
	'''
	mass_and_mass_eq_grams_per_package = Fraction ("84238347589283870046299/112589990684262400000")
	energy_food_calories_per_package = Fraction ("154133/50")
	
	assert (
		essential_nutrients ["measures"] ==
		{
			'mass + mass equivalents': {
				'per recipe': {
					'grams': {
						'fraction string': str (mass_and_mass_eq_grams_per_package)
					}
				}
			}, 
			'energy': {
				'per recipe': {
					'food calories': {
						'fraction string': str (energy_food_calories_per_package)
					}
				}
			}
		}
	), essential_nutrients ["measures"]

	#print (json.dumps (essential_nutrient_measures, indent = 4))
	#return;

	
	iron_amount_per_package = Fraction ("1461913475040736643/112589990684262400000")
	
	iron = grove_seek_name_or_accepts.politely (
		grove = grove,
		name_or_accepts = "iron"
	)
	assert (
		iron ["measures"] ["mass + mass equivalents"] ["per recipe"] ["grams"] ["fraction string"] ==
		str (iron_amount_per_package)
	), iron


	multiply_land_amount.smoothly (
		land = essential_nutrients,
		amount = amount
	)
	
	'''
		120.036576 = 1351491697361075527451/11258999068426240000
		262.7 = 2627/10
	'''
	assert (
		essential_nutrients ["measures"] ==
		{
			'mass + mass equivalents': {
				'per recipe': {
					'grams': {
						'fraction string': str (mass_and_mass_eq_grams_per_package * amount)
					}
				}
			}, 
			'energy': {
				'per recipe': {
					'food calories': {
						'fraction string': str (energy_food_calories_per_package * amount)
					}
				}
			}
		}
	), essential_nutrients ["measures"]

	
	iron = grove_seek_name_or_accepts.politely (
		grove = grove,
		name_or_accepts = "iron"
	)
	assert (
		iron ["measures"] ["mass + mass equivalents"] ["per recipe"] ["grams"] ["fraction string"] ==
		str (iron_amount_per_package * 9)
	)
	
	print (json.dumps (iron, indent = 4))
	
	return;
	
checks = {
	'check 1': check_1
}