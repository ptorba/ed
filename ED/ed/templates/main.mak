<html>
	<head>
		<link rel="shortcut icon" href="${request.static_url('ed:static/favicon.ico')}" />
		<link rel="stylesheet" href="${request.static_url('ed:static/main.css')}" />
		<script type="text/javascript" src="${request.static_url('ed:static/js/sigma.concat.js')}"></script>
		<script type="text/javascript" src="${request.static_url('ed:static/js/sigma.parseGexf.js')}"></script>
		<script type="text/javascript" src="${request.static_url('ed:static/js/sigma.forceatlas2.js')}"></script>
		
	</head>
		
	<body>
		<p>Hello</p>
		<div id='sigma'>
			
		</div>
		<div class='weird'></div>
	</body>
	<script type="text/javascript">
		function init() {
			// Instanciate sigma.js and customize rendering :
			var sigInst = sigma.init(document.getElementById('sigma')).drawingProperties({
			defaultLabelColor: '#fff',
			defaultLabelSize: 14,
			defaultLabelBGColor: '#fff',
			defaultLabelHoverColor: '#000',
			labelThreshold: 6,
			defaultEdgeType: 'curve'
			}).graphProperties({
			minNodeSize: 0.5,
			maxNodeSize: 5,
			minEdgeSize: 1,
			maxEdgeSize: 1
			}).mouseProperties({
			maxRatio: 32
			});
			 
			// Parse a GEXF encoded file to fill the graph
			// (requires "sigma.parseGexf.js" to be included)
			sigInst.parseGexf("${request.static_url('ed:static/graphs/test.gexf')}");
			 
			// Draw the graph :
			sigInst.draw();
			
			
			//start ForceAtlas
			sigInst.startForceAtlas2();
		}
			 
		if (document.addEventListener) {
			document.addEventListener("DOMContentLoaded", init, false);
		} else {
			window.onload = init;
		}
	</script>
</html>