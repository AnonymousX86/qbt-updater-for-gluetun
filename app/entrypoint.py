# -*- coding: utf-8 -*-
from requests import get, Session

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


def is_gluetun_ready(s: Session) -> bool:
    res = get(f'{GLUETUN_URL}/v1/openvpn/status')
    if (code := res.status_code) == 200:
        if res.json().get('status') == 'running':
            return True
    if not res.ok:
        raise RuntimeError(f'Error {code}: {res.text}')
    sleep(5.0)


def get_assigned_port(s: Session) -> int:
    res = get(f'{GLUETUN_URL}/v1/openvpn/portforwarded')
    if (code := res.status_code) != 200:
        raise RuntimeError(f'Error {code}: {res.text}')
    return int(res.json().get('port'))


def login_to_qbittorrent(s: Session) -> None:
    res = s.post(
        url=f'{QBITTORRENT_URL}/api/v2/auth/login',
        data=f'username={QBITTORRENT_USER}&password={QBITTORRENT_PASSWORD}',
        headers=DEFAULT_QBT_HEADERS
    )
    if (code := res.status_code) != 200:
        raise RuntimeError(f'Error {code}: {res.text}')
    if not res.cookies.get('SID'):
        raise RuntimeError('Can\'t login (wrong password?)')


def update_qbittorrent_port(s: Session, port: int) -> None:
    res = s.post(
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
    # gluetun
    try:
        with Session() as s:
            sep('gluetun')

            # Wait for gluetun
            while not is_gluetun_ready(s):
                print('Waiting for gluetun...')
            print('Gluetun is running')

            # Get assigned port
            port = get_assigned_port(s)
            print(f'Assigned port: {port}')
    except Exception as e:
        raise e
    finally:
        s.close()

    # qBittorrent
    try:
        with Session() as s:
            sep('qBittorrent')

            # Login to qBittorent
            print('Trying to login to qBittorrent...')
            login_to_qbittorrent(s)
            print('Logged in')

            # Update listening port
            print('Trying to update listening port...')
            update_qbittorrent_port(s, port)
            print('Port updated')

            # Verify if port has been changed (for my sanity)
            print('Verifying port...')
            verify_qbittorrent_port(s, port)
            print('Port verified')

            sep('Done')
            print(f'Next run in {int(TIMEOUT)} seconds...')
            sleep(TIMEOUT)
    except Exception as e:
        raise e
    finally:
        s.close()


if __name__ == '__main__':
    while True:
        try:
            main()
        except Exception as e:
            print(f'{e.__class__.__name__}: {e}')
            break
