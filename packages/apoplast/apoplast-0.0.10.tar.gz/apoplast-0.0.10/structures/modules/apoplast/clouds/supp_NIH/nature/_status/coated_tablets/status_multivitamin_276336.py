

'''
	status_multivitamin_276336
'''
'''
	python3 insurance.py clouds/supp_NIH/nature/_status/coated_tablets/status_multivitamin_276336.py
'''

import apoplast.clouds.supp_NIH.nature as supp_NIH_nature
import apoplast.clouds.supp_NIH.examples as NIH_examples

import json

def check_1 ():	
	supp_NIH_example = NIH_examples.retrieve ("coated tablets/multivitamin_276336.JSON")
	nature = supp_NIH_nature.create (supp_NIH_example)
	
	print (json.dumps (nature, indent = 4))
	
	return;
	
checks = {
	"check 1": check_1
}