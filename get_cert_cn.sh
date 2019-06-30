#!/bin/bash

timeout $2 openssl s_client -connect $1:443 2>&1 </dev/null | sed -ne '/BEGIN CERT/,/END CERT/p' | openssl x509 -noout -subject 2>/dev/null
