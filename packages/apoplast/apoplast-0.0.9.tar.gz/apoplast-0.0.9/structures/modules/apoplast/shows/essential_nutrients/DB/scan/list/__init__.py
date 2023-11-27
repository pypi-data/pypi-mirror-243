
'''
#
#	actual
#
import apoplast.shows.essential_nutrients.DB.scan.list as essentials_list_scan
essentials_DB_list = essentials_list_scan.retrieve ()
'''	

'''
#
#	extra
#
import apoplast.shows.essential_nutrients.DB.scan.list as essentials_list
import apoplast.shows.essential_nutrients.DB.access as access
essentials = essentials_list.retrieve (
	essentials_DB = access.DB ()
)
'''
	
import apoplast.shows.essential_nutrients.DB.access as access

def retrieve (
	essentials_DB = access.DB ()
):	
	return essentials_DB.all ()