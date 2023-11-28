

'''
	
'''

import lymphatic.system.climate as ly_system_climate

def change_ports ():
	ly_system_climate.change ("ports", {
		"driver": 18871,
		"cluster": 0,
		"http": 0	
	})