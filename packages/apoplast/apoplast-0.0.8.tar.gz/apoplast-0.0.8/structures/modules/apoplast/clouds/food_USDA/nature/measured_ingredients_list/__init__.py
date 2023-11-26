

import apoplast.clouds.food_USDA.nature.measured_ingredient as measured_ingredient_builder

def build (
	food_USDA,
	mass_and_volume,
	form,
	
	records = 0
):
	assert ("foodNutrients" in food_USDA)

	measured_ingredients_list = []

	food_nutrients = food_USDA ["foodNutrients"]
	for USDA_food_nutrient in food_nutrients:
		measured_ingredient = measured_ingredient_builder.build (
			USDA_food_nutrient,
			mass_and_volume,
			form,
			
			records = 0
		)
	
		measured_ingredients_list.append (measured_ingredient)

	
	return measured_ingredients_list