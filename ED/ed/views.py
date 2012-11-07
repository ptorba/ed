from pyramid.view import view_config
from lib import *
import logging
log = logging.getLogger(__name__)



class GraphController(object):
    def __init__(self,request):
        text = urllib2.urlopen(request.static_url('ed:static/texts/test.txt')).read().decode('UTF-8')
        self.words = get_words(text)
        self.graph = generate_graph(self.words) 

        
        
@view_config(route_name='count', renderer='main.mak')    
class CountController(GraphController):
    def __init__(self,request):
        GraphController.__init__(self,request)
        self.request = request
            
    def __call__(self):
        log.debug(self.request.static_path('ed:static/graphs'))
        counts = {}
        for w in self.words:
            counts[w] = counts.get(w,0)+1
        
        for n in self.graph.nodes():
            self.graph.node[n]['count'] = counts[n]
        
        
        generate_gexf2(self.graph,'count')
        return {'project':'ED'}
    
    
@view_config(route_name='betweenness', renderer='main.mak')
class BetweenController(GraphController):
    def __init__(self,request):
        GraphController.__init__(self,request)
        #self.request = request
    

    def __call__(self):
        betweenness = nx.betweenness_centrality(self.graph)
        
        for n in self.graph.nodes():
            self.graph.node[n]['betweenness']=betweenness[n]
            
        generate_gexf2(self.graph,'betweenness')
        return {'project':'ED'}
    
    
@view_config(route_name='random', renderer='main.mak')
class RandomController(GraphController):
    def __init__(self,request):
        GraphController.__init__(self,request)
        #self.request = request
        
    def __call__(self):
        for n in self.graph.nodes():
            self.graph.node[n]['random']=random.randint(1,10)
            
        generate_gexf2(self.graph,'random')
        return {'project':'ED'}


@view_config(route_name='page_rank', renderer='main.mak')
class PageRankController(GraphController):
    def __init__(self,request):
        GraphController.__init__(self,request)
        #self.request = request
        
    def __call__(self):
        page_rank = nx.pagerank(self.graph)
        for n in self.graph.nodes():
            self.graph.node[n]['page_rank']=page_rank[n]
            
        generate_gexf2(self.graph,'page_rank')
        return {'project':'ED'}


@view_config(route_name='main', renderer='main.mak')
def main(request):
    return {'project':'ED'}
