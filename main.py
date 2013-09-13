#!/usr/bin/python


#  Algorithm:
#  1. Maintain a document frequency hash
#  2. Iterate through file and feed it to ArticleParser  
#  3. ArticleParser returns list of article data(id, topics, places, title, text) in that file
#  4. For each article, build word-count for title and text; also update document frequency
#  5. Sort the document frequency by the value(frequency) and trim 1% on value
#  6. Load list of stopwords from file and remove stopwords from trimmed words
#  7. Create topics and places lists from all articles
#  8. Write data matrix and transaction matrix to files

import os
import re
import math
import operator
from parse import ArticleParser
from collections import defaultdict
import timeit

start = timeit.default_timer()

# Constants
PATH = r'reuters'
WORD_REGEX = '[a-z]+'
NORMAL_WEIGHT = 1
TITLE_WEIGHT = 5
TOPIC_WEIGHT = 1
PLACES_WEIGHT = 1
THRESHOLD_PERCENTAGE = 1


#############
# Functions #
#############

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
# Find the index of tuple from which to trim
def find_index(sorted_tuple_list, value):
    for i, v in enumerate(sorted_tuple_list):
        if v[1] > value:
            return i
    return -1        


# Compute and write Document Frequency and Inverse Document Frequency to file
def write_IDF(document_freq_dict_sorted):
    print "Writing inverse document frequency to IDF.txt"
    total_docs= float(len(document_freq_dict_sorted))
    idf_file = open("IDF.txt","w")
    for i in document_freq_dict_sorted:
        idf_file.write(i[0] + " " + str(i[1]) + " " + str(math.log(total_docs/i[1])) + "\n")
    idf_file.close()


# Find the thresholds on IDF and trim it
def get_trimmed_list(document_freq_dict_sorted):
    max_freq = document_freq_dict_sorted[-1][1]
    lower_threshold = max_freq/100*THRESHOLD_PERCENTAGE
    upper_threshold = max_freq/100*(100 - THRESHOLD_PERCENTAGE)

    lower_index = find_index(document_freq_dict_sorted, lower_threshold)
    upper_index = find_index(document_freq_dict_sorted, upper_threshold)
    trimmed_list = document_freq_dict_sorted[lower_index:upper_index]
    return trimmed_list


# Remove stopwords
def remove_stopwords(trimmed_list):
    word_list = []
    for i in trimmed_list:
        if not i[0] in stopwords:
            word_list.append(i[0])
    return word_list


# Write the word list to word_list.txt
def write_word_list(word_list):
    print "Writing word list in file word_list.txt"
    word_file = open('word_list.txt','w')
    for word in word_list:
        word_file.write(word + '\n')
    word_file.close()


# Create all topics list
def create_topics_list(article_data_list):
    topics_set = set()
    for record in article_data_list:
        topics_set.update(record.get("topics", []))
    return list(topics_set)


# Create all places list
def create_places_list(article_data_list):
    places_set = set()
    for record in article_data_list:
        places_set.update(record.get("places", []))
    return list(places_list)


# Write data matrix to data_matrix.csv
def write_data_matrix(article_data_list, word_list, topics_list, places_list):
    dmat_file = open("data_matrix.csv", "w")

    # on the first line, write word# / topic# / place#
    for index in range(1, 1+len(word_list)):
        dmat_file.write(", Word " + str(index))
    for index in range(1, 1+len(topics_list)):
        dmat_file.write(", Topic " + str(index))
    for index in range(1, 1+len(places_list)):
        dmat_file.write(", Place " + str(index))
    dmat_file.write("\n")

    # On the second line, write actual words/topics/place names
    for word in word_list:
        dmat_file.write("," + word)
    for topic in topics_list:
        dmat_file.write("," + topic)
    for place in places_list:
        dmat_file.write("," + place)
    dmat_file.write("\n")

    # Each line is for an article
    for article_data in article_data_list:
        string = "Article " + str(article_data["article_id"])
        for word in word_list:
            string += "," + str(article_data["freq_dict"][word])
        for topic in topics_list:
            if topic in article_data["topics"]:
                string += "," + str(TOPIC_WEIGHT)
            else:
                string += ",0"
        for topic in places_list:
            if topic in article_data["places"]:
                string += "," + str(PLACE_WEIGHT)
            else:
                string += ",0"
        dmat_file.write(string + "\n")
    dmat_file.close()


# Write transaction matrix to transaction_matrix.csv
def write_transaction_matrix(article_data_list, word_list):
    tmat_file = open("transaction_matrix.csv", "w")
    for article_data in article_data_list:
        string = "Article " + str(article_data["article_id"])
        bag = []
        for word in word_list:
            if article_data["freq_dict"][word] > 0:
                bag.append(word)
        string += ", \"" + ", ".join(bag) + "\""
        string += ", \"" + ", ".join(article_data["topics"]) + "\""
        string += ", \"" + ", ".join(article_data["places"]) + "\""
        tmat_file.write(string + "\n")
    tmat_file.close()




########
# Main #
########

# article_data_list is a list, with each element a dictionary.
# The dictionary(for an aricle) consists of:
# 1. article_id - The NEWID of reuters article
# 2. topics - This is a list of topics
# 3. places - This is a list of places
# 4. freq_dict - This is again a dictionary consisting of word-count pairs
article_data_list = []  # Store the word count for each article in this list
document_freq_dict = defaultdict(int)   # Store the number of articles in which a word appears

# Iterate through each file, parse and iterate through article
parse_time = -timeit.default_timer()
for dir_entry in sorted(os.listdir(PATH)):   #each file
    dir_entry_path = os.path.join(PATH, dir_entry)
    file = open(dir_entry_path)
    print "Reading file: " + dir_entry_path
    content = re.sub('&(.+?);|,|\'|"', '',file.read())  #remove &xxx; and comma and quotes, which may interfere with parsing
    parser = ArticleParser()  # Used for parsing the files
    parser.feed(content)
    file.close()

    for record in parser.records_list: #each article
        article_id = record.get("article_id", -1)
	topics_list = record.get("topics", [])
        places_list = record.get("places", [])
        freq_dict = get_frequency(record)
        article_data_list.append( {'article_id':article_id, 'topics':topics_list, 'places':places_list,'freq_dict':freq_dict} )

        for word in freq_dict.keys():
            document_freq_dict[word] += 1


parse_time += timeit.default_timer()
print "Parsed all articles in "+ str(round(parse_time,2)) + " seconds\n"


# Sort the document_freq_dict dictionary by the value
document_freq_dict_sorted = sorted(document_freq_dict.iteritems(), key=operator.itemgetter(1))

# Compute and write Document Frequency and Inverse Document Frequency to file
write_IDF(document_freq_dict_sorted)

# Find the thresholds on IDF and trim it
trimmed_list = get_trimmed_list(document_freq_dict_sorted)
print "Trimmed word list... Number of words:  " + str(len(trimmed_list))

# Load stopwords
file = open('stopwords')
stopwords = file.read().split()
file.close()
# Remove stopwords
word_list = remove_stopwords(trimmed_list)

# Write the word list
write_word_list(word_list)
print "Removed stopwords... Number of words: " + str(len(word_list))

# Create topics and places lists
topics_list = create_topics_list(article_data_list)
places_list = create_places_list(article_data_list)

# Write data matrix to data_matrix.csv
print "Writing data matrix in file data_matrix.csv"
dm_write_time = -timeit.default_timer()
write_data_matrix(article_data_list, word_list, topics_list, places_list)
dm_write_time += timeit.default_timer()
print "Data matrix written in " + str(round(dm_write_time,2)) + " seconds"

# Write transaction matrix to transaction_matrix.csv
print "Writing transaction matrix in file transaction_matrix.csv"
trm_write_time = -timeit.default_timer()
write_transaction_matrix(article_data_list, word_list)
trm_write_time += timeit.default_timer()
print "Transaction matrix written in " + str(round(trm_write_time,2)) + " seconds"

end = timeit.default_timer()
print "Total Execution Time :" + str(round(end- start,2))


