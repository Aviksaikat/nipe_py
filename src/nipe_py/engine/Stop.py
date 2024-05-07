from nipe_py.utils.Device import Device
import subprocess
from pathlib import Path


class Stop:
    def __init__(self):
        device = Decice()
        self.device = device.get_device()
        tables = ["nat", "filter"]
        stop_tor = "systemctl stop tor"

        if self.device.distribution == "void":
            start_tor = "sv stop tor > /dev/null"
        
        for table in tables:
            subprocess.call(f"iptables -t {table} -F OUTPUT", shell=True)
            subprocess.call(f"iptables -t {table} -F OUTPUT", shell=True)

        if Path("/etc/init.d/tor").exists():
            stop_tor = "/etc/init.d/tor stop > /dev/null"

    def stop() -> bool:
        subprocess.call(stop_tor, shell=True)
        return True
        
        