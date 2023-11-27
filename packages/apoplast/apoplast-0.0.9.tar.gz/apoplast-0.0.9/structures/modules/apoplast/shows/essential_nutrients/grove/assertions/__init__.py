

'''
	import apoplast.shows.essential_nutrients.grove.assertions as make_grove_assertions
	make_grove_assertions.about (grove)
'''


'''
[{
	"essential"
	"measures"
	"natures": []
	"unites"
}]
'''

import apoplast.shows.essential_nutrients.DB.scan.list as essentials_list_scan
import apoplast.shows.essential_nutrients.DB.access as access

def entries_are_formatted_correctly (
	grove,	
	story = 1
):
	for entry in grove:		
		#print ("entry:", entry)
	
		assert ("essential" in entry)
		assert ("measures" in entry)
		assert ("natures" in entry)		
		assert ("unites" in entry)
	
		if (len (entry ["unites"]) >= 1):
			grove = entry ["unites"]
		
			entries_are_formatted_correctly (
				grove,
				story = story + 1
			);


def about (grove):
	entries_are_formatted_correctly (grove)

