
'''
	#
	#	This retrieves a supp's data from the NIH.	
	#
	import apoplast.clouds.supp_NIH.deliveries.one as retrieve_1_supp
	supp_NIH = retrieve_1_supp.presently ()

	import apoplast.clouds.supp_NIH.nature as supp_NIH_nature
	nature = supp_NIH_nature.create (supp_NIH)
'''

'''
	Limitations:
		1. The package mass is not always known.
'''

import apoplast.clouds.supp_NIH.nature.form.unit as form_unit_calculator
import apoplast.clouds.supp_NIH.nature.form.amount as form_amount_calculator

import apoplast.clouds.supp_NIH.nature.form.serving_size.amount as serving_size_amount_calculator

from fractions import Fraction

def create (supp_NIH):
	nature = {
		"kind": "food",
		"identity": {
			"name":	supp_NIH ["fullName"],
			"FDC ID": str (supp_NIH ["id"]),
			"UPC": supp_NIH ["upcSku"],
			"DSLD ID": ""
		},
		"brand": {
			"name":	supp_NIH ["brandName"]
		},
		"measures": {
			"form": {
				"unit": ""
			},
		}
	}
	
	
	assert ("netContents" in supp_NIH)
	assert ("physicalState" in supp_NIH)
	assert ("servingSizes" in supp_NIH)
	net_contents = supp_NIH ["netContents"]	
	physical_state = supp_NIH ["physicalState"]
	serving_sizes = supp_NIH ["servingSizes"]
	servings_per_container = supp_NIH ["servingsPerContainer"]
	
	form_unit = form_unit_calculator.calc (
		net_contents = net_contents,
		physical_state = physical_state,
		serving_sizes = serving_sizes
	)
	form_amount = form_amount_calculator.calc (
		net_contents = net_contents,
		form_unit = form_unit
	)
	
	'''
		Every shape listed might already have this
		in the shape data.
	'''
	serving_size_amount = serving_size_amount_calculator.calc (
		net_contents = net_contents,
		serving_sizes = serving_sizes,
		servings_per_container = servings_per_container,
		form_unit = form_unit
	)

	nature ["measures"]["form"]["amount"] = form_amount;
	nature ["measures"]["form"]["unit"] = form_unit
	nature ["measures"]["form"]["serving size amount"] = serving_size_amount
	
	'''
		Is the servings per container an estimate,
		and therefore the nutrient amounts are estimates?
	'''
	nature ["measures"]["form"]["amount is an estimate"] = "?"
	if (form_unit == "gram"):
		is_an_estimate = Fraction (form_amount) != (
			Fraction (servings_per_container) *
			Fraction (serving_size_amount)
		)
		if (is_an_estimate):
			nature  ["measures"]["form"]["amount is an estimate"] = "yes"
	
	
	

	return nature