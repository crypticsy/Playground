import os
import re
import matplotlib.pyplot as pit
from wordcloud import WordCloud, STOPWORDS


path = os.path.dirname(os.path.abspath(__file__))
words = {}

def word_counter(line):
    for text in line.split():
        for i in text.split('|'): 
            cur = re.sub(r'[\'\" \.\?\,\;\-\!\�\:]+', '', i.lower())
            cur = re.sub(r'\<[^>]*\)', '', i.lower())
            if len(cur)>2 and not cur.isdigit():
                words[cur] = words.get(cur,0) + 1

for file in os.listdir(path+"\\data\\"):
    if file.endswith(".srt"):
        count, space, valid  = 1, True, False
        with open(path+"\\data\\"+file) as f:
            for i in f.readlines():
                if space and not valid and i.strip() == str(count):
                    count+=1
                    space = False
                elif space == False and not valid:
                    valid = True
                elif i == "\n" and valid:
                    valid = False
                    space = True
                elif not space and valid:
                    word_counter(i)

    elif file.endswith(".sub"):
        with open(path+"\\data\\"+file) as f:
            for i in f.readlines():
                reverse = i[::-1]
                pos = reverse.find("}")
                word_counter(reverse[:pos][::-1].strip())

# print("Number of unique words", len(words))

wordcloud = WordCloud(
    width = 640,
    height = 640,
    background_color= 'black',
    stopwords = STOPWORDS).generate(str(words))          # at the end it also removes words like "a" "ah" and so on
fig = pit.figure(
    figsize = (12,8),
    facecolor='k',
    edgecolor='k')

pit.imshow(wordcloud, interpolation='bilinear')
pit.axis('off')
pit.tight_layout(pad =0)
pit.savefig(os.path.join(path,'wordcloud.png'))
pit.show()