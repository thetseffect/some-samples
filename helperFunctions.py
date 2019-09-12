import os
import gensim
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from gensim.models.keyedvectors import KeyedVectors
from gensim.models.wrappers import FastText
from wordcloud import WordCloud, ImageColorGenerator
from nltk import sent_tokenize, pos_tag, word_tokenize
from nltk.corpus import stopwords
from nltk import sent_tokenize, pos_tag, word_tokenize

class helperFunctions:
    def remove_punctuation(input_string):
        punctuation = ".,:;!?,<>=-)(][|"
        for item in punctuation:
            for i in range(len(input_string)):
                input_string[i] = str(input_string[i]).replace(item, '')

    def create_wordclouds(input_string):
        result_1 = []
        result_2=[]
        result_3=[]
        result_4=[]
        for i in range(len(input_string)):
            token1=sent_tokenize(input_string[i])
            intresult=[]
            nouns=[]
            adj=[]
            verb=[]
            for sent in token1:
                for word,pos in pos_tag(word_tokenize(str(sent))):
                    if ((pos=='NN' or pos == 'NNP' or pos == 'NNS' or pos == 'NNPS' or #Nouns
                        pos=='JJR' or pos =='JJ' or pos=='JJS' or # Adjectives
                        pos=='VB'or pos=='VBD'or pos=='VBG'or pos=='VBN')):
                        intresult.append(word)
                    
                    if(pos=='NN' or pos == 'NNP' or pos == 'NNS' or pos == 'NNPS'):
                        nouns.append(word)
                    
                    if ( pos=='JJR' or pos =='JJ' or pos=='JJS'):
                        adj.append(word)
                    
                    if(pos=='VB'or pos=='VBD'or pos=='VBG'or pos=='VBN'):
                        verb.append(word)
                
                result_1.append(intresult)
                result_2.append(nouns)
                result_3.append(adj)
                result_4.append(verb)             
        
        return result_1, result_2, result_3, result_4