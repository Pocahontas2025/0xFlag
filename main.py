import sys
import os

# 1. Aseguramos que Python encuentre la carpeta 'src'
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# 2. Importaciones
from src.app import app
from src.libraries.utils import get_nics
from libraries.config_manager import save_configuration, load_configuration

def start_server():
    # Crear carpeta de logs si no existe
    if not os.path.exists('logs'):
        os.makedirs('logs')

    # --- LÓGICA DE SELECCIÓN DE INTERFAZ ---
    nics = get_nics()
    selected_ip = None
    selected_iface_name = None

    # Cargar configuración previa para sugerirla
    saved_conf = load_configuration()

    # Si hay config guardada y la interfaz sigue existiendo
    if saved_conf and saved_conf.get('interface') in nics:
        pref_iface = saved_conf['interface']
        pref_ip = nics[pref_iface]
        
        print(f"\n[★] Preferencia detectada: {pref_iface} ({pref_ip})")
        # Timeout visual o input directo
        use_pref = input("¿Quieres usarla? [S/n]: ").lower().strip()
        
        if use_pref in ['', 's', 'si', 'y', 'yes']:
            selected_iface_name = pref_iface
            selected_ip = pref_ip

    # Si no se eligió la automática, mostrar menú
    if not selected_ip:
        print("\n--- Interfaces Disponibles ---")
        nic_list = list(nics.items()) 
        
        for i, (iface, ip) in enumerate(nic_list, start=1):
            print(f"{i}. {iface:<10} - {ip}")
            
        while True:
            try:
                choice = input("\nSeleccione número de interfaz: ")
                idx = int(choice) - 1
                if 0 <= idx < len(nic_list):
                    selected_iface_name, selected_ip = nic_list[idx]
                    break
                else:
                    print("⚠ Número fuera de rango.")
            except ValueError:
                print("⚠ Por favor, introduce un número válido.")

    # --- GUARDADO AUTOMÁTICO DE SESIÓN ---
    # Guardamos la IP seleccionada en la config para que la App la use
    # Mantenemos el target_ip anterior si existe
    current_target = saved_conf.get('target_ip', '') if saved_conf else ''
    save_configuration(selected_ip, selected_iface_name, current_target)

    # --- SELECCIÓN DE PUERTO ---
    try:
        p_input = input("\nSeleccione un puerto [Default: 5000]: ")
        set_port = int(p_input) if p_input.strip() else 5000
    except ValueError:
        print("⚠ Entrada no válida. Usando puerto 5000.")
        set_port = 5000

    print(f"\n[+] Lanzando 0xFlag en: http://{selected_ip}:{set_port}")
    print(f"[i] Presiona CTRL+C para detener el servidor.\n")
    
    # Arrancamos la app importada de src/app.py
    app.run(debug=True, use_reloader=False, host=selected_ip, port=set_port)

if __name__ == '__main__':
    start_server()