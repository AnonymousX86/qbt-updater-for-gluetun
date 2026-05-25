# -*- coding: utf-8 -*-
from os import getenv


class GluetunSettings:
    def __init__(self) -> None:
        self.url = getenv('GLUETUN_URL', 'http://127.0.0.1:8000')
        self.api_key = getenv('GLUETUN_API_KEY', '')


class QbittorrentSettings:
    def __init__(self) -> None:
        self.url = getenv('QBITTORRENT_URL', 'http://127.0.0.1:8080')
        self.api_key = getenv('QBITTORRENT_API_KEY', '')


class Settings:
    def __init__(self) -> None:
        self.gluetun = GluetunSettings()
        self.qbittorrent = QbittorrentSettings()
        self.timeout = float(getenv('TIMEOUT', '3600'))
        self.debug = bool(getenv('QBT_UPDATER_DEBUG', 'false').lower())

    @property
    def default_headers(self) -> dict[str, str]:
        return {
            'Referer': self.qbittorrent.url,
            'Content-Type': 'application/x-www-form-urlencoded'
        }


settings = Settings()
