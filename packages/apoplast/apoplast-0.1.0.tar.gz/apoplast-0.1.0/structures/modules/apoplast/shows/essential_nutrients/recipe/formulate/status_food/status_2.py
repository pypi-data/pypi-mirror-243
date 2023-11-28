





'''
	python3 insurance.py shows/essential_nutrients/recipe/formulate/status_food/status_2.py
'''

import json

import apoplast.clouds.food_USDA.deliveries.one.assertions.foundational as assertions_foundational
import apoplast.clouds.food_USDA.examples as USDA_examples	
import apoplast.clouds.food_USDA.nature as food_USDA_nature
import apoplast.insure.equality as equality

import apoplast.shows.essential_nutrients.recipe.formulate as formulate_recipe
import apoplast.shows.essential_nutrients.grove.seek_name_or_accepts as grove_seek_name_or_accepts

import apoplast.shows.essential_nutrients.recipe.formulate.assertions.ingredient as ingredient_assertion

from fractions import Fraction

from copy import deepcopy

def find_grams (measures):
	return Fraction (
		measures ["mass + mass equivalents"] ["per recipe"] ["grams"] ["fraction string"]
	)

def check_1 ():
	food_1 = food_USDA_nature.create (
		USDA_examples.retrieve ("branded/walnuts_1882785.JSON")
	) ["essential nutrients"]
	food_2 = food_USDA_nature.create (
		USDA_examples.retrieve ("branded/vegan_pizza_2672996.JSON")
	) ["essential nutrients"]

	food_1_1 = deepcopy (food_1)
	food_2_1 = deepcopy (food_2)

	food_1_mass_and_mass_eq_grams = Fraction ("84238347589283870046299/112589990684262400000")
	food_1_energy_food_calories = Fraction ("154133/50")
	food_1_multiplier = 10

	food_2_mass_and_mass_eq_grams = Fraction ("1351491697361075527451/22517998136852480000")
	food_2_energy_food_calories = Fraction ("2627/20")
	food_2_multiplier = 100
		
	assert (
		food_1 ["measures"] ==
		{
			"mass + mass equivalents": {
				"per recipe": {
					"grams": {
						"fraction string": str (food_1_mass_and_mass_eq_grams)
					}
				}
			},
			"energy": {
				"per recipe": {
					"food calories": {
						"fraction string": str (food_1_energy_food_calories)
					}
				}
			}
		}
	), food_1 ["measures"]
	assert (
		food_2 ["measures"] ==
		{
			"mass + mass equivalents": {
				"per recipe": {
					"grams": {
						"fraction string": str (food_2_mass_and_mass_eq_grams)
					}
				}
			},
			"energy": {
				"per recipe": {
					"food calories": {
						"fraction string": str (food_2_energy_food_calories)
					}
				}
			}
		}
	), food_2 ["measures"]

	recipe = formulate_recipe.adroitly ([
		[ food_1, food_1_multiplier ],
		[ food_2, food_2_multiplier ]
	])
	
	assert (
		recipe ["measures"] ==
		{
			"mass + mass equivalents": {
				"per recipe": {
					"grams": {
						"fraction string": str (
							(food_1_mass_and_mass_eq_grams * food_1_multiplier) +
							(food_2_mass_and_mass_eq_grams * food_2_multiplier)							
						)
					}
				}
			},
			"energy": {
				"per recipe": {
					"food calories": {
						"fraction string": str (
							(food_1_energy_food_calories * food_1_multiplier) +
							(food_2_energy_food_calories * food_2_multiplier)							
						)
					}
				}
			}
		}
	), food_1 ["measures"]
	
	
	'''
	assert_ingredient ("protein")
	assert_ingredient ("carbohydrates")
	assert_ingredient ("Cholesterol")
	assert_ingredient ("Sodium, Na")
	'''
	
	ingredient_assertion.check (
		"carbohydrates",
		
		recipe,
		
		food_1_1,
		food_2_1,
		
		food_1_multiplier,
		food_2_multiplier,
		
		food_1,
		food_2
	)
	ingredient_assertion.check (
		"Cholesterol",
		
		recipe,
		
		food_1_1,
		food_2_1,
		
		food_1_multiplier,
		food_2_multiplier,
		
		food_1,
		food_2
	)
	ingredient_assertion.check (
		"protein",
		
		recipe,
		
		food_1_1,
		food_2_1,
		
		food_1_multiplier,
		food_2_multiplier,
		
		food_1,
		food_2
	)
	
checks = {
	"check 1": check_1
}