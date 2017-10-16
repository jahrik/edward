#!/usr/bin/env python
"""
Facebook bot
"""
import os
import sys
import logging
# import json
# import time
# import urllib
from facepy import GraphAPI
from pymongo import MongoClient

def get_facebook_envars():
    """
    * get facebook api token from envars
    * obtain an api token at:
    * https://developers.facebook.com/apps
    * return facebook_token
    """

    if os.environ.get('FACEBOOK_API_TOKEN') is None:
        logging.error("export FACEBOOK_API_TOKEN=''")
        sys.exit(1)
    else:
        facebook_api_token = os.environ['FACEBOOK_API_TOKEN']

    return facebook_api_token


# Initialize the Graph API with a valid access token (optional,
# but will allow you to do all sorts of fun stuff).

FB_TOKEN = get_facebook_envars()
graph = GraphAPI(FB_TOKEN)

# Get my latest posts
# Supported types are post, user, page, event, group, place, checkin
POSTS = graph.get('me/posts')
# print(POSTS)
# CAT = graph.search(term='cat',type='post')
# print(CAT)

friend_likes = graph.get('me?fields=friends.fields(likes)')
print(friend_likes['friends'])
for data, summary in friend_likes:
    print(data)
    print(summary)


# Post a photo of a parrot
#GRAPH.post(
#    path='me/photos',
#    source=open('edward.png', 'rb')
#)


# graph_data = graph.get('me/posts?fields=likes',since=sTime, until=uTime)
# 
# 
# for info in graph_data['data']:
#     while True:
#        try:
#            for comment in info['likes']['data']:
# 
#                print(comment)
#            info =requests.get(info['likes']['paging']['next']).json()
#        except KeyError:
#            break

def counts():
    posts= "no likes"
    client = MongoClient()
    db = client.fb
    collection = db.check
    query = db.posts.find()
    for q in query:
            liker_id = "null"
            liker_name = "null"
            likes = "no likes in the post"
            id = q['post_id']
            response=graph.get(id+'?fields=likes.summary(true),comments.summary(true),shares')
            if 'likes' in response:
                for d in response['likes']['data']:
                     liker_id = d['id']
                     liker_name = d['name']
                     for i in liker_id:
                          posts = {"id":[liker_id]}
                post = {"post_id":id,"likes":posts}
                print(post)
# print(counts())

# {'post_id': u'256015257837672_1017155801723610', 'likes': {'id': [u'905803702763261']}}
# {'post_id': u'256015257837672_1016685905103933', 'likes': {'id': [u'808269765904912']}}
