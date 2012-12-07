from pyramid.view import view_config
from lib import *
import logging
from pyramid.httpexceptions import HTTPFound, HTTPNotFound
from pyramid.url import route_url
import pkg_resources
import os
from lib.community import best_partition
log = logging.getLogger(__name__)
from operator import itemgetter


class GraphController(object):
    def __init__(self,request):
        try:
            text = urllib2.urlopen(request.static_url('ed:static/texts/user_input.txt')).read().decode('UTF-8')
        except Exception,e:
            log.debug('exception: %s',e)
            text = urllib2.urlopen(request.static_url('ed:static/texts/test.txt')).read().decode('UTF-8')
        
        
        log.debug('ngrams: %s',request.GET.get('ngrams',None))
        if request.GET.get('ngrams',None):
	    self.words = get_pairs(text, int(request.GET.get('ngrams')))
	elif request.GET.get('1tongrams',None):
	    self.words = get_pairsTo(text, int(request.GET.get('1tongrams')))
	else:
	    self.words = get_words(text)
        
        
        #log.debug('words: %s',self.words)
        self.graph = generate_graph(self.words) 
        #self.graph = generate_graph_synsets(get_synsets(text)) 
        self.partitioned_graph = best_partition(self.graph)
        #log.debug('self.partitioned_graph: %s',self.partitioned_graph)
        for n in self.graph.nodes():
            self.graph.node[n]['partition']=self.partitioned_graph[n]
        self.request = request
        self.request.context.text = text
        tl = os.listdir(pkg_resources.resource_filename('ed','static/prepared'))
        log.debug(tl)
        self.request.context.text_list = tl
        
        
    def insert_measure(self,name,values):
        partitions = {}
        for n in self.graph.nodes():
            self.graph.node[n][name]=values[n]
            partitions[self.graph.node[n]['partition']] = partitions.get(self.graph.node[n]['partition'],[])+[(n,values[n])]
            
        generate_gexf2(self.graph,name)
        
        for k,v in partitions.iteritems():
            v.sort(key=itemgetter(1),reverse=True)
        self.request.context.partitions = partitions
        
        
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
        return {'project':'ED','prop_name':'count','min':min(counts.values()),'max':max(counts.values()),'threshold':int(self.request.GET.get('threshold',-1) or -1)}
    
    
@view_config(route_name='betweenness', renderer='main.mak')
class BetweenController(GraphController):
    def __init__(self,request):
        GraphController.__init__(self,request)
        
    def __call__(self):
        betweenness = nx.betweenness_centrality(self.graph,weight='weight' if self.request.GET.get('weighted',None) else None)
        log.debug("weighted: %s",self.request.GET.get('weighted',None))
        self.insert_measure('betweenness', betweenness)
        return {'project':'ED','prop_name':'betweenness','min':min(betweenness.values()),'max':max(betweenness.values()),'threshold':float(self.request.GET.get('threshold',-1) or -1)}

    
    
@view_config(route_name='random', renderer='main.mak')
class RandomController(GraphController):
    def __init__(self,request):
        GraphController.__init__(self,request)
        
    def __call__(self):
        for n in self.graph.nodes():
            self.graph.node[n]['random']=random.randint(1,10)
            
        generate_gexf2(self.graph,'random')
        return {'project':'ED','prop_name':'','min':'','max':'','threshold':-1}


@view_config(route_name='page_rank', renderer='main.mak')
class PageRankController(GraphController):
    def __init__(self,request):
        GraphController.__init__(self,request)
        
    def __call__(self):
        page_rank = nx.pagerank(self.graph,weight='weight' if self.request.GET.get('weighted',None) else None)
        self.insert_measure('page_rank', page_rank)
        return {'project':'ED','prop_name':'page_rank','min':min(page_rank.values()),'max':max(page_rank.values()),'threshold':float(self.request.GET.get('threshold',-1) or -1)}
    

    
@view_config(route_name='degree', renderer='main.mak')
class DegreeController(GraphController):
    def __init__(self,request):
        GraphController.__init__(self,request)
        
    def __call__(self):
        deg = self.graph.degree()
        self.insert_measure('degree', deg)
        self.request.context.avg = sum(deg.values())/len(deg.values())
        return {'project':'ED','prop_name':'degree','min':min(deg.values()),'max':max(deg.values()), 'threshold':int(self.request.GET.get('threshold',-1) or -1)}


@view_config(route_name='change_text')
def change_text(request):
    log.debug('change_text, %s',request.params)

    
    if request.params.get('text_choice',None):
        text = open(pkg_resources.resource_filename('ed','static/prepared/%s'%request.params.get('text_choice')),'r').read()
    else:
        text = request.params.get('text')
    
    f = open(pkg_resources.resource_filename('ed','static/texts/user_input.txt'),'w')
    
    f.write(text)
    request.context.text = text
    f.close()
    log.debug('change_text end')
    return HTTPFound(route_url('betweenness',request))

@view_config(route_name='reset_text')
def reset_text(request):
    log.debug('reset text')
    os.remove(pkg_resources.resource_filename('ed','static/texts/user_input.txt'))
    return HTTPFound(route_url('betweenness',request))

@view_config(route_name='main', renderer='main.mak')
def main(request):
    return {'project':'ED','prop_name':'','min':'','max':'','threshold':-1}
