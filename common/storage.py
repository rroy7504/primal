from datetime import datetime
import json
import pytz
import os
import pandas as pd


class Storage(object):
    def __init__(self):
        self.quote_base_path = '/home/ubuntu/crawler/crawler/data/'
        
        
    def write_article(self, out_dir, article):
        json_obj = json.dumps(article, default=lambda o: o.__dict__)    
        if not os.path.exists(out_dir):
              os.makedirs(out_dir)
        with open(out_dir + article['title'].replace(' ', '_') + '.json', 'w') as outfile:
            outfile.write(json_obj)
        
        
    def read_historic_quote(self, symbol):
        path = self.quote_base_path + symbol + '/historical_quote.csv'  
        return pd.read_csv(path)