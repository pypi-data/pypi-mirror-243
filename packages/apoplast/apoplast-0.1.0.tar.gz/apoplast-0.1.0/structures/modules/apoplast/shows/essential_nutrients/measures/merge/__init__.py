
'''
	import apoplast.shows.essential_nutrients.measures.merge as merge_measures
	merge_measures.calc (
		aggregate_measures,
		new_measures
	)
'''

from fractions import Fraction

def calc (
	aggregate_measures, 
	new_measures
):
	for measure in new_measures:
		pers = new_measures [ measure ]
		
		for per in pers:
			units = pers [per]
		
			if (per not in [ "per recipe" ]):
				raise Exception (f"The divisor found, '{ per }', was not accounted for.");
			
			for unit in units:
				#print ("unit:", unit)
			
				if (measure not in aggregate_measures):
					aggregate_measures [ measure ] = {}
					aggregate_measures [ measure ] [per] = {}
					aggregate_measures [ measure ] [per] [unit] = {}
					aggregate_measures [ measure ] [per] [unit] ["fraction string"] = "0"

			
				aggregate_measures [ measure ] [per] [unit] ["fraction string"] = str (
					Fraction (new_measures [ measure ] [per] [unit] ["fraction string"]) + 
					Fraction (aggregate_measures [ measure ] [per] [unit] ["fraction string"])
				)
				