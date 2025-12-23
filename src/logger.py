import os
from datetime import datetime

# ------------------------
LOG_DIR = "logs"
LOG_FILE = "history.txt"

# función para guardar comandos generados en un fichero de texto con fecha
def save_log(command):
    try:
        # Verificamos si la carpeta existe, si no, la creamos
        if not os.path.exists(LOG_DIR):
            os.makedirs(LOG_DIR)
            print(f"[*] Carpeta '{LOG_DIR}' creada automáticamente.")

        # Construimos la ruta completa
        file_path = os.path.join(LOG_DIR, LOG_FILE)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] CMD GENERADO: {command}\n"

        # Intentamos escribir en el fichero
        with open(file_path, "a", encoding="utf-8") as f:
            f.write(log_entry)
        
        print(f"[OK] Log guardado correctamente en {file_path}")

    except PermissionError:
        print(f"[!] ERROR CRÍTICO: No tengo permisos para escribir en '{LOG_DIR}'.")
    except OSError as e:
        print(f"[!] ERROR DE SISTEMA: No se pudo guardar el log. Detalle: {e}")
    except Exception as e:
        print(f"[!] ERROR DESCONOCIDO: {e}")

# ------------------------
# función para leer el fichero de logs y devolverlo en una lista de diccionarios
def get_logs():
    logs = []
    file_path = os.path.join(LOG_DIR, LOG_FILE)

    if not os.path.exists(file_path):
        return []

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            # leemos en orden inverso para ver los más recientes primero
            lines = f.readlines()[::-1]
            
            for line in lines:
                # separamos la fecha del comando usando el texto fijo que pusimos
                if "CMD GENERADO:" in line:
                    parts = line.split("CMD GENERADO:")
                    timestamp_part = parts[0].strip("[] ")
                    command_part = parts[1].strip()
                    
                    logs.append({
                        "timestamp": timestamp_part,
                        "command": command_part
                    })
        return logs
    except Exception as e:
        print(f"[!] Error leyendo logs: {e}")
        return []