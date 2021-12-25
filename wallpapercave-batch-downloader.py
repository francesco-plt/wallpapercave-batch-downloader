#!/usr/local/bin/python3
import urllib3
import requests
import os
import pathlib
import sys
from bs4 import BeautifulSoup
from time import sleep
from argparse import ArgumentParser
from progress.bar import Bar

# parsing the url from the command line
parser = ArgumentParser(description='small script to download wallpaper from wallpapercave.com')
parser.add_argument('--url', help='link to the wallpaper collection', required=True)
args = vars(parser.parse_args())
url = args['url']
print("wallpapercave collection url: '" + url + "'")

# getting current directory
pwd = pathlib.Path(__file__).parent.resolve()

# query the website and return the html to the variable ‘page’
print("requesting '" + url + "'...")
http = urllib3.PoolManager()
response = http.request('GET', url)

# parse the html using beautiful soup and store in variable `soup`
soup = BeautifulSoup(response.data, "html.parser")

links = []
for i in soup.find_all("a", {"class":"download"}):
    links.append("https://wallpapercave.com" + i['href'])
print("found ", len(links), " links")

# creating download folder
foldername = os.path.join(str(pwd), url.rsplit('/',1)[1])

try:
    pathlib.Path(foldername).mkdir(parents=True, exist_ok=True)
except OSError:
    print("Creation of the directory '" + pdw + "' failed")
else:
    print("Successfully created/reused the directory '" + foldername + "'")

# downloading files
with Bar("downloading...", max=len(links)) as bar:
    for link in links:
        tmp = requests.get(link)
        filepath = os.path.join(str(pwd), foldername, link.rsplit('/',1)[1].replace("?", "") + ".png")
        open(filepath, 'wb').write(tmp.content)
        bar.next()
