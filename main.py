import gexf
from lxml import etree
from nltk.stem import WordNetLemmatizer

from nltk.tokenize import *
from nltk.corpus import stopwords

from nltk.util import ngrams
import sys
import networkx as nx
import random

    
def generate_graph(g,filename='test.gexf'):  
    ge = gexf.Gexf("ED","ED test")
    graph=ge.addGraph("undirected","static","a test graph")
    count = graph.addNodeAttribute("count","0")
    betwenness = graph.addNodeAttribute("betweenness","0")
    print count,betwenness
    
    edge_id = 0
    for n in g.nodes():
        node = graph.addNode(n,n,r=str(random.randint(0,255)),g=str(random.randint(0,255)),b=str(random.randint(0,255)),size=g.node[n]['count']*10)
        node.addAttribute(count,str(g.node[n]['count']))
        node.addAttribute(betwenness,str(g.node[n]['betweenness']))

    for e1,e2 in g.edges():
            edge = graph.addEdge(str(edge_id),e1,e2,r="0",g="255",b="0",weight="1.0")
            edge_id+=1
    f = open(filename,'w')
    f.write(etree.tostring(ge.getXML(), pretty_print=True))
    f.close()
    
if __name__=="__main__":
    text = open('text.txt','r').read().decode('UTF-8')
    
    words = RegexpTokenizer(r'\b[a-z]+\b').tokenize(text)
    
    stoplist = set(stopwords.words('english'))
    
    words = [x for x in words if x not in stoplist]
    

    
    
    wnl = WordNetLemmatizer()
    
    words_stemmed = [wnl.lemmatize(x) for x in words]
    
    counts = {}
    for w in words_stemmed:
        counts[w] = counts.get(w,0)+1
    #print words_stemmed
    ns = ngrams(words_stemmed,2)
    #print ns
    
    g = nx.Graph()
    
    g.add_nodes_from(words_stemmed)
    g.add_edges_from(ns)
    
    print len(words_stemmed), len(g.nodes())
    print len(ns), len(g.edges())
    
    for k,v in counts.iteritems():
        g.node[k]['count']=v
    
    centrality = nx.betweenness_centrality(g)
    for k,v in centrality.iteritems():
        g.node[k]['betweenness']=v

    generate_graph(g)
