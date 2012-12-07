from lxml import etree
from nltk.stem import WordNetLemmatizer

from nltk.tokenize import *
from nltk.corpus import stopwords, wordnet
import nltk.data

from nltk.util import ngrams
import sys
import networkx as nx
import random
import urllib2
import colorsys
import itertools
    
import pkg_resources
import logging
log = logging.getLogger(__name__)

def generate_gexf2(g,property,default="0"):
    partitions = set([g.node[n]['partition'] for n in g.nodes()])
    colors = {}
    for p in partitions:
        colors[p] = {'r':str(random.randint(0,255)), 'g':str(random.randint(0,255)), 'b':str(random.randint(0,255)) }
    #wpisz visuals
    for n in g.nodes():
        g.node[n]['viz'] = {}
        g.node[n]['viz']['color']=colors[g.node[n]['partition']]
        g.node[n]['viz']['size']=g.node[n][property]
    
    nx.write_gexf(g,pkg_resources.resource_filename('ed','static/graphs/test.gexf'),version='1.2draft')
    
def get_sentences(text):
    s = nltk.data.load('tokenizers/punkt/english.pickle')
    sentences = s.tokenize(text)
    stoplist = set(stopwords.words('english'))
    
    new = []
    
    #words = RegexpTokenizer(r'\b[a-z]+\b').tokenize(text)
    
    wnl = WordNetLemmatizer()
    
    for words in sentences:
	words = RegexpTokenizer(r'\b[a-z]+\b').tokenize(words)
	#words = [x for x in words if x not in stoplist]
	words = [wnl.lemmatize(x) for x in words]
	new.append(tuple(words))
    
    
    
    #words_stemmed = [wnl.lemmatize(x) for x in words]
    
    return new
    
def get_words(text):
    
    words = RegexpTokenizer(r'\b[a-z]+\b').tokenize(text)
    
    stoplist = set(stopwords.words('english'))
    
    words = [x for x in words if x not in stoplist]
    
    wnl = WordNetLemmatizer()
    
    words_stemmed = [wnl.lemmatize(x) for x in words]
    
    return words_stemmed


def get_synsets(text):
    words = get_words(text)
    return [{'word' : w,'synsets': set(wordnet.synsets(w))} for w in words]
    

def get_pairs(text,i=2):
    words = get_words(text)
    pairs = ngrams(words,i)
    #pairs.extend(ngrams(words,3))
    #pairs.extend(ngrams(words,2))
    return pairs
    
def get_pairsTo(text,i=2):
    words = get_words(text)
    pairs = map(lambda x: (x,), get_words(text))
    #print pairs
    for j in xrange(2,i+1):
	pairs.extend(ngrams(words,j))
    #print pairs
    return pairs
    
    
def generate_graph2(words_stemmed):
    edges = {}
    for i in words_stemmed:
	for j in words_stemmed:
	    #print i,j
	    if len(set(i)&set(j))>0:
		
		p = (i, j)
		edges[p] = edges.get(p,0) + float(len(set(i)&set(j)))/(len(i)+len(j))
    
    g = nx.Graph()
    
    g.add_nodes_from(words_stemmed)
    g.add_edges_from([(k[0],k[1],{'weight':v}) for k,v in edges.iteritems()])
    
    return g

def generate_graph(words_stemmed):
    edges = {}
    for i in range(2,6):
        ns = ngrams(words_stemmed,i)
        for ngram in ns:
            pairs = [x for x in itertools.combinations(ngram,2)]
            for p in pairs:
                edges[p] = edges.get(p,0)+1.0/i
    
    g = nx.Graph()
    
    g.add_nodes_from(words_stemmed)
    g.add_edges_from([(k[0],k[1],{'weight':v}) for k,v in edges.iteritems()])
    
    return g

def generate_graph_synsets(word_synsets):
    edges = set([])
    pairs = [x for x in itertools.combinations(word_synsets,2)]
    for p in pairs:
        if p[0]['synsets'] & p[1]['synsets']:
            edges.add((p[0]['word'],p[1]['word']))
    
    g = nx.Graph()
    
    g.add_nodes_from([x['word'] for x in word_synsets])
    g.add_edges_from(edges)
    return g
        