"reuters/businessNews"
from pymongo import Connection
import unicodedata
from nltk import word_tokenize
from collections import defaultdict,Counter
import math
import string
from stopwords import stopwords
import re
import unicodedata
import operator
import cPickle as pickle

#source /home/infolab/env/attitudebuzz/bin/activate

def strip_punctuation(text):
    """
    >>> strip_punctuation(u'something')
    u'something'

    >>> strip_punctuation(u'something.,:else really')
    u'somethingelse really'
    """
    punctutation_cats = set(['Pc', 'Pd', 'Ps', 'Pe', 'Pi', 'Pf', 'Po'])
    return ''.join(x for x in text
                   if unicodedata.category(x) not in punctutation_cats)


def tokenize_article(text):
	#clean punctuation
	text = strip_punctuation(text)
	#text = ' '.join(word.strip(string.punctuation) for word in text.split())
	return word_tokenize(text.lower())