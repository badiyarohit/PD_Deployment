import pandas as pd 
import numpy as np
import spacy
import networkx as nx
import matplotlib.pyplot as plt
from spacy import displacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def isRelationCandidate(token):
    deps = ["ROOT", "adj", "attr", "agent", "amod"]
    return any(subs in token.dep_ for subs in deps)

def source_target_relation_triple(sentence, k):
    source = ''
    target = ''
    relation = ''
    for token in sentence:
        if token.dep_ != "punct":
            if isRelationCandidate(token):
                relation = relation + ' ' + token.lemma_
            if "subj" in token.dep_:
                source = source + ' ' + token.text
            if "obj" in token.dep_:
                target = target + ' ' + token.text
    return (source.strip(), relation.strip(), target.strip())

def similar(arr1,arr2):
    tfidf_vectorizer = TfidfVectorizer()
    tfidf_matrix = tfidf_vectorizer.fit_transform([arr1,arr2])
    similar = cosine_similarity(tfidf_matrix[0], tfidf_matrix[1])
    return ('%.3f'%(similar*100))

def generate_array(triples):
    arr = ""
    for i in range(0, len(triples)):
        arr += triples[i][0]
        arr += triples[i][1]
        arr += triples[i][2]
    return arr

def generate_triples(sentences,nlp):
    triples = []
    i = 1
    k = 1
    for sentence in sentences:
        tokens = nlp(sentence)
        i = i + 1
        triples.append(source_target_relation_triple(tokens, k))
        k = k +1
    return triples

def Plagiarism_Detector(input_doc1,input_doc2):
    nlp = spacy.load('en_core_web_lg')

    document1 = open(input_doc1, 'r')
    sentences1 = document1.read().split('.')[:-1]
    document2 = open(input_doc2, 'r')
    sentences2 = document2.read().split('.')[:-1]

    triples1 = generate_triples(sentences1,nlp)
    triples2 = generate_triples(sentences2,nlp)

    arr1 = generate_array(triples1)
    arr2 = generate_array(triples2)
    
    result = similar(arr1,arr2)
    return result