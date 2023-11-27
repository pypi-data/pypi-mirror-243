


'''
	python3 insurance.py shows/essential_nutrients/DB/scan/seek_next_region/status_actual/status_1.py
'''
import apoplast.shows.essential_nutrients.DB.scan.seek_next_region as seek_next_region
import apoplast.shows.essential_nutrients.DB.access as access
	
def check_1 ():
	next_region = seek_next_region.politely (
		essentials_DB = access.DB ()
	)
	print ("next region:", next_region)	
	
	assert (type (next_region) == int)
	
checks = {
	'check 1': check_1
}