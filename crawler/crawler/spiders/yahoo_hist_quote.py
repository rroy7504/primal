import json, csv, sys, os, time
import scrapy

from string import Template


class StockSpider(scrapy.Spider):
    name = "yahoo_hist_quote"
    allowed_domains = ['finance.yahoo.com']
    
    def __init__(self):
	self.url_template = Template(('https://query2.finance.yahoo.com/v8/finance/chart/$symbol'
				 '?formatted=true&crumb=vdcqEPi9DhR&lang=en-US&region=US&period1=946800000&period2=$end_time'
                                 '&interval=1d&events=div%7Csplit&corsDomain=finance.yahoo.com'))
        self.base_dir = os.getcwd() + '/data/'
        self.symbol_path = os.getcwd() + '/spiders/sp500.csv'
        self.dev = False


    def start_requests(self):
        end_timestamp = int(time.time())
	with open(self.symbol_path) as csvfile:
    	    readCSV = csv.reader(csvfile, delimiter=',')
    	    for row in readCSV:
	       if 'symbol' != row[0]:
                 req_url = self.url_template.substitute(symbol=row[0], end_time=end_timestamp) 
                 if (not self.dev) or (self.dev and 'AAPL' == row[0]):
	           yield scrapy.Request(url=req_url, callback=self.parse)
                   
   

    def parse(self, response):
        jsonresponse = json.loads(response.body_as_unicode())
        for result in jsonresponse['chart']['result']:
	    if not 'timestamp' in result or not 'meta' in result:
              raise Exception('No timestamp or meta found in response')
            if not 'symbol' in result['meta']:
              raise Exception('No symbol found in response')
            timestamp = result['timestamp']
            symbol = result['meta']['symbol']
            div_date = []
            div_amount = []
            if 'events' in result and 'dividends' in result['events']:
              div = result['events']['dividends']
 	      for key in sorted(div.keys()):
		if div[key]['date'] and div[key]['amount']:
	          div_date.append(div[key]['date'])
                  div_amount.append(div[key]['amount'])
            if 'indicators' in result and 'quote' in result['indicators']:
	      for quote in result['indicators']['quote']:
                closeprice = quote['close']
                openprice = quote['open']
                volume = quote['volume']
                highprice = quote['high']
                lowprice = quote['low']
        quote_data = list(zip(timestamp, closeprice, openprice, lowprice, highprice, volume))
        div_data = list(zip(div_date, div_amount))
        directory = ''.join([self.base_dir,  symbol])
        if not os.path.exists(directory):
          os.makedirs(directory)
        with open((directory + '/historical_quote.csv'), 'w') as fp:
    	    outputFile = csv.writer(fp, delimiter=',')
            outputFile.writerow(['timestamp', 'close', 'open', 'low', 'high', 'volume'])  # header row
            outputFile.writerows(quote_data)
        if len(div_data):
	  with open((directory + '/historical_div.csv'), 'w') as fp:
            outputFile = csv.writer(fp, delimiter=',')
            outputFile.writerow(['timestamp', 'amount'])  # header row
            outputFile.writerows(div_data)

