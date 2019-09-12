#=====================================LIBS FOR FLASK SERVER=========================================

from flask import Flask, render_template, url_for, request
from flask_basicauth import BasicAuth
from flask_cors import CORS, cross_origin
from sklearn.externals import joblib
from werkzeug import secure_filename
import os
import regex as re
import pandas as pd
import json

import functions

import warnings
warnings.filterwarnings("ignore")



#=========================================FLASK INIT============================================

template_dir = os.path.abspath('./templates')
static_dir = os.path.abspath('./static')
CSV_dir = os.path.abspath('./CSVs')
app = Flask(__name__, template_folder = template_dir, static_url_path = '', static_folder = static_dir)
CORS(app)
app.jinja_env.globals.update(zip=zip)
app.config['BASIC_AUTH_USERNAME'] = 'automizeapps'
app.config['BASIC_AUTH_PASSWORD'] = 'adminpass'
app.config['BASIC_AUTH_FORCE'] = True
basic_auth = BasicAuth(app)

#=============================================Main CSV / DataFile==================================

MAIN_CSV_Filename = '/master_script_results.csv'
Feature_Breakdown_CSV_Filename = '/forfeaturehtml.csv'

#===========================================ROUTES=================================================

@app.route('/')
@basic_auth.required
def home():
    df = pd.read_csv(CSV_dir + MAIN_CSV_Filename)
    date = []
    review = []
    for i in range(len(df)):
        if(i%20 == 0):
            date.append((df['Review_Date'][i]))
            review.append(df['Review_Stars'][i])
        
    return render_template('index.html', date = date, review = review)

@app.route('/sentiment')
@basic_auth.required
def sentiment_template():
    sentiObj = functions.Sentiment(CSV_dir + MAIN_CSV_Filename)
    positiveScore, negativeScore, revp, revn = sentiObj.createSentimentScore()
    return render_template('detailed_sentiment.html', positiveScore = positiveScore, negativeScore = negativeScore, review_pos = revp, review_neg = revn )

@app.route('/wordcloud')
@basic_auth.required
def wordcloud_template():
    wordObj = functions.wordcloudCreate(CSV_dir + MAIN_CSV_Filename)
    url_all, url_noun, url_adj, url_verb = wordObj.createWordClouds()
    return render_template('wordcloud.html', url_all = url_all, url_noun = url_noun, url_adj = url_adj, url_verb = url_verb)

@app.route('/featurebreak')
@basic_auth.required
def feature_template():
    df = pd.read_csv(CSV_dir + Feature_Breakdown_CSV_Filename)
    print(df.to_dict())
    row_list = []
    for index, rows in df.iterrows():
        row_list.append([rows.Word, rows.PRev, rows.NRev])
    return render_template('feature_breakdown.html', list = row_list)

@app.route('/all_textual')
@basic_auth.required
def textual_template():
    return render_template('tables.html')

@app.route('/suggestions')
@basic_auth.required
def suggestions_template():
    return render_template('suggestions.html')

@app.route('/map')
@basic_auth.required
def map_template():
    return render_template('map.html')

@app.route('/upload')
@basic_auth.required
def upload_file_starter():
    return 'Feature Turned off!'

@app.errorhandler(500)
def server_error(e):
    logging.exception('An error occurred during a request.')
    return """
    An internal error occurred: <pre>{}</pre>
    See logs for full stacktrace.
    """.format(e), 500

#=====================================APP ACTIVATOR=============================================

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
