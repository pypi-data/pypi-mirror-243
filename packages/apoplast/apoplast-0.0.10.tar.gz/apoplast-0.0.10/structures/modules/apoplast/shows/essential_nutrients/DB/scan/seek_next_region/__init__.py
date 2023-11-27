



'''
import apoplast.shows.essential_nutrients.DB.scan.seek_next_region as seek_next_region
import apoplast.shows.essential_nutrients.DB.access as access
next_region = seek_next_region.politely (
	essentials_DB = access.DB ()
)

'''

import apoplast.shows.essential_nutrients.DB.access as access

def politely (
	essentials_DB = access.DB ()
):
	physicals = essentials_DB.all ()
	physicals.sort (key = lambda physical : physical ["region"])
	last_index = len (physicals) - 1;
	
	return physicals [ last_index ][ "region" ] + 1
	
	