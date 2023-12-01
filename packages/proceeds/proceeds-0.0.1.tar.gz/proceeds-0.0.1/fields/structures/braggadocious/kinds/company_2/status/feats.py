



import proceeds.climate as climate
border_width = climate.find () ["layout"] ["border width"]
	
	
def introduce (FEATS):
	START = ("""
	<section>
		<h3>feats</h3>
		<ul>
""")
	
	END = ("""
		</ul>
	</section>
""")

	STRING = ""
	
	for FEAT in FEATS:
		STRING += (
f"""			<li>{ FEAT }</li>"""
		)

	return START + STRING + END;