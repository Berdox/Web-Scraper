#!/usr/bin/python

from bs4 import BeautifulSoup
import requests
import argparse

def writeFile(fileName, text):
    with open(fileName, "a") as file:
        for line in text: 
            file.writelines(line)

parser = argparse.ArgumentParser(description='Scrapes HTML from a website')

parser.add_argument('-t','--tags', nargs='+',
                    help='Tags for the scraper to look for; If left empty will return all of html')
parser.add_argument('-rt','--rmtag', nargs='+',
                    help='Will remove the html tags and be left with text')
parser.add_argument('-wt','--writetag', nargs='+',
                    help='Will write the output to a file named whatever you passed for the argument')
parser.add_argument('-l','--link', nargs='?', 
                    help='The link for the website for the scraper to pull from; will only take first link')

args = parser.parse_args()

if(args.link is None):
    print('There need to be a link to a website to scrape')
    exit()

if(args.tags is None):
    html_text = requests.get(args.link).text
    soup = BeautifulSoup(html_text, 'lxml')
    print(soup.text)
else:
    html_text = requests.get(args.link).text
    soup = BeautifulSoup(html_text, 'lxml')
    collection = soup.find_all(args.tags)
    if(args.rmtag):
        for tag in collection:
            print(tag.text, sep="\n")
        if(args.writetag is not None):
            writeFile(args.writetag, tag.text)
        if(args.writetag is None):
            print('Need to include filename to write to file')
            exit()
    else:
        for tag in collection:
            print(tag, sep="\n") 
        if(args.writetag is not None):
            writeFile(args.writetag, tag)
        if(args.writetag is None):
            print('Need to include filename to write to file')
            exit()