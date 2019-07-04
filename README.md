# REVDNS.PY

This program is invoked with an IP address as first and only parameter (example):
```
python revdns.py 146.112.62.105
```
The output will be in JSON format (a few examples):
```

{host : ["ec2-34-250-148-148.eu-west-1.compute.amazonaws.com"], cn : "www.fortum.com"}
{host : ["server-f45.er33.bos50.r.cloudfront.net"], cn : "*.pandora.net"}
{host : ["bog02s07.1e100.net", "gru06s09.1e100.net", "bog02s07.1e100.net"], cn : "*.google.com"}
{host : [], cn : "www.update.microsoft.com"}
{host : [], cn : "*.stackexchange.com"}
{host : ["mail-wm1-f10.google.com"], cn : null}
{host : [], cn : null}
```
Note, of course there is no guarantee that the cn field encountered will always be in correct format (domain/wildcard)  
```
{host : ["black.ilatina.com"], cn : "Parallels Panel/emailAddress=info@parallels.com"}
```
however any such instances in a tcp traffic log would itself indicate traffic over malconfigured/self signed ssl. 

## Environment
It can run on python 2.7\
It needs to be deployed together with bash script get_cert_cn.sh\
It has been tested on Debian and it depends on `host` and `openssl` commands (what version are curently tested and verified are documented in the comments in the scripts). 


## What and why?
This program is intended to make a best effort "reverse dns check" on an IP number (tested only wih IPv4)\
It uses the `host` command to attempt resolving one or more host names for a given IP,  moreover then tries to pull *Subject CN* info from a https certificate, if there is one, on the IP endpoint.\
That way we can more often than not find the actual domain/organization providing its service on a given IP even in the many cases when it is **obscured by a CDN (content delivery network such as amazonaws, cloudfront, akamai, etc...)**.

The reverse dns problem is indeed a tricky one (partly because dns is not one-to-one). This program is not the end of the story. In the case of http(s) traffic there are deployments where a reverse proxy server will determine how to relay traffic on a certain endpoint. Depending on things like http request headers there may be several web servers with several legit certificates for different domains responding on one single IP endpoint. In such cases we will not be able to determine what server or what domain a IP log traffic entry represents, we will probably be able to pull the certificate of the facading reverse proxy however.

In any case I have found this trick of trying to pull the Subject CN of a deployed certificate to be suprisingly useful in revealing the nature web traffic given IP logs only. Give it a try and you'll see what I mean.

*Use cases*: traffic control, traffic monitoring and traffic analysis (it was built to enrich TCP log entries in a log server and could also be useful in automated routines for blocking or alerting).
