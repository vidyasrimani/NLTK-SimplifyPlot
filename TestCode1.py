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
    WH	wh determiner	who, which, when, what, where, how'''

import nltk
import re
import pprint
import networkx as nx
import matplotlib.pyplot as plt
from nltk.tag.util import untag
text1 = ['Jack had a good day . He and his friends went for a walk . They loved it']
text3 = ['When a green ogre called Shrek discovers his swamp has been \'swamped\' with all so6rts of fairytale creatures by the scheming Lord Farquaad, Shrek sets out, with a very loud donkey by his side, to \'persuade\' Farquaad to give his swamp back . ']
text4=['Shrek is a grouchy, terrifying green ogre. He loves the solitude in his swamp . Lord Farquaad exiles fairytale characters. Shrek finds  life interrupted when fairytale characters. Shrek meets Lord Farquaad . Shrek brings along a talking donkey who is the only fairytale character who knows the way to Duloc . Lord Farquaad tortures the Gingerbread Man into giving the location of the remaining fairytale characters . Magic Mirror tells Lord Farquaad that he is not even a king . Lord Farquaad must marry a princess to be a king. He chooses Princess Fiona, who is locked in a castle . Shrek marries Princess Fiona . ']
default_tagger = nltk.data.load(nltk.tag._POS_TAGGER)
i=0
LivingNounList=[]
NonLivingNounList=[]
VerbList=[]
def processContent():
    
    for item in text4:
        
    
        grammar = r"""
        ProperNoun: {<NNP|NNS>}
        Verb: {<BT|VBD>|<VBD>|<BT>*<VBD>}
        OtherNouns: {<IN><NP>|*<NNS|NN>*|<PRP\$>?<NN>+|<PRP\$>?}
        jj: {*<JJ>*}
        Pronoun:{<PRP>|<PRP\$>|<PRO>}
        NonlivingPronoun: {<NLPRO>}
        """

        train_sents = [
                       [('it', 'NLPRO')],
                       [('walk', 'NN')],
                       [('discovers', 'VBD')],
                       [('finds','VBD')],
                       [('meets','VBD')]
                       ]
        tokenized = nltk.word_tokenize(item)
        tagger = nltk.UnigramTagger(train_sents, backoff=default_tagger)
        i=tagger.tag(tokenized)
                       
        cp = nltk.RegexpParser(grammar)
        result = cp.parse(i)
    
    G=nx.DiGraph()
    Gc=nx.DiGraph()
    Gcc=nx.DiGraph()
    
    flag=0
    for a in result:
        if type(a) is nltk.Tree:
            
            if(a.label()=='ProperNoun') :
                cur=a.leaves()
                ProperNoun.append(cur)
                
                if flag == 0:
                    n1=a.leaves()
                    un1=untag(n1)
                else:
                    n2=a.leaves()
                    un2=untag(n2)
                    print(un1,  uv   ,un2)
                    G.add_node(tuple(un1))
                    G.add_node(tuple(un2))
                    G.add_edge(tuple(un1),tuple(un2),label=tuple(uv))
                    n1=n2
                    un1=untag(n1)
                    flag=0
            if(a.label()=='Noun2'):
                cur2=a.leaves()
                noun.append(cur2)
                
                if flag == 0:
                    n1=a.leaves()
                    un1=untag(n1)
                else:
                    n2=a.leaves()
                    un2=untag(n2)
                print(un1,  uv   ,un2)
                Gcc.add_node(tuple(un1))
                Gcc.add_node(tuple(un2))
                Gcc.add_edge(tuple(un1),tuple(un2),label=tuple(uv))
                flag=0
            if(a.label()=='OtherNouns') :
                cur1=a.leaves()
                noun.append(cur1)
                if flag == 0:
                    n1=a.leaves()
                    un1=untag(n1)
                else:
                    n2=a.leaves()
                    un2=untag(n2)
                    print(un1,  uv ,un2  )
                    Gc.add_node(tuple(un1))
                    Gc.add_node(tuple(un2))
                    Gc.add_edge(tuple(un1),tuple(un2),label=tuple(uv))
                    flag=0
                    n1=n2
                    un1=untag(n1)
            if(a.label()=='Pronoun') :
                #print('Pronoun',a.leaves(),'stands for',cur)
                ProperNoun.append(cur)
                if flag == 0:
                    n1=cur
                    un1=untag(n1)
                #print('n1', n1)
                else:
                    n2=cur
                    un2=untag(n2)
                    print('pronoun::',un1,  uv ,un2  )
                    G.add_node(tuple(un1))
                    G.add_node(tuple(un2))
                    G.add_edge(tuple(un1),tuple(un2),label=tuple(uv))
                    flag=0
                    n1=n2
                    un1=untag(n1)
            if(a.label()=='NonlivingPronoun') :
                #print('Pronoun',a.leaves(),'stands for',cur1)
                noun.append(cur1)
                if flag == 0:
                    n1=cur1
                    un1=untag(n1)
                else:
                    n2=cur1
                    un2=untag(n2)
                    print(un1 , uv ,  un2)
                    G.add_node(tuple(un1))
                    G.add_node(tuple(un2))
                    G.add_edge(tuple(un1),tuple(un2),label=tuple(uv))
                    flag=0
                    n1=n2
                    un1=untag(n1)
            if(a.label()=='Verb') :
                flag=1
                v=a.leaves()
                uv=untag(v)
                VerbList.append(v)
    
    print('List of living nouns')
    print(ProperNoun)
    print('List of Non living nouns')
    print(noun)
    print('List of verbs')
    print(VerbList)
    
    graph_pos=nx.spring_layout(G)
    graph_pos=nx.spring_layout(Gc)
    graph_pos=nx.spring_layout(Gcc)
    nx.draw_networkx_nodes(G,graph_pos,node_size=3000,
                           alpha=0.3, node_color='red',node_shape='o')
    nx.draw_networkx_nodes(Gc,graph_pos,node_size=2000,
                               alpha=0.3, node_color='green',node_shape='o')
    nx.draw_networkx_nodes(Gcc,graph_pos,node_size=1000,
                                   alpha=0.3, node_color='yellow',node_shape='o')
    nx.draw_networkx_edges(G,graph_pos,width=1,
                                                  alpha=0.3,edge_color='blue')
    nx.draw_networkx_labels(G, graph_pos,font_size=10,
                                                                    font_family='sans-serif')
    nx.draw_networkx_edges(Gc,graph_pos,width=1,alpha=0.3,edge_color='blue')
    nx.draw_networkx_labels(G, graph_pos,font_size=10,font_family='sans-serif')
    nx.draw_networkx_edges(Gcc,graph_pos,width=1,alpha=0.3,edge_color='blue')
    nx.draw_networkx_labels(G, graph_pos,font_size=10,font_family='sans-serif')
    nx.draw_networkx_edge_labels(G, graph_pos,font_size=10,label_pos=0.3)
    nx.draw_networkx_edge_labels(Gc, graph_pos,font_size=10,label_pos=0.3)
    nx.draw_networkx_edge_labels(Gcc, graph_pos,font_size=10,label_pos=0.3)
                                                                                                       
    plt.show()
    result.draw()


