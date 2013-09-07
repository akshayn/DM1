#!/usr/bin/python

import os
import re
from HTMLParser import HTMLParser
from collections import defaultdict
import csv

class TitleParser(HTMLParser):
    def reset(self):
        HTMLParser.reset(self)
        self.tag_flag = False
        self.data_list = []
    def handle_starttag(self, tag, attrs):
        if tag.upper() == "BODY":
            self.tag_flag = True
    def handle_endtag(self, tag):
        if tag.upper() == "BODY":
            self.tag_flag = False
    def handle_data(self, data):
        if self.tag_flag:
            self.data_list.append(data)

# Main
path = r'reuters'
data = {}
parser = TitleParser()

file = open("reuters/reut2-000.sgm")
content = re.sub('&(.+?);', '',file.read())  #remove &xxx;
parser.feed(content)
file.close()

d = defaultdict(int)
for item in parser.data_list:
   item = re.sub( '[<>]', '', item) #remove <, >
   item = item.replace('\n','') #remove newlines
   list = item.split()   #tokenize
   for i in list:
      d[i] += 1

file = open("out.txt","w")
writer = csv.writer(file,delimiter = ':')
for key, value in d.items():
   writer.writerow([key, value])

file.close()


