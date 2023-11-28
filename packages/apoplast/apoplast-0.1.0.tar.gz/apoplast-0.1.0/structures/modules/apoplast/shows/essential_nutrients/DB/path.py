



'''
	import apoplast.shows.essential_nutrients.DB.path as essentials_DB_path
	path = essentials_DB_path.find ()
'''




import pathlib
from os.path import dirname, join, normpath

this_folder = pathlib.Path (__file__).parent.resolve ()

paths = {
	"DB": normpath (join (this_folder, "essentials.JSON"))
}

def find ():
	return paths ["DB"]




