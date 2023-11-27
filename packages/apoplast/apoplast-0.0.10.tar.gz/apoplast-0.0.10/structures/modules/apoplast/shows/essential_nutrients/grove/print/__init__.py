

'''
import apoplast.shows.essential_nutrients.grove.print as print_grove
print_grove.beautifully (
	grove
)
'''


'''
import apoplast.shows.essential_nutrients.grove_prototype.print as print_grove_prototype
print_grove_prototype.beautifully (
	grove_prototype = [{
		"names": [ "carbohydrates" ],
		"unites": [{
			"names": [ "fiber" ],
			"unites": []
		}]
	}]
)
'''
import apoplast.shows.essential_nutrients.grove.sort as sort_the_grove

import copy

def beautifully (grove):
	sort_the_grove.charismatically (grove)

	print ()
	print ("The essential nutrients grove:")
	print ()

	essentials_count = 0

	def print_this (unites, story = 1):
		nonlocal essentials_count;
	
		for prototype in unites:
			essentials_count += 1
		
			prototype_copy = copy.deepcopy (prototype)
			del prototype_copy ['unites']
			
			accepts = []
			if ("accepts" in prototype_copy ["essential"]):
				accepts = prototype_copy ["essential"] ["accepts"]
			
			indent = " " * ((story - 0) * 4)
			print (f'''{ 
				indent 
			}{
				prototype_copy ["essential"] ["names"] 
			}{
				accepts
			}[ { 
				prototype_copy ["essential"] ["region"] 
			} ]''')
			
			if (len (prototype ["unites"]) >= 1):
				print_this (
					prototype ["unites"],
					story = story + 1
				)

	print_this (grove)
	print ()
	print ("	essentials count =", essentials_count)
	print ()


	class Proceeds:
		count = ""

	proceeds = Proceeds ();
	proceeds.count = essentials_count

	return proceeds