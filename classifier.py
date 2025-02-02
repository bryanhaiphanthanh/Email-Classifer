#Author: Bryan Phan & Daniel Kwan

import pandas as pd
import nltk
nltk.download('wordnet')
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import matplotlib.pyplot as plt
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import svm
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import confusion_matrix, accuracy_score
from utils import get_polly_client
from pygame import mixer
from PIL import Image
import os
from pygame import mixer


global FILE
FILE = 'output.mp3'
def play_speech(text:str) -> None:
    """Uses AWS Polly to convert text to speech"""
    client = get_polly_client()
    speech_text = client.synthesize_speech(Text=f"You have entered: {text}",OutputFormat ='mp3',VoiceId = 'Joanna')

    with open(FILE, 'wb') as f:
        f.write(speech_text['AudioStream'].read())
        f.close()
    mixer.init()
    mixer.music.load(FILE)
    mixer.music.play()
    while mixer.music.get_busy(): 
        pass
    mixer.quit()
    os.remove(FILE)
"""Program to preform exploratory data analysis on emails.csv data set."""
#1 is spam, 0 is not spam
#read our data set into a pandas data frame

df = pd.read_csv("emails.csv")
print(df)

print("Spam, Count")
print(df['spam'].value_counts())
print("-------")

df['text'] = df['text'].str.replace("Subject:","")
df['text'] = df['text'].str.replace("re : ","")

def visualize(df: pd.DataFrame) -> None:
    """Visualization of text data"""
    #Lets first review spam and not spam data
    spam_data = df[df.spam == 1]
    not_spam_data = df[df.spam == 0]
    print(not_spam_data)
    print(spam_data)
    spam_emails = spam_data['text'].to_list()
    spam_emails = " ".join(spam_emails)
    not_spam_emails = not_spam_data['text'].to_list()
    not_spam_emails = " ".join(not_spam_emails)
    cloud_mask = np.array(Image.open("cloud.png"))
    spam_cloud = WordCloud(max_font_size = 150, mask=cloud_mask, background_color = "white", colormap="Reds").generate(spam_emails)
    not_spam_cloud = WordCloud(max_font_size = 150, mask=cloud_mask, background_color = "white").generate(not_spam_emails)

    plt.imshow(spam_cloud, interpolation="bilinear")
    plt.axis("off")
    plt.show()

    values = ['not spam', 'spam']
    df['spam'].value_counts().plot(kind='bar')
    plt.xticks(df['spam'].unique(), values)
    #plt.axis("off")
    plt.show()

x_train, x_test, y_train, y_test = train_test_split(df['text'], df['spam'], test_size = 0.3)
lemmatizer = nltk.WordNetLemmatizer()
x_train = [lemmatizer.lemmatize(word) for word in x_train]
global vectorizer
vectorizer = TfidfVectorizer(input = x_train, lowercase = True, stop_words = 'english')

tfidf_xtrain = vectorizer.fit_transform(x_train) #gives tf idf vector for x train
tfidf_xtest = vectorizer.transform(x_test) #gives tf idf for x trest

classifier = MultinomialNB()
classifier.fit(tfidf_xtrain, y_train)
actual = y_test.to_list()
print("classifier accuracy {:.2f}%".format(classifier.score(tfidf_xtest, y_test) * 100))
labels = classifier.predict(tfidf_xtest)
results = confusion_matrix(actual, labels)
#TP, FP
#FN, TN
print('Confusion Matrix :')
print(results)

print("------------------------------------------------------------------------------------")

global svm_model
svm_model = svm.SVC(C=1.0, kernel='linear', degree = 2, gamma='auto')
svm_model.fit(tfidf_xtrain, y_train)


predictions = svm_model.predict(tfidf_xtest)
# Use accuracy_score function to get the accuracy
print("SVM Accuracy Score -> ",accuracy_score(predictions, y_test)*100)
results2 = confusion_matrix(y_test.to_list(), predictions)
print(results2)

def get_input() -> int:
    text =input("Enter email: ")
    play_speech(text) # can probably add "enter blah blah blah, this is classified as ___"
    vectorized_string = vectorizer.transform([text])
    if svm_model.predict(vectorized_string)[0] == 0:
        return 0
    else:
        return 1

visualize(df)
if(get_input() == 0):
    print("Not spam")
else:
    print("Spam")