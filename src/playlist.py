import os
import datetime
import re

from googleapiclient.errors import HttpError
from googleapiclient.discovery import build


api_key: str = os.getenv('API_KEY')
youtube = build('youtube', 'v3', developerKey=api_key)


class PlayList:
    def __init__(self, playlist_id, title=''):
        self.playlist_id = playlist_id
        self.title = title
        self.url = f'https://www.youtube.com/playlist?list={playlist_id}'
        self.videos = []
        try:
            playlist = youtube.playlists().list(
                part='snippet',
                id=playlist_id
            ).execute()
            self.title = playlist['items'][0]['snippet']['title']
            playlist_items = youtube.playlistItems().list(
                part='snippet',
                playlistId=playlist_id,
                maxResults=50
            ).execute()
            while playlist_items:
                for item in playlist_items['items']:
                    video_id = item['snippet']['resourceId']['videoId']
                    video_title = item['snippet']['title']
                    video_likes = 0
                    try:
                        video = youtube.videos().list(
                            part='statistics',
                            id=video_id
                        ).execute()
                        video_likes = int(video['items'][0]['statistics']['likeCount'])
                    except HttpError:
                        pass
                    self.videos.append({
                        'id': video_id,
                        'title': video_title,
                        'likes': video_likes
                    })
                if 'nextPageToken' in playlist_items:
                    playlist_items = youtube.playlistItems().list(
                        part='snippet',
                        playlistId=playlist_id,
                        maxResults=50,
                        pageToken=playlist_items['nextPageToken']
                    ).execute()
                else:
                    break
        except HttpError:
            pass

    @property
    def total_duration(self):
        total_seconds = sum([self._get_video_duration(video['id']) for video in self.videos])
        return datetime.timedelta(seconds=total_seconds)

    def show_best_video(self):
        best_video = max(self.videos, key=lambda video: video['likes'])
        return f'https://youtu.be/{best_video["id"]}'

    def _get_video_duration(self, video_id):
        video = youtube.videos().list(
            part='contentDetails',
            id=video_id
        ).execute()
        duration = video['items'][0]['contentDetails']['duration']
        duration_regex = re.compile(r'PT(\d+M)?(\d+S)?')
        minutes = 0
        seconds = 0
        match = duration_regex.match(duration)
        if match:
            if match.group(1):
                minutes = int(match.group(1)[:-1])
            if match.group(2):
                seconds = int(match.group(2)[:-1])
        return minutes * 60 + seconds
