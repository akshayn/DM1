Vaibhav Devekar (devekar.1@osu.edu)
Akshay Nikam (nikam.5@osu.edu)


==========================
Data Mining - Assignment 1
==========================
*** NOTE: The program makes use of NLTK for stemming. ***


Executing the program
---------------------
1) Run command "make run" to execute the python program.
2) Run command "make clean" to remove output files.


Viewing Output
--------------
The feature vectors are in csv files and are best viewed in CSV readers like LibreOffice Calc/Microsoft Excel.
You may need to enable "Quoted field as text" to allow quoted list of words to appear in single column in transaction matrix.

The output generated consists of following files:
1) Inverse Document Frequency (IDF.csv)
   This provides a list of words over all the articles and document frequency and inverse document frequency for each word.

   Output Format:
   Word, Document Frequency, Inverse Document Frequency

2) Word List (word_list.txt)
   The list of words after trimming and removing stopwords and is used for constructing feature vectors.

3) Data Matrix (data_matrix.csv)
   This feature vector displays number of occurences of each word from word list in each article.

   Output Format:
   Article Id, Word 1, Word 2,... Topic 1, Topic 2, ..., Place 1, Place 2,...

4) Transaction Matrix (transaction_matrix.csv)
   This feature vector displays a list of words appearing in each article, followed by topics and places.

   Output Format:
   Article Id, Bag of words, Bag of topics, Bag of places


Source files
------------
1) main.py
2) parse.py
3) stopwords
4) reuters/*
5) Makefile
 
