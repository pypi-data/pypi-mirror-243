
'''
import apoplast.shows.essential_nutrients.land.build as build_essential_nutrients_land
land = build_essential_nutrients_land.eloquently ()
'''

'''
	plan:
		1. 	build the grove of essential nutrients 
			from the essential nutrients DB
		
		2. 
'''

import apoplast.shows.essential_nutrients.grove.nurture as grove_nurture
	
def eloquently ():
	structure = {
		"measures": {
			"mass + mass equivalents": {
				"per recipe": {
					"grams": {
						"fraction string": "0"
					}
				}
			},
			"biological activity": {
				"per recipe": {
					"IU": {
						"fraction string": "0"
					}
				}
			},
			"energy": {
				"per recipe": {
					"calories": {
						"fraction string": "0"
					},
					"joules": {
						"fraction string": "0"
					}
				}
			}
		},
		"grove": grove_nurture.beautifully (),
		"exclusions": []
	}

	return structure