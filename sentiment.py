import numpy as np
import pandas as pd
import re
import emoji
from textblob import TextBlob
import nltk
from nltk.tokenize import word_tokenize,sent_tokenize
nltk.download('punkt')
from nltk.corpus import stopwords
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('vader_lexicon')
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import CountVectorizer
from wordcloud import WordCloud
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from sklearn.metrics import accuracy_score,f1_score
import streamlit as st
import pickle
result = None

st.title("Sentiment Analysis on User Reviews using ML")
text = st.text_input("Enter the Review")
import os

current_dir = os.path.dirname(__file__)

pickle_file_path = os.path.join(current_dir, "sentiment_yonex.pkl")

with open(pickle_file_path, "rb") as f:
    model = pickle.load(f)
if st.button("Submit")==True:
    result = model.predict([text])[0]

if result == 'Positive':
    st.image("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRSTH32czn83vjx3z0LeXRHgWRAG5vzrS1zmQ&s")
elif result == 'Negative':
    st.image("data:image/jpeg;base64,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")
elif result == 'Neutral':
    st.image("data:image/png;base64,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")