import subprocess
import sys


host_timeout = "4" # timeout in seconds for the host command
ssl_timeout= "6" # timeout in seconds for the ssl command



ipv4 = sys.argv[1];

host_name=""
try:
    host_output = subprocess.check_output(["host","-W "+host_timeout,ipv4])
    host_name = (host_output.split("name pointer ")[1]).rstrip().strip('.')
except:
    host_name="host-not-resolved"
print(host_name)


cert_cn=""
try:
    ssl_output = subprocess.check_output(["./get_cert_cn.sh",ipv4,ssl_timeout]);
    cert_cn = ""
    if "CN=" in ssl_output:
        cert_cn = (ssl_output.split("CN=")[1]).rstrip()
        if "/" in cert_cn:
            cert_cn = cert_cn.split("/")[0].strip()
            # the separator for additional trailing fields in the cert info is "/"
except:
    cert_cn = "cert-cn-not-resolved"

print(cert_cn)

# Alternatively to using openssl you can pull cert info with curl:
# curl --insecure --head -v https://
# more suggestions: https://serverfault.com/questions/661978/displaying-a-remote-ssl-certificate-details-using-cli-tools
# curl --insecure -v https://www.google.com 2>&1 | awk 'BEGIN { cert=0 } /^\* SSL connection/ { cert=1 } /^\*/ { if (cert) print }'


