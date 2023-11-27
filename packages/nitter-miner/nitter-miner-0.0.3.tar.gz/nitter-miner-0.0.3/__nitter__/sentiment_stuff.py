import numpy as np
import pandas as pd
from transformers import pipeline
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# need profanity_check==1.0.3 and it uses old scikit-learn==0.21.x cause of some sklearn...joblib so yea...
# from profanity_check import predict_prob as measure_swear

import os

wd = os.path.dirname(os.path.abspath(__file__))

bertweet = pipeline('sentiment-analysis', model='finiteautomata/bertweet-base-sentiment-analysis')
_sid = SentimentIntensityAnalyzer()

# fixing ssl verification issue by setting env var to point to the .pem ssl certificate
# if not on wsl need to install pip-system-certs==4.0 or latest and comment this out
os.environ["REQUESTS_CA_BUNDLE"] = r'/etc/ssl/certs/ca-bundle.crt'

# private afinn bing numpy lookup tables
_AFINN_PATH, _BING_PATH = os.path.join(wd, "sentiment_dictionaries/afinn.csv"), os.path.join(wd, "sentiment_dictionaries/bing.csv")
_AFINN, _BING = pd.read_csv(_AFINN_PATH).to_numpy(), pd.read_csv(_BING_PATH).to_numpy()

# measure sentiment by the passed in sentiment dictionary
def measure(txt: str, sentiment_df: np.ndarray):
    measure = 0
    for w in txt.split(' '):
        if w in sentiment_df[:, 0]: measure += int(sentiment_df[sentiment_df[:, 0] == w, 1][0])

    return measure

# making abstracted functions to use in tweet extraction file
measure_sid = lambda txt : _sid.polarity_scores(txt)['compound']
measure_afinn = lambda txt : measure(txt, _AFINN)
measure_bing = lambda txt : measure(txt, _BING)

def measure_bertweet(txt: str):
    yh = bertweet(txt, truncation=True)
    
    if len(yh) != 1: 
        return 0, 0
    
    yh = yh[0]
    if yh['label'] == 'POS': label = 1
    elif yh['label'] == 'NEG': label = -1
    else: label = 0

    score = float(yh['score'])
    return label, score


if __name__ == '__main__':
    # still need to do ncr stuff
    # txt = 'super cute little fantasy poro that looks like a hamster mixed with a poro from league of legends is has a translucent shiny horn in the  made with nightcafe creator'
    # print(f'afinn: {measure_afinn(txt)}\nbing: {measure_bing(txt)}\nsid: {measure_sid(txt)}')
    txt = 'thats a terrible idea. seriously idk how riot thinks these balance changes are good for the game'
    res = measure_bertweet(txt)
    print(res)







