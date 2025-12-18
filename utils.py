
# ------------ FUNCIONES UTILES EN LA EJECUCION DEL PROGRAMA ------------
import psutil
import socket

def generate_nmap_command(ip, scan_type):
    if not ip:
        return "Error: Falta la IP"

    if scan_type == "fast":
        return f"nmap -F {ip} -oN scan_fast.txt"
    elif scan_type == "full":
        return f"nmap -p- -sV -sC {ip} -oN scan_full.txt"
    elif scan_type == "udp":
        return f"nmap -sU --top-ports 100 {ip}"
    else:
        return f"nmap {ip}"
    
def get_nics():
    nics = {}
    for iface, addrs in psutil.net_if_addrs().items():
        for addr in addrs:
            if addr.family == socket.AF_INET:
                nics[iface] = addr.address
    return nics
