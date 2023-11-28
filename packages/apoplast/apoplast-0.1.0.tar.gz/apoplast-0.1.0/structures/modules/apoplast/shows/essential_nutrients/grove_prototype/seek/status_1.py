

'''
	python3 insurance.py shows/essential_nutrients/grove_prototype/seek/status_1.py
'''


import apoplast.shows.essential_nutrients.grove_prototype.seek as grove_seek
import apoplast.shows.essential_nutrients.DB.access as access
import apoplast.shows.essential_nutrients.DB.scan.list as essentials_list_scan

def check_1 ():
	essentials_list = [{
		"names": [ "carbohydrates" ],
		"unites": [{
			"names": [ "fiber" ],
			"unites": []
		}]
	}]
	
	amount = 0
	def for_each (essential):
		nonlocal amount;
		amount += 1
		return;
	
	grove_seek.beautifully (
		essentials_list,
		for_each = for_each
	)
	
	assert (amount == 2);
	
	return;
	
	
	
checks = {
	'check 1': check_1
}