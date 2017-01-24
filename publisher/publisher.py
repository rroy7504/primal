#!/usr/bin/env python

import json
import pytz
import os
import sys
import time
import getopt

from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods.posts import NewPost

from datetime import datetime
from dateutil import tz
from random import randint

class Publisher(object):
    def __init__(self):
        with open('/home/ubuntu/pass/prod_pass.json', 'r') as f:
            cred = json.load(f)
        self.client = Client(cred['url'], cred['user'], cred['password'])

        
    def post(self, article, dry_run):
        wp_post = WordPressPost()
        wp_post.title = article['title']
        wp_post.content = article['content']
        wp_post.terms_names = article['terms_names']
        wp_post.custom_fields = []
        wp_post.custom_fields.append(article['custom_fields'])
        wp_post.post_status = 'publish'
        if not dry_run:
            wp_id = self.client.call(NewPost(wp_post))
            print 'Article published with title: %s and ID: %s' % (article['title'], wp_id)
        else:
            print 'Dry run is True. Skipped publishing.'
        return int(time.time())

    
def main(argv):
    dry_run = False
    republish = False
    try:
        opts, args = getopt.getopt(argv,"hdr",["dry_run", "republish"])
    except getopt.GetoptError:
        print 'publisher.py -d <True/False>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'publisher.py -d <True/False>'
            sys.exit()
        elif opt in ("-d", "--dry_run"):
            dry_run = True
        elif opt in ("-r", "--republish"):
            republish = True
 
    publisher = Publisher()
    path = '../article/' + datetime.now(pytz.timezone('US/Pacific')).strftime("%Y/%m/%d/")
    files = []
    for (dirpath, dirnames, filenames) in os.walk(path):
        files.extend(filenames)
        break


    # Reading data back
    for article_file in files:
        with open(path + article_file, 'r+') as f:
            article = json.load(f)
            if article['post_status'] != 'publish' or republish:
                article['publish_timestamp']  = publisher.post(article, dry_run)
                article['post_status'] = 'publish'
                f.seek(0)
                f.write(json.dumps(article))
                f.truncate()
            else:
                print 'Skipping article as it is already pusblished at %s' % article['publish_timestamp']

                
if __name__ == "__main__":
    main(sys.argv[1:])