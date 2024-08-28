# 
# RSS Feed Updates Bot for Istituto Maffucci
# created by @sdoublesm in 2020
#

import telepot
from datetime import datetime
import feedparser

import cssutils
import urllib.request
from bs4 import BeautifulSoup
import re

import yaml
secrets = yaml.safe_load(open("secrets.yml"))
access_tokens = [secrets["bitly_token"]]

# setting up
token = secrets["bot_token"]
bot = telepot.Bot(token)
FEED_URL = 'https://istitutosuperioremaffucci.edu.it/feed/'
channel_id = "-1001559810700" #  testing 1559810700 -- real 1153133800

# write urls on the database
def writeOnDatabase(url):
    f = open('feed_datab.txt', 'a')
    f.write("- {}\n".format(url))
    f.close()

def getbackground(url):
    html = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(html, features="lxml")
    div_style = soup.find('section')['style']
    style = cssutils.parseStyle(div_style)['background']
    res = re.search("(?P<url>https?://[^\s]+)", style).group("url").replace(")", "").replace(" ", "")
    if(res!="https://istitutosuperioremaffucci.edu.it/wp-content/uploads/2020/03/person-984236_1280.jpg"):
        url = res
    else:
        url = "https://i.ibb.co/5YwRTdk/person-984236-1280-1.jpg"
    
    return url

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
        short = articles['id']
        tagstr = ""
        for tags in articles["tags"]:
            tag = tags["term"].replace(" ", "")
            tagstr = tagstr + " #" + tag

        
        # if there is a new url in the feed, send news to the Telegram channel
        if isNewUrl(url, urls):
            imageurl=getbackground(url)
            print("[", getbackground(url), "]")
            #writeOnDatabase(url)
            #cover_link = "https://i.ibb.co/5YwRTdk/person-984236-1280-1.jpg"
            short = short.replace('https://', '')
            bot.sendMessage(
                chat_id=channel_id,
                text=
                '*📋 {}*\n[ ]({})\n🔗 *Link*: {} 👈🏼\n\n📚 Istituto Maffucci di Calitri\n🏷️{} | @IstitutoMaffucci\n\n'
                .format(title, imageurl, short, tagstr),
                parse_mode='Markdown',
                disable_web_page_preview=False,
                disable_notification=False)
            print("New message sent on 'Istituto Maffucci - Calitri'")
        else:
            pass

if __name__ == '__main__':
    main()
