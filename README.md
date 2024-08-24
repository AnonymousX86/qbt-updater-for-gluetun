# qbt-updater-for-gluetun

qBittorrent port updater for gluetun.

```sh
python app/entrypoint.py
```

Available environment variables:

| Name | Example | Default value | Description |
| --- | --- | --- | --- |
| `GLUETUN_URL` | `http://127.0.0.1:8000` | | URL to gluetun's control server. |
| `QBITTORRENT_URL` | `http://127.0.0.1:8080` | | URL to qBittorrent's web UI. |
| `QBITTORRENT_USER` | `admin` | `admin` | qBittorrent login. |
| `QBITTORRENT_PASSWORD` | `adminadmin` | | qBittorrents password. |
| `TIMEOUT` | `120` | `3600` | How often port will be changed. |

