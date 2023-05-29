import json
import os

# необходимо установить через: pip install google-api-python-client
from googleapiclient.discovery import build

import isodate


class Channel:
    """Класс для ютуб-канала"""
    api_key: str = os.getenv('YT_API_KEY')
    youtube = build('youtube', 'v3', developerKey=api_key)
    channel_id = 'UC-OVMPlMA3-YCIeg4z5z23A'
    channel = youtube.channels().list(id=channel_id, part='snippet,statistics').execute()

    def __init__(self, channel_id) -> None:
        """Экземпляр инициализирует id канала. Дальше все данные будут подтягиваться по API."""

        for item in self.channel['items']:
            self.__channel_id = channel_id
            self.title = item['snippet']['title']
            self.description = item['snippet']['description']
            self.url = item['snippet']['thumbnails']['default']['url']
            self.subscriberCount = item['statistics']['subscriberCount']
            self.viewCount = item['statistics']['viewCount']
            self.videoCount = item['statistics']['videoCount']

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        print(json.dumps(self.channel, indent=4, ensure_ascii=False))

    @classmethod
    def get_service(self):
        return self.youtube

    def to_json(self, file_name) -> None:
        dict = {"channel_id": self.channel_id, "title": self.title, 'description': self.description, "url": self.url,
                'subscriberCount': self.subscriberCount, 'viewCount': self.viewCount, 'videoCount': self.videoCount}
        with open(file_name, "w", encoding='utf-8') as outfile:
            json.dump(dict, outfile, ensure_ascii=False, indent=4)

