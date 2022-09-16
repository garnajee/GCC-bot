#!/usr/bin/env python3
from dateutil.parser import parse
import json
from discord import Embed, Colour
from urllib import request
from urllib.request import Request, urlopen
import re

class CtfTimeScraper:
    def __init__(self):
        self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"}
        self.url = "https://ctftime.org/api/v1/events/?limit=15"    # limit of the last 15 CTF

    def parsing(self):
        answ = Request(self.url, headers=self.headers)
        resp = urlopen(answ).read()

        # Decode response json into utf8 then load
        # into a dictionary using json module
        resp_body = resp.decode('utf8')
        events = json.loads(resp_body)

        nevt = len(events)
        # Initialize string to return
        for i,event in enumerate(events):
            # Iterate over the dictionary to extract
            # info for all on-line competitions
            if event['onsite'] == True:
                continue
            # creating an "Embed" object
            contests_string = Embed(title=f"**{i+1}/{nevt} - {event['title']}**",description=f"**From:** {parse(event['start']).strftime('%d/%m/%Y - %H:%M:%S')}\n**To:** {parse(event['finish']).strftime('%d/%m/%Y - %H:%M:%S')}\n**Format:** {event['format']}\n**Duration:** {event['duration']['days']} Days {event['duration']['hours']} Hours\n\n**url:** {event['ctftime_url']}",colour=Colour.light_grey())
            yield contests_string

if __name__ == "__main__":
    # instantiate the class
    scraper = CtfTimeScraper()
    # for testing purpose
    for i in scraper.parsing():
        print(i)
        print()
    
