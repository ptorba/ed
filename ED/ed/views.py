from pyramid.view import view_config
from lib import *
import logging
from pyramid.httpexceptions import HTTPFound, HTTPNotFound
from pyramid.url import route_url
import pkg_resources
import os
log = logging.getLogger(__name__)



class GraphController(object):
    def __init__(self,request):
        try:
            text = urllib2.urlopen(request.static_url('ed:static/texts/user_input.txt')).read().decode('UTF-8')
        except Exception,e:
            log.debug('exception: %s',e)
            text = urllib2.urlopen(request.static_url('ed:static/texts/test.txt')).read().decode('UTF-8')
        
        self.words = get_words(text)
        log.debug('words: %s',self.words)
        self.graph = generate_graph(self.words) 
        self.request = request
        self.request.context.text = text

        
        
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
        
    def __call__(self):
        for n in self.graph.nodes():
            self.graph.node[n]['random']=random.randint(1,10)
            
        generate_gexf2(self.graph,'random')
        return {'project':'ED'}


@view_config(route_name='page_rank', renderer='main.mak')
class PageRankController(GraphController):
    def __init__(self,request):
        GraphController.__init__(self,request)
        
    def __call__(self):
        page_rank = nx.pagerank(self.graph)
        for n in self.graph.nodes():
            self.graph.node[n]['page_rank']=page_rank[n]
            
        generate_gexf2(self.graph,'page_rank')
        return {'project':'ED'}
    
@view_config(route_name='degree', renderer='main.mak')
class DegreeController(GraphController):
    def __init__(self,request):
        GraphController.__init__(self,request)
        
    def __call__(self):
        deg = self.graph.degree()
        for n in self.graph.nodes():
            self.graph.node[n]['degree']=deg[n]
            
        generate_gexf2(self.graph,'degree')
        return {'project':'ED'}


@view_config(route_name='change_text')
def change_text(request):
    log.debug('change_text')
    text = request.params.get('text')
    f = open(pkg_resources.resource_filename('ed','static/texts/user_input.txt'),'w')
    f.write(text)
    request.context.text = text
    f.close()
    log.debug('change_text end')
    return HTTPFound(route_url('count',request))

@view_config(route_name='reset_text')
def reset_text(request):
    log.debug('reset text')
    os.remove(pkg_resources.resource_filename('ed','static/texts/user_input.txt'))
    return HTTPFound(route_url('count',request))

@view_config(route_name='main', renderer='main.mak')
def main(request):
    return {'project':'ED'}
