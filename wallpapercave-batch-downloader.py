#!/usr/local/bin/python3
import urllib3
import requests
from time import sleep
import os
from bs4 import BeautifulSoup
import pathlib
from progress.bar import Bar
import subprocess
import sys

pwd = pathlib.Path(__file__).parent.resolve()

# specify the url
url = sys.argv[1]
print("wallpapercave collection url: '" + url + "'")

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
    print("Creation of the directory '", pdw, "' failed")
else:
    print("Successfully created/reused the directory '" + foldername + "'")

# downloading files
with Bar("downloading...", max=len(links)) as bar:
    for link in links:
        tmp = requests.get(link)
        filepath = os.path.join(str(pwd), foldername, link.rsplit('/',1)[1].replace("?", "") + ".png")
        open(filepath, 'wb').write(tmp.content)
        bar.next()