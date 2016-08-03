from __future__ import print_function
import argparse
import os, sys
from zendeskhc import HelpCenter
import codecs
import unicodedata

env = os.environ

parser = argparse.ArgumentParser()

parser.add_argument('date', type=str,
                    help='start date in the format YYYY-MM-DD')

parser.add_argument('categories', metavar='categories', type=int, nargs='+',
                    help='list of categories to check')

args = parser.parse_args()

start_time = args.date.split('-')

try:
    zendesk_url = env['ZENDESK_URL']
except:
    print("the 'ZENDESK_URL' environment variable must be set")
    sys.exit(1)
try:
    zendesk_email = env['EMAIL']
except:
    zendesk_email = None
try:
    zendesk_pass = env['ZENDESK_PASS']
except:
    zendesk_pass = None

hc = HelpCenter.HelpCenter(zendesk_url, zendesk_email, zendesk_pass)

articles = None

for i in args.categories:
    temp = hc.list_articles_by_category(i)
    if not articles:
        articles = temp
    else:
        articles['articles'] = articles['articles'] + temp['articles']

for article in articles['articles']:
    creation_time = article['created_at']
    creation_time = creation_time.split('T')[0].split('-')
    if int(creation_time[0]) - int(start_time[0]) >= 0:
        if int(creation_time[1]) - int(start_time[1]) >= 0:
            if int(creation_time[2]) - int(start_time[2]) >= 0:
                title = unicodedata.normalize('NFKC', article['title']).encode('ascii',
                        'ignore')
                print('"' + title + '" created at ' + article['created_at'])
