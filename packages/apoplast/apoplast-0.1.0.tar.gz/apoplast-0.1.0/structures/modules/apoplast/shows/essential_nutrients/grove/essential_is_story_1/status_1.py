

'''
	python3 insurance.py shows/essential_nutrients/grove/essential_is_story_1/status_1.py
'''

import apoplast.shows.essential_nutrients.grove.essential_is_story_1 as essential_is_story_1
import apoplast.shows.essential_nutrients.grove.nurture as grove_nurture
	
def check_1 ():
	grove = grove_nurture.beautifully ()
	
	story_1_list = essential_is_story_1.generate_list (grove)
	
	assert (essential_is_story_1.check (story_1_list, "carbohydrates") == True)
	assert (essential_is_story_1.check (story_1_list, "sugars, added") == False)
		
	assert (essential_is_story_1.check (story_1_list, "polyunsaturated fat") == False)

	assert (essential_is_story_1.check (story_1_list, "protein") == True)
	
	assert (essential_is_story_1.check (story_1_list, "dietary fiber") == False)

checks = {
	'check 1': check_1
}