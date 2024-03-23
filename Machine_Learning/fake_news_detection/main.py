import gensim
import matplotlib.pyplot as plt
import nltk
import numpy as np
import os
import pandas as pd
import re
import seaborn as sns
import tensorflow as tf

from gensim.utils import simple_preprocess
from gensim.parsing.preprocessing import STOPWORDS
from jupyterthemes import jtplot
from nltk.corpus import stopwords
from nltk import metrics
from nltk import word_tokenize
from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk.tokenize import word_tokenize, sent_tokenize
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from tensorflow.keras.layers import Dense, Flatten, Embedding, Input, LSTM, Conv1D, MaxPool1D, Bidirectional
from tensorflow.keras.models import Sequential, Model
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.preprocessing.text import one_hot, Tokenizer
from wordcloud import WordCloud, STOPWORDS




# nltk.download('stopwords')
# nltk.download('punkt')

jtplot.style(theme='monokai',context='notebook', ticks=True, grid=False)

directory = os.path.dirname(os.path.abspath(__file__))


if not os.path.exists(os.path.join(directory,"Processed.csv")):             # if data hasn't been pre-processed

    df_true = pd.read_csv(os.path.join(directory, "True.csv"))
    df_fake = pd.read_csv(os.path.join(directory, "Fake.csv"))

    # print(df_true.head())           # View top 5 data from dataframe
    # print(df_fake.head())           
    # print(df_true.info())           # daframe information
    # print(df_fake.info())           
    # print(df_true.isnull().sum())   # checks and prints the number of null values
    # print(df_fake.isnull().sum())   




    # --------------------------------   Exploratory Data Analysis   --------------------------------

    # addition of a target class to indicate fake news
    df_true['isfake'] = 0
    df_fake['isfake'] = 1

    # Concatenate Real and Fake news
    df = pd.concat([df_true, df_fake]).reset_index(drop=True)
    df.drop(columns=['date'], inplace=True)     # removing date column as it isn't valid identifier
    df['original'] = df['title'] + ' ' + df['text']     # combine title and text together

    # print(df.head())            # view the combined dataframe
    # print(df.tail())




    # --------------------------------   Data Cleaning   --------------------------------

    stop_words = stopwords.words('english')
    stop_words.extend(['from', 'subject', 're', 'edu', 'use'])

    # Remove stopwords and words with 2 or less characters
    def preprocess(text):
        result = []
        for token in gensim.utils.simple_preprocess(text):
            if token not in gensim.parsing.preprocessing.STOPWORDS and len(token) > 3 and token not in stop_words:
                result.append(token)

        return result

    df['clean'] = df['original'].apply(preprocess)          # applying data cleaning to dataframe
    df['clean_joined'] = df['clean'].apply(lambda x: " ".join(x))

    # print(df['original'][0])
    # print(df['clean'][0])

    df.to_csv(os.path.join(directory, "Processed.csv"),sep='\t', encoding='utf-8')
    print("Data has been processed and saved for future use")
    




# --------------------------------   Visualize Cleaned up Dataset   --------------------------------

df  = pd.read_csv(os.path.join(directory, "Processed.csv"),sep='\t', encoding='utf-8')
stop_words = stopwords.words('english')
stop_words.extend(['from', 'subject', 're', 'edu', 'use'])

# plot the word cloud for text that is Real
if not os.path.exists(os.path.join(directory,"real_news_wordcloud.png")):
    plt.figure(figsize=(12,8))
    wc = WordCloud(max_words=2000,width=1600, height=800, stopwords=stop_words).generate(" ".join(df[df.isfake == 1].clean_joined))
    plt.imshow(wc, interpolation="bilinear")
    plt.axis('off')
    plt.tight_layout(pad =0)
    plt.savefig(os.path.join(directory,'real_news_wordcloud.png'))
    plt.show()


# plot the word cloud for text that is Fake
if not os.path.exists(os.path.join(directory,"fake_news_wordcloud.png")):
    plt.figure(figsize=(12,8))
    wc = WordCloud(max_words=2000,width=1600, height=800, stopwords=stop_words).generate(" ".join(df[df.isfake == 0].clean_joined))
    plt.imshow(wc, interpolation="bilinear")
    plt.axis('off')
    plt.tight_layout(pad =0)
    plt.savefig(os.path.join(directory,'fake_news_wordcloud.png'))
    plt.show()


# maxlen = -1                       # length of maximum document (News) will be needed to create word embeddings
# for doc in df.clean_joined:
#     tokens = nltk.word_tokenize(doc)
#     maxlen = max(maxlen, len(tokens))
# print(f"The maximum number of words in any document is = {maxlen}")         # here it is 4405


# import plotly.express as px
# fig = px.histogram(x = [len(nltk.word_tokenize(x)) for x in df.clean_joined], nbins=100)          # visualize the distribution of number of words in a text
# fig.show()
    




# --------------------------------   Preparing data before model training   --------------------------------

x_train, x_test, y_train, y_test = train_test_split(df.clean_joined, df.isfake, test_size=0.2)

# Create a tokenizer to tokenize the words and create seqeunce of tokenized words
total_words = 108704   
tokenizer  = Tokenizer(num_words = total_words)
tokenizer.fit_on_texts(x_train)
train_seqeunces = tokenizer.texts_to_sequences(x_train)
test_seqeunces = tokenizer.texts_to_sequences(x_test)

# Add padding to make sure all texts are of equal length
padded_train = pad_sequences(train_seqeunces, maxlen=4405, padding='post', truncating='post')
padded_test = pad_sequences(test_seqeunces, maxlen=4405, truncating='post')
    




# --------------------------------   Build and Train the model   --------------------------------

model = Sequential()

model.add(Embedding(total_words, output_dim=128))
model.add(Bidirectional(LSTM(128)))

model.add(Dense(128, activation='relu'))
model.add(Dense(1, activation='sigmoid'))
model.compile(optimizer='adam',loss='binary_crossentropy', metrics=['acc'])
# print(model.summary())

y_train = np.asarray(y_train)

model.fit(padded_train, y_train, batch_size=64, validation_split=0.1, epochs=2)
    




# --------------------------------   Access the trained model performance   --------------------------------

pred = model.predict(padded_test)

prediction = []
for i in range(len(pred)):
    if pred[i].item()>0.5:
        prediction.append(1)
    else:
        prediction.append(0)

accuracy =  accuracy_score(list(y_test), prediction)
print("Model Accuracy: ", accuracy)

