import nltk
import numpy as np
import random
import string
import bs4 as bs
import re
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from nltk.corpus import stopwords
from tkinter import *

file = open("D:\\Universty\\Last year\\2d Term\\NLP\\assignment1\\nlp.txt", encoding='utf-8')
stoplist = stopwords.words('arabic')
article_paragraphs = file.read()

article_text = article_paragraphs
article_text = re.sub(r'[^\u0621-\u064a\ufb50-\ufdff\ufe70-\ufefc]', ' ', article_text)  # remove unused char in text
article_text = re.sub('\.', ' ', article_text)  # remove dot
article_text = ' '.join([word for word in article_text.split() if word not in stoplist])
article_text = " ".join(article_text.split())  # remove extra spaces
print(len(article_text))

# reads and tokenize the file
tokens = nltk.word_tokenize(article_text)
ngrams_list = []

for num in range(0, len(tokens)):
    ngram = ' '.join(tokens[num:num + 3])
    ngrams_list.append(ngram)
# print(ngrams_list)
freq = {}
for item in ngrams_list:
    if item in freq:
        freq[item] += 1
    else:
        freq[item] = 1

df_ngram = pd.DataFrame([(freq[key], key) for key in freq]
                        # but the output in data frame and change the name of columns
                        ).rename(columns={0: 'frequency', 1: 'trigram'})


def search(word):


    dff=df_ngram[df_ngram['trigram'].str.match(word)]  #get the word that user enter and get all grams start with this word
    output=pd.DataFrame(columns=['result','prob'])

    for index in dff.index:
        row = dff['trigram'][index]
        second_word = ' '.join(row.split()[:2])
        count = article_text.count(second_word)
        if(count == 0):
            prob = 0.0
        else :
            prob = dff['frequency'][index] / count
        new_row={'result':row ,'prob':prob }
        output=output.append(new_row, ignore_index=True)

    output=output.sort_values(by=['prob'], ascending=False)

    final_output=output.iloc[:5, : 1]
    if final_output.empty:
        update(["No Result"])
    else:
        update(final_output.astype(str).values.tolist())
        print(final_output.to_string(index=False, header=False))


#update output
def update(data):
    output.delete(0,END)

    for item in data:
        output.insert(END,item)



def check():
    typed =input.get()

    if typed == '':
        update(["Please type any word to search"])
    else:
        search(typed)

root=Tk()
root.geometry("700x700")


#create lable
lable=Label(root,text="Autofill Search")
lable.pack(pady=20)
lable2=Label(root,text="Enter Your word")
lable2.place(relx = 1, x =-460, y = 60, anchor = NE)






button1 =  Button(root, text="Search", command=check)
#put on screen
button1.place(relx = 1, x =-180, y = 57, anchor = NE)

#create input box
input=Entry(root , width=20)

input.pack()

#create output results
output=Listbox(root,width=50,height=10)
output.pack(pady=40)

root.mainloop()


