#!/usr/bin/env python
# -*- coding: utf-8 -*-

from twitterscraper import query_tweets
import gzip
import gensim
import logging
import os
import codecs
import numpy as np
from nltk import FreqDist
import datetime


def sent2vect(sentences, model):
    # Init
    vectors = []
    # Loop through the sentences
    for entry in sentences:
        # Previous knowledge that the vectors have 300 dim
        weights = np.array(word2vect(entry,model,vector_size=300))
        # Save the weights
        avr = np.average(weights)
        # Look for NaN entries and just skip them
        if np.isnan(avr):
            # Just a bunch of zeros probably not that good in the long run
            avr = np.zeros(300)
        else:
            # The average ( our bad aprox of sentence to vector )
            avr = np.average(weights,axis=0)
        vectors.append(avr)
    return vectors


def word2vect(words, model,vector_size=2):
    vectors = []
    for word in words:
        try:
            vectors.append(model.wv.get_vector(word)[:vector_size])
        except:
            continue
    return vectors

# Harvest sentences, not removing the stopwords
def harvest_sentences(keyword_to_harvest,limit=2000):
    sentences = []
    # Decode the text to support swedish characters
    keyword_to_harvest = keyword_to_harvest.encode('utf-8')

    # Query twitter with the "keyword"        
    for query in query_tweets(keyword_to_harvest,
                              lang='sv',
                              poolsize=20,
                              limit=limit,
                              begindate=datetime.date(2014,1,1,)):
        # Split the result to get the words
        new_list = query.text.split(u' ')
        current_sentence= []
        for word in new_list:
            current_sentence.append(word)
        sentences.append(current_sentence)
    return sentences

# Harvest while removing the stopwords
def harvest_words(keyword_to_harvest, stopwords,limit=2000):
    words = []
    # Decode the text to support swedish characters
    keyword_to_harvest = keyword_to_harvest.encode('utf-8')
    # Query twitter with the "keyword"
    for query in query_tweets(keyword_to_harvest,
                              lang='sv',
                              limit=limit,
                              poolsize=20,
                              begindate=datetime.date(2014,1,1,)):
        # Split the result to get the words
        new_list = query.text.split(u' ')
        for word in new_list:
            try:
                # Remove the stopwords --> Not interesting!
                if word.encode('utf-8').lower() in stopwords:
                    new_list.remove(word)
                else:
                    words.append(word)
            except:
                print (word, " is not unicode")
    return words


def train(orden, stopwords):
    all_text=[]
    words = []

    for query in query_tweets(orden, lang='sv',poolsize=100):
        new_list = query.text.lower().split(u' ')
        new_sentence = []
        for word in new_list:
            if word not in stopwords:
                words.append(word)
                new_sentence.append(word)
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
        print ("The closest words to ", word_to_search)
        for word,freq in model.wv.most_similar(positive=word_to_search.lower(),
                                               topn=5):
                print (word)
                words.append(word)
        return words
# Print the 5 most common given a freq analysis result
def get_most_freq(word_to_search, freq_analysis):
        print ("The most frequent words around ", word_to_search.lower())
        counter = 0
        for word,freq in freq_analysis.most_common(20):
                if counter == 5:
                        break
                if word_to_search.lower() in word:
                        pass
                else:
                        print ("The word: ", word, ", |  Times:", freq)
                        counter+=1
                
