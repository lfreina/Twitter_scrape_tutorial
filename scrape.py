#!/usr/bin/env python
# -*- coding: utf-8 -*-
# TODO:
# get just one word or verify agains more than one the search.

# Got the stopwords from: https://github.com/stopwords-iso/stopwords-sv/blob/master/stopwords-sv.txt
# To use run:
#    pip install twitterscraper gensim nltk

from twitterscraper import query_tweets
import gzip
import gensim
import logging
import os
import codecs
import numpy as np
from nltk import FreqDist
import datetime as dt
import sys

def test_bib (word, stopwords):
    '''
    Function that will scrape Twitter for the "word".

    word: One word to scrape twitter for
    stopwords: A list with words that are to be considered stopwords
               from the scraped text.


    TODO: Verify that the stopwords are actually removed from the scraped text.
    '''
    all_text=[]
    words = []
    # Peform the query in swedish
    # poolsize will be used for querying the dates as follows:
    #     dateranges = begindate + linspace(0, #days, poolsize+1 )
    # You can set a limit of tweets per pool, but why?
    
    start_date = dt.date(2008,1,1)
    stop_date = dt.date.today()
    for query in query_tweets(word,lang='sv',poolsize=10,begindate=start_date,enddate=stop_date):
        # 1. Change to lower case
        new_list = query.text.lower().split(u' ')
        # 1.5 TODO: Remove https/http links

        new_sentence = []
        # 2. Remove the stopwords in a very naive way
        for word in new_list:
            if word not in stopwords:
                new_sentence.append(word)
                words.append(word)
                
        all_text.append(new_sentence)
    # Return the list with sentences and a list with words
    unique_words = np.unique(words)
    return all_text, unique_words


# Print the similar words given a model
def get_similar(word_to_search,model):
    '''
    word_to_search: Print similar words to word_to_search with a model.
    model: Is a word2vec model
    '''
    print ("The closest words to ", word_to_search )
    for word,freq in model.wv.most_similar(positive=word_to_search.lower(),
                                                topn=5):
        print ( word )
        
# Print the 5 most common given a freq analysis result
def get_most_freq(word_to_search, freq_analysis):
    '''
    word_to_search: 5 most frequent words around this word
    freq_analysis: an nltk FreqDist result
    '''
    print ("The most frequent words around ", word_to_search.lower() )
    counter = 0
    for word,freq in freq_analysis.most_common(20):
        if counter == 5:
            break
        if word_to_search.lower() in word:
            pass
        else:
            print ("The word: ", word, ", |  Times:", freq )
            counter+=1
                

# Main
# --------------------------------
# Create a stopwords list
# --------------------------------
stopwords_sv = []
# Remove the new lines in the file
with open('stopwords-sv.txt','r') as sw:
    for line in sw:
        word_to_insert = line.replace('\n','')                
        stopwords_sv.append(word_to_insert)



# Add some stop words to the list.
stopwords_sv.append(u'-')
stopwords_sv.append(u' ')
stopwords_sv.append(u'')
stopwords_sv.append(u'.')
stopwords_sv.append(u'&')

# --------------------------------
# Define the word to search
# --------------------------------
words_to_search = "hej"
documents, words = test_bib(words_to_search,stopwords_sv)

if len(words) == 0:
    sys.exit('No tweets fetched :S !! ')
# --------------------------------
# Maybe remove this? I do not think we need it!
# --------------------------------
# build vocabulary and train Word2Vec model with the scraped text
model = gensim.models.Word2Vec(documents,
                               size=150,
                               window=20,
                               min_count=2,
                               workers=4,
                               sg=0)

model.train(documents, total_examples=len(documents), epochs=10)
get_similar(words_to_search,model)
print ("------------------")
freq_analysis = FreqDist(words)
get_most_freq(words_to_search, freq_analysis)

