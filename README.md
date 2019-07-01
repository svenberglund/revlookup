# REVDNS.PY

This program is invoked with a IP address as first and only parameter (example):
```
python revdns.py 146.112.62.105
```
The output will be in JSON format (a few examples):
```
{host : ["opendns.com", "www.opendns.com"], cn : "www.opendns.com"}
{host : ["bog02s07-in-f14.1e100.net", "gru06s09-in-f110.1e100.net", "gru06s09-in-f110.1e100.net", bog02s07-in-f14.1e100.net"], cn : "*.google.com"}
{host : ["mail-wm1-f10.google.com"], cn : null}
{host : [null], cn : null}
```

## Environment
It can run on python 2.7\
It needs to be deployed together with bash script get_cert_cn.sh\
It has been tested on Debian and it depends on `host` and `openssl` commands (what version are curently tested and verified are documented in the comments in the scripts). 


## What and why?
This program is intended to make a best effort "reverse dns check" on an IP number (tested only wih IPv4)\
It uses the `host` command to attempt resolving one or more host names for a given IP,  moreover then tries to pull CN info from a https certificate on the IP endpoint if there is one.\
That way we can more often than not find the actual domain/organization of an IP even in the many cases when it is "hidden" by a content delivery network (amazonws, akamai, etc...).\

*Use cases*: traffic control and traffic analysis (it was built to enrich TCP log entries in a log server and could also be useful in automated routines for blocking or alerting).
