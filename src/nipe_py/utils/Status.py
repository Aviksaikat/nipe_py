import json
import requests
from rich.console import Console

console = Console()

API_URL = "https://check.torproject.org/api/ip"

class Status:
    def __init__(self):
        response = requests.get(API_URL)
        
        if response.status_code == 200:
            data = json.loads(response.content)

            check_ip = data["IP"]
            check_tor = "true" if data["IsTor"] else "false"

            if check_tor == "true":
                console.print(f"[magenta][+] Status: [green]{check_tor}[/green] \n[+] Ip: [/magenta][yellow]{check_ip}")
            else:
                console.print(f"[magenta][+] Status: [red]{check_tor}[/red] \n[+] Ip: [/magenta][yellow]{check_ip}")
        else:
            console.print("[red][!] ERROR: sorry, it was not possible to establish a connection to the server.[/red]")
