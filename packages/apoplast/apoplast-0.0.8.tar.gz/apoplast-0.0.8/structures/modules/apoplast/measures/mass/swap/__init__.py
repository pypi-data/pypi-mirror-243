

'''
	https://www.wolframalpha.com/input?i=gram+to+pound
'''

'''
	import apoplast.measures.mass.swap as mass_swap
	mass_swap.start ([ 432, "GRAMS" ], "POUNDS")
'''

from fractions import Fraction 

grams_to_pounds = Fraction (1, Fraction (453.59237))
pounds_to_ounces = 16

conversions = {
	"grams": {
		"pounds": grams_to_pounds,
		"ounces": Fraction (grams_to_pounds, pounds_to_ounces),
		
		"milligrams": Fraction (1000, 1),
		"micrograms": Fraction (1000000, 1)
	},
	"milligrams": {		
		"micrograms": Fraction (1000, 1),
		"grams": Fraction (1, 1000)
	},
	"micrograms": {
		"grams": Fraction (1, 1000000),
		"milligrams": Fraction (1, 1000)
	},
	
	
	#
	#	avroidupois
	#
	"pounds": {
		"ounces": 16,
		"grams": Fraction (453.59237)
	},
	"ounces": {
		"pounds": Fraction (1, 16),
		"grams": Fraction (28.349523125)
	},
	
	#
	#	troy
	#
	"troy pounds": {},
	"troy ounces": {}	
}

#
#	these need to be lowercase currenly
#
GROUPS = [
	[ "grams", "gram(s)", "gram", "g", "grm" ],
	[ "milligrams", "milligram", "mg" ],
	[ "micrograms", "microgram", "mcg", "\u00b5g", "µg" ],

	[ "pounds", "pound", "lbs", "lb" ],
	[ "ounces", "ounce", "oz", "ozs" ],
]


def find_unit (TO_find):
	for GROUP in GROUPS:		
		for UNIT in GROUP:
			if (UNIT == TO_find):
				return GROUP [0]
	
	raise Exception ("Unit was not found.")



def start (from_quantity, to_unit):
	[ from_amount, from_unit ] = from_quantity;

	from_unit = find_unit (from_unit.lower ())
	to_unit = find_unit (to_unit.lower ())

	if (from_unit == to_unit):
		return from_amount

	assert (from_unit in conversions), { "from_unit": from_unit, "to_unit": to_unit }
	assert (to_unit in conversions [ from_unit ]), { "from_unit": from_unit, "to_unit": to_unit }

	return conversions [ from_unit ] [ to_unit ] * Fraction (from_amount);