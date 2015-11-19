# NLTK-SimplifyPlot
Graphically shows textual content using Python, NLTK, Matplotlib

The program simplifies every sentence in a paragraph and graphically represents them as two connected entities. The two entities represent prominent nouns and the connection between them is an action which is performed.

For example ,consider the sentence: Jack had a good day.


Entity1 :  Jack

Entity2 : day

Action  : had

Our expected output should be


                            Jack    ----------had-------------->   day


NLTK (Natural Language ToolKit) module is used to break down the given sentence and understand the meaning of each word.

https://cloud.githubusercontent.com/assets/8260656/11280036/dd80c420-8f19-11e5-8f1b-21b2354b7ea8.png

NLTK uses a set of predefined tag words  with which it compares the sentence.
Some tag word defined are:

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
    
    for item in ExampleText:
                     
       				.
				.
				.
        tokenized = nltk.word_tokenize(item)
        tagger = nltk.UnigramTagger(train_sents, backoff=default_tagger)
        i=tagger.tag(tokenized)
				.
				.
				.

	word_tokenize() : Splits each word in a sentence and stores it as a list.
	Each word that must be split must be tagged. That is nouns, verbs adjectives etc,. must be identified. In the example sentence, ' Jack had a good day.' the output does not mention the nature of the day. Whether the day was good or bad is not known.
	In order to include details of the day, like good(adjective) a suitable grammar needs to be specified. One grammar which satisfies simple sentences is:

grammar = r"""
          LivingNoun: {<NN.>+}
          Noun2: {<IN><NP>|<DT><JJ><NN\w*>|<JJ><NNP>}                      
          Verb: {<VBD><TO>|<VB.*><RB>*<VB>*}                                  
          Pronoun:{<PRP>|<PRP\$>|<PRO>}
          NonlivingPronoun: {<NLPRO>}
          OtherNoun: {<NN>+}
        """


	The grammar defines six tags
o	LivingNoun		: One or more nouns together. (Jack, Boy, George Bush...)
o	Noun2         		: Nouns preceded by 'in', 'the' or by an adjective (in pain, the ........................................old  school, nice day...)
o	Verb			: Verbs, combination of verb adverb verb(sings, slowly ........................................walked...)
o	Pronoun		: Identifies pronouns which can be linked to previous ........................................LivingNoun.(Him,her...)
o	NonlivingPronoun	: Identifies non living nouns(it, that...)
o	OtherNoun		: A combination of nouns not described by adjectives


In order to tag words correctly, the parser must be trained with a combination of different styles of sentences.

train_sents = [
        [('select', 'VB'), ('the', 'DT'), ('files', 'NNS')],
        [('use', 'VB'), ('the', 'DT'), ('select', 'JJ'), ('function', 'NN'), ('on', 'IN'), ('the', 'DT'), ('sockets', 'NNS')],
        [('the', 'DT'), ('select', 'NN'), ('files', 'NNS')],
        [('it', 'NLPRO')],
        [('walk', 'NN')]]

        The tokenized words must be tagged using the train_sents.

tagger = nltk.UnigramTagger(train_sents, backoff=default_tagger)
i=tagger.tag(tokenized)

Now, the tagged words must be grouped as mentioned in the grammar.

cp = nltk.RegexpParser(grammar)
result = cp.parse(i)


Using networkX, a python module that helps in visual representation, the grouped nouns can be represented as nodes and verbs as edges.

G=nx.DiGraph()
    for a in result:
        if type(a) is nltk.Tree:
           #Case1 : Living Noun
           if(a.label()=='LivingNoun') :
                curNNP=a.leaves()
                
                graphlabelNouns.append(curNNP)                                     
       			      	      .
      				      .
		      		      .
                  G.add_node(tuple(n1))
                  G.add_node(tuple(n2))
                  G.add_edge(tuple(n1),tuple(n2),label=tuple(v))                                       
       				      .
			      	      .
				      .
To verify if a pronoun encountered links to the previously mentioned LivingNoun, the example sentence is modified.

https://cloud.githubusercontent.com/assets/8260656/11280045/edbd1406-8f19-11e5-949f-062d9c4a5ae7.png

Encountering another noun should add nodes to the graph correspondingly.
https://cloud.githubusercontent.com/assets/8260656/11280070/04dc06a6-8f1a-11e5-8778-f7034360a144.png

				            
				    
