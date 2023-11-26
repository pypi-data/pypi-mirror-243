
'''
	python3 insurance.py shows/essential_nutrients/DB/status_1.py
'''


import apoplast.shows.essential_nutrients.DB.access as access
	
def check_1 ():
	essentials_DB = access.DB ()
	
	print (essentials_DB)
	
	
checks = {
	'check 1': check_1
}