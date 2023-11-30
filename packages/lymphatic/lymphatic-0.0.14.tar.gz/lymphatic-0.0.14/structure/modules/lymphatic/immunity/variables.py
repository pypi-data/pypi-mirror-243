
'''
import lymphatic.immunity.variables as variables
variables.change ("utilize", True)
'''

'''
import lymphatic.immunity.variables as variables
if (variables.utilize):
	ports = variables.find ("ports")
	

variables.change ("ports", {
	"driver": 18871,
	"cluster": 0,
	"http": 0
})


'''

import copy

climate = {
	"utilize": False,
	"ports": {
		"driver": 18871,
		"cluster": 0,
		"http": 0
	}
}

def utilize ():
	return climate ["utilize"]

def change (field, plant):
	#global climate;
	climate [ field ] = plant

	return;

def find (field):
	return copy.deepcopy (climate) [ field ] 