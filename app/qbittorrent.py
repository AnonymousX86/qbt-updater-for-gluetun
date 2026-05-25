# -*- coding: utf-8 -*-
from time import sleep

from requests import Session

from settings import settings
from utils import debug


BASE_URL = settings.qbittorrent.url


def is_qbittorrent_ready(s: Session) -> bool:
    if (qbittorrent_api_key := settings.qbittorrent.api_key) == '':
        raise RuntimeError('qBittorrent API key is not set.')
    debug(f'Using qBittorent API key: {qbittorrent_api_key}')
    res = s.get(
        f'{BASE_URL}/api/v2/app/version',
        headers={ 'Authorization': f'Bearer {qbittorrent_api_key}' }
    )
    if (code := res.status_code) == 200:
        return True
    if not res.ok:
        raise RuntimeError(f'Error {code}: {res.text}')
    return False


def wait_for_qbittorrent(s: Session) -> None:
    retries = 0
    while True:
        try:
            is_qbittorrent_ready(s)
            break
        except RuntimeError as e:
            print(f'Error connecting to qBittorrent: {e}')
        retries += 1
        debug(f'Retrying to connect to qBittorrent... (attempt #{retries})')
        sleep(5.0)


def get_qbittorrent_port(s: Session) -> int:
    res = s.get(
        f'{BASE_URL}/api/v2/app/preferences',
        headers={ 'Authorization': f'Bearer {settings.qbittorrent.api_key}' }
    )
    if (code := res.status_code) != 200:
        raise RuntimeError(f'Error {code}: {res.text}')
    return int(res.json().get('listen_port'))


def update_qbittorrent_port(s: Session, port: int) -> bool:
    headers = settings.default_headers.copy()
    headers.update({
        'Authorization': f'Bearer {settings.qbittorrent.api_key}'
    })
    res = s.post(
        url=f'{BASE_URL}/api/v2/app/setPreferences',
        headers=headers,
        data='json={"listen_port":' + str(port) + '}'
    )
    if (code := res.status_code) != 200:
        raise RuntimeError(f'Error {code}: {res.text}')
    return get_qbittorrent_port(s) == port

