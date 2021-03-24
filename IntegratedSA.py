import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt
import spacy
import seaborn as sns
from wordcloud import WordCloud
import warnings
warnings.filterwarnings("ignore")
import re
from bs4 import BeautifulSoup
import nltk
from tqdm import tqdm
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from matplotlib import pyplot
from keras.models import Sequential
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score,f1_score, confusion_matrix
from keras.layers import Dense
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.layers import Dense , Input , LSTM , Embedding, Dropout , Activation, GRU, Flatten
from keras.layers import Bidirectional, GlobalMaxPool1D
from keras.models import Model, Sequential
from keras.layers import Convolution1D
from keras import initializers, regularizers, constraints, optimizers, layers
from tensorflow import keras
nltk.download('wordnet')
nltk.download('stopwords')



stop_words_fr = set(stopwords.words("french"))

lemmatizer = WordNetLemmatizer()

def decontract(text):
    text = re.sub(r"won\'t", "will not", text)
    text = re.sub(r"can\'t", "can not", text)
    text = re.sub(r"n\'t", " not", text)
    text = re.sub(r"\'re", " are", text)
    text = re.sub(r"\'s", " is", text)
    text = re.sub(r"\'d", " would", text)
    text = re.sub(r"\'ll", " will", text)
    text = re.sub(r"\'t", " not", text)
    text = re.sub(r"\'ve", " have", text)
    text = re.sub(r"\'m", " am", text)
    return text

def stopwords(language):
    stop_words_fr = stopwords.words(language)
    stop_words_fr = set(stop_words_fr)
    return stop_words_fr

lemmatizer = WordNetLemmatizer()

def preprocess_text(review):
    review = re.sub(r"http\S+", "", review)             # removing website links
    review = BeautifulSoup(review, 'html').get_text()   # removing html tags
    review = decontract(review)                         # decontracting
    review = re.sub("\S*\d\S*", "", review).strip()     # removing the words with numeric digits
    review = re.sub('[^A-Za-z]+', ' ', review)          # removing non-word characters
    review = review.lower()                             # converting to lower case
    #review = [word for word in review.split(" ") if not word in stop_words]
    review = [word for word in review.split(" ") if not word in stop_words_fr] # removing stop words
    review = [lemmatizer.lemmatize(token, "v") for token in review] #Lemmatization
    review = " ".join(review)
    review.strip()
    return review

def model_lstm(train_df):  
    top_words = 10000
    tokenizer = Tokenizer(num_words=top_words)
    tokenizer.fit_on_texts(train_df)
    list_tokenized_train = tokenizer.texts_to_sequences(train_df)

    max_review_length = 130
    X_train = pad_sequences(list_tokenized_train, maxlen=max_review_length)
    y_train = train_df


    embedding_vecor_length = 32
    model = Sequential()
    model.add(Embedding(top_words+1, embedding_vecor_length, input_length=max_review_length))
    model.add(LSTM(200))
    model.add(Dense(1, activation='sigmoid'))
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
    model.summary()
    
    lstm = model.fit(X_train, y_train, epochs=10, batch_size=64, validation_split=0.2)
    
    list_tokenized_test = tokenizer.texts_to_sequences(test_df)
    X_test = pad_sequences(list_tokenized_test, maxlen=max_review_length)
    y_test = test_df['Rating']
    prediction = model.predict(X_test)
    y_pred = (prediction > 0.5)
    print("Accuracy of the model : ", accuracy_score(y_pred, y_test))
    print('F1-score: ', f1_score(y_pred, y_test))
    print('Confusion matrix:')
    confusion = confusion_matrix(y_test,y_pred)
    score = model.evaluate(X_test, y_test, verbose=1)
    return score, confusion

#score = model.evaluate(X_test, y_test, verbose=1)

#print("Test Score:", score[0])
#print("Test Accuracy:", score[1])
