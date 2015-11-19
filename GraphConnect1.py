# Graphicalliy shows sentences in Noun-Verb-Noun form


'''
ADJ	adjective	new, good, high, special, big, local
ADV	adverb	really, already, still, early, now
CNJ	conjunction	and, or, but, if, while, although
DET	determiner	the, a, some, most, every, no
EX	existential	there, there's
FW	foreign word	dolce, ersatz, esprit, quo, maitre
MOD	modal verb	will, can, would, may, must, should
N	noun	year, home, costs, time, education
NP	proper noun	Alison, Africa, April, Washington
NUM	number	twenty-four, fourth, 1991, 14:24
PRO	pronoun	he, their, her, its, my, I, us
P	preposition	on, of, at, with, by, into, under
TO	the word to	to
UH	interjection	ah, bang, ha, whee, hmpf, oops
V	verb	is, has, get, do, make, see, run
VD	past tense	said, took, told, made, asked
VG	present participle	making, going, playing, working
VN	past participle	given, taken, begun, sung
WH	wh determiner	who, which, when, what, where, how
'''

import nltk
import re
import pprint
import networkx as nx
import matplotlib.pyplot as plt

ExampleText1=['Jack had a good day.']
ExampleText=['Jack had a good day. He went to a party.']
ExampleText2=['Jack had a good day. He went to a party. The host welcomed him.']

default_tagger = nltk.data.load(nltk.tag._POS_TAGGER)
i=0

graphlabelNouns=[]
graphlabelVerbs=[]

def processContent():
    
    for item in ExampleText:
                     
        grammar = r"""
          LivingNoun: {<NN.>+}
          Noun2: {<IN><NP>|<DT><JJ><NN\w*>|<JJ><NNP>}                      
          Verb: {<VBD><TO>|<VB.*><RB>*<VB>*}                                  
          Pronoun:{<PRP>|<PRP\$>|<PRO>}
          NonlivingPronoun: {<NLPRO>}
          OtherNoun: {<NN>+}
        """  
        train_sents = [
        [('select', 'VB'), ('the', 'DT'), ('files', 'NNS')],
        [('use', 'VB'), ('the', 'DT'), ('select', 'JJ'), ('function', 'NN'), ('on', 'IN'), ('the', 'DT'), ('sockets', 'NNS')],
        [('the', 'DT'), ('select', 'NN'), ('files', 'NNS')],
        [('it', 'NLPRO')],
        [('walk', 'NN')]]

        tokenized = nltk.word_tokenize(item)
        tagger = nltk.UnigramTagger(train_sents, backoff=default_tagger)
        i=tagger.tag(tokenized)
##        print(tokenized)
##        print(i)

        
        cp = nltk.RegexpParser(grammar)
        result = cp.parse(i)

    
    G=nx.DiGraph()

    flag=0
    for a in result:
        if type(a) is nltk.Tree:
           #Case1 : Living Noun
           if(a.label()=='LivingNoun') :
                curNNP=a.leaves()
                
                graphlabelNouns.append(curNNP)
                
                if flag == 0:
                  n1=a.leaves()
                else:
                  n2=a.leaves()
                  
                  print(n1,  v   ,n2)
                  G.add_node(tuple(n1))
                  G.add_node(tuple(n2))
                  G.add_edge(tuple(n1),tuple(n2),label=tuple(v))
                  
                  flag=0

                  
           #Case2 : Noun2
           if(a.label()=='Noun2'):
                curNoun=a.leaves()
                graphlabelNouns.append(curNoun)
                
                if flag == 0:
                  n1=a.leaves()
                else:
                  n2=a.leaves()
                  print(n1,  v   ,n2)
                  G.add_node(tuple(n1))
                  G.add_node(tuple(n2))
                  G.add_edge(tuple(n1),tuple(n2),label=tuple(v))

                  flag=0

           #Case3 : Other Noun       
           if(a.label()=='OtherNoun') :
               curOtherNoun=a.leaves()
               graphlabelNouns.append(curOtherNoun)
               if flag == 0:
                  n1=a.leaves()
               else:
                  n2=a.leaves()
                  print(n1,  v ,n2  )
                  G.add_node(tuple(n1))
                  G.add_node(tuple(n2))
                  G.add_edge(tuple(n1),tuple(n2),label=tuple(v))
                  flag=0

           #Case4: Pronoun like him, her
           if(a.label()=='Pronoun') :
              #print('Pronoun',a.leaves(),'stands for',cur)
              if flag == 0:
                  n1=curNNP
                  #print n1
              else:
                  n2=curNNP
                  print('pronoun::',n1,  v ,n2  )
                  G.add_node(tuple(n1))
                  G.add_node(tuple(n2))
                  G.add_edge(tuple(n1),tuple(n2),label=tuple(v))
                  flag=0

           #Case5 : Non Living Pronoun like it,that       
           if(a.label()=='NonlivingPronoun') :
              #print('Pronoun',a.leaves(),'stands for',cur1)
              if flag == 0:
                  n1=curOtherNoun[0]
              else:
                  n2=curOtherNoun[0]
                  print(n1 , v ,  n2)
                  G.add_node(tuple(n1))
                  G.add_node(tuple(n2))
                  G.add_edge(tuple(n1),tuple(n2),label=tuple(v))
                  flag=0
           if(a.label()=='Verb') :
              flag=1
              v=a.leaves()
              graphlabelVerbs.append(v)
    print('\n_______________________________________________________________________\n')              
    print('List of nouns')
    print(graphlabelNouns)
    print('\n_______________________________________________________________________\n')
    print('List of verbs')
    print(graphlabelVerbs)
    print('\n_______________________________________________________________________\n')

    graph_pos=nx.shell_layout(G)
    nx.draw_networkx_nodes(G,graph_pos,node_size=10000, 
                               alpha=0.3, node_color='blue')
    nx.draw_networkx_edges(G,graph_pos,width=1,
                               alpha=0.3,edge_color='green')
    nx.draw_networkx_labels(G, graph_pos,font_size=11,
                                font_family='sans-serif')
    nx.draw_networkx_edge_labels(G, graph_pos,font_size=9,
                                    label_pos=0.5)
        
        
    #nx.draw(G)
    
    plt.show()
    result.draw()

    
processContent()
