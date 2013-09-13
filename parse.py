from HTMLParser import HTMLParser

# class for parsing input file.
# This class creates a list of records.
# Each record represents a Reuters article.
# A record is a dictionary and contains 3 fields (keys):
#    1. topics
#          This is a python list of topics
#          Each topic is a string
#    2. title
#    3. places
#          This is a python list of places
#          Each place is a string
#    4. text

class ArticleParser(HTMLParser):

    # Set all flags to False and initialize records_list
    def reset(self):

        HTMLParser.reset(self)
	self.topics_flag = False
	self.places_flag = False
	self.title_flag = False
	self.body_flag = False
	self.topic_d_flag = False
	self.place_d_flag = False
	# List of records: each record represents an article
        self.records_list = []
	self.topics_list = []
	self.places_list = []


    def handle_starttag(self, tag, attrs):

        # Initialize a dictionary for this article's record 
        if tag.upper() == "REUTERS":
	    self.record = {}
            for attr in attrs:
                if attr[0].upper() == "NEWID":
                    self.record["article_id"] = int(attr[1])
                    break

        # A topic is found
	elif tag.upper() == "D":
	    if self.topics_flag:
	        self.topic_d_flag = True
	    elif self.places_flag:
	        self.place_d_flag = True

        # Initialize the list of topics to empty
	elif tag.upper() == "TOPICS":
            self.topics_flag = True
	    self.topics_list = []

	elif tag.upper() == "PLACES":
            self.places_flag = True
	    self.places_list = []

	elif tag.upper() == "TITLE":
            self.title_flag = True

	elif tag.upper() == "BODY":
            self.body_flag = True



    def handle_endtag(self, tag):

        # Append current record to the records_list when 
	# the article ends
        if tag.upper() == "REUTERS":
            if self.record.get("title", -1) != -1 or self.record.get("text", -1) != -1:
                self.records_list.append(self.record)

        elif tag.upper() == "D":
	    if self.topics_flag:
	        self.topic_d_flag = False
	    elif self.places_flag:
	        self.place_d_flag = False

	elif tag.upper() == "TOPICS":
	    self.record["topics"] = self.topics_list
            self.topics_flag = False

	elif tag.upper() == "PLACES":
	    self.record["places"] = self.places_list
            self.places_flag = False

	elif tag.upper() == "TITLE":
            self.title_flag = False

	elif tag.upper() == "BODY":
            self.body_flag = False



    def handle_data(self, data):

        # Append this topic to the current topics list
        if self.topic_d_flag:
	    if self.topics_flag:
	        self.topics_list.append(data)
	    elif self.places_flag:
	        self.places_list.append(data)

	elif self.title_flag:
	    self.record["title"] = data.lower() 

        elif self.body_flag:
	    self.record["text"] = data.lower()



