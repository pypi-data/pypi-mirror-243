
'''
	python3 insurance.py shows/essential_nutrients/grove/seek/status_1.py
'''

import apoplast.shows.essential_nutrients.grove.nurture as grove_nurture
import apoplast.shows.essential_nutrients.grove.seek as grove_seek
		
def check_1 ():
	grove = grove_nurture.beautifully ()	

	
	sodium = grove_seek.beautifully (
		grove = grove,
		for_each = (
			lambda entry : True if (
				"sodium, na" in list (map (
					lambda name : name.lower (), 
					entry ["essential"] ["names"]
				))
			) else False
		)
	)
	
	assert (type (sodium) == dict)

	return;
	
	
checks = {
	'check 1': check_1
}