from flask import Flask, render_template, url_for, request
import pandas as pd
import pickle
import re
from bs4 import BeautifulSoup
import nltk
from nltk.corpus import stopwords
import praw
import joblib
import sys
import json

app = Flask(__name__,template_folder='templates')


cid = '#'
csecret = '#'
user_agent = '#'
redirect_uri='#'


REPLACE_BY_SPACE_RE = re.compile('[/(){}\[\]\|@,.;_]')
BAD_SYMBOLS_RE = re.compile('[^0-9a-z #+_]')
STOPWORDS = set(stopwords.words('english'))

def decontracted(phrase):
    # specific
    phrase = re.sub(r"won\'t", "will not", phrase)
    phrase = re.sub(r"can\'t", "can not", phrase)
    phrase = re.sub(r"ive ", "i have ", phrase)
    phrase = re.sub(r" hes ", " he is ", phrase)
    phrase = re.sub(r" shes ", " she is ", phrase)
    phrase = re.sub(r"http", "", phrase)
    phrase = re.sub(r"www", "", phrase)
    phrase = re.sub(r"\.com", "", phrase)

    # general
    phrase = re.sub(r"n\'t", " not", phrase)
    phrase = re.sub(r"\'re", " are", phrase)
    phrase = re.sub(r"\'s", " is", phrase)
    phrase = re.sub(r"\'d", " would", phrase)
    phrase = re.sub(r"\'ll", " will", phrase)
    phrase = re.sub(r"\'t", " not", phrase)
    phrase = re.sub(r"\'ve", " have", phrase)
    phrase = re.sub(r"\'m", " am", phrase)
    return phrase

def conv_str(text):
    return str(text)

def cleaner(text):

    text = BeautifulSoup(text, "lxml").text
    text = text.lower()
    text = ' '.join(decontracted(word) for word in text.split())
    text = REPLACE_BY_SPACE_RE.sub(' ', text)
    text = BAD_SYMBOLS_RE.sub('', text)
    text = ' '.join(word for word in text.split() if word not in STOPWORDS)
    return text

def detect_flair(url):
	reddit = praw.Reddit(client_id=cid, client_secret=csecret, user_agent=user_agent, redirect_uri=redirect_uri)
	submission = reddit.submission(url = url)

	data = {}

	data['title'] = submission.title
	data['url'] = url
	data['body'] = submission.selftext

	submission.comment_sort = "top"
	all_comments = submission.comments
	comm = ''
	i = 0
	for comment in all_comments:
		comm = comm + " " + comment.body
		i = i + 1
		if i>=3:
			break
	data['comments'] = comm

	data['title'] = cleaner(data['title'])
	data['body'] = cleaner(data['body'])
	data['comments'] = cleaner(data['comments'])
	data['all_data'] = data['title'] + data['body'] + data['comments']

	return data['all_data']

@app.route('/')
def home():
	return render_template('home.html')


@app.route('/predict',methods=['POST'])
def predict():
	if request.method == 'POST':
		rf_model = open('rf_model.pkl','rb')
		clf = joblib.load(rf_model)
		text = request.form['message']
		extract = detect_flair(text)
		my_prediction = clf.predict([extract])
	return render_template('result.html',prediction = my_prediction)


@app.route('/automated_testing', methods=['POST'])
def automated_testing():
	rf_model = open('rf_model.pkl','rb')
	clf = joblib.load(rf_model)
	output = {}
	for line in request.files['upload_file']:
		line = line.decode().replace('\n', '').replace('\r', '')
		extract = detect_flair(line)
		output[line] = clf.predict([extract])[0]
	output = json.dumps(output)
	return output

if __name__ == "__main__":
    app.run(use_reloader=False)