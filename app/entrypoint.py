# -*- coding: utf-8 -*-
from requests import get, Session, session as requests_session

from os import getenv
from time import sleep


GLUETUN_URL = str(getenv('GLUETUN_URL'))
QBITTORRENT_URL = str(getenv('QBITTORRENT_URL'))
QBITTORRENT_USER = str(getenv('QBITTORRENT_USER', 'admin'))
QBITTORRENT_PASSWORD = str(getenv('QBITTORRENT_PASSWORD'))
TIMEOUT = float(getenv('TIMEOUT', 3600))

# TODO - Check if variables are set

DEFAULT_QBT_HEADERS = {
    'Referer': QBITTORRENT_URL,
    'Content-Type': 'application/x-www-form-urlencoded'
}


def sep(text: str, *, n: int = 4, char: str = '*') -> None:
    print('\n{0} {1} {0}'.format(n * char, text))


def is_gluetun_ready() -> bool:
    res = get(f'{GLUETUN_URL}/v1/openvpn/status')
    if (code := res.status_code) == 200:
        if res.json().get('status') == 'running':
            return True
    if not res.ok:
        raise RuntimeError(f'Error {code}: {res.text}')
    sleep(5.0)


def get_assigned_port() -> int:
    res = get(f'{GLUETUN_URL}/v1/openvpn/portforwarded')
    if (code := res.status_code) != 200:
        raise RuntimeError(f'Error {code}: {res.text}')
    return int(res.json().get('port'))


def login_to_qbittorrent(session: Session) -> None:
    res = session.post(
        url=f'{QBITTORRENT_URL}/api/v2/auth/login',
        data=f'username={QBITTORRENT_USER}&password={QBITTORRENT_PASSWORD}',
        headers=DEFAULT_QBT_HEADERS
    )
    if (code := res.status_code) != 200:
        raise RuntimeError(f'Error {code}: {res.text}')


def update_qbittorrent_port(session: Session, port: int) -> None:
    res = session.post(
        url=f'{QBITTORRENT_URL}/api/v2/app/setPreferences',
        headers=DEFAULT_QBT_HEADERS,
        data='json={"listen_port":' + str(port) + '}'
    )
    if (code := res.status_code) != 200:
        raise RuntimeError(f'Error {code}: {res.text}')


def get_qbittorrent_port(session: Session) -> int:
    res = session.get(f'{QBITTORRENT_URL}/api/v2/app/preferences')
    if (code := res.status_code) != 200:
        raise RuntimeError(f'Error {code}: {res.text}')
    return int(res.json().get('listen_port'))


def verify_qbittorrent_port(session: Session, port: int) -> None:
    if (actual_port := get_qbittorrent_port(session)) != port:
        raise RuntimeError(f'Port mismatch! Got: {actual_port}')


def main():
    sep('gluetun')

    # Wait for gluetun
    try:
        while not is_gluetun_ready():
            print('Waiting for gluetun...')
    except RuntimeError:
        return
    print('Gluetun is running')

    # Get assigned port
    try:
        port = get_assigned_port()
    except RuntimeError:
        return
    print(f'Assigned port: {port}')

    # Use session to save cookies
    qbt_session = requests_session()

    sep('qBittorrent')

    # Login to qBittorent
    print('Trying to login to qBittorrent...')
    try:
        login_to_qbittorrent(qbt_session)
    except RuntimeError:
        return
    print('Logged in')

    # Update listening port
    print('Trying to update listening port...')
    update_qbittorrent_port(qbt_session, port)
    print('Port updated')

    # Verify if port has been changed (for my sanity)
    print('Verifying port...')
    try:
        verify_qbittorrent_port(qbt_session, port)
    except RuntimeError:
        return
    print('Port verified')

    sep('Done')
    print(f'Next run in {int(TIMEOUT)} seconds...')
    sleep(TIMEOUT)


if __name__ == '__main__':
    while True:
        try:
            main()
        except Exception as e:
            print(f'{e.__class__.__name__}: {e}')
            break
