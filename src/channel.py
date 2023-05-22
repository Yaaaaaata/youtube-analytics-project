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

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        response = self.youtube.channels().list(
            part='snippet,statistics',
            id=self.channel_id
        ).execute()

        channel = response['items'][0]

        print('Название канала:', channel['snippet']['title'])
        print('Описание:', channel['snippet']['description'])
        print('Количество подписчиков:', channel['statistics']['subscriberCount'])
        print('Количество просмотров:', channel['statistics']['viewCount'])

