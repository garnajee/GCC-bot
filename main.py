#!/usr/bin/env python3

# This script send message when a new ctf event is added in ctftime.org.

import os
from dotenv import load_dotenv
import discord
from discord.utils import get
# import our ctftime scraper python script
import ctftime_scraper

client = discord.Client()   # create client (the bot)

# Instantiate CtfTimeScraper class from ctftime-scraper.py
scraper = ctftime_scraper.CtfTimeScraper()

# Create an event with the same name as the function
# "@client.event" indique que la fonction on_ready doit recevoir les infos 
# envoyées lorsque l'évènement est appelé par discord, devant chaque fonction

@client.event
async def on_ready():
    print("Bot is ready!")
    print(f'Logged in as {client.user} (ID: {client.user.id})')
    print('----------------------------------------------------------')

@client.event
async def on_event():
    """
    Send message when a new ctf is added on https://ctftime.org/event/list/upcoming
    """

    # "Upcomming Event" channel
    channel = client.get_channel(ChAnGe_hErE_By_tHe_dIsCoRd_iD_ChAnNeL)
    
    # run python script to scrape the ctf
    ctfs = scraper.ctftime_contest()
    # display
    #TODO: send message with the latest ctf we want to show
    #something like:
    #await message.send(blabla, ...)

               
# load ".env" file with the token information
load_dotenv()
token = os.environ.get('DISCORD_TOKEN')
#token = "insert_your_token_here(deprecated)"
client.run(token)   # run discord client (bot)
