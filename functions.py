import helperFunctions # Helper Functions Imported

import numpy as np
import pandas as pd
from nltk.corpus import stopwords
from wordcloud import WordCloud, ImageColorGenerator
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer



#=================================MAIN CLASS FOR SENT. ANALYSIS=============================
class Sentiment:
    def __init__(self, csv_file_name):
        self.csv_file_name = csv_file_name
    
    def createSentimentScore(self):
        data = pd.read_csv(self.csv_file_name , delimiter=',')
        stop = set(stopwords.words('english'))
        list_process=data['Review_Text'].tolist()
        list_final=[]
        helperFunctions.helperFunctions.remove_punctuation(list_process)
        for i in range(len(list_process)):
            stop_free = " ".join([i for i in list_process[i].lower().split() if i not in stop])
            list_final.append(stop_free)
        
        analyzer = SentimentIntensityAnalyzer()
        review_pos = []
        revp = []
        review_neg=[]
        revn = []
        count=0
        for line in list_final:
            vs = analyzer.polarity_scores(line)
            if(vs['pos']>vs['neg']):
                count+=1
                revp.append(line)
            else:
                revn.append(line)
            review_pos.append(vs['pos'])

            review_neg.append(vs['neg'])
        
        positiveScore = round(count/len(list_process)*100, 2)
        negativeScore = round((1-(count/len(list_process)))*100, 2)

        return positiveScore, negativeScore, revp, revn

#===============================Main Class for Wordcloud Creation ======================================

class wordcloudCreate:
    def __init__(self, csv_file_name):
        self.csv_file_name = csv_file_name

    def onecloud(wordcloud_X, fileName):
        token_data = [item for sublist in wordcloud_X for item in sublist]
        list_word1=' '.join(token_data)
        wordcloud = WordCloud(width=800, height=400, background_color="white").generate(list_word1)
        pathToFile = './static/img/' + fileName
        wordcloud.to_file(pathToFile)
        return 'img/' + fileName

    def createWordClouds(self):
        data = pd.read_csv(self.csv_file_name , delimiter=',')
        list_process = data['Review_Text'].tolist()
        helperFunctions.helperFunctions.remove_punctuation(list_process)
        wordcloud_1, wordcloud_2, wordcloud_3, wordcloud_4 = helperFunctions.helperFunctions.create_wordclouds(list_process)
        
        url_all = wordcloudCreate.onecloud(wordcloud_1, 'titan_all.png')
        url_noun = wordcloudCreate.onecloud(wordcloud_2, 'titan_noun.png')
        url_adj = wordcloudCreate.onecloud(wordcloud_2, 'titan_adj.png')
        url_verb = wordcloudCreate.onecloud(wordcloud_4, 'titan_verb.png')
        
        return url_all, url_noun, url_adj, url_verb