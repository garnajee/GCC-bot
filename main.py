#!/usr/bin/env python3

# This script send message once a week, based on ctf events on ctftime.org.

import os
from dotenv import load_dotenv
import discord
from discord.utils import get
# import our ctftime scraper python script
import ctftime_scraper
# to send message once a week
#import datetime as dt

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

# apparetnly it's no more supported now
#@client.command
@tasks.loop(hours=168) # 168h in a week, so run once a week (easiest way to send message once a week...)
async def ctf_events(ctx):
    """
    Send a message with multiple pages for the last 15 ctf on ctftime.org
    Based on:
    https://www.youtube.com/watch?v=izXfHCTlD6M
    https://github.com/alphascriptyt/Discord_Rewrite_Tutorials/blob/master/episodes/episode-13.py
    """
    # get the list with all ctf parsed for multiple pages
    allctf_string = scraper.ctftime_contest()
    ctf_pages = scraper.parse(allctf_string)

    buttons = [u"\u23EA", u"\u2B05", u"\u27A1", u"\u23E9"] # skip to start, left, right, skip to end

    # "Upcomming Event" GCC discord channel
    channel = client.get_channel(ChAnGe_hErE_By_tHe_dIsCoRd_iD_ChAnNeL)

    current = 0
    msg = await channel.send(embed=ctf_pages[current])buttons = [u"\u23EA", u"\u2B05", u"\u27A1", u"\u23E9"] # skip to start, left, right, skip to end
    current = 0
    msg = await channel.send(embed=ctf_pages[current])

    for button in buttons:
        await msg.add_reaction(button)

    while True:
        try:
            #reaction, user = await bot.wait_for("reaction_add", check=lambda reaction, user: user == ctx.author and reaction.emoji in buttons, timeout=60.0)
            # check if the reaction is on the correct message
            reaction, user = await client.wait_for("reaction_add", check=lambda reaction, user: user == ctx.author and reaction.message == msg and reaction.emoji in buttons, timeout=60.0)
        except asyncio.TimeoutError:
            return print("Time out error")
        else:
            previous_page = current
            if reaction.emoji == u"\u23EA":
                current = 0
            elif reaction.emoji == u"\u2B05":
                if current > 0:
                    current -= 1
            elif reaction.emoji == u"\u27A1":
                if current < len(ctf_pages)-1:
                    current += 1
            elif reaction.emoji == u"\u23E9":
                current = len(ctf_pages)-1
            for button in buttons:
                await msg.remove_reaction(button, ctx.author)
            if current != previous_page:
                await msg.edit(embed=ctf_pages[current])

"""
# https://stackoverflow.com/a/63770665
@ctf_events.before_loop
async def before_ctf_events():
    for _ in range(60*60*24): # loop the whole day
        if dt.datetime.now().hour == 10+12: # 24 hour format
            print('It is time')
            return
        await asyncio.sleep(1) # wait a second before looping again. You can make it more
"""

# or more simply
# https://discordpy.readthedocs.io/en/stable/ext/tasks/index.html
@ctf_events.before_loop
async def before_ctf_events():
    print("Waiting...")
    await client.wait_until_ready()
  
# load ".env" file with the token information
load_dotenv()
token = os.environ.get('DISCORD_TOKEN')
#token = "insert_your_token_here(deprecated)"
client.run(token)   # run discord client (bot)
