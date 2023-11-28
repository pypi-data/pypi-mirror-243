
'''
	import apoplast.shows.essential_nutrients.grove.seek_name_or_accepts as grove_seek_name_or_accepts
	protein = grove_seek_name_or_accepts.politely (
		grove = grove,
		name_or_accepts = "protein"
	)
'''
import apoplast.shows.essential_nutrients.grove.seek as grove_seek

def politely (
	name_or_accepts = "",
	grove = []
):
	name_or_accepts = name_or_accepts.lower ()

	checked = []
	def for_each (entry):		
		accepts = []
		if ("accepts" in entry ["essential"]):
			accepts = entry ["essential"] ["accepts"]
	
		patterns = [
			* entry ["essential"] ["names"],
			* accepts
		]	
		
		checked.append (patterns)
			
		for name in patterns:
			if (name_or_accepts == name.lower ().strip ()):			
				return True;
			
		return False

	entry = grove_seek.beautifully (
		grove = grove,
		for_each = for_each
	)
	if (type (entry) != dict):
		print (entry)
		#print (checked)
		raise Exception (f'''
			
			The "name" or "accepts" "{ name_or_accepts }" was not found.
			
		''')

	return entry