import nltk
import numpy as np
import os
import re
import pandas as pd
import pickle
from pandas.io.stata import precision_loss_doc
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer, strip_accents_ascii
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegressionCV
from sklearn.model_selection import train_test_split
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer




# --- Loading the dataset ---

path = os.path.dirname(os.path.abspath(__file__))
df = pd.read_csv(os.path.join(path,'data','movie_data.csv'))

# print(df.head(10))      # viewing the first 10 reviews
# print(df['review'][0])  # Expanding the comment of the first data 



# --- Transforming Documents into Feature Vectors ---

count = CountVectorizer()

# docs = np.array( ['The sun is shining', 
#                   'The weather is sweet',
#                   'The is shining, the weather is sweet, and one and one is two.'])

# bag = count.fit_transform(docs)           # Demo

# print(count.vocabulary_)
# print(bag.toarray())



# --- Word relevancy using term frequency-inverse document frequency ---

np.set_printoptions(precision=2)

# tfidf = TfidfTransformer(use_idf=True, norm='l2', smooth_idf=True)
# print(tfidf.fit_transform(bag).toarray())



# --- Data Preparation ---

def preprocessor(text):
    text = re.sub('<[^>]*>', '', text)
    emoticons = re.findall('(?::|;|=)(?:-)?(?:\)|\(|D|P)', text)
    text = re.sub('[\W]+', ' ', text.lower()) +\
                ' '.join(emoticons).replace('-','')
    return text

# print(preprocessor(df.loc[0, 'review'][-50:]))
# print(preprocessor("</a>This  :) is a :(  test :-)!"))
df['review'] = df['review'].apply(preprocessor)



# --- Tokenizatoin of documents ---

porter = PorterStemmer()

def tokenizer(text): 
    return text.split()

def tokenizer_porter(text): 
    return [porter.stem(word) for word in text.split()]

stop = stopwords.words('english')
# print([w for w in tokenizer_porter('a running runner likes to run a lot') if w not in stop])



# --- Tansform Text Data into TF-IDF vectors ---

tfidf = TfidfVectorizer(strip_accents=None, lowercase=False, preprocessor=None, tokenizer=tokenizer_porter, use_idf=True, norm='l2', smooth_idf=True)

y = df.sentiment.values
X = tfidf.fit_transform(df.review)



# --- Document Classification using Logistic Regression ---

X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=1, test_size=0.5, shuffle=False )

if not os.path.exists(os.path.join(path, 'saved_model.sav')):
    clf = LogisticRegressionCV(cv = 5, scoring='accuracy', random_state=0, n_jobs=-1, verbose=3, max_iter=300).fit(X_train, y_train)

    with open(os.path.join(path,"saved_model.sav"), 'wb') as saved_model:
        pickle.dump(clf, saved_model)



# --- Model Evaluation ---

filename = 'saved_model.sav'
saved_clf = pickle.load(open(os.path.join(path, filename),'rb'))

print(saved_clf.score(X_test, y_test))