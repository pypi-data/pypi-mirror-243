import pandas as pd                 # 2.0.2
import numpy as np                  # 1.24.3         

from bs4 import BeautifulSoup       # 0.0.1
import requests                     # 2.28.1
import tabulate                     # 0.9.0
from langdetect import detect       # 1.0.9
import text2emotion as te           # 0.0.5 please downgrade following library emoji==1.7.0 

import os
import re
import time
import string
from datetime import datetime

from .sentiment_stuff import measure_afinn, measure_bertweet, measure_bing, measure_sid

# disabiling ssl verification 
requests.packages.urllib3.disable_warnings()

class nitter_scraper:
    # SETTINGS AND GLOBAL STUFF
    HEADERS = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.9",
            "Sec-Ch-Ua": '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": '"Windows"',
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
        }
    
    # list of different mirrors
    _endpoint = r'https://nitter.net/search'
    # _endpoint = r'https://nitter.nicfab.eu/search'
    # _endpoint = r'https://tweet.whateveritworks.org/search'
    
    wd = os.path.dirname(os.path.abspath(__file__))
    def __init__(self, headers=HEADERS):
        self._headers = headers

    '''
        generates formatted query to search nitter.net
        how to format search queries *q:
        https://developer.twitter.com/en/docs/twitter-api/tweets/search/integrate/build-a-query

        exs:
        snow day #noschool                          searches tweets with the words snow and day and hashtag #noschool
        snow OR day OR #noschool                    searches tweets with snow or day or the hashtag #noschool
        (@twitterdev OR @twitterapi) -@twitter      searches tweets that mention (@twitterdev or @twitterapi) and dont mention @twitter

        notes/useful:
        -is:retweet                                 for filtering out retweets *seems not working
        -                                           for negative
        #                                           for hashtags
        @user                                       for tweets mentioning user
        is:                                         for filtering tweets
        has:                                        for filtering e.x has:images
        from:user                                   for filtering tweets from user
        ()                                          for grouping terms
        OR                                          for matching term_i or term_j *default AND when no separator
        "term1 term2..."                            for terms with spaces
    '''
    def search(
        self, 
        q: str='', 
        max_pgs: int=50, 
        clean: bool=True, 
        lang: str='en', 
        filter_lang: bool=True, 
        show_rt: bool=False,
        sentiments: bool=False,
        add_q_col: bool=False,
        save: bool=False,
        wait_mins_rlim: int=4,
        short_date_format: bool=True,
        tweet_css: str='tweet-content', 
        showmore_css: str='show-more', 
        username_css: str='username', 
        date_css: str='tweet-date'):

        url = nitter_scraper.form_query(q)

        tweets = []
        for pg in range(max_pgs):
            resp = requests.get(url, headers=self._headers, verify=False)

            # loop to wait for rate limit * keeps track of how long rate limit waits
            waited = time.time()
            while resp.status_code == 429:
                print(f'rate limited waited for {(time.time() - waited) / 60}m')
                time.sleep(wait_mins_rlim * 60)
                resp = requests.get(url, headers=self._headers, verify=False)
                
            soup = BeautifulSoup(resp.text, 'html.parser')

            print(f'pgs {pg+1}/{max_pgs}')
            print(f'searching {url}\n')
            results = list(soup.find_all(class_=tweet_css))
            usernames = list(soup.find_all(class_=username_css))
            dates = list(soup.find_all(class_=date_css))
            zipped = zip(usernames, results, dates)

            if zipped: 
                for user, tweet, date in zipped:
                    # clean tweet
                    tweet_raw = nitter_scraper.soft_clean(tweet.text)
                    tweet = nitter_scraper.reformat_text(tweet.text) if clean else tweet.text
                    user = user.text[1:]
                    date = nitter_scraper.reformat_text(date.findChild('a')['title'])

                    # skip empty tweets
                    if not tweet: continue

                    # skip if not in desired language 
                    try:
                        if filter_lang and detect(tweet) != lang: continue
                    except:
                        continue

                    # skip if not showing retweets
                    if not show_rt and tweet.lower().startswith('rt'): continue
                    
                    # truncate date if short_date_format flag is on
                    if short_date_format: 
                        _ = datetime.strptime(date.split('  ')[0], "%b %d %Y")
                        date = _.strftime("%m/%d/%Y")

                    # finds all the sentiments
                    if sentiments:
                        happy, angry, surprise, sad, fear = list(te.get_emotion(tweet).values())
                        afinn = measure_afinn(tweet)
                        bing = measure_bing(tweet)
                        sid = measure_sid(tweet)
                        bertweet, confidence = measure_bertweet(tweet)

                        tweets.append({
                            'username': user,
                            'tweet_text': tweet,
                            'tweet_raw': tweet_raw,
                            'date': date,
                            'happy': happy,
                            'angry': angry,
                            'surprise': surprise,
                            'sad': sad,
                            'fear': fear,
                            'afinn': afinn,
                            'bing': bing,
                            'sid': sid,
                            'bertweet': bertweet,
                            'bertweet_confidence': confidence,
                        })

                    else:
                        tweets.append({
                            'username': user,
                            'tweet_text': tweet,
                            'tweet_raw': tweet_raw,
                            'date': date,
                        })



            # navigate to next page if it exists 
            # the -1 because the selector will also pick up the previous page link
            show_more = soup.find_all(class_=showmore_css)
            if show_more: show_more = show_more[-1]
            if not show_more:
                break

            url = show_more.findChild('a')['href']
            url = f'{self._endpoint}/{url}'

        if add_q_col: tweets['q'] = q
        tweets = pd.DataFrame(tweets).drop_duplicates(subset=['username', 'tweet_text'])
        print(f'results: {len(tweets)}\n')
        if save: 
            savep = datetime.today().strftime(f'%y%m%d_{nitter_scraper.reformat_text(q)}_{len(tweets)}.csv')
            tweets.to_csv(savep, index=False)

        return tweets


    # searches a list of queries, concatenates results and filters dups out
    def search_list(self, b: list, sentiments: bool=False, max_pgs: int=50, save: bool=True):
        tweets_df = []
        for q in b:
            print(f'searching for: {q}\n')
            tweets = self.search(q=q, sentiments=sentiments, max_pgs=max_pgs)
            tweets_df.append(tweets)

        tweets_df = pd.concat(tweets_df, axis=0, ignore_index=True).astype(str).fillna('-').drop_duplicates(subset=['username', 'tweet_text'])
        if save: 
            savep = datetime.today().strftime(f'%y%m%d_{b[0][1:-1]}_{len(tweets_df)}.csv')
            tweets_df.to_csv(savep, index=False)

        return tweets_df

    
    @staticmethod
    def form_query(q: str, since: str='', until: str='', near: str=''):
        f = 'tweets'
        url = f'{nitter_scraper._endpoint}?f={f}&q={q}&since={since}&until={until}&near={near}'
        return url
    
    # formats text by all alphanumeric lowercase no trailing punctuation + ' ' \n no special characters
    # edit this to apply more filters on resp.full_text
    @staticmethod
    def reformat_text(text: str) -> str:
        text = text.lower()
        text = re.sub(r'[^\w\s]', '', text)
        text = text.replace('\n', ' ')
        text = re.sub(r'http.*', '', text)
        text = text.strip(string.punctuation + string.whitespace)
        return text

    @staticmethod
    def soft_clean(text: str) -> str:
        text = re.sub(r"[\n'\",]", '', text)
        text = text.strip(string.whitespace)
        return text

    # utility function to read query file into word lists
    @staticmethod
    def read_queries(query_file: str=None):

        # default query file is bank_queries.csv for td stuff
        if not query_file:
            query_file = os.path.join(nitter_scraper.wd, 'query', 'bank_queries.csv')
        
        # reading the twitter queries for all banks
        # quoting = 1 is the same as csv.QUOTE_ALL so no need to import csv library
        if not os.path.exists(query_file):
            print(f'unable to read {query_file}\n')
            return 0
            
        queries = pd.read_csv(query_file, dtype=str)
        queries = queries.applymap(lambda txt : f'"{txt}"' if pd.notnull(txt) else np.nan)
        return [list(queries[col].dropna()) for col in queries.columns]


if __name__ == '__main__':
    # nitter = nitter_scraper()
    # banks = nitter_scraper.read_queries()

    # for b in banks:
    #     nitter.search_list(b=b, sentiments=True, max_pgs=50)

    nitter = nitter_scraper()
    bmo,cibc,rbc,scotiabank,td = nitter_scraper.read_queries()
    nitter.search_list(b=td, sentiments=True, max_pgs=50)


    # nitter = nitter_scraper()
    # nitter.search(q='"nasa" OR "spacex"', max_pgs=50, sentiments=True, save=True)
