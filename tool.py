from __future__ import print_function
import argparse
import os, sys
from zendeskhc import HelpCenter
import codecs
import unicodedata
from datetime import datetime

env = os.environ

parser = argparse.ArgumentParser()

parser.add_argument('start_date', type=str,
                    help='start date in the format YYYY-MM-DD')

parser.add_argument('--end_date', '-e', dest='end_date', type=str,
                    help='end date in the format YYYY-MM-DD')

parser.add_argument('categories', metavar='categories', type=int, nargs='+',
                    help='list of categories to check')

args = parser.parse_args()

start_time = datetime.strptime(args.start_date, '%Y-%m-%d')

if args.end_date:
    end_time = datetime.strptime(args.end_date, '%Y-%m-%d')
else:
    end_time = None

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

if not end_time:
    for article in articles['articles']:
        creation_time = article['created_at']
        creation_time = creation_time.split('T')[0]
        creation_time = datetime.strptime(creation_time, '%Y-%m-%d')
        if creation_time > start_time:
            title = unicodedata.normalize('NFKC', article['title']).encode('ascii',
                    'ignore')
            print('"' + title + '" created at ' + article['created_at'] + ' ' +
                    article['html_url'])

else:
    for article in articles['articles']:
        creation_time = article['created_at']
        creation_time = creation_time.split('T')[0]
        creation_time = datetime.strptime(creation_time, '%Y-%m-%d')
        if creation_time > start_time and creation_time < end_time:
            title = unicodedata.normalize('NFKC', article['title']).encode('ascii',
                    'ignore')
            print('"' + title + '" created at ' + article['created_at'] + ' ' +
                    article['html_url'])
