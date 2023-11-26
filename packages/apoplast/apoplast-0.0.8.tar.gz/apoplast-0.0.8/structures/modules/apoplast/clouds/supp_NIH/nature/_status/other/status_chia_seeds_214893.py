

'''
status_chia_seeds_214893
'''
'''
	python3 insurance.py clouds/supp_NIH/nature/_status/other/status_chia_seeds_214893.py
'''

import apoplast.clouds.supp_NIH.nature as supp_NIH_nature
import apoplast.clouds.supp_NIH.examples as NIH_examples

import json

def check_1 ():	
	supp_NIH_example = NIH_examples.retrieve ("other/chia_seeds_214893.JSON")
	nature = supp_NIH_nature.create (supp_NIH_example)
	
	print (json.dumps (nature, indent = 4))
	
	return;
	
checks = {
	"check 1": check_1
}