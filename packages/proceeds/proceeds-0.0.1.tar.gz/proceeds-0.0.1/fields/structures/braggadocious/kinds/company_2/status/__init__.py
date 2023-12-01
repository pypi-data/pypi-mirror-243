


import proceeds.climate as climate
border_width = climate.find () ["layout"] ["border width"]

import proceeds.kinds.company_2.status.places as places
import proceeds.kinds.company_2.status.dates as dates
import proceeds.kinds.company_2.status.feats as feats
import proceeds.kinds.company_2.status.positions as positions

def introduce (dictionary):
	NAMES = dictionary ["names"]

	START = (
	f"""
<article
	style="
		border: { border_width } solid black;
		border-radius: .1in;
		padding: .25in;
		
		margin-bottom: .1in;
	"
>
	{ positions.introduce (NAMES) }
""")

	END = (
f"""
</article>"""	
	)	

	structure = ""
	if ("places" in dictionary):
		structure += places.introduce (dictionary ["places"])
		
	if ("dates" in dictionary):
		structure += dates.introduce (dictionary ["dates"])
		
	if ("feats" in dictionary):
		structure += feats.introduce (dictionary ["feats"])

	return START + structure + END;