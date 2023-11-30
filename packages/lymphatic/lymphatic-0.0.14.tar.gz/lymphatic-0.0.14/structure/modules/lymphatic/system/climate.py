
'''
	Maybe the only things that use this currently
	are "start" and "connect".
'''

'''
	import lymphatic.system.climate as ly_system_climate
	ly_system_climate.change ("ports", {
		"driver": 18871,
		"cluster": 0,
		"http": 0	
	})
'''

'''
	import lymphatic.system.climate as ly_system_climate
	ports = ly_system_climate.find ("ports")
'''

import copy

climate = {
	"ports": {
		"driver": 18871,
		"cluster": 0,
		"http": 0
	}
}

def change (field, plant):
	climate [ field ] = plant


def find (field):
	return copy.deepcopy (climate) [ field ]