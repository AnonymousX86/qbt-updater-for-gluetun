# -*- coding: utf-8 -*-
from requests import get, Session

from time import sleep

from settings import settings


def is_gluetun_ready(s: Session) -> bool:
    res = get(f'{settings.gluetun.url}/v1/openvpn/status')
    if (code := res.status_code) == 200:
        if res.json().get('status') == 'running':
            return True
    if not res.ok:
        raise RuntimeError(f'Error {code}: {res.text}')
    sleep(5.0)


def get_assigned_port(s: Session) -> int:
    res = get(f'{settings.gluetun.url}/v1/openvpn/portforwarded')
    if (code := res.status_code) != 200:
        raise RuntimeError(f'Error {code}: {res.text}')
    return int(res.json().get('port'))
