# -*- coding: utf-8 -*-
from requests import Session

from time import sleep

from settings import settings


BASE_URL = settings.gluetun.url


def is_gluetun_ready(s: Session) -> bool:
    res = s.get(f'{BASE_URL}/v1/vpn/status')
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
    res = s.get(f'{BASE_URL}/v1/portforward')
    if (code := res.status_code) != 200:
        raise RuntimeError(f'Error {code}: {res.text}')
    return int(res.json().get('port'))
