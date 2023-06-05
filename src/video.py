from googleapiclient.discovery import build

api_key = 'AIzaSyB06v3kxtA7KnxyTRBnNPtXI-wC-33BCak'
youtube = build('youtube', 'v3', developerKey=api_key)


class Video:
    def __init__(self, video_id):
        self.video_id = video_id
        self.title = ''
        self.url = ''
        self.views = 0
        self.likes = 0
        self._get_video_info()

    def _get_video_info(self):
        response = youtube.videos().list(
            part='snippet,statistics',
            id=self.video_id
        ).execute()

        item = response['items'][0]
        self.title = item['snippet']['title']
        self.url = f"https://www.youtube.com/watch?v={self.video_id}"
        self.views = int(item['statistics']['viewCount'])
        self.likes = int(item['statistics']['likeCount'])

    def __str__(self):
        return self.title if self.title else f"Video {self.video_id}"


class PLVideo(Video):
    def __init__(self, video_id, playlist_id):
        super().__init__(video_id)
        self.playlist_id = playlist_id

    def __str__(self):
        return f"{self.title}"
