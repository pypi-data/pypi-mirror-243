



import proceeds.climate as climate
border_width = climate.find () ["layout"] ["border width"]

def introduce (PLACES):
	START = ("""
	<section>
		<h3>places</h3>
		<ul>
""")
	
	END = ("""
		</ul>
	</section>
""")

	STRING = ""
	
	for PLACE in PLACES:
		STRING += (
f"""			<li>{ PLACE }</li>"""
		)
	
	
	

	return START + STRING + END;