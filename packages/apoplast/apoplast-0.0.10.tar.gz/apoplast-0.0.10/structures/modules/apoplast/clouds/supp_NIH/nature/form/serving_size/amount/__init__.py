

'''
import apoplast.clouds.supp_NIH.nature.form.serving_size.amount as serving_size_amount_calculator
serving_size_amount_calculator.calc (
	net_contents = "",
	serving_sizes = "",
	servings_per_container = "",
	form_unit = ""
)
'''

'''
	?
		Maybe, This calculates the number that nutrient amount needs
		to be multiplied by, in order to get the sum of the nutrient
		amount in the package?
'''

import apoplast.measures.number.integer.string_is_integer as string_is_integer
import apoplast.insure.equality as equality

import apoplast.insure.equalities as equalities

from fractions import Fraction

def calc (
	net_contents = "",
	serving_sizes = "",
	servings_per_container = "",
	form_unit = ""
):

	servings_per_container = str (Fraction (servings_per_container))

	print ("servings_per_container:", servings_per_container)

	'''
		examples: chia_seeds_214893
	'''
	if (form_unit == "gram"):
		if (equalities.check ([
			[ len (serving_sizes), 1 ],
			[
				serving_sizes [0] ["minQuantity"], 
				serving_sizes [0] ["maxQuantity"]
			]
		])):
			return str (Fraction (serving_sizes [0] ["maxQuantity"]))

			

	'''
	
	
	'''
	if (equalities.check ([
		[ len (net_contents), 1 ],
		[ len (serving_sizes), 1 ],
		[
			serving_sizes [0] ["minQuantity"],
			serving_sizes [0] ["maxQuantity"]
		],
		[
			Fraction (
				Fraction (net_contents [0] ["quantity"]),
				Fraction (servings_per_container)
			),
			Fraction (serving_sizes [0] ["maxQuantity"])
		]
	])):
		return str (Fraction (serving_sizes [0] ["maxQuantity"]))
	
	'''
	if (
		len (net_contents) == 1 and
		len (serving_sizes) == 1 and
		string_is_integer.check (servings_per_container) and
		serving_sizes [0] ["minQuantity"] == serving_sizes [0] ["maxQuantity"] and
		net_contents [0] ["quantity"] / int (servings_per_container) == serving_sizes [0] ["maxQuantity"]
	):
		return str (Fraction (serving_sizes [0] ["maxQuantity"]))
	'''	
		
	raise Exception ("The defined serving size of the supplement could not be calculated.")
		

	#
	#	This is necessary for composition calculations,
	#	but recommendations should be determined elsewhere.
	#
	#	if:
	#		len (netContents)  == 1 and
	#
	#		import cyte.integer.STRING_IS_integer as STRING_IS_integer
	#		STRING_IS_integer.CHECK (servingsPerContainer)
	#
	#		len (servingSizes) == 1
	#
	#		servingSizes [0].minQuantity == servingSizes[0].maxQuantity
	#
	#		netContents [0].quantity / int (servingsPerContainer) == servingSizes[0].maxQuantity
	#
	#	then:
	#		"quantity" = servingSizes[0].maxQuantity
	#		"quantity" = 3
	#
	


	return;