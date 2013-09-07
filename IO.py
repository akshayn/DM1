#!/usr/bin/python

import os
from HTMLParser import HTMLParser

class TitleParser(HTMLParser):
    def reset(self):
        HTMLParser.reset(self)
        self.tag_flag = False
        self.data_list = []
    def handle_starttag(self, tag, attrs):
        if tag.upper() == "TITLE":
            self.tag_flag = True
    def handle_endtag(self, tag):
        if tag.upper() == "TITLE":
            self.tag_flag = False
    def handle_data(self, data):
        if self.tag_flag:
            self.data_list.append(data)

def write_to_file(data):
   file = open("out.txt","w")
   for list in data:
      for item in data[list]:
         file.write(item)
         file.write("\n")
      file.write("\n\n")



# Main
path = r'reuters'
data = {}
parser = TitleParser()

for dir_entry in os.listdir(path):
    dir_entry_path = os.path.join(path, dir_entry)
    with open(dir_entry_path, 'r') as my_file:
         parser.feed(my_file.read())
         data[dir_entry] = parser.data_list

write_to_file(data)
