
# ------------ FUNCIÓN PARA GENERAR COMANDO NMAP BASADO EN PARÁMETROS ------------

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