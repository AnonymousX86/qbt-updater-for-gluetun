# -*- coding: utf-8 -*-
from requests import Session

from time import sleep

from gluetun import wait_for_gluetun, get_assigned_port
from qbittorrent import wait_for_qbittorrent, get_qbittorrent_port, update_qbittorrent_port
from settings import settings
from utils import sep


def precheck() -> bool:
    try:
        with Session() as s:
            sep('gluetun')
            print('Waiting for gluetun...')
            wait_for_gluetun(s)
            print('Gluetun is running')

            sep('qBittorrent')
            print('Waiting for qBittorrent...')
            wait_for_qbittorrent(s)
            print('qBittorrent is ready')
    except Exception as e:
        raise e
    else:
        s.close()
        return True


def update_port() -> bool:
    with Session() as s:
        current_port = get_qbittorrent_port(s)
        port = get_assigned_port(s)

        if current_port == port:
            print(f'Port {port} is already set in qBittorrent')
            return True

        print(f'Updating qBittorrent port from {current_port} to {port}...')
        if update_qbittorrent_port(s, port):
            print('Port updated successfully')
            return True
        else:
            print('Failed to update port')
            return False


def main() -> None:
    if not precheck():
        raise RuntimeError('Precheck failed')
    while True:
        if update_port():
            sep('Done')
            print(f'Next run in {settings.timeout} seconds...')
            sleep(settings.timeout)
        else:
            raise RuntimeError('Failed to update port')


if __name__ == '__main__':
    try:
        while True:
            main()
    except Exception as e:
        print(f'{e.__class__.__name__}: {e}')
    except KeyboardInterrupt:
        exit()
