
'''
	python3 insurance.py clouds/supp_NIH/nature/form/unit/status_coated_tablets_276336.py
'''

import apoplast.clouds.supp_NIH.nature.form.unit as form_unit

def check_1 ():	
	unit = form_unit.calc (
		net_contents = [
			{
				"order": 1,
				"quantity": 90,
				"unit": "Coated Tablet(s)",
				"display": "90 Coated Tablet(s)"
			}
		],
		physical_state = {
			"langualCode": "E0155",
			"langualCodeDescription": "Tablet or Pill"
		},
		serving_sizes = [
			{
				"order": 1,
				"minQuantity": 1,
				"maxQuantity": 1,
				"minDailyServings": 1,
				"maxDailyServings": 1,
				"unit": "Tablet(s)",
				"notes": "",
				"inSFB": True
			}
		]
	)
	
	assert (unit == "Coated Tablet"), unit
	
	return;
	
	
checks = {
	"check 1": check_1
}