
'''
#
#	find name
#
import apoplast.shows.essential_nutrients.DB.scan.seek as seek_nutrient
nutrient = seek_nutrient.presently (
	for_each = lambda essential : True if "thiamin" in essential ["names"] else False
)
'''

'''
#
#	find region
#
import apoplast.shows.essential_nutrients.DB.scan.seek as seek_nutrient
nutrient = seek_nutrient.presently (
	for_each = lambda essential : True if essential ["region"] == 1 else False
)
'''

import apoplast.shows.essential_nutrients.DB.scan.list as essentials_list

def for_each ():
	return False
	
def presently (
	for_each = for_each
):
	essentials = essentials_list.retrieve ()
	for essential in essentials:
		if (for_each (essential)):
			return essential
	
	return None