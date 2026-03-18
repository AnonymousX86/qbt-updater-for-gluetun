# -*- coding: utf-8 -*-
from time import sleep

from requests import Session

from settings import settings


BASE_URL = settings.qbittorrent.url


def login_to_qbittorrent(s: Session) -> None:
    res = s.post(
        url=f'{BASE_URL}/api/v2/auth/login',
        data='username={0.user}&password={0.password}'.format(settings.qbittorrent),
        headers=settings.default_headers
    )
    if (code := res.status_code) != 200:
        raise RuntimeError(f'Error {code}: {res.text}')
    if not res.cookies.get('SID'):
        raise RuntimeError('Can\'t login (wrong password?)')


def wait_for_qbittorrent(s: Session) -> None:
    retries = 0
    max_retries = 5
    while retries < max_retries:
        try:
            login_to_qbittorrent(s)
            break
        except RuntimeError as e:
            if str(e).startswith('Can\'t login'):
                raise e
        # TODO - Supress `HTTPConnectionPool` or `NewConnectionError` exception.
        else:
            retries += 1
            sleep(5.0)


def get_qbittorrent_port(s: Session) -> int:
    res = s.get(f'{BASE_URL}/api/v2/app/preferences')
    if (code := res.status_code) != 200:
        raise RuntimeError(f'Error {code}: {res.text}')
    return int(res.json().get('listen_port'))


def update_qbittorrent_port(s: Session, port: int) -> bool:
    res = s.post(
        url=f'{BASE_URL}/api/v2/app/setPreferences',
        headers=settings.default_headers,
        data='json={"listen_port":' + str(port) + '}'
    )
    if (code := res.status_code) != 200:
        raise RuntimeError(f'Error {code}: {res.text}')
    return get_qbittorrent_port(s) == port

