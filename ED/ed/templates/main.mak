<html>
	<head>
		<link rel="shortcut icon" href="${request.static_url('ed:static/favicon.ico')}" />
		<link rel="stylesheet" href="${request.static_url('ed:static/main.css')}" />
		<script type="text/javascript" src="${request.static_url('ed:static/js/sigma.concat.js')}"></script>
		<script type="text/javascript" src="${request.static_url('ed:static/js/sigma.parseGexf.js')}"></script>
		<script type="text/javascript" src="${request.static_url('ed:static/js/sigma.forceatlas2.js')}"></script>
		
	</head>
		
	<body>
		<div style="float:left;">
		<p>Hello ${project}</p>
		<p>Size based on:</p>
		<ul>
		<li><a href="/count">count</a></li>
		<li><a href="/betweenness">betweenness</a></li>
		<li><a href="/random">random</a></li>
		<li><a href="/page_rank">page rank</a></li>
		<li><a href="/degree">degree</a></li>
		</ul>
		<form id='text-change' method='POST' action='/change_text'>
			<textarea name="text" rows='20' cols='60'>${request.context.text if hasattr(request.context,'text') else ''}</textarea>
			<input type='submit' value='Send'/>
		</form>
		<form id='text-reset' method='POST' action='/reset_text'>
			<input type='submit' value='Reset text'/>
		</form>
		</div>
		<div id='visualize-wrapper' style="float:right;">
			
		<div id='sigma'>
			
		</div>
		<input type="submit" id='startfa' value="Start ForceAtlas2"/>
		<input type="submit" id='stopfa' value="Stop ForceAtlas2"/>
		</div>
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
			defaultEdgeType: 'curve',
			}).graphProperties({
			minNodeSize: 1,
			maxNodeSize: 20,
			minEdgeSize: 0.1,
			maxEdgeSize: 4
			}).mouseProperties({
			maxRatio: 32
			});
			 
			// Parse a GEXF encoded file to fill the graph
			// (requires "sigma.parseGexf.js" to be included)
			sigInst.parseGexf("${request.static_url('ed:static/graphs/test.gexf')}");
			 
			 sigInst.bind('overnodes',function(event){
				var nodes = event.content;
				var neighbors = {};
				sigInst.iterEdges(function(e){
				if(nodes.indexOf(e.source)>=0 || nodes.indexOf(e.target)>=0){
					neighbors[e.source] = 1;
					neighbors[e.target] = 1;
				}
				}).iterNodes(function(n){
					if(!neighbors[n.id]){
						n.hidden = 1;
					} else {
						n.hidden = 0;
					}
					}).draw(2,2,2);
				}).bind('outnodes',function(){
					sigInst.iterEdges(function(e){
					e.hidden = 0;
					}).iterNodes(function(n){
						n.hidden = 0;
					}).draw(2,2,2);
				});
			 
			 
			// Draw the graph :
			sigInst.draw();
			
			
			//start ForceAtlas
			
			sigInst.startForceAtlas2();
			setTimeout(function() {
				sigInst.stopForceAtlas2();
			},5000);
			
			function startForceAtlas() {
				sigInst.startForceAtlas2();
			} 
			function stopForceAtlas() {
				sigInst.stopForceAtlas2();
			}
			
			document.getElementById('startfa').addEventListener('click',startForceAtlas,false);
			document.getElementById('stopfa').addEventListener('click',stopForceAtlas,false);
		}
			 
		if (document.addEventListener) {
			document.addEventListener("DOMContentLoaded", init, false);
		} else {
			window.onload = init;
		}
	</script>
</html>