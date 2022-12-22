#------------------------------------------------------------------------
#   RSS Feed Reader Bot for Istituto Maffucci's Official Telegram channel. 
#   Created by Mirko Tenore in 2020.
#------------------------------------------------------------------------  

import os
import telepot
from datetime import datetime
import feedparser
import pyshorteners
import socket
import yaml
secrets = yaml.safe_load(open("secrets.yml"))

# link shortner init
bitly_token = secrets["bitly_token"]
s = pyshorteners.Shortener(api_key=bitly_token)

# setting up
token = secrets["bot_token"]
bot = telepot.Bot(token)
FEED_URL = 'https://istitutosuperioremaffucci.edu.it/feed/'
channel_id = "-1001153133800" #testing 1559810700  -- real 1153133800

# write urls on the database
def writeOnDatabase():
    f = open('feed_datab.txt', 'a')
    f.write("- {}\n".format(url))
    f.close()

# check if it's a new article
def isNewUrl(urlstr, urls):
    if urlstr in urls:
        return False
    else:
        return True

def main():
    # feed parsing
    rss_feed = feedparser.parse(FEED_URL)

    # store in-database urls
    f = open('feed_datab.txt', 'r')
    urls = f.read()
    f.close()

    for articles in rss_feed["entries"][::-1]:

        # metas
        title = articles['title']
        url = articles['links'][0]['href']

        # if there is a new url in the feed, send news to the Telegram channel
        if isNewUrl(url, urls):
            writeOnDatabase()
            bitly_link = s.bitly.short(url)
            short = bitly_link.replace('https://', '')
            bot.sendMessage(
                chat_id=channel_id,
                text=
                '*📋 {}*\n📚 Istituto Maffucci di Calitri (AV)\n[⠀](https://i.ibb.co/5YwRTdk/person-984236-1280-1.jpg)\n🔗 *Link*: {}'
                .format(title, short),
                parse_mode='Markdown',
                disable_web_page_preview=False,
                disable_notification=False)
            print("New message sent on 'Istituto Maffucci - Calitri'")
        else:
            pass

main()