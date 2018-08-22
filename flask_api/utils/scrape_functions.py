#!/usr/bin/env python
# -*- coding: utf-8 -*-
# TODO:
# get just one word or verify agains more than one the search.

from twitterscraper import query_tweets
import gzip
import gensim
import logging
import os
import codecs
import numpy as np
from nltk import FreqDist


def train(orden, stopwords):
        all_text=[]
        words = []

	for query in query_tweets(orden, lang='sv',poolsize=100):
                new_list = query.text.split(u' ')
                
                for word in new_list:
                        try:
                                if word.encode('utf-8').lower() in stopwords:
                                        new_list.remove(word)#.encode('utf-8'))
                                else:
                                        words.append(word.lower())
                        except:
                                print word, " is not unicode"
                new_sentence = []
                for word in new_list:
                        new_sentence.append(word.lower())
                all_text.append(new_sentence)
        return all_text, words



# Got the stopwords from: https://github.com/stopwords-iso/stopwords-sv/blob/master/stopwords-sv.txt
stopwords_sv = []
with open('stopwords-sv.txt','r') as sw:
        for line in sw:
                word_to_insert = line.replace('\n','')       
                stopwords_sv.append(word_to_insert)
stopwords_sv.append(u'-')
stopwords_sv.append(u' ')
stopwords_sv.append(u'')
stopwords_sv.append(u'.')
stopwords_sv.append(u'&')


# Print the similar words given a model
def get_similar(word_to_search,model):
        words= []
        print "The closest words to ", word_to_search
        for word,freq in model.wv.most_similar(positive=word_to_search.lower(),
                                               topn=5):
                print word
                words.append(word)
        return words
# Print the 5 most common given a freq analysis result
def get_most_freq(word_to_search, freq_analysis):
        print "The most frequent words around ", word_to_search.lower()
        counter = 0
        for word,freq in freq_analysis.most_common(20):
                if counter == 5:
                        break
                if word_to_search.lower() in word:
                        pass
                else:
                        print "The word: ", word, ", |  Times:", freq
                        counter+=1
                