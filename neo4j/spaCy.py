============================================================================================================================================
Triplets or Triples
============================================================================================================================================
>>> pip install spacy 
>>> python -m spacy download en_core_web_sm


en_core_web_sm (English	~12 MB)	 => Lightweight, good for demo
en_core_web_md (English	~43 MB)	 => Medium, includes vectors
en_core_web_lg (English	~741 MB) => Large, better accuracy

basic coding using the above models - 

>>> nlp = spacy.load("en_core_web_md")
>>> doc = nlp(text)

-- these models are not efficient, and misses complex semantic data

-- Thus use dependency parsing more deeply to find noun phrases and prepositions 
-- Use libraries like:

openie (Open Information Extraction from Stanford)
transformers (BERT + relation extractors)
LLMs (ChatGPT or others can extract triplets very well)


============================================================================================================================================
Triplets or Triples
============================================================================================================================================
for knowledge graphs, triplets (also called triples) are the basic building blocks. A triplet represents a simple fact or relationship 
in the form of:

(subject, predicate, object)
ie - 
(Elon, founded, Spacex)

-- triplets form the basis of nodes and relationships
-- Subjects and objects become nodes
-- Predicates become relationships (edges) between nodes

-- can use NLP libraries like spaCy, OpenIE, or LLMs to extract triplets from unstructured text

