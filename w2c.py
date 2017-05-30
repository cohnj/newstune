import os
import pandas as pd
import nltk
import gensim
from gensim import corpora, models, similarities
import json
import unicodedata
import pickle
from pymongo import Connection
import re


def main():
    sentences = read_mongo_data()
    #model = gensim.models.Word2Vec(sentences, size = 200, workers=4)
    #model.save('testmodel')
    load_model()
    get_similar("hope",model)

def train_model(sentences):
    '''sentences: list of strings, each article is a string'''
    model = gensim.models.Word2Vec(sentences, size = 200, workers=4)
    model.save('testmodel')

def load_model():
    model = gensim.models.Word2Vec.load('testmodel')
    return model

def save_parsed_data(sentences):
    # parsed_json = open('parsed_json.txt', 'w')
    # for item in sentences:
    #     parsed_json.write("%s\n" % item)
    with open('parsed_json', 'wb') as fp:
        pickle.dump(sentences, fp)

def read_parsed_data():
    sentences = []
    # with open('parsed_json.txt') as data:
    #     for line in data:
    #         sentences.append(line)
    # return sentences
    with open ('parsed_json', 'rb') as fp:
        sentences = pickle.load(fp)
    return sentences

def read_mongo_data():
    conn = Connection().newstune
    articles = conn.er_articles.find({'date': {'$in': [ re.compile('2017[-]05[-]1')]}},{"text":1,"title":1})
    sentences = []
    for article in articles:
        sentences.append(article['text'])
        sentences.append(article['title'])

def read_json_data(filename):
    sentences = []
    with open(filename) as json_data:
        for line in json_data:
            try:
                article = {}
                article = json.loads(line)
                title = nltk.word_tokenize(unicodedata.normalize('NFKD', article['title']).encode('ascii','ignore'))
                text = nltk.word_tokenize(unicodedata.normalize('NFKD', article['text']).encode('ascii','ignore'))
                sentences.append(title)
                sentences.append(text)
            except:
                continue
    save_parsed_data(sentences)


def get_similar(input,model):
    '''input is word or list of words'''
    return model.wv.most_similar(input, topn=10)
