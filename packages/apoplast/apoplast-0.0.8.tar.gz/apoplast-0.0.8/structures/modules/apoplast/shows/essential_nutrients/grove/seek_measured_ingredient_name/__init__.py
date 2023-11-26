
'''
	import apoplast.shows.essential_nutrients.grove.seek_measured_ingredient_name as grove_seek_measured_ingredient_name
	protein = grove_seek_measured_ingredient_name.politely (
		grove = grove,
		measured_ingredient_name = "protein"
	)
'''
import apoplast.shows.essential_nutrients.grove.seek as grove_seek

def politely (
	measured_ingredient_name = "",
	grove = []
):
	measured_ingredient_name = measured_ingredient_name.lower ()

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
			if (measured_ingredient_name == name.lower ().strip ()):			
				return True;
			
		return False

	entry = grove_seek.beautifully (
		grove = grove,
		for_each = for_each
	)
	if (type (entry) != dict):
		print (entry)
		#print (checked)
		raise Exception ("A measured ingredient was not found.")

	return entry