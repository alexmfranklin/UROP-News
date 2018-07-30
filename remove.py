from nltk.tokenize import word_tokenize #should install nltk in advance 
from nltk.corpus import stopwords
#coding:utf-8 -*-
text=open('haha.txt','r')  #any text input
courses=[line.strip() for line in text]
courses_name=[course.split('\t')[0] for course in courses]
texts_lower=[[word for word in document.lower().split()]for document in courses]
texts_tokenized=[[word.lower()for word in word_tokenize(document.encode('utf-8').decode('utf-8'))]for document in courses]
english_stopwords=stopwords.words('english')
texts_filtered_stopwords=[[word for word in document if not word in english_stopwords]for document in texts_tokenized]
english_punctuations=[',','.',';','?','(',')','[',']','&','!','*','@','#','$','%',]
texts_filtered=[[word for word in document if not word in english_punctuations] for document in texts_filtered_stopwords]
print(texts_filtered[0]) #texts_filtered a list variable contain all the left words without the basic words
