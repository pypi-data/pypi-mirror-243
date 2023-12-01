

'''
{
	"kind": "projects",
	"fields": {
		"name": "project 1",
		"summary": ""
	}
}
'''

'''
import proceeds.kinds.project as project
project.preset ({
	"name": "",
	"description": ""
})
'''

from mako.template import Template

import proceeds.climate as climate
border_width = climate.find () ["layout"] ["border width"]
border_radius = climate.find () ["layout"] ["border radius"]
repulsion = climate.find () ["layout"] ["repulsion"]

def present (fields):
	name = fields ['name']
	summary = fields ['summary']
	
	if (type (summary) == list):
		summary = "\n".join (summary)
	
	
	this_template = f"""
<article
	tile
	style="
		border: { border_width } solid black;
		border-radius: { border_radius };
		padding: .15in;
		
		margin-bottom: { repulsion };
	"
>
	<header>
		<h1>{ name }</h1>	
	</header>
	<p style="white-space: pre-wrap;">{ summary }</p>
</article>
	"""
	
	return this_template;
	
	return Template (this_template).render (
		name = name,
		summary = summary
	)
	
	
	
	
	
	
	
	
#