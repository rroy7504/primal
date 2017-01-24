#!/usr/bin/env python

import re
import sys
import json
import os

from generator import util
from common import article
from common import storage

from datetime import datetime
from dateutil import tz
import pytz

class Generator(object):
    def __init__(self):
        self.article_base_path = '../article/'

    def generate(self, template):
        article_template = template['article']
        fn_list = re.findall('%([^%]*)%', article_template)
        for fn in fn_list:
            article_template = article_template.replace('%'+fn+'%', str(eval('util.' + fn)))
        a = article.getArticle()
        a['title'] = template['title']
        a['content'] = article_template
        a['terms_names'] = {
        'post_tag': ['US Stock'],
        'category': ['Markets'] }
        a['custom_fields'] = [{'key': 'wpzoom_is_featured', 'value': '1'},
                          {'key': 'wpzoom_is_breaking', 'value': '1'},
                          {'key': 'wpzoom_post_template', 'value': 'side-right'}]
        output_dir = self.article_base_path + datetime.now(pytz.timezone('US/Pacific')).strftime("%Y/%m/%d/")
        json_obj = json.dumps(a, default=lambda o: o.__dict__)    
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        output_filename = output_dir + a['title'].replace(' ', '_') + '.json'
        if not os.path.isfile(output_filename):
            with open(output_filename, 'w') as outfile:
                outfile.write(json_obj)
                print 'Article generated at %s' % output_filename
        else:
            print 'Article already exists skiiping over writing: %s' % output_filename
    

def main(argv):
    generator = Generator()
    template_dir = '../templates/'
    files = []
    for (dirpath, dirnames, filenames) in os.walk(template_dir):
        files.extend(filenames)
        break
    for template_file in files:
        with open(template_dir + template_file, 'r') as f:
            template = json.load(f)
            generator.generate(template)
    

    
if __name__ == "__main__":
    main(sys.argv[1:])