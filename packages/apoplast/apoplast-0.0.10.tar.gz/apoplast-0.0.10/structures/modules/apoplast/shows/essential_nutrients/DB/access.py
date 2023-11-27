



'''
	priorities, plan:
		
		This should be for accessing the list of essential 
		nutrients, and the nutrients that they are comprised of.
		
		There could be another access point (like a rethinkdb weave
		access point) for accessing a network weave.
'''

'''
	#
	#	Accessing the core DB:
	#
	import apoplast.shows.essential_nutrients.DB.access as access
	essentials_DB = access.DB ()
'''

'''
	#
	#	Accessing another DB (replica, etc.):
	#
	import apoplast.shows.essential_nutrients.DB.access as access
	import apoplast.shows.essential_nutrients.DB.path as essentials_DB_path
	essentials_DB = access.DB (
		path = essentials_DB_path.find ()
	)
'''

from tinydb import TinyDB, Query
import apoplast.shows.essential_nutrients.DB.path as essentials_DB_path
	
def DB (
	path = essentials_DB_path.find (),
	sort_keys = True
):
	DB = TinyDB (
		path, 
		sort_keys = sort_keys
	)
	
	return DB;