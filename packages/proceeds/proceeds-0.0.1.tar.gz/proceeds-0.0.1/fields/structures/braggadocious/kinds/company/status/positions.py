


def introduce (names):
	names_string = ""
	for name in names:
		names_string += (f"""
			<li>{ name }</li>		
		""")
		
	template = f"""
	<header>
		<h3>positions</h3>
		<ul>
			{ names_string }
		</ul>
	</header>
	"""

	return template