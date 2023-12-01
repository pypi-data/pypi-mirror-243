



def build ():
	html_document = {
		"start": (
"""
<html>
<head></head>
<body>
<style>

body {
	padding-bottom: 10in;
}

h1, h2, h3, p, ul, li {
	margin: 0;
	padding: 0;
}

h1, h2, h3 {
	font-weight: normal;
	font-style: italic;
}

p {
	font-weight: normal;
	font-style: normal;
}

li {
	/* list-style-type: circle; */
	list-style-type: disclosure-closed
}

ul {
	padding-left: 20px;
}

main {
	position: relative;
	margin: 0 auto;
	width: 8.5in;
	height: 11in;
}

</style>
<main>
	<article page>
"""),
		"main": "",
		"end": (
"""
	</article>
</main>
<script>
document.addEventListener("DOMContentLoaded", function(event) {

	
	
});
</script>
</body>
""")
	}
	
	return html_document