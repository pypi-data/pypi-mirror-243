


import proceeds.climate as climate
border_width = climate.find () ["layout"] ["border width"]
	
	
def introduce (DATES):
	START = ("""
	<section>
		<h3>dates</h3>
		<ul>
""")
	
	END = ("""
		</ul>
	</section>
""")

	STRING = ""
	
	for DATE in DATES:
		STRING += (
f"""			<li>{ DATE }</li>"""
		)
	
	
	

	return START + STRING + END;