import gexf
from lxml import etree
from nltk.stem import WordNetLemmatizer

from nltk.tokenize import *
from nltk.corpus import stopwords

from nltk.util import ngrams

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
    print ns
    
    
    g = gexf.Gexf("ED","ED test")
    graph=g.addGraph("undirected","static","a test graph")
    attr = graph.addNodeAttribute("count","0")
    
    edge_id = 0
    nodes = set([])
    for i1,i2 in ns:
        edge=True
        if i1 in nodes and i2 in nodes:
            edge=False
        if i1 not in nodes:
            node = graph.addNode(i1,i1)
            node.addAttribute(attr,str(counts[i1]))
            nodes.add(i1)
            

        if i2 not in nodes:
            node = graph.addNode(i2,i2)
            node.addAttribute(attr,str(counts[i2]))
            nodes.add(i2)
        
        if edge:
            graph.addEdge(str(edge_id),i1,i2)
            edge_id+=1
    f = open('test.gexf','w')
    f.write(etree.tostring(g.getXML(), pretty_print=True))
    f.close()
    
    #print etree.tostring(g.getXML(),pretty_print=True)