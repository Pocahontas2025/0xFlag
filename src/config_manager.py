import os

# ------------ RUTAS CONSTANTES ------------
DATA_DIR = "data"
CONFIG_FILE = "user_config.bin"
CONFIG_PATH = os.path.join(DATA_DIR, CONFIG_FILE)

# ------------ FUNCIONES ------------

# función escribir archivos binarios 
def save_configuration(attacker_ip, interface):

    # declaramos los datos con un formato de texto simple
    data_string = f"{attacker_ip};{interface}"
    
    # codificamos a utf-8 para luego escribirlo en bytes
    data_bytes = data_string.encode('utf-8')

    # asegurmos que la carpeta data existe
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

    try:
        # escribimos los bytes en vez de texto.
        with open(CONFIG_PATH, "wb") as f:
            f.write(data_bytes)
            
        print(f"[INFO] Configuración guardada en {CONFIG_PATH}")
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
            content_bytes = f.read()
            
        # decodificamos los bytes a utf-8
        content_str = content_bytes.decode('utf-8')
        
        # separamos los datos por el punto y coma que pusimos al guardar
        if ";" in content_str:
            ip, interface = content_str.split(";")
            
            # devolvemos el diccionario
            return {
                "attacker_ip": ip,
                "interface": interface
            }
        return None
    
    # hacemos el control de errores pos si algo falla y que muestre el codigo de error concreto
    except Exception as e:
        print(f"[ERROR] Error cargando configuración: {e}")
        return None