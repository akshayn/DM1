#!/usr/bin/python

import os
import re
import gc
import operator
from parse import TitleParser
from collections import defaultdict
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.stem.porter import PorterStemmer

# Constants
PATH = r'reuters'
WORD_REGEX = '[a-z]+'
NORMAL_WEIGHT = 1
TITLE_WEIGHT = 10
TOPIC_WEIGHT = 1
PLACES_WEIGHT = 1
THRESHOLD_PERCENTAGE = 1

# Strip/replace specific characters
def stripchars(string):
    string = re.sub( '[<>]', '', string) #remove <, >
    string = string.replace('\n',' ') #remove newlines    
    return string

# Return dictionary specifying the word count in the title and text of article
def get_frequency(record):
    freq_dict = defaultdict(int)

    title = record.get("title", "default")
    title = stripchars(title)
    for word in re.findall(WORD_REGEX, title):
        freq_dict[word] += TITLE_WEIGHT

    text = record.get("text", "default")
    text = stripchars(text)
    for word in re.findall(WORD_REGEX, text):
        freq_dict[word] += NORMAL_WEIGHT

    return freq_dict

# sorted_tuple_list is a list of tuples
# Find the index of tuple whose second element equals value
def find_index(sorted_tuple_list, value):
    for i, v in enumerate(sorted_tuple_list):
        if v[1] > value:
            return i
    return -1        


parser = TitleParser()
lemma = WordNetLemmatizer()
stemmer = PorterStemmer()

# record_freq_list is a list of dictionaries
# Each dictionary consists of:
# 1. topics - This is a list of topics
# 2. places - This is a list of places
# 2. freq_dict - This is dictionary consisting of word-count pairs
record_freq_list = []
word_article_freq = defaultdict(int)   # Store the number of articles in which a word appears

#load stopwords
file = open('stopwords')
stopwords = file.read().split()
file.close()

for dir_entry in os.listdir(PATH):   #each file
    dir_entry_path = os.path.join(PATH, dir_entry)
    file = open(dir_entry_path)
    content = re.sub('&(.+?);|,|\'|"', '',file.read())  #remove &xxx; and comma and quotes
    parser.feed(content)
    file.close()

    for record in parser.records_list: #each article
	topics_list = record.get("topics", [])
        places_list = record.get("places", [])
        freq_dict = get_frequency(record)
        record_freq_list.append( {'topics':topics_list, 'places':places_list,'freq_dict':freq_dict} )

        for word in freq_dict.keys():
            word_article_freq[word] += 1



#trimming
# Sort the word vs number of article frequency list by the frequency
word_article_freq_sorted = sorted(word_article_freq.iteritems(), key=operator.itemgetter(1))
max_freq = word_article_freq_sorted[-1][1]
lower_threshold = max_freq/100*THRESHOLD_PERCENTAGE
upper_threshold = max_freq/100*(100 - THRESHOLD_PERCENTAGE)

lower_index = find_index(word_article_freq_sorted, lower_threshold)
upper_index = find_index(word_article_freq_sorted, upper_threshold)
trimmed_list = word_article_freq_sorted[lower_index:upper_index]

# Remove stopwords
word_list = []
for i in trimmed_list:
    if not i[0] in stopwords:
        word_list.append(i[0])

# Add topics and places to word_list
for record in record_freq_list:
    topics_list = record.get("topics", [])
    for topic in topics_list:
        if topic not in word_list:
            word_list.append(topic)

for record in record_freq_list:
    places_list = record.get("places", [])
    for place in places_list:
        if place not in word_list:
            word_list.append(place)


# Create data matrix
data_matrix = []
for record in record_freq_list:
    matrix_row = defaultdict(int)
    freq_dict = record.get("freq_dict", {})
    topics = record.get("topics", [])
    places = record.get("places", [])
    for word in word_list:
        if word in freq_dict:
	    matrix_row[word] += freq_dict[word]
	if word in topics:
	    matrix_row[word] += TOPIC_WEIGHT
	if word in places:
	    matrix_row[word] += PLACE_WEIGHT
    data_matrix.append(matrix_row)

gc.collect()

# Write data matrix in a file
dmat_file = open("data_matrix.csv", "w")
for word in word_list:
    dmat_file.write("," + word)
dmat_file.write("\n")
article_index = 1
for matrix_row in data_matrix:
    dmat_file.write("\"Article " + str(article_index) + "\"")
    for word in word_list:
        dmat_file.write("," + str(matrix_row[word]))
    dmat_file.write("\n")
    article_index += 1
dmat_file.close()
        

print len(trimmed_list)
print len(word_list)

#TODO : remove later
out  = open("out.txt","w")
for i in word_article_freq_sorted:
    out.write(i[0] + ' ' + str(i[1]) + '\n')
out.close()
