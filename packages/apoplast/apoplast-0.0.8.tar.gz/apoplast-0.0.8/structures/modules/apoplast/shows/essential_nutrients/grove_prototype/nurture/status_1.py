


'''
	python3 insurance.py shows/essential_nutrients/grove_prototype/nurture/status_1.py
'''

import apoplast.shows.essential_nutrients.grove_prototype.nurture as grove_prototype_nurture
import apoplast.shows.essential_nutrients.grove_prototype.print as print_grove_prototype
import apoplast.shows.essential_nutrients.grove_prototype.seek as grove_seek

import apoplast.shows.essential_nutrients.DB.scan.list as essentials_list_scan

import apoplast.insure.equality as equality


def check_1 ():
	essentials_DB_list = essentials_list_scan.retrieve ()

	grove_prototype = grove_prototype_nurture.beautifully ()
	print_grove_prototype.beautifully (
		grove_prototype
	)
	
	amount = 0
	def for_each (essential):
		nonlocal amount;
		amount += 1
		return;

	essentials_grove_nutrient = grove_seek.beautifully (
		essentials = grove_prototype,
		for_each = for_each
	)
	
	equality.check (
		len (essentials_DB_list),
		amount
	)
		

	return;
	
checks = {
	'check 1': check_1
}


