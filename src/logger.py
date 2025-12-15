import os
from datetime import datetime

# ------------ FUNCIÓN PARA GUARDAR COMANDOS GENERADOS EN UN FICHERO DE TEXTO CON FECHA ------------

LOG_DIR = "logs"
LOG_FILE = "history.txt"

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