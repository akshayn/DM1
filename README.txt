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
The feature vectors are in csv files and are best viewed in CSV readers like LibreOffice Calc/Microsoft Excel


The output generated consists of following files:
1) Inverse Document Frequency (IDF.csv)
   This provides a list of words over all the articles and document frequency and inverse document frequency for each word.

2) Word List (word_list.txt)
   The list of words after trimming and removing stopwords and used for constructing feature vectors.

3) Data Matrix (data_matrix.csv)
   This feature vector displays number of occurences of each word from word list in each article.

4) Transaction Matrix (transaction_matrix.csv)
   This feature vector displays a list of word appearing in each article.



Source files
------------
1) main.py
2) parse.py
3) stopwords
4) reuters/*
5) Makefile
 
