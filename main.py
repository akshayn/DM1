#!/usr/bin/python

from parse import TitleParser
import os
import re
from collections import defaultdict
from nltk.stem.wordnet import WordNetLemmatizer
import operator

def stripchars(string):
    string = re.sub( '[<>]', '', string) #remove <, >
    string = string.replace('\n',' ') #remove newlines    
    return string

# Constants
path = r'reuters'
wordnum_regex = '[a-z]+|[0-9]+.[0-9]+'
word_regex = '[a-z]+'
title_weight = 10
normal_weight = 1

parser = TitleParser()
lemma = WordNetLemmatizer()
d = defaultdict(int)    #TODO: remove

# record_freq_list is a list of the form
# record_freq_list = [
#                      {
#                        'class': "topic1, topic2, ..."
#                        'freq_dict' : {
#                                       'word1': 2
#                                       'word2': 5
#                                        ...
#                                      }
#                       },
#                       .....
#                    ]
record_freq_list = []
word_article_freq = defaultdict(int)   # Store the number of articles in which a word appears

out  = open("out.txt","w")
out1  = open("out1.txt","w")

for dir_entry in os.listdir(path):
    dir_entry_path = os.path.join(path, dir_entry)
    file = open(dir_entry_path)

    content = re.sub('&(.+?);|,|\'|"|`', '',file.read())  #remove &xxx; and comma
    parser.feed(content)

    file.close()

    for record in parser.records_list:
        record_freq = {}

	topics_list = record.get("topics", [])
        record_freq['class'] = ', '.join(topics_list)

        freq_dict = defaultdict(int)
        title = record.get("title", "default")
        title = stripchars(title)
        for i in re.findall(re.compile(word_regex), title):
            word = lemma.lemmatize(i)
            d[word] += 1
            freq_dict[word] += title_weight

	text = record.get("text", "default")
        text = stripchars(text)
        for i in re.findall(re.compile(word_regex), text):
            word = lemma.lemmatize(i)
            d[word] += 1
            freq_dict[word] += normal_weight

        record_freq['freq_dict'] = freq_dict
        record_freq_list.append(record_freq)

        for word in freq_dict.keys():
            word_article_freq[word] += 1

d_list = sorted(d.iteritems(), key=operator.itemgetter(0))
for i in d_list:
    out.write(i[0] + ' ' + str(i[1]) + '\n')


for key, value in word_article_freq.iteritems():
    out1.write(key + ' ' + str(value) + '\n')

