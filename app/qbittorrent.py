# -*- coding: utf-8 -*-
from requests import Session

from settings import settings


def login_to_qbittorrent(s: Session) -> None:
    res = s.post(
        url=f'{settings.qbittorrent.url}/api/v2/auth/login',
        data='username={0.user}&password={0.password}'.format(settings.qbittorrent),
        headers=settings.default_headers
    )
    if (code := res.status_code) != 200:
        raise RuntimeError(f'Error {code}: {res.text}')
    if not res.cookies.get('SID'):
        raise RuntimeError('Can\'t login (wrong password?)')


def update_qbittorrent_port(s: Session, port: int) -> None:
    res = s.post(
        url=f'{settings.qbittorrent.url}/api/v2/app/setPreferences',
        headers=settings.default_headers,
        data='json={"listen_port":' + str(port) + '}'
    )
    if (code := res.status_code) != 200:
        raise RuntimeError(f'Error {code}: {res.text}')


def get_qbittorrent_port(session: Session) -> int:
    res = session.get(f'{settings.qbittorrent.url}/api/v2/app/preferences')
    if (code := res.status_code) != 200:
        raise RuntimeError(f'Error {code}: {res.text}')
    return int(res.json().get('listen_port'))


def verify_qbittorrent_port(session: Session, port: int) -> None:
    if (actual_port := get_qbittorrent_port(session)) != port:
        raise RuntimeError(f'Port mismatch! Got: {actual_port}')

