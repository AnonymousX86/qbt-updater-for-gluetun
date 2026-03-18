# -*- coding: utf-8 -*-
from time import sleep

from requests import Session

from settings import settings
from utils import debug


BASE_URL = settings.gluetun.url


def is_gluetun_ready(s: Session) -> bool:
    if (gluetun_api_key := settings.gluetun.api_key) == '':
        raise RuntimeError('Gluetun API key is not set')
    res = s.get(
        f'{BASE_URL}/v1/vpn/status',
        headers={ 'X-API-Key': gluetun_api_key }
    )
    if (code := res.status_code) == 200:
        if res.json().get('status') == 'running':
            return True
    if not res.ok:
        raise RuntimeError(f'Error {code}: {res.text}')
    return False


def wait_for_gluetun(s: Session) -> None:
    retries = 0
    max_retries = 5
    while not is_gluetun_ready(s) and retries < max_retries:
        sleep(2.0)
        retries += 1


def get_assigned_port(s: Session) -> int:
    assigned_port = 0
    while assigned_port == 0:
        res = s.get(
            f'{BASE_URL}/v1/portforward',
            headers={ 'X-API-Key': settings.gluetun.api_key }
        )
        if (code := res.status_code) != 200:
            raise RuntimeError(f'Error {code}: {res.text}')
        assigned_port = int(res.json().get('port'))
    return assigned_port
