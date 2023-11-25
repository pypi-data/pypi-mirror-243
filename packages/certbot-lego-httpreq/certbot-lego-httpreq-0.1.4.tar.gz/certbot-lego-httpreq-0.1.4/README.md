# Certbot plugin for HTTP Requests

This plugin provides a DNS challenge authenticator to solve the challenge using
a HTTP request to a custom endpoint. It uses the same logic as [lego](https://go-acme.github.io/lego/dns/httpreq/) with no HTTPREQ_MODE set.

To use the plugin install it using pip and then run certbot using

```bash
certbot certonly --authenticator dns-httpreq --dns-httpreq-credentials=mycreds.ini
```

with `mycreds.ini`:

```ini
dns_httpreq_endpoint = https://myhost/api/dns/acme/lego
dns_httpreq_username = someuser
dns_httpreq_password = somepassword
```
