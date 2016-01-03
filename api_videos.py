# -*- coding: utf-8 -*-
import os
import urllib
import time
from videoids import videoIds
import sys
from config import API_KEY, YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, CHANNEL_ID, COMMENT_DATE
from apiclient.discovery import build # pip install --upgrade google-api-python-client

youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=API_KEY)

def checkComment(comment):
    if comment["snippet"].get("authorChannelId", None) != None:
        if comment["snippet"]["authorChannelId"]["value"] == CHANNEL_ID:
            if comment["snippet"]["publishedAt"].startswith(COMMENT_DATE):
                print("https://www.youtube.com/watch?v=" + comment["snippet"]["videoId"] + " - " + comment["snippet"]["publishedAt"])
                print(comment["snippet"]["textDisplay"].encode("utf-8"))
                print("--------------------------------")

commentThreads = youtube.commentThreads()

for videoId in videoIds[int(sys.argv[1])]:
    requestCommentThreads = commentThreads.list(part="snippet", videoId=videoId)
    responseCommentThreads = requestCommentThreads.execute()
    for item in responseCommentThreads.get("items", []):
        checkComment(item["snippet"]["topLevelComment"])
