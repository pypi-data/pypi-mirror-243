
'''
	This is assertions about the essential nutrients once 1
	food or supp has been added to them.
'''

'''
import apoplast.shows.essential_nutrients.assertions.one as essentials_nutrients_assertions_one
essentials_nutrients_assertions_one.sweetly (
	essentials_nutrients = land
)
'''

import apoplast.shows.essential_nutrients.grove.assertions as make_grove_assertions
	

def sweetly (essentials_nutrients):
	assert (len (essentials_nutrients ["natures"]) == 1)

	make_grove_assertions.about (essentials_nutrients ["grove"])

	return;