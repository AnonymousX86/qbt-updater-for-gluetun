# -*- coding: utf-8 -*-
from time import sleep

from requests import Session

from settings import settings
from utils import debug


BASE_URL = settings.gluetun.url


def is_gluetun_ready(s: Session) -> bool:
    if (gluetun_api_key := settings.gluetun.api_key) == '':
        raise RuntimeError('Gluetun API key is not set')
    debug(f'Using API key: {gluetun_api_key[:5]}***')
    res = s.get(
        f'{BASE_URL}/v1/vpn/status',
        headers={ 'X-API-Key': gluetun_api_key }
    )
    debug(f'Gluetun: {res.status_code} {res.text}')
    if (code := res.status_code) == 200:
        gluetun_status = res.json().get('status', 'unknown')
        debug(f'Gluetun is "{gluetun_status}"')
        if gluetun_status == 'running':
            return True
    if not res.ok:
        raise RuntimeError(f'Error {code}: {res.text}')
    return False


def wait_for_gluetun(s: Session) -> None:
    retries = 0
    while not is_gluetun_ready(s):
        retries += 1
        debug(f'Waiting for gluetun... (attempt #{retries})')
        sleep(2.0)


def get_assigned_port(s: Session) -> int:
    retries = 0
    assigned_port = 0
    while True:
        res = s.get(
            f'{BASE_URL}/v1/portforward',
            headers={ 'X-API-Key': settings.gluetun.api_key }
        )
        if (code := res.status_code) != 200:
            raise RuntimeError(f'Error {code}: {res.text}')
        assigned_port = int(res.json().get('port', '0'))
        if assigned_port > 0:
            debug(f'Assigned port: {assigned_port}')
            break
        retries += 1
        debug(f'Waiting for assigned port... (attempt #{retries})')
        sleep(2.0)
    return assigned_port
