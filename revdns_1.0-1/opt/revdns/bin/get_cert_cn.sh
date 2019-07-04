#!/bin/bash

# Tested with [OpenSSL 1.0.2g  1 Mar 2016] on Debian
timeout $2 openssl s_client -connect $1:443 2>&1 </dev/null | sed -ne '/BEGIN CERT/,/END CERT/p' | openssl x509 -noout -subject 2>/dev/null
