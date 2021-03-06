#!/usr/bin/python3
import os, pathlib
from sys import argv
from requests import get, post, Session
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from progress.bar import Bar
from IPython import embed

# parsing the url as cli argument
if len(argv) != 2:
    exit("Usage: python3 wbd.py <COLLECTION_URL>")
url = argv[1]

# querying the website
print("requesting '" + url + "'..")
ua = UserAgent()
s = Session()
s.headers.update({"User-Agent": ua.random})
r = s.get(url)
if r.status_code != 200:
    exit(f"error {r.status_code}. exiting..")

# parsing the html and getting links
soup = BeautifulSoup(r.text, "html.parser")

links = []
for i in soup.find_all("a", {"class": "download"}):
    links.append("https://wallpapercave.com" + i["href"])
if len(links) == 0:
    exit("no links found")
print("found ", len(links), " links")

# creating download folder
# $PWD/downloads/<COLLECTION_NAME>
outdir = (
    str(pathlib.Path(__file__).parent.resolve()) + "/downloads/" + url.rsplit("/", 1)[1]
)
try:
    pathlib.Path(outdir).mkdir(parents=True, exist_ok=True)
except OSError:
    exit("Creation of output directory failed")

# downloading files
with Bar("downloading...", max=len(links)) as bar:
    for link in links:
        tmp = s.get(link)
        if tmp.status_code != 200:
            exit(f"error {tmp.status_code}. exiting..")
        # outdir/<FILENAME>
        fpath = outdir + "/" + link.rsplit("/", 1)[1].replace("?", "") + ".jpg"
        open(fpath, "wb").write(tmp.content)
        bar.next()
