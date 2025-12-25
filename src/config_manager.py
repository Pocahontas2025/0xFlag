import os
import pickle

# ------------ RUTAS CONSTANTES ------------
DATA_DIR = "data"
CONFIG_FILE = "user_config.bin"
CONFIG_PATH = os.path.join(DATA_DIR, CONFIG_FILE)

# ------------ FUNCIONES ------------

# función escribir archivos binarios 
def save_configuration(attacker_ip, interface, target_ip):

    # creamos el diccionario
    config_data = {
        "attacker_ip": attacker_ip,
        "interface": interface,
        "target_ip": target_ip
    }
    # aseguramos que la carpeta data existe
    if not os.path.exists(DATA_DIR):
        try:
            os.makedirs(DATA_DIR)
        except OSError as e:
            print(f"[ERROR] No se pudo crear directorio: {e}")
            return False

    try:
        # escribimos los bytes en vez de texto.
        with open(CONFIG_PATH, "wb") as f:
            pickle.dump(config_data, f)
            
        print(f"[INFO] Configuración guardada en binario: {CONFIG_PATH}")
        print(f"[INFO] Datos: {data_string}")
        return True
    
    # hacemos el control de errores pos si algo falla y que muestre el codigo de error concreto
    except Exception as e:
        print(f"[ERROR] No se pudo guardar la configuración: {e}")
        return False

# ------------------------

# funcion para cargar configuración de usuario
def load_configuration():

    if not os.path.exists(CONFIG_PATH):
        return None 

    try:
        # leemos el contenido del archivo binario
        with open(CONFIG_PATH, "rb") as f:
            data = pickle.load(f)
        
        return data
    
    # hacemos el control de errores pos si algo falla y que muestre el codigo de error concreto
    except (pickle.UnpicklingError, EOFError):
        print("[ERROR] El archivo binario está corrupto o vacío.")
        return None
    except Exception as e:
        print(f"[ERROR] Error cargando configuración: {e}")
        return None