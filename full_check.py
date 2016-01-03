# -*- coding: utf-8 -*-
import os
import urllib
import time
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

channels = youtube.channels()
playlistItems = youtube.playlistItems()
commentThreads = youtube.commentThreads()

requestChannel = channels.list(part="contentDetails", id=CHANNEL_ID)
responseChannel = requestChannel.execute()
playlist_id = responseChannel["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]

requestPlaylistItems = playlistItems.list(part="contentDetails", playlistId=playlist_id)

while requestPlaylistItems != None:
    responsePlaylistItems = requestPlaylistItems.execute()

    for itemPlaylist in responsePlaylistItems.get("items", []):
        requestCommentThreads = commentThreads.list(part="snippet,replies", videoId=itemPlaylist["contentDetails"]["videoId"])

        while requestCommentThreads != None:
            responseCommentThreads = requestCommentThreads.execute()
            for item in responseCommentThreads.get("items", []):
                checkComment(item["snippet"]["topLevelComment"])
                if item["snippet"]["topLevelComment"].get("replies", None) != None:
                    for subitem in item["snippet"]["topLevelComment"]["replies"]["comments"]:
                        checkComment(subitem)
            requestCommentThreads = commentThreads.list_next(requestCommentThreads, responseCommentThreads)

    requestPlaylistItems = playlistItems.list_next(requestPlaylistItems, responsePlaylistItems)
