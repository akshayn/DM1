#!/usr/bin/python

from HTMLParser import HTMLParser

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


