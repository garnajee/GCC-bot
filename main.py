#!/usr/bin/env python3

import discord
from discord import Embed, Colour
from discord.ext import commands
from dotenv import load_dotenv
import asyncio
import os
import ctftime_scraper

# Instantiate CtfTimeScraper class from ctftime_scraper.py
scraper = ctftime_scraper.CtfTimeScraper()

#For a more secure, we loaded the .env file and assign the token value to a variable 
load_dotenv(".env")
TOKEN = os.getenv("DISCORD_TOKEN")

#Intents are permissions for the bot that are enabled based on the features necessary to run the bot.
intents=discord.Intents.all()

prefix = '$'
bot = commands.Bot(command_prefix=prefix, help_command=None, intents=intents)

@bot.event
async def on_ready():
    print('Bot is ready to use!')
    print(f'{bot.user} has logged in.')

@bot.event
async def on_message(message):
    # channel blablabla
    channel = bot.get_channel(123456789012345678)

    if message.author == bot.user:
        return

    if message.content == 'Updating CTFs...':
        """
        Send a message with multiple pages for the last 15 ctf on ctftime.org
        Based on:
        https://www.youtube.com/watch?v=izXfHCTlD6M
        https://github.com/alphascriptyt/Discord_Rewrite_Tutorials/blob/master/episodes/episode-13.py
        """
        ctf_pages = list(scraper.parsing())

        buttons = [u"\u23EA", u"\u2B05", u"\u27A1", u"\u23E9"] 

        current = 0
        msg = await channel.send(embed=ctf_pages[current])

        for button in buttons:
            await msg.add_reaction(button)

        while True:
            try:
                # check if the reaction is on the correct message
                #reaction, user = await bot.wait_for("reaction_add", check=lambda reaction, user: user == message.author and reaction.message == msg and reaction.emoji in buttons, timeout=60.0)
                reaction, user = await bot.wait_for("reaction_add", check=lambda reaction, user : reaction.message == msg and reaction.emoji in buttons, timeout=167*60*60) # timeout until the next auto send message, the next week one hour before (167h vs 168h)
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
                    await msg.remove_reaction(button, message.author)
                if current != previous_page:
                    await msg.edit(embed=ctf_pages[current])

bot.run(TOKEN)

