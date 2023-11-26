

'''
	python3 insurance.py clouds/supp_NIH/nature/form/serving_size/amount/status_1.py
'''

import apoplast.clouds.supp_NIH.nature.form.serving_size.amount as serving_size_amount_calculator

def check_1 ():

	'''
		454 / 38 = 11.947368421052632
	'''
	serving_size_amount = serving_size_amount_calculator.calc (
		net_contents = [
			{
				"order": 1,
				"quantity": 16,
				"unit": "Oz(s)",
				"display": "16 Oz(s)"
			},
			{
				"order": 2,
				"quantity": 454,
				"unit": "Gram(s)",
				"display": "454 Gram(s)"
			}
		],
		serving_sizes = [
			{
				"order": 1,
				"minQuantity": 12,
				"maxQuantity": 12,
				"minDailyServings": 1,
				"maxDailyServings": None,
				"unit": "Gram(s)",
				"notes": "(1 Tbsp)(1 scoop)",
				"inSFB": True
			}
		],
		servings_per_container = "38",
		form_unit = "gram"
	)
	
	print ("serving_size_amount:", serving_size_amount)

	assert (serving_size_amount == "12"), serving_size_amount

	return;
	
checks = {
	'check 1': check_1
}