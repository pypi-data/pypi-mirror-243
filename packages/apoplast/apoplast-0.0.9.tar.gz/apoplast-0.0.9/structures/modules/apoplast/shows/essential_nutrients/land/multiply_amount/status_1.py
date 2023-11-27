


'''
	python3 insurance.py shows/essential_nutrients/land/multiply_amount/status_1.py
'''

import apoplast.clouds.food_USDA.deliveries.one.assertions.foundational as assertions_foundational
import apoplast.clouds.food_USDA.examples as USDA_examples	
import apoplast.clouds.food_USDA.nature as food_USDA_nature
import apoplast.insure.equality as equality

import apoplast.shows.essential_nutrients.land.multiply_amount as multiply_land_amount
import apoplast.shows.essential_nutrients.grove.seek_name_or_accepts as grove_seek_name_or_accepts
	

import json	

def check_1 ():
	nature = food_USDA_nature.create (
		USDA_examples.retrieve ("branded/vegan_pizza_2672996.JSON")
	)

	essential_nutrients = nature ["essential nutrients"];
	grove = essential_nutrients ["grove"]
	essential_nutrient_measures = essential_nutrients ["measures"]

	'''
		60.018288 = 1351491697361075527451/22517998136852480000
		131.35 = 2627/20
	'''
	assert (
		essential_nutrients ["measures"] ==
		{
			'mass + mass equivalents': {
				'per recipe': {
					'grams': {
						'fraction string': '1351491697361075527451/22517998136852480000'
					}
				}
			}, 
			'energy': {
				'per recipe': {
					'food calories': {
						'fraction string': '2627/20'
					}
				}
			}
		}
	), essential_nutrients ["measures"]

	#print (json.dumps (essential_nutrient_measures, indent = 4))
	#return;

	
	iron = grove_seek_name_or_accepts.politely (
		grove = grove,
		name_or_accepts = "iron"
	)
	assert (
		iron ["measures"] ["mass + mass equivalents"] ["per recipe"] ["grams"] ["fraction string"] ==
		"89531560592125469/45035996273704960000"
	)


	multiply_land_amount.smoothly (
		land = essential_nutrients,
		amount = 2
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
						'fraction string': '1351491697361075527451/11258999068426240000'
					}
				}
			}, 
			'energy': {
				'per recipe': {
					'food calories': {
						'fraction string': '2627/10'
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
		"89531560592125469/22517998136852480000"
	)
	
	print (json.dumps (iron, indent = 4))
	
	return;
	
checks = {
	'check 1': check_1
}