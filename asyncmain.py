# 
# RSS Feed Updates Bot for Istituto Maffucci
# created by @sdoublesm in 2020
# async version created in 2024 
#

import asyncio
from aiogram import Bot
import feedparser
import cssutils
import urllib.request
from bs4 import BeautifulSoup
import re
import yaml
import logging
from argparse import ArgumentParser
from aiogram.enums import ParseMode

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("MaffucciBot")
cssutils.log.setLevel(logging.CRITICAL)

# setting up
FEED_URL = 'https://istitutosuperioremaffucci.edu.it/feed/'
CHAT_ID = -1001559810700 # testing: 1559810700 - official: 1153133800
with open("secrets.yml") as f:
    secrets = yaml.safe_load(f)
    token = secrets["bot_token"]

# ---------

def writeOnDatabase(url):
    with open('feed_datab.txt', 'a') as f:
        f.write(f"- {url}\n")

def getbackground(url):
    html = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(html, 'html.parser')  # Usa html.parser come parser
    div_style = soup.find('section')['style']
    style = cssutils.parseStyle(div_style)['background']
    res = re.search(r"https?://[^\s]+", style)
    if res:
        res_url = res.group().replace(")", "").replace(" ", "")
        if res_url != "https://istitutosuperioremaffucci.edu.it/wp-content/uploads/2020/03/person-984236_1280.jpg":
            return res_url
    return "https://i.ibb.co/5YwRTdk/person-984236-1280-1.jpg"

def isNewUrl(urlstr, urls):
    return urlstr not in urls

async def check_feed(bot, chat_id):
    while True:
        # Parsing del feed RSS
        rss_feed = feedparser.parse(FEED_URL)

        # Lettura degli URL dal database
        try:
            with open('feed_datab.txt', 'r') as f:
                urls = f.read()
        except FileNotFoundError:
            urls = ""

        for article in rss_feed.entries[::-1]:
            title = article.title
            url = article.links[0].href
            short = article.id
            tagstr = " ".join(f"#{tag.term.replace(' ', '')}" for tag in article.tags)

            # Se c'è un nuovo URL nel feed, invia l'articolo al canale Telegram
            if isNewUrl(url, urls):
                imageurl = getbackground(url)
                
                await bot.send_message(
                    chat_id=chat_id,
                    text=(
                        f'*🆕 {title}*\n[ ]({imageurl})\n🔗 *Link*: {short} 👈🏼\n\n'
                        f'📚 Istituto Maffucci di Calitri\n'
                        f'🏷️ {tagstr} | @IstitutoMaffucci\n\n'
                    ),
                    parse_mode=ParseMode.MARKDOWN,  # MARKDOWN / HTML
                    disable_web_page_preview=False,
                    disable_notification=False
                )
                logger.info(f" New message sent - {title}")
                writeOnDatabase(url)  # Scrive l'URL nel database per evitare duplicati
        
        await asyncio.sleep(5) 

async def main():
    bot = Bot(token)
    await check_feed(bot, CHAT_ID)

if __name__ == "__main__":
    asyncio.run(main())