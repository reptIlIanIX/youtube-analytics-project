import os

import isodate
from googleapiclient.discovery import build
from functools import reduce
import operator


class PlayList:
    def __init__(self, playlist_id):
        api_key: str = os.getenv('YT_API_KEY')
        self.youtube = build('youtube', 'v3', developerKey=api_key)
        self.playlist_videos = self.youtube.playlistItems().list(playlistId=playlist_id,
                                                                 part='contentDetails, snippet, status, id',
                                                                 maxResults=50,
                                                                 ).execute()
        self.youtube_url = 'https://www.youtube.com/playlist?list='
        self.playlist_id = playlist_id
        self.title: str = self.playlist_videos['items'][0]['snippet']['title'][0:24]
        self.url = self.youtube_url + self.playlist_id
        video_ids: list[str] = [video['contentDetails']['videoId'] for video in self.playlist_videos['items']]
        self.video_response = self.youtube.videos().list(part='contentDetails,statistics',
                                                         id=','.join(video_ids),
                                                         ).execute()

    @property
    def total_duration(self):
        global q
        tot_dur = []
        for video in self.video_response['items']:
            # YouTube video duration is in ISO 8601 format
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            tot_dur.append(duration)
            q = reduce(operator.add, tot_dur)
        return q

    def show_best_video(self):
        best_videos = []

        for video in self.video_response['items']:
            best_videos.append(video['statistics']['likeCount'])
        max_n = max(best_videos)
        for video in self.video_response['items']:
            if video['statistics']['likeCount'] == max_n:
                return f'https://youtu.be/{video["id"]}'
