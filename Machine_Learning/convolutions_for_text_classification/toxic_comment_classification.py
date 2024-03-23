import os
import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras.preprocessing import text, sequence
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Activation, Embedding
from tensorflow.keras.layers import Conv1D, GlobalMaxPooling1D, MaxPooling1D
from sklearn.model_selection import train_test_split
from tensorflow.python.keras.engine import sequential
from tensorflow.python.ops.gen_batch_ops import batch
from tensorflow.python.ops.variables import trainable_variables
import wordcloud


# print(tf.__version__)         # To check the current tensorflow version
path = os.path.dirname(os.path.abspath(__file__))






# --- Load data ---

train_df = pd.read_csv(path+'\\train.csv.zip').fillna(' ')         # fillna(' ')  fills all the missing values as space
# print( train_df.sample(10, random_state=1) )          # view 10 random data from the file

x = train_df['comment_text'].values                 # python object to store comments
y = train_df['toxic'].values

# --- View few toxic comments --- 

# print( train_df.loc[train_df['toxic'] == 1].sample(10, random_state=10) )






# --- View few toxic comments in a word bubble ---
  
# from wordcloud import WordCloud, STOPWORDS
# import matplotlib.pyplot as pit

# comments = train_df['comment_text'].loc[train_df['toxic']==1].values
# wordcloud = WordCloud(
#     width = 640,
#     height = 640,
#     background_color= 'black',
#     stopwords = STOPWORDS).generate(str(comments))          # at the end it also removes words like "a" "ah" and so on
# fig = pit.figure(
#     figsize = (12,8),
#     facecolor='k',
#     edgecolor='k')

# pit.imshow(wordcloud, interpolation='bilinear')
# pit.axis('off')
# pit.tight_layout(pad =0)
# pit.show()


# --- Frequency of toxic commetns ---

# print( train_df['toxic'].value_counts() )







# --- Data prep - Tokenize and Pad Text Data ---

max_features = 20000        # maximum number of most frequent numbers count
max_text_length = 400       # comments less than this length will be padded to normalize

x_tokenizer = text.Tokenizer(max_features)
x_tokenizer.fit_on_texts(list(x))
x_tokenized = x_tokenizer.texts_to_sequences(x)
x_train_val = sequence.pad_sequences(x_tokenized, maxlen = max_text_length)






# --- Prepare Embedding Matrix with Pre-trained GloVe Embeddings ---

embedding_dim = 100
embeddings_index = dict()


with open(path+'\\glove.6B.100d.txt', encoding="utf8") as f:
    for line in f:
        values = line.split()
        word = values[0]
        coefs = np.asarray(values[1:],dtype='float32')
        embeddings_index[word] = coefs

print(f'Found {len(embeddings_index)} word vectors.')

embedding_matrix = np.zeros((max_features, embedding_dim))
for word, index in x_tokenizer.word_index.items():
    if index > max_features - 1: 
        break
    else:
        embedding_vector = embeddings_index.get(word)
        if embedding_vector is not None:
            embedding_matrix[index] = embedding_vector
            





# --- Create the embedding layer ---

model = Sequential()
model.add(Embedding(max_features,
                    embedding_dim, 
                    embeddings_initializer = tf.keras.initializers.Constant( embedding_matrix),
                    trainable = False))
model.add(Dropout(0.2))






# --- Build the model ---

filters = 250
kernel_size = 3
hidden_dims = 250

model.add(Conv1D(filters, kernel_size, padding='valid'))
model.add(MaxPooling1D())
model.add(Conv1D(filters, 5, padding='valid',activation='relu'))

model.add(GlobalMaxPooling1D())
model.add(Dense(hidden_dims, activation='relu'))
model.add(Dropout(0.2))

model.add(Dense(1, activation='sigmoid'))
# print(model.summary())

model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])






# --- Train model ---

x_train, x_val, y_train, y_val = train_test_split(x_train_val, y, test_size=0.15, random_state=1)
batch_size = 32
epochs = 3

model.fit(x_train, y_train, batch_size=batch_size, epochs=epochs, validation_data = (x_val, y_val))






# --- Evaluate model ---

test_df = pd.read_csv(path+'\\test.csv.zip')

x_test = test_df['comment_text'].values

x_test_tokenized = x_tokenizer.texts_to_sequences(x_test)
x_testing = sequence.pad_sequences(x_test_tokenized, maxlen=max_text_length)

y_testing = model.predict(x_testing, verbose=1,batch_size=32)

print(y_testing.shape)
print(y_testing[0])

test_df['Toxic'] = ['not toixc' if x<.5 else 'toxic' for x in y_testing]
print(test_df[['comment_text', 'Toxic']].head(20))
