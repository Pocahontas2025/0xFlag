import pickle
import os
import psutil
import socket

# --- UTILIDADES DEL SISTEMA ---

def get_nics():
    nics = {}
    try:
        # psutil.net_if_addrs() devuelve un diccionario con las interfaces
        for iface, addrs in psutil.net_if_addrs().items():
            for addr in addrs:
                # Filtramos solo las direcciones IPv4 (AF_INET)
                if addr.family == socket.AF_INET:
                    nics[iface] = addr.address
    except Exception as e:
        print(f"[!] Error obteniendo interfaces de red: {e}")
    
    return nics


# --- CARGADORES DE BINARIOS ---

# función auxiliar para encontrar la ruta absoluta de la carpeta 'data'
def _get_data_path(filename):
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    return os.path.join(base_dir, 'data', filename)

def load_tty_data():
    path = _get_data_path('tty_procedures.bin')
    try:
        with open(path, 'rb') as f:
            return pickle.load(f)
    except Exception as e:
        print(f"[ERROR] No se pudo cargar TTY bin: {e}")
        return {}

def load_nmap_data():
    path = _get_data_path('nmap_scans.bin')
    try:
        with open(path, 'rb') as f:
            return pickle.load(f)
    except Exception as e:
        print(f"[ERROR] No se pudo cargar Nmap bin: {e}")
        return {}
