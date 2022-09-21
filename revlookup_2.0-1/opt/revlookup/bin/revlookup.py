import subprocess
import sys
import re
import socket
import sys

# This program is invoked with a IP address as first and only parameter (example):
# python revdns.py 146.112.62.105
# The output will be in JSON format (a few examples):
# {host : ["opendns.com", "www.opendns.com"], cn : "www.opendns.com"}
# {host : ["bog02s07-in-f14.1e100.net", "gru06s09-in-f110.1e100.net", "gru06s09-in-f110.1e100.net", "bog02s07-in-f14.1e100.net"], cn : "*.google.com"}
# {host : ["mail-wm1-f10.google.com"], cn : null}
# {host : [], cn : null}
#
# It can run on python 2.7
# It needs to be deployed together with bash script get_cert_cn.sh
#
# It is intended to make a best effort reverse check on a IP number (tested only wih IPv4)
# It uses the host command to attempt a reverse dns check and moreover then tries to pull CN info from a https certificate on the IP endpoint
# That way we can more often than not find the actual domain/organization of an IP even in cases when it is "hidden" by a content delivery network (amazonws, akamai, etc...)
# Use cases: traffic control and traffic analysis (like in a log server or in automated routines for blocking or alerting).

host_timeout = "4" # timeout in seconds for the host command
ssl_timeout= "5" # timeout in seconds for the openssl command


try:
    ipv4 = sys.argv[1]
    socket.inet_aton(ipv4)
except:
    sys.exit("Could not execute revlookup. An IPv4 address needs to be provided.")


# Invoking and parsing host is tested with host command version 9.10.3-P4-Ubuntu
#
# The output of the host command shall have the following format in order for parsing to work:
#
# X.X.X.X.in-addr.arpa domain name pointer www.acme.topdomain.
# X.X.X.X.in-addr.arpa domain name pointer acme.topdomain.
#
# (yes there may be more than one row, more than one name in the response)
#
host_name=""
try:
    host_output = str(subprocess.check_output(["host","-W "+host_timeout,ipv4]))
    raw_host_array=host_output.split("name pointer ")
    raw_host_lenght = len(raw_host_array)
    for i in range(1,raw_host_lenght): # in fist item (0th) there is never a host name
        if i>1:
            host_name += ", "
        host_name += "\""+((raw_host_array[i]).split(".\n"))[0]+"\"" # if there are more than one they  are separated by punctuation and newline
except:
    host_name = ""
host_name = "[{0}]".format(host_name)


# Invoking and parsing openssl to pull cert info
# See the bash script for what version of openssl it is verified with
#
cert_cn="null"
try:
    ssl_output = str(subprocess.check_output(["/opt/revlookup/bin/get_cert_cn.sh",ipv4,ssl_timeout]))
    ssl_output = ssl_output.replace("CN =","CN=")
    if "CN=" in ssl_output:
        parsed_cn = (ssl_output.split("CN=")[1]).rstrip() # peel off leading fields
        parsed_cn = re.split("/|,",parsed_cn)[0].strip()  # peel off trailing fields, either "/" or ","
        cert_cn ="\""+parsed_cn+"\"" # padding
except:
    cert_cn = "null"

print("{{host : {0}, cn : {1}}}".format(host_name,cert_cn))

# Alternatively to using openssl we could implement this by pulling cert info with curl:
# curl --insecure --head -v https://
# more suggestions: https://serverfault.com/questions/661978/displaying-a-remote-ssl-certificate-details-using-cli-tools
# curl --insecure -v https://www.google.com 2>&1 | awk 'BEGIN { cert=0 } /^\* SSL connection/ { cert=1 } /^\*/ { if (cert) print }'
#

