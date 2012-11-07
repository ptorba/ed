from lxml import etree
from nltk.stem import WordNetLemmatizer

from nltk.tokenize import *
from nltk.corpus import stopwords

from nltk.util import ngrams
import sys
import networkx as nx
import random
import urllib2
    
import pkg_resources
import logging
log = logging.getLogger(__name__)

def generate_gexf2(g,property,default="0"):
    #wpisz visuals
    for n in g.nodes():
        g.node[n]['viz'] = {}
        g.node[n]['viz']['color']={ 'r':str(random.randint(0,255)), 'g':str(random.randint(0,255)), 'b':str(random.randint(0,255))}
        g.node[n]['viz']['size']=g.node[n][property]
    
    nx.write_gexf(g,pkg_resources.resource_filename('ed','static/graphs/test.gexf'))
    
    
def get_words(text):
    
    words = RegexpTokenizer(r'\b[a-z]+\b').tokenize(text)
    
    stoplist = set(stopwords.words('english'))
    
    words = [x for x in words if x not in stoplist]
    
    wnl = WordNetLemmatizer()
    
    words_stemmed = [wnl.lemmatize(x) for x in words]
    
    return words_stemmed

    
def generate_graph(words_stemmed):
    ns = ngrams(words_stemmed,2)
    
    g = nx.Graph()
    
    g.add_nodes_from(words_stemmed)
    g.add_edges_from(ns)
    
    return g