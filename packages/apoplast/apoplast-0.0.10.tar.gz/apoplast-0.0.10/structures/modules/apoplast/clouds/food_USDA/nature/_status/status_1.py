
'''
	python3 insurance.py clouds/food_USDA/nature/_status/status_1.py
'''

from apoplast.insure.override_print import override_print
#override_print ()

import apoplast.clouds.food_USDA.deliveries.one.assertions.foundational as assertions_foundational
import apoplast.clouds.food_USDA.examples as USDA_examples
import json	
	
import apoplast.clouds.food_USDA.nature as food_USDA_nature

import apoplast.insure.equality as equality


	
def check_1 ():
	walnuts_1882785 = USDA_examples.retrieve ("branded/walnuts_1882785.JSON")
	assertions_foundational.run (walnuts_1882785)
	
	nature = food_USDA_nature.create (walnuts_1882785)

	#print (json.dumps (nature, indent = 4))

	equality.check (nature ["identity"]["FDC ID"], "1882785")

	assert (
		nature ["measures"]["form"] ==
		{
            "unit": "gram",
            "amount": "454",
            "servings": {
                "listed": {
                    "serving size amount": "28",
                    "serving size unit": "g"
                },
                "calculated": {
                    "serving size amount": "28",
                    "servings per package": "227/14",
                    "foodNutrient per package multiplier": "227/50",
                    "labelNutrient per package multiplier": "227/14"
                }
            }
        }
	), nature ["measures"]["form"]


	equality.check (nature ["measures"]["mass"]["ascertained"], True)
	equality.check (
		nature ["measures"]["mass"]["per package"]["grams"]["fraction string"], 
		"454"
	)
	
	equality.check (nature ["measures"]["volume"]["ascertained"], False)
	
	equality.check (nature ["measures"]["energy"]["ascertained"], True)
	equality.check (
		nature ["measures"]["energy"]["per package"]["food calories"]["fraction string"], 
		"154133/50"
	)
	
	
	
	
checks = {
	'check 1': check_1
}