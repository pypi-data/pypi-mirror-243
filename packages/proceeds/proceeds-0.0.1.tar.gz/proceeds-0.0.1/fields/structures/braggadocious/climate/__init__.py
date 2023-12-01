




'''
import proceeds.climate as climate
climate.change ("", {})
'''

'''
import proceeds.climate as climate
border_width = climate.find () ["layout"] ["border width"]
border_radius = climate.find () ["layout"] ["border radius"]
repulsion = climate.find () ["layout"] ["repulsion"]

'''

import copy

climate = {
	"layout": {
		"border width": ".03in",
		"border radius": ".07in",
		
		"repulsion": "0.1in"
	},
	"palette": {
		1: "#FFF",
		2: "#000"
	}
}

def change (ellipse, planet):
	climate [ ellipse ] = planet


def find ():
	return copy.deepcopy (climate)