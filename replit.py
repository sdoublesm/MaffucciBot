#-----------------------------------------------------------------------
#   RSS Feed Reader Bot for Istituto Maffucci's Official Telegram channel. [REPLIT VERSION]
#   Created by Mirko Tenore in 2020.
#-----------------------------------------------------------------------

import os
import telepot
from datetime import datetime
import feedparser
import pyshorteners
import socket

#-----------------------------------------------------------------------

def main():
    # link shortner initialization
    bitly_token = os.environ['BITLY_TOKEN']
    s = pyshorteners.Shortener(api_key=bitly_token)

    # variables
    token = os.environ['TG_TOKEN']
    bot = telepot.Bot(token)
    FEED_URL = 'https://istitutosuperioremaffucci.edu.it/feed/'
    channel_id = "-1001153133800"  #"-1001559810700"

    # write url specs on the database
    def writeOnDatabase():
        f = open('feed_datab.txt', 'a')
        f.write("- {}\n".format(url))
        f.close()

    # check if it's a new article
    def isNewUrl(urlstr):
        if urlstr in urls:
            return False
        else:
            return True

    # feed parsing
    rss_feed = feedparser.parse(FEED_URL)

    # read in-database urls
    f = open('feed_datab.txt', 'r')
    urls = f.read()
    f.close()

    for articles in rss_feed["entries"][::-1]:
        # infos about articles
        title = articles['title']
        url = articles['links'][0]['href']
        tagstr = ""
        for tags in articles["tags"]:
            tag = tags["term"].replace(" ", "")
            tagstr = tagstr + " #" + tag

        # if there is a new url in the feed, send news to the Telegram channel
        if isNewUrl(url):
            writeOnDatabase()
            bitly_link = s.bitly.short(url)
            short = bitly_link.replace('https://', '')
            bot.sendMessage(
                chat_id=channel_id,
                text=
                '*📋 {}*\n[⠀](https://i.ibb.co/5YwRTdk/person-984236-1280-1.jpg)\n🔗 *Link*: {} 👈🏼\n\n📚 Istituto Maffucci di Calitri\n🏷️{} | @IstitutoMaffucci\n\n'
                .format(title, short, tagstr),
                parse_mode='Markdown',
                disable_web_page_preview=False,
                disable_notification=False)
            print("New message sent on 'Istituto Maffucci - Calitri'")
        else:
            pass

# x Replit (HTTP(s) request from https://uptimerobot.com/)

HOST, PORT = '0.0.0.0', 8080

listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
listen_socket.listen(1)

while True:
    client_connection, client_address = listen_socket.accept()
    request = client_connection.recv(1024)
    print("Request on {}".format(datetime.now()))
    data = "HTTP/1.0 200 OK"
    client_connection.send(data.encode())
    main()