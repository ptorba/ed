<html>
	<head>
		<link rel="shortcut icon" href="${request.static_url('ed:static/favicon.ico')}" />
		<link rel="stylesheet" href="${request.static_url('ed:static/main.css')}" />
		<script type="text/javascript" src="${request.static_url('ed:static/js/sigma.concat.js')}"></script>
		<script type="text/javascript" src="${request.static_url('ed:static/js/sigma.parseGexf.js')}"></script>
		<script type="text/javascript" src="${request.static_url('ed:static/js/sigma.forceatlas2.js')}"></script>
	</head>
	<style>
		input[type="text"] {
			width: 40px;
		}
	</style>
	<body>
		<div style="float:left; width:500px;">
		<p>Hello ${project}</p>
		<p>Size based on:</p>
		<ul>
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
			<textarea name="text" rows='20' cols='60'>${request.context.text if hasattr(request.context,'text') else ''}</textarea><br/>
			% if hasattr(request.context,'text_list'):
			% for text in request.context.text_list:
				<input type="radio" name="text_choice" value="${text}">${text}</input><br/>
			% endfor
			% endif
			<input type='submit' value='Send'/>
		</form>
		<form id='text-reset' method='POST' action='/reset_text'>
			<input type='submit' value='Reset text'/>
		</form>
		<p>
			Property: ${prop_name}<br/>
			Max: ${max}<br/>
			Min: ${min}<br/>
			Avg: ${request.context.avg if hasattr(request.context,'avg') else ''}
		</p>
		% if hasattr(request.context,'partitions'):
		<table>
			<tr>
				<th>Partition</th><th>Node</th><th>${prop_name}</th>
			</tr>
			% for k,v in request.context.partitions.iteritems():
				<tr>
					<td>${k} (size: ${len(request.context.partitions[k])})</td><td></td><td></td>
				</tr>
				% for item in v[:5]:
					<tr>
						<td>${k}</td><td>${item[0]}</td><td>${item[1]}</td>
					</tr>
				% endfor
			% endfor
		</table>
		% endif
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
			labelThreshold: 4,
			defaultEdgeType: 'curve',
			}).graphProperties({
			minNodeSize: 1,
			maxNodeSize: 20,
			minEdgeSize: 0.1,
			maxEdgeSize: 1
			}).mouseProperties({
			maxRatio: 32
			});
			 
			// Parse a GEXF encoded file to fill the graph
			// (requires "sigma.parseGexf.js" to be included)
			sigInst.parseGexf("${request.static_url('ed:static/graphs/test.gexf')}");
			 
			 sigInst.bind('overnodes',function(event){
				var nodes = event.content;
				
				var node = sigInst.getNodes(nodes)[0]
				sigInst.iterNodes(function(n){
					if(node.color!=n.color){
						n.hidden = 1;
					}
					else{
						n.hidden =0;
					}
				}).draw(2,2,2);
				}).bind('outnodes',function(){
					sigInst.iterEdges(function(e){
					e.hidden = 0;
					}).iterNodes(function(n){
						n.hidden = 0;
						var attr = n['attr']['attributes']
				 		attr.map(function(o){
				 			if (o.attr=='${prop_name}' && o.val<=${threshold}){
				 				n.hidden=1;
				 			}
					});
					}).draw(2,2,2);
				});
			 
			
			sigInst.iterNodes(function(n){
				 var attr = n['attr']['attributes']
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