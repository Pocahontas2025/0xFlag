
# ------------ FUNCIONES UTILES EN LA EJECUCION DEL PROGRAMA ------------
import psutil
import socket
import shlex
from urllib.parse import urlparse

SUPPORTED_TOOLS = {"gobuster", "ffuf", "dirsearch"}

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


def normalize_url(raw: str) -> str:
    """
    Acepta:
      - 10.10.10.10
      - http://10.10.10.10
      - https://example.com
    Devuelve siempre URL con esquema.
    """
    raw = (raw or "").strip()
    if not raw:
        return ""

    if "://" not in raw:
        raw = "http://" + raw

    # validación mínima para no generar comandos basura
    parsed = urlparse(raw)
    if not parsed.scheme or not parsed.netloc:
        return ""
    return raw


def parse_extensions(raw: str) -> list[str]:
    """
    Entrada: ".php, txt, .bak"
    Salida:  ["php", "txt", "bak"]   (sin puntos, sin duplicados)
    """
    raw = (raw or "").strip()
    if not raw:
        return []

    parts = [p.strip() for p in raw.split(",") if p.strip()]
    cleaned: list[str] = []
    seen = set()

    for p in parts:
        if p.startswith("."):
            p = p[1:]
        p = p.strip().lower()
        if p and p not in seen:
            cleaned.append(p)
            seen.add(p)

    return cleaned


def q(value: str) -> str:
    """Quote seguro para mostrar comandos (no se ejecuta)."""
    return shlex.quote(value)


def build_discovery_command(tool: str, target_url: str, wordlist: str, extensions_raw: str = "") -> str:
    """
    Genera el comando como texto. NO ejecuta.
    """
    tool = (tool or "").strip().lower()
    if tool not in SUPPORTED_TOOLS:
        raise ValueError(f"Herramienta no soportada: {tool}")

    url = normalize_url(target_url)
    if not url:
        raise ValueError("URL inválida.")

    wordlist = (wordlist or "").strip()
    if not wordlist:
        raise ValueError("Wordlist vacía.")

    exts = parse_extensions(extensions_raw)

    if tool == "gobuster":
        cmd = f"gobuster dir -u {q(url)} -w {q(wordlist)}"
        if exts:
            cmd += f" -x {q(','.join(exts))}"
        return cmd

    if tool == "ffuf":
        fuzz_url = url if "FUZZ" in url else url.rstrip("/") + "/FUZZ"
        cmd = f"ffuf -u {q(fuzz_url)} -w {q(wordlist)}"
        if exts:
            cmd += f" -e {q(','.join('.' + e for e in exts))}"
        return cmd

    # dirsearch
    cmd = f"dirsearch -u {q(url)} -w {q(wordlist)}"
    if exts:
        cmd += f" -e {q(','.join(exts))}"
    return cmd