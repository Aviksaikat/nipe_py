import subprocess
from pathlib import Path
from nipe_py.utils.Device import Device

class Start:
    def __init__(self):
        device = Device()
        self.device = device.get_device()
        dns_port = "9061"
        transfer_port = "9051"
        table = ["nat", "filter"]
        network = "10.66.0.0/255.255.0.0"
        start_tor = "systemctl start tor"

        if self.device.distribution == "void":
            start_tor = "sv start tor > /dev/null"

        elif Path("/etc/init.d/tor").exists():
            start_tor = "/etc/init.d/tor start > /dev/null"

    def start(self) -> bool:
        subprocess.call(f"tor -f .configs/{self.device.distribution}-torrc > /dev/null", shell=True)
        subprocess.call(start_tor, shell=True)

        for t in table:
            target = "ACCEPT"

            if t == "nat":
                target = "RETURN"

            subprocess.call(f"iptables -t {t} -F OUTPUT", shell=True)
            subprocess.call(f"iptables -t {t} -A OUTPUT -m state --state ESTABLISHED -j {target}", shell=True)
            subprocess.call(f"iptables -t {t} -A OUTPUT -m owner --uid {device.username} -j {target}", shell=True)

            match_dns_port = dns_port

            if t == "nat":
                target = f"REDIRECT --to-ports {dns_port}"
                match_dns_port = "53"

            subprocess.call(f"iptables -t {t} -A OUTPUT -p udp --dport {match_dns_port} -j {target}", shell=True)
            subprocess.call(f"iptables -t {t} -A OUTPUT -p tcp --dport {match_dns_port} -j {target}", shell=True)

            if t == "nat":
                target = f"REDIRECT --to-ports {transfer_port}"

            subprocess.call(f"iptables -t {t} -A OUTPUT -d {network} -p tcp -j {target}", shell=True)

            if t == "nat":
                target = "RETURN"

            subprocess.call(f"iptables -t {t} -A OUTPUT -d 127.0.0.1/8    -j {target}", shell=True)
            subprocess.call(f"iptables -t {t} -A OUTPUT -d 192.168.0.0/16 -j {target}", shell=True)
            subprocess.call(f"iptables -t {t} -A OUTPUT -d 172.16.0.0/12  -j {target}", shell=True)
            subprocess.call(f"iptables -t {t} -A OUTPUT -d 10.0.0.0/8     -j {target}", shell=True)

            if t == "nat":
                target = f"REDIRECT --to-ports {transfer_port}"

            subprocess.call(f"iptables -t {t} -A OUTPUT -p tcp -j {target}", shell=True)

        subprocess.call("iptables -t filter -A OUTPUT -p udp -j REJECT", shell=True)
        subprocess.call("iptables -t filter -A OUTPUT -p icmp -j REJECT", shell=True)

        subprocess.call("sysctl -w net.ipv6.conf.all.disable_ipv6=1 >/dev/null", shell=True)
        subprocess.call("sysctl -w net.ipv6.conf.default.disable_ipv6=1 >/dev/null", shell=True)

        return True
