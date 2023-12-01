




import proceeds.kinds.company.status as status
import proceeds.modules.line as line


import proceeds.climate as climate
border_width = climate.find () ["layout"] ["border width"]

def introduce (fields):
	company_name = fields ["name"]
	statuses = fields ["statuses"]
	
	START = (
	f"""
<article
	tile
	style="
		border: { border_width } solid black;
		border-radius: .1in;
		padding: .2in;
		margin-bottom: .1in;
	"
>
	<header
		style="
			display: flex;		
		"
	>
		<h2
			style="
				padding-right: .1in;
			"
		>company:</h2>
		<p
			style="
				text-align: center;
				padding-bottom: .1in;
				font-size: 1.5em;
			"
		>{ company_name }</p>	
	</header>
""")

	END = (
f"""
</article>"""	
	)
	
	positions_string = ""
	
	index = 0;
	for _status in statuses:
		positions_string += status.introduce (_status)
		
		if (index < len (statuses)):
			positions_string += line.create ()
			
		index += 1
		
	return START + positions_string + END;