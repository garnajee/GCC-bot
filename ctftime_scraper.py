#!/usr/bin/env python3
from dateutil.parser import parse
import json
from urllib import request
from urllib.request import Request, urlopen
import re

class CtfTimeScraper:
    def __init__(self):
        self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"}
        self.url = "https://ctftime.org/api/v1/events/?limit=15"

    def ctftime_contest(self):
        answ = Request(self.url, headers=self.headers)
        resp = urlopen(answ).read()

        # Decode response json into utf8 then load
        # into a dictionary using json module
        resp_body = resp.decode('utf8')
        events = json.loads(resp_body)

        # Initialize string to return
        #contests_string = "Latest 15 Capture The Flags\n"
        for event in events:
            # Iterate over the dictionary to extract
            # info for all on-line competitions
            if event['onsite'] == True:
                continue

            contests_string += "Name: {}\n".format(event['title'])

            time_meta = event['start']
            time_comp = parse(time_meta).strftime("%d/%m/%Y - %H:%M:%S")
            contests_string += "From: {}\n".format(time_comp)

            time_meta = event['finish']
            time_comp = parse(time_meta).strftime("%d/%m/%Y - %H:%M:%S")
            contests_string += "To: {}\n".format(time_comp)

            contests_string += "Format: {}\n".format(event['format'])
            contests_string += "Duration: {} Days {} Hours\n\n".format(event['duration']['days'], event['duration']['hours'])
            
            contests_string += "url: {}\n\n".format(event['ctftime_url'])
        return contests_string
    
    def parse(self,allctf):
        """
        Function to parse the last 15 ctf events in a list to display it in a dynamic message
        """
        blocs = re.findall(r'Name: (.*)\nFrom: (.*)\nTo: (.*)\nFormat: (.*)\nDuration: (.*)\nurl: (.*)\n', allctf)

        ctf_pages = []
        for bloc in blocs:
          Name, From, To, Format, Duration, url = bloc
          sous_str = f'title="{Name}",description="From: {From}\nTo: {To}\nFormat: {Format}\nDuration: {Duration}\nurl: {url}",colour=discord.Colour.grey()'
          ctf_pages.append(sous_str)
        return ctf_pages

if __name__ == "__main__":
    # instanciate the class
    scraper = CtfTimeScraper()
    # call the function, and print the results
    # print(scraper.ctftime_contest())
    allctf_string=scraper.ctftime_contest()
    print(scraper.parse(allctf_string))
    
