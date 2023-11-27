

'''
	import apoplast.shows.essential_nutrients.grove.seek as grove_seek
	
	#
	#	This does a lower casing of all the names in the essential ingredient names
	#
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
'''

'''
	def for_each (entry):
		names = entry ["essential"] ["names"]
		for name in names:
			if (name.lower () == "protein"):
				return True
				
		return False		

	import apoplast.shows.essential_nutrients.grove.seek as grove_seek
	protein = grove_seek.beautifully (
		grove = grove,
		for_each = for_each
	)
'''

'''
	description:
		This loops through the entire grove,
		unless True is returned.
'''

'''
{
	"essential": {},
	"natures": [],
	"unites": []
}
'''

'''
	# recursive
'''
import apoplast.shows.essential_nutrients.DB.scan.list as essentials_list_scan
import apoplast.shows.essential_nutrients.DB.access as access

def beautifully (
	grove,
	for_each = lambda * p, ** k : None,
	
	story = 1
):
	for entry in grove:
		if (for_each (entry)):
			return entry
		
		if (len (entry ["unites"]) >= 1):
			grove = entry ["unites"]
		
			found = beautifully (
				grove,
				for_each = for_each,
				story = story + 1
			);
			if (type (found) == dict):
				return found;
		
		

	return None