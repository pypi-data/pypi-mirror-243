
'''
	caution: not case sensitive
'''

'''
	import apoplast.measures._interpret.unit_kind as unit_kind
	kind = unit_kind.calc ("ml")
'''

volume_unit_groups = [
	[ "liters", "litres", "l" ],
	[ "milliliters", "millilitres", "ml" ],

	[ "fluid ounces", "fl oz" ]
]

#
#	maybe these are case sensitive?
#
mass_unit_groups = [
	[ "grams", "gram", "g", "grm" ],
	[ "milligrams", "milligram", "mg" ],
	[ "micrograms", "microgram", "mcg", "\u00b5g", "µg" ],

	[ "pounds", "pound", "lbs", "lb" ],
	[ "ounces", "ounce", "oz", "ozs" ],
]

energy_unit_groups = [
	[ "kcal", "food calories", "joules" ]
]

biological_activity_groups = [
	[ "iu" ]
]

def calc (unit):
	for group in volume_unit_groups:
		for group_unit in group:
			if (unit.lower () == group_unit):
				return "volume"

	for group in mass_unit_groups:
		for group_unit in group:
			if (unit.lower () == group_unit):
				return "mass"
	
	for group in energy_unit_groups:
		for group_unit in group:
			if (unit.lower () == group_unit.lower ()):
				return "energy"
	
	for group in biological_activity_groups:
		for group_unit in group:
			if (unit.lower () == group_unit.lower ()):
				return "biological activity"
	
	raise Exception (f'The unit "{ unit }" could not be interpretted.')
	return "?"