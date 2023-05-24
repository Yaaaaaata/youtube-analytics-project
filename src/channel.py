import json
import os

from googleapiclient.discovery import build

import isodate


api_key: str = os.getenv('API_KEY')


class Channel:
    """Класс для ютуб-канала"""

    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.channel_id = channel_id
        self.title = ''
        self.description = ''
        self.url = ''
        self.subscriber_count = ''
        self.video_count = ''
        self.view_count = ''
        self._get_channel_info()

    def _get_channel_info(self) -> None:
        """Получает информацию о канале и заполняет атрибуты экземпляра."""
        response = self.youtube.channels().list(
            part='snippet,statistics',
            id=self.channel_id
        ).execute()

        channel = response['items'][0]

        self.title = channel['snippet']['title']
        self.description = channel['snippet']['description']
        self.url = f"https://www.youtube.com/channel/{self.channel_id}"
        self.subscriber_count = channel['statistics']['subscriberCount']
        self.video_count = channel['statistics']['videoCount']
        self.view_count = channel['statistics']['viewCount']

    @classmethod
    def get_service(cls):
        """Возвращает объект для работы с YouTube API."""
        return cls.youtube

    def to_json(self, filename: str) -> None:
        """Сохраняет значения атрибутов экземпляра в файл в формате JSON."""
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
