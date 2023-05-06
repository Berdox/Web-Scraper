#!/usr/bin/python

from bs4 import BeautifulSoup
import requests
import re
import argparse

parser = argparse.ArgumentParser(description='Scrape HtML for a website')
parser.add_argument('-t','--tags', metavar='N', nargs='+',
                    help='Tags for the scraper to look for; If left empty will return all of html')
parser.add_argument('-l','--link', nargs='+', 
                    help='The link for the website for the scraper to pull from')

args = parser.parse_args()
#print(args.tags)
#print(args.link)

html_text = requests.get(args.link[0]).text
soup = BeautifulSoup(html_text, 'lxml')
print(soup.text)