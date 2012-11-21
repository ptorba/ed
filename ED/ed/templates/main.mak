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
		<li><form id='count' action="/count">
			<input type="text" name="threshold"/>
			<input type="submit" value="count"/>
		</form></li>
		<li><form id='betweenness' action="/betweenness">
			<input type="text" name="threshold"/>
			<input type='checkbox' name="weighted">Weighted</input>
			<input type='checkbox' name="ngrams">Ngrams</input>
			<input type="submit" value="betweenness"/>
		</form></li>
				<li><form id='page_rank' action="/page_rank">
			<input type="text" name="threshold"/>
			<input type='checkbox' name="weighted">Weighted</input>
			<input type='checkbox' name="ngrams">Ngrams</input>
			<input type="submit" value="page_rank"/>
		</form></li>
		<li><form id='degree' action="/degree">
			<input type="text" name="threshold"/>
			<input type='checkbox' name="ngrams">Ngrams</input>
			<input type="submit" value="degree"/>
		</form></li>
		</ul>
		<form id='text-change' method='POST' action='/change_text'>
			<textarea name="text" rows='20' cols='60'>${request.context.text if hasattr(request.context,'text') else ''}</textarea>
			<input type='submit' value='Send'/>
		</form>
		<form id='text-reset' method='POST' action='/reset_text'>
			<input type='submit' value='Reset text'/>
		</form>
		<p>
			Property: ${prop_name}<br/>
			Max: ${max}<br/>
			Min: ${min}<br/>
		</p>
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
			 
			
			sigInst.iterNodes(function(n){
				 var attr = n['attr']['attributes']
				 for (var i in attr){
				 //	alert(i);
				 }
				 
				 attr.map(function(o){
				 	if (o.attr=='${prop_name}' && o.val<=${threshold}){
				 		n.hidden=1;
				 	}
					});
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