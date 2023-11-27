
'''
	import apoplast.clouds.supp_NIH.examples as NIH_examples
	NIH_example = NIH_examples.retrieve ("tablets/multivitamin_249664.JSON")
'''


def retrieve (path):
	import pathlib
	from os.path import dirname, join, normpath

	this_directory = pathlib.Path (__file__).parent.resolve ()
	example_path = normpath (join (this_directory, path))

	import json
	with open (example_path) as FP:
		data = json.load (FP)
	

	return data