

'''
	import apoplast._ellipses as ellipses
	API_USDA_ellipse = ellipses.scan () ['USDA'] ['food']
	API_NIH_ellipse = ellipses.scan () ['NIH'] ['supplements']
'''

'''
/online ellipsis/cyte/ellipsis.json 

{
	"USDA": {
		"food": ""
	},
	"NIH": {
		"supplements": ""
	}
}
'''

import json
fp = open ("/online ellipsis/cyte/ellipsis.json", "r")
bounce = json.loads (fp.read ())
fp.close ()


def scan ():
	return bounce