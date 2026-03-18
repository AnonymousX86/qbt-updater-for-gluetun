# qbt-updater-for-gluetun

qBittorrent port updater for Gluetun.

Gluetun by default offers only integrations with VPN providers. Manual scripting is usually very limited, mostly by the Bash high ceiling (that's me). This micro-service automates the process of changing the qBittorrent's torreting port to the fowarded one from the VPN provider.

This project is a result of many hours of a trails and errors, so a [Ko-Fi](https://ko-fi.com/anonymousx86) will be very appreciated!

## Running directly

```sh
python -m pip install -r requirements.txt
python app/main.py
```

## Available environment variables

| Name |  Default value | Description |
| --- |  --- | --- |
| `GLUETUN_URL` | `http://127.0.0.1:8000` | URL to Gluetun control server. |
| `GLUETUN_API_KEY` | `''` | API key for communicating with Gluetun control server. |
| `QBITTORRENT_URL` | `http://127.0.0.1:8080` | URL to qBittorrent web UI. |
| `QBITTORRENT_USER` | `admin` | qBittorrent login. |
| `QBITTORRENT_PASSWORD` | `adminadmin` | qBittorrent password. |
| `TIMEOUT` | `3600` | How often port will be changed. |
| `QBT_UPDATER_DEBUG` | `false` | Whether output more information. |


## Running in Docker Compose

```yaml
---
services:
  qbt-updater:
    build: https://github.com/AnonymousX86/qbt-updater-for-gluetun.git#v1.3
    container_name: qbt-updater
    restart: unless-stopped
    environment:
      # Assuming apps expose ports on gateway of "custom-network"
      GLUETUN_URL: http://gluetun:8000
      QBITTORRENT_URL: http://qbittorrent:8080
    env_file:
      - .env # Contains secrets
    networks:
      - custom-network # Must be the same as Gluetun and qBittorrent

networks:
  custom-network:
    external: true
```

Alternatively *(recommended)* you can use `network_mode` ([reference](https://docs.docker.com/reference/compose-file/services/#network_mode)):

```yaml
---
serices:
  gluetun:
    # ...

  qbittorrent:
    network_mode: service:gluetun

  qbt-updater:
    network_mode: service:gluetun
    environment:
      GLUETUN_URL: http://localhost:8000
      QBITTORRENT_URL: http://localhost:8080
```

In this scenario use a [loopback address](https://en.wikipedia.org/wiki/Localhost) to communicate with both Gluetun and qBittorrent, as they share the `localhost`. However, keep in mind to use different ports for each service (by default they don't conflict, just in case you'd like to change them).

Don't forget the `.env` file.

```env
QBITTORRENT_PASSWORD="super-secret-password"
GLUETUN_API_KEY="super-secret-api-key"
```

### Gluetun configuration

Since Gluetun now requires authentication configuartion, the **qbt-updater** now uses `X-API-Key` HTTP header during the communication and it's not optional.

*More on that topic [here](https://github.com/qdm12/gluetun-wiki/blob/main/setup/advanced/control-server.md#authentication).*

To configure it, create a TOML file (I'm using `auth_config.toml`) in the Gluetun's stack structure and use a bind volume as below:

```yaml
---
services:
  gluetun:
    volumes:
      - ./auth_config.toml:/gluetun/auth/config.toml
```

Create the file **first**, then run the container. Otherwise, Docker will automatically create a folder named `*.toml`.

This file should include at least:

```toml
[[roles]]
name = "qbtupdater"
routes = ["GET /v1/vpn/status", "GET /v1/portforward"]
auth = "apikey"
apikey = "super-secret-api-key"
```

Quick routes explaination:

| Route | Used for |
| --- | --- |
| `/v1/vpn/status` | Check if Gluetun is running. |
| `/v1/portforward` | Retreive the forwarded port. |

If this will change in th future, I'll update this table to always include an explaination why a route is required.

You can generate the API key, for exmaple: with using your password manager, `wg genkey`, or [Gluetun's built-in tool](https://github.com/qdm12/gluetun-wiki/blob/main/setup/advanced/control-server.md#authentication-methods).

```sh
docker run --rm qmcgaw/gluetun genkey
```

## FAQ

**Q: Why there's no `compose.yaml` file?**

A: There's no single "correct" way of implementing this micro-service. You should always decide on how **you** would like to do this. I'm also a huge fan of tinkering and trying things by myself and a huge enemy of telling people on how to live.

