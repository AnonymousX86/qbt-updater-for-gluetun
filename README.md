# qbt-updater-for-gluetun

qBittorrent port updater for gluetun.

## Running directly

```sh
python app/main.py
```

## Available environment variables

| Name |  Default value | Description |
| --- |  --- | --- |
| `GLUETUN_URL` | `http://127.0.0.1:8000` | URL to gluetun's control server. |
| `QBITTORRENT_URL` | `http://127.0.0.1:8080` | URL to qBittorrent's web UI. |
| `QBITTORRENT_USER` | `admin` | qBittorrent login. |
| `QBITTORRENT_PASSWORD` | `adminadmin` | qBittorrents password. |
| `TIMEOUT` | `3600` | How often port will be changed. |


## Running in Docker Compose

```yaml
---
services:
  qbt-updater:
    build: https://github.com/AnonymousX86/qbt-updater-for-gluetun.git#v1.1
    container_name: qbt-updater
    restart: unless-stopped
    environment:
      # Assuming apps expose ports on gateway of "custom-network"
      # Note: without Docker DNS tricks, hostnames are unsopported
      GLUETUN_URL: http://172.18.0.1:8000
      QBITTORRENT_URL: http://172.18.0.1:8080
    env_file:
      - .env # Contains QBITTORRENT_PASSWORD
    networks:
      - custom-network # Must be the same as gluetun and qBittorrent

networks:
  custom-network:
    external: true
```

