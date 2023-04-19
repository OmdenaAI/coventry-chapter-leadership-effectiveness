#!/usr/bin/env python
# coding: utf-8

# In[20]:


import pandas as pd
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Download nltk resources
nltk.download('stopwords')
nltk.download('punkt')

# Define function to clean text
def clean_text(text):
    # Remove URLs
    text = re.sub(r'http\S+', '', str(text))
    # Remove mentions and hashtags
    text = re.sub(r'@\w+|#\w+', '', text)
    # Remove punctuation and convert to lowercase
    text = re.sub(r'[^\w\s]', '', text).lower()
    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    tokens = word_tokenize(text)
    text = [word for word in tokens if not word in stop_words]
    text = ' '.join(text)
    return text

# Read in the data
df = pd.read_csv('Europe_replies_fixed.csv', dtype={'id': 'str'})

# Clean the 'tweet' column of the dataframe
df['tweet'] = df['tweet'].apply(clean_text)

# Clean the 'reply' column of the dataframe
df['reply'] = df['reply'].astype(str).apply(clean_text)

# Clean the 'secon_reply' column of the dataframe
df['second_reply'] = df['second_reply'].astype(str).apply(clean_text)

# Save the cleaned data to a new csv file
df.to_csv('Europe_preprocessed.csv', index=False)


# In[ ]:





# In[ ]:




