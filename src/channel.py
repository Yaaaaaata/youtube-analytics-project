import json
import os
from pprint import pprint

from googleapiclient.discovery import build


api_key: str = os.getenv('API_KEY')


class Channel:

    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, channel_id: str) -> None:
        self.channel_id = channel_id
        self.title = ''
        self.description = ''
        self.url = ''
        self.subscriber_count = 0
        self.video_count = 0
        self.view_count = 0
        self.channel = self.get_channel_info(channel_id)
        self._get_channel_info()

    def _get_channel_info(self) -> None:
        self.title = self.channel['snippet']['title']
        self.description = self.channel['snippet']['description']
        self.url = f"https://www.youtube.com/channel/{self.channel_id}"
        self.subscriber_count = int(self.channel['statistics']['subscriberCount'])
        self.video_count = int(self.channel['statistics']['videoCount'])
        self.view_count = int(self.channel['statistics']['viewCount'])

    @classmethod
    def get_service(cls):
        return cls.youtube

    def to_json(self, filename: str) -> None:
        data = {
            'channel_id': self.channel_id,
            'title': self.title,
            'description': self.description,
            'url': self.url,
            'subscriber_count': self.subscriber_count,
            'video_count': self.video_count,
            'view_count': self.view_count
        }

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def __str__(self) -> str:
        return f"{self.title} ({self.url})"

    def __add__(self, other) -> int:
        return self.subscriber_count + other.subscriber_count

    def __sub__(self, other) -> int:
        return self.subscriber_count - other.subscriber_count

    def __eq__(self, other) -> bool:
        return self.subscriber_count == other.subscriber_count

    def __ne__(self, other) -> bool:
        return self.subscriber_count != other.subscriber_count

    def __lt__(self, other) -> bool:
        return self.subscriber_count < other.subscriber_count

    def __le__(self, other) -> bool:
        return self.subscriber_count <= other.subscriber_count

    def __gt__(self, other) -> bool:
        return self.subscriber_count > other.subscriber_count

    def __ge__(self, other) -> bool:
        return self.subscriber_count >= other.subscriber_count

    def get_channel_info(self, channel_id: str) -> dict:
        response = self.youtube.channels().list(
            part='snippet,statistics',
            id=channel_id
        ).execute()

        return response['items'][0]

    def print_info(self) -> None:
        """
        Show info.
        """
        pprint(self.title, sort_dicts=False)
