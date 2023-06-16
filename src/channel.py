import json
import os

# необходимо установить через: pip install google-api-python-client
from googleapiclient.discovery import build


class Channel:
    """Класс для ютуб-канала"""
    api_key: str = os.getenv('YT_API_KEY')
    youtube = build('youtube', 'v3', developerKey=api_key)
    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализирует id канала. Дальше все данные будут подтягиваться по API."""
        self.channel = self.youtube.channels().list(id=channel_id, part='snippet,statistics').execute()
        for item in self.channel['items'][0]:
            self.__channel_id = channel_id
            self.title = item['snippet']['title']
            self.description = item['snippet']['description']
            self.url = item['snippet']['thumbnails']['default']['url']
            self.subscriberCount = item['statistics']['subscriberCount']
            self.viewCount = item['statistics']['viewCount']
            self.videoCount = item['statistics']['videoCount']

    def __str__(self):
        return f"{self.title} ({self.url})"

    def __add__(self, other):
        return int(self.subscriberCount) + int(other.subscriberCount)

    def __sub__(self, other):
        return int(self.subscriberCount) - int(other.subscriberCount)

    def __mul__(self, other):
        return int(self.subscriberCount) * int(other.subscriberCount)

    def __truediv__(self, other):
        return int(self.subscriberCount) / int(other.subscriberCount)

    def __lt__(self, other):
        return int(self.subscriberCount) < int(other.subscriberCount)

    def __le__(self, other):
        return int(self.subscriberCount) <= int(other.subscriberCount)

    def __gt__(self, other):
        return int(self.subscriberCount) > int(other.subscriberCount)

    def __ge__(self, other):
        return int(self.subscriberCount) >= int(other.subscriberCount)

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        print(json.dumps(self.channel, indent=4, ensure_ascii=False))

    @classmethod
    def get_service(self):
        return self.youtube

    def to_json(self, file_name) -> None:
        dict_json = {"channel_id": self.channel_id, "title": self.title, 'description': self.description,
                     "url": self.url,
                     'subscriberCount': self.subscriberCount, 'viewCount': self.viewCount,
                     'videoCount': self.videoCount}
        with open(file_name, "w", encoding='utf-8') as outfile:
            json.dump(dict_json, outfile, ensure_ascii=False, indent=4)
