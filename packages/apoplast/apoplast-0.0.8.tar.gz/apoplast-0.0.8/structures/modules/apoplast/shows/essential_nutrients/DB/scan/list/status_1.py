



'''
	python3 insurance.py shows/essential_nutrients/DB/scan/list/status_1.py
'''


import apoplast.shows.essential_nutrients.DB.access as access
import apoplast.shows.essential_nutrients.DB.scan.list as essentials_list


def check_1 ():
	essentials = essentials_list.retrieve (
		essentials_DB = access.DB ()
	)
	
	for essential in essentials:
		print (essential)
	
	
checks = {
	'check 1': check_1
}