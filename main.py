# WARNING - se tiene que instalar con pip (está especificado en el README)
from flask import Flask, render_template, request, url_for, redirect
from src import logger
from utils import get_nics,generate_nmap_command
from src.config_manager import save_configuration, load_configuration
import os
import pickle
from utils import build_discovery_command


def load_tty_procedures():
    with open("tty_procedures.bin", "rb") as f:
        return pickle.load(f)

TTY_PROCEDURES = load_tty_procedures()

# Definimos que busque templates en src/templates y estáticos en src/static
app = Flask(__name__, template_folder='src/templates', static_folder='src/static')

# -----------------------------------------------------------------------

# Landing Page
@app.route('/')
def home():
    return render_template('index.html')

# -----------------------------------------------------------------------

# Herramienta funcional nmap
@app.route('/nmap')
def nmap():
    current_conf = load_configuration()
    return render_template('nmap.html', current_conf=current_conf)

# -----------------------------------------------------------------------
# Discovery UI
@app.route('/discovery')
def discovery():
    return render_template("discovery.html", current={"tool": "gobuster"})


# Procesa el formulario de discovery

@app.route("/generate_discovery", methods=["POST"])
def generate_discovery():
    form = request.form

    target_url = (form.get("target_url") or "").strip()
    wordlist   = (form.get("wordlist") or "").strip()
    extensions = (form.get("extensions") or "").strip()
    tool       = (form.get("tool") or "gobuster").strip()

    # Para no perder datos en errores
    current = {
        "target_url": target_url,
        "wordlist": wordlist,
        "extensions": extensions,
        "tool": tool,
    }

    if not target_url or not wordlist:
        return render_template(
            "discovery.html",
            message="URL y wordlist son obligatorios.",
            current=current
        )

    try:
        # Generar comando (NO ejecutar)
        command = build_discovery_command(
            tool,
            target_url,
            wordlist,
            extensions
        )

        # LOG exactamente igual que Nmap
        logger.save_log(command)

    except ValueError as e:
        return render_template(
            "discovery.html",
            message=f"Entrada inválida: {e}",
            current=current
        )

    return render_template(
        "discovery.html",
        message="Comando generado correctamente.",
        current=current,
        command=command
    )

@app.route("/reverse", methods=["GET", "POST"])
def reverse_shell():
    if request.method == "GET":
        return render_template("reverse.html", current=None, output=None, message=None)

    lhost = (request.form.get("lhost") or "").strip()
    lport = (request.form.get("lport") or "").strip()
    template = request.form.get("template") or ""

    current = {"lhost": lhost, "lport": lport, "template": template}

    if not lhost or not lport or not template.strip():
        return render_template("reverse.html", current=current, output=None,
                               message="Completa LHOST, LPORT y la plantilla.")

    logger.save_log(output)
    
    output = template.replace("{LHOST}", lhost).replace("{LPORT}", lport)

    return render_template("reverse.html", current=current, output=output, message=None)


# -----------------------------------------------------------------------
@app.route("/tty", methods=["GET", "POST"])
def tty_assist():
    selected = None
    procedure = None

    if request.method == "POST":
        selected = request.form.get("procedure")
        procedure = TTY_PROCEDURES.get(selected)

    return render_template(
        "tty.html",
        procedures=TTY_PROCEDURES,
        selected=selected,
        procedure=procedure
    )

# -----------------------------------------------------------------------

# Procesa el formulario de la nmap
@app.route('/generate', methods=['POST'])
def generate():
    ip = request.form.get('target_ip')
    scan_type = request.form.get('scan_type')
    
    # Lógica y Logs
    command = generate_nmap_command(ip, scan_type)
    logger.save_log(command)
    
    # Al terminar, volvemos a mostrar nmap.html con el resultado
    return render_template('nmap.html', result=command)

# -----------------------------------------------------------------------

# Espacio de configuración del usuario
@app.route('/settings', methods=['GET', 'POST'])
def settings():
    message = None

    if request.method == 'POST':
        # obtener datos del formulario
        ip = request.form.get('attacker_ip')
        interface = request.form.get('interface')
        target = request.form.get('target_ip')

        # usar nuestra función modular para guardar en BINARIO
        if save_configuration(ip, interface, target):
            message = "¡Configuración guardada correctamente!"
        else:
            message = "Error al guardar la configuración."

    # cargamos la config actual para mostrarla en los inputs
    current_conf = load_configuration()
    return render_template('settings.html', message=message, current_conf=current_conf)



# -----------------------------------------------------------------------

# Espacio de historial de comandos usados

@app.route('/history')
def history():
    # Obtenemos la lista de logs parseada
    logs = logger.get_logs()
    return render_template('history.html', logs=logs)

# limpiar historial
@app.route('/clear_history', methods=['POST'])
def clear_history_route():
    logger.clear_logs()
    return redirect(url_for('history'))

# -----------------------------------------------------------------------

if __name__ == '__main__':
    # crear carpeta de logs si no existe
    if not os.path.exists('logs'):
        os.makedirs('logs')
        
    # obtener interfaces actuales
    nics = get_nics()
    selected_ip = None
    selected_iface_name = None

    # cargamos configuración por si se definió previamente
    saved_conf = load_configuration()

    # si hay config guardada y esa interfaz existe en este momento:
    if saved_conf and saved_conf['interface'] in nics:
        pref_iface = saved_conf['interface']
        pref_ip = nics[pref_iface]
        
        print(f"\n[★] Preferencia detectada: {pref_iface} ({pref_ip})")
        use_pref = input("¿Quieres usarla? [S/n]: ").lower().strip()
        
        # si pulsa alguna de las siguientes confirmaciones, usamos la guardada
        if use_pref in ['', 's', 'si', 'y', 'yes']:
            selected_iface_name = pref_iface
            selected_ip = pref_ip

    # si no eligió interfaz automática
    if not selected_ip:
        print("\n--- Interfaces Disponibles ---")
        # convertimos a lista para poder indexar por número
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

    # selección de puerto
    try:
        p_input = input("\nSeleccione un puerto [Default: 500]: ")
        # si está vacío usa 500, si no, intenta convertir a entero
        set_port = int(p_input) if p_input.strip() else 500
    except ValueError:
        print("⚠ Entrada no válida. Usando puerto 500 por defecto.")
        set_port = 500

    print(f"\n[+] Lanzando 0xFlag en: http://{selected_ip}:{set_port}")
    print(f"[i] Presiona CTRL+C para detener el servidor.\n")
    
    app.run(debug=False, use_reloader=False, host=selected_ip, port=set_port)