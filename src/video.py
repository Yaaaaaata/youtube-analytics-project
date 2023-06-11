import os
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


api_key: str = os.getenv('API_KEY')
youtube = build('youtube', 'v3', developerKey=api_key)


class Video:
    def __init__(self, video_id):
        self.video_id = video_id
        self.title = None
        self.url = None
        self.views = None
        self.like_count = None
        try:
            self._get_video_info()
        except (HttpError, IndexError):
            pass

    def _get_video_info(self):
        response = youtube.videos().list(
            part='snippet,statistics',
            id=self.video_id
        ).execute()

        item = response['items'][0]
        self.title = item['snippet']['title']
        self.url = f"https://www.youtube.com/watch?v={self.video_id}"
        self.views = int(item['statistics']['viewCount'])
        self.like_count = int(item['statistics']['likeCount'])

    def __str__(self):
        return self.title if self.title else f"Video {self.video_id}"


class PLVideo(Video):
    def __init__(self, video_id, playlist_id):
        super().__init__(video_id)
        self.playlist_id = playlist_id

    def __str__(self):
        return f"{self.title}"


if __name__ == '__main__':
    broken_video = Video('broken_video_id')
    assert broken_video.title is None
    assert broken_video.like_count is None
