# -*- coding: utf-8 -*-
from os import getenv


class GluetunSettings:
    def __init__(self) -> None:
        self.url = getenv('GLUETUN_URL', 'http://127.0.0.1:8000')


class QbittorrentSettings:
    def __init__(self) -> None:
        self.url = getenv('QBITTORRENT_URL', 'http://127.0.0.1:8080')
        self.user = getenv('QBITTORRENT_USER', 'admin')
        self.password = getenv('QBITTORRENT_PASSWORD', 'adminadmin')


class Settings:
    def __init__(self) -> None:
        self.gluetun = GluetunSettings()
        self.qbittorrent = QbittorrentSettings()
        self.timeout = float(getenv('TIMEOUT', '3600'))

    @property
    def default_headers(self) -> dict:
        return {
            'Referer': self.qbittorrent.url,
            'Content-Type': 'application/x-www-form-urlencoded'
        }


settings = Settings()
