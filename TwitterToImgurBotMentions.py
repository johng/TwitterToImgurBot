# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from imgurpython import ImgurClient
import praw
from praw.models import Comment
import urllib
import re
import requests
import os
import time

### API ###

client_id = #**
client_secret = #**
imgur = ImgurClient(client_id, client_secret)
authorization_url = imgur.get_auth_url('pin')


reddit = praw.Reddit('TwitterToImgurBot')
subreddit = reddit.subreddit("formula1")

### CHECK INBOX FOR MENTIONS ###

for comment in reddit.inbox.unread():
	if comment in reddit.inbox.mentions():
		comment.mark_unread()
		if comment.submission.domain == "twitter.com":
			comment.upvote()
			url = comment.submission.url
			username = comment.author
			page = requests.get(url)
			soup = BeautifulSoup(page.text, "html.parser")
			soup_string = str(soup)
			tweet = soup.find('p', {'class': 'tweet-text'}).text
			soup_filter = str(soup.find('div', {'class': 'AdaptiveMedia-photoContainer'}))
			image_url = re.search('data-image-url="(.*)"', soup_filter)
			if image_url == None:
				continue
			tweet = tweet.split('pic', 1)[0]
			tweet = tweet.replace('#','/#')
			image_url = image_url.group(1)
			
			# UPLOAD IMAGE TO IMGUR, RETRIEVE URL ###
			time.sleep(10)
			ImgurImage = imgur.upload_from_url(image_url, config=None, anon=True)
			final_url = ImgurImage['link']
			
			# POST TO REDDIT ###
			if not os.path.isfile("tti_posts_replied_to.txt"):
				posts_replied_to = []
			else:
				with open("tti_posts_replied_to.txt", "r") as f:
					posts_replied_to = f.read()
					posts_replied_to = posts_replied_to.split("\n")
					posts_replied_to = list(filter(None, posts_replied_to))
			if comment.submission.id not in posts_replied_to:
				comment.submission.reply('I was summoned by /u/%s. Thank you for notifying me!\n\n %s\n\n[Image Contained in Tweet](%s)\n***\n ^(You can leave feedback by replying to me)' % (username, tweet, final_url))
				posts_replied_to.append(submission.id)
				
				with open("tti_posts_replied_to.txt", "w") as f:
					for post_id in posts_replied_to:
						f.write(post_id + "\n")