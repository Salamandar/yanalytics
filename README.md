# yanalytics

A YunoHost instances analytics server, inspired by https://www.home-assistant.io/integrations/analytics.

> [!IMPORTANT]
> Sharing analytics is completely optional. Nothing is sent from your installation
> unless you explicitly opt in, and you can change what is shared or turn it off
> at any time. Only aggregated, anonymized totals are published publicly. Your
> individual installation is never identifiable from the public data.

## What is sent

A number of informations is sent to our server:

* A unique identifier for your installation, so each installation is only counted once.
  It is derived from `/etc/machine-id` but is NOT identical to preserve privacy.
* The Debian and YunoHost versions you are using
* Hardware information:
  * architecture
  * number of CPUs
  * total RAM amount (rounded)
  * total disk size (rounded)
* A geocode based on the IP address (the IP address itself is NOT stored)
  The geographic information is NOT determined on the instance's side to preserve
  privacy: In case you decide to use a VPN, the VPN information will be stored on our side.
* The list of the installed apps
* The number of users
* The number of domains / subdomains

Of course, this (will be) is configurable on your side via a configuration file.

### Data retention

We regularly aggregate data and remove "unanonymised" data from our servers.

If your instance doesn't send any data for 60 days, any received data containing
your unique identifier will be deleted.

## Development

This project is based on FastAPI, Uvicorn and Gunicorn.

To run the development server:

```bash
uv run uvicorn --reload "yanalytics.app:create_app()"
```

To run the production server:

```bash
uv run gunicorn "yanalytics.app:create_app()" -k uvicorn_worker.UvicornWorker
```
