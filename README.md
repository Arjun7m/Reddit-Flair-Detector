#### Link to the web application: https://reddit-detect-flair-app.herokuapp.com/
#### url of automated_testing endpoint: https://reddit-detect-flair-app.herokuapp.com/automated_testing

## Description
#### Flair Detector for Reddit India using Multi-Class Classification techniques. The web application has been created using Flask web framework, and has been deployed on the Heroku server.
#### The application categorises a flair in one of the nine flairs: Non-Political, Scheduled, AskIndia, Science/Technology, Politics, Business/Finance, Policy/Economy, Sports and Food.
#### The application also has an endpoint for automated testing, url to which is given above, which takes a .txt file as input, which contains a url to a Reddit India post in each line, and outputs a .json file with the urls and their predicted flairs.

## Running the /automated_testing endpoint
#### 1. Open the command line and change the directory to the directory where the "file.txt" file is stored.
#### 2. Invoke python at the directory.
#### 3. import requests
#### 4. files = {'upload_file': open('file.txt','rb')}
#### 5. r = requests.post("https://reddit-detect-flair-app.herokuapp.com/automated_testing", files=files)
#### 6. r.text
#### The output will give the url of the post, and its corresponding flair.

## Running the web application
#### 1. Open the link to the web application: https://reddit-detect-flair-app.herokuapp.com/
#### 2. Input the complete url of the Reddit India post in the text field.
#### 3. Click on the "predict" button.
#### 4. The flair of the reddit india post will be shown.

## GitHub Directory Structure
#### app.py : Contains the code of the Flask web application
#### nltk.txt : Contains the NLTK dependencies
#### Procfile : Sets up Heroku
#### requirements.txt : Contains the Python libraries used in the project
#### rf_model.pkl : Pickle file of the stored Classifier model
#### Data Extracted from Reddit : Folder containing the .csv files of the extracted Reddit India data
#### Exploratory Data Analysis : Folder containing the Jupyter notebook used for EDA
#### Extracting and Pre-Processing Data : Folder containing the Jupyter notebooks used for data extraction from Reddit India, and for pre-processing it
#### Pre-Processed Data : Folder containing the .csv files of the pre-processed Reddit India data
#### static : Folder containing the .css file
#### templates : Folder containing the .html files
#### Training Models: Folder containing the Jupyter notebooks used for training and testing the classifier models

## Approach
#### Multinomial Naive Bayes, Linear Support Vector Machine, Logistic Regression and Random Forest models were trained and tested on combinations of the following features:
#### 1. Title of the post
#### 2. Body of the post
#### 3. Comments of the post
#### Various subsets of the CommentForest of a post were tested.

## Results
#### The Random Forest model trained on the features Title + Body + Top 3 "Top-sorted" Top Level Comments of a post, for a dataset of 2080 posts, gave a test accuracy of 80.28 percent. 
