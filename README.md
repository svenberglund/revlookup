# REVDNS

This CLI for Linux is invoked with an IPv4 address as first and only parameter (example):
```
revdns 146.112.62.105
```
The output will be in JSON format (a few examples):
```

{host : ["ec2-34-250-148-148.eu-west-1.compute.amazonaws.com"], cn : "www.fortum.com"}
{host : ["server-f45.er33.bos50.r.cloudfront.net"], cn : "*.pandora.net"}
{host : ["a23-219-46-110.deploy.static.akamaitechnologies.com"], cn : "www.turner.com"}
{host : ["bog02s07.1e100.net", "gru06s09.1e100.net", "bog02s07.1e100.net"], cn : "*.google.com"}
{host : [], cn : "www.update.microsoft.com"}
{host : [], cn : "*.stackexchange.com"}
{host : ["mail-wm1-f10.google.com"], cn : null}
{host : [], cn : null}
{host : ["black.ilatina.com"], cn : "Parallels Panel"} 
```

The first few examples in the list show a typical situation where the `host` resolved is actually a *content delivery network host* while the `cn` field in these cases indeed manages to achieve the "cdn transparency" that we want, hence it will reveal the service provider on the endpoint.\
The last example shows a case where the endpoint https certificate has a malconfigured *Subject CN*.


## Installation
### .deb package
On a Debian based distro (ubuntu, mint, etc...) the program can be installed with some of the following `.deb` packages

* [installer for 64 bit architecture](https://github.com/svenberglund/cdn-transparency-revdns/blob/amd64-build/revdns_1.0-1.deb)
* [installer for 32 bit architecture](https://github.com/svenberglund/cdn-transparency-revdns/blob/master/revdns_1.0-1.deb)

Install with
```
dpkg -i revdns<version>.deb
```
... or of course with a window based handler for `.deb` packages if your system has one.\
**Current installers are tested with recent (2018-2019) versions of Mint, Q4OS and Peppermint.**

**Disclaimer:** The author/publisher of these executables/scripts will assume no responsability for consequences of the installation, execution or removal of `revdns`.

#### dpkg package removal
```
dpkg --remove revdns
```

#### Manual removal
Remove the executable `/usr/local/bin/revdns` and the folder `/opt/revdns`. 

### Manual installation
Alternatively you can place the two files [`revdns.py` and `get_cert_cn.sh`](https://github.com/svenberglund/cdn-transparency-revdns/tree/master/revdns_1.0-1/opt/revdns/bin) as exectutables anywhere on your system. Although if you choose a location other than `/opt/revdns/bin` you will have to change the path to the shell script in the python script. I.e. change the line that looks like this 
```
ssl_output = subprocess.check_output(["/opt/revdns/bin/get_cert_cn.sh",ipv4,ssl_timeout])
```
to match the path to where ever you place the `.sh` file.


With this sort of installation the program will then be invoked as `python <path-to-executables>/revdns.py <ipv4-number>` or (nicer) by [registering an alias](https://www.hostingadvice.com/how-to/set-command-aliases-linuxubuntudebian/) on your system to that very command.



## Dependencies and Environment
`revdns` uses the system default python interpreter to run.\
The program can run on a system with python 2.7\
(Forward compatiblity if a later python version is OS default has not yet been verified.)\
The python script needs to be deployed together with bash script `get_cert_cn.sh` (which is done automatically with `.deb` installer).\
It has been tested on various Debian based distros and it depends on `host` and `openssl` commands (what version are curently tested and verified are documented in the comments in the scripts). 


## What, how and why?
This program is intended to make a *"best effort reverse dns check"* on an IP number (tested only wih IPv4)\
It uses the `host` command to attempt resolving one or more host names for a given IP,  moreover then tries to pull *Subject CN* info from a https certificate, if there is one, on the IP endpoint.\
That way we can more often than not find the actual domain/organization providing its service on a given IP even in the many cases when it is **obscured by a CDN (content delivery network such as amazonaws, cloudfront, akamaitechnologies, etc...)**.

The "reverse dns problem" is a difficult one (partly because dns is not one-to-one). This program is not the end of the story. In the case of https traffic there are deployments where a reverse proxy server will determine how to relay traffic on a certain endpoint. Depending on things like http request headers there may be several web servers with several legit certificates for different domains responding on one single IP endpoint. In such cases we will not be able to determine what server or what domain a IP log traffic entry represents, we will probably be able to pull the certificate of the facading reverse proxy however.

In any case I have found this trick of trying to pull the Subject CN of a deployed certificate to be suprisingly useful in revealing the nature web traffic given IP logs only. Give it a try and you'll see what I mean.

*Use cases*: traffic control, traffic monitoring and traffic analysis (it was built to enrich TCP log entries in a log server and could also be useful in automated routines for blocking or alerting).
