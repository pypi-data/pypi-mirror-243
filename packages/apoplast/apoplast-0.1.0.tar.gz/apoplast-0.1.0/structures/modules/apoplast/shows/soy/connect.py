
'''
	import apoplast.shows.soy.connect as connect
	[ r, c ] = connect.it ()
'''

import lymphatic.system.connect as ly_connect

def it ():
	
	[ r, c ] = ly_connect.start ()
	
	return [ r, c ]