# WARNING - se tiene que instalar con pip (está especificado en el README)
from flask import Flask, render_template, request, url_for
from src import logger
from utils import get_nics,generate_nmap_command
from src.config_manager import save_configuration, load_configuration
import os
import pickle

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
    return render_template('nmap.html')

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
        # 1. Obtener datos del formulario
        ip = request.form.get('attacker_ip')
        interface = request.form.get('interface')

        # 2. Usar nuestra función modular para guardar en BINARIO
        if save_configuration(ip, interface):
            message = "¡Configuración guardada correctamente! (fichero binario actualizado)"
        else:
            message = "Error al guardar la configuración."

    # 3. Cargamos la config actual para mostrarla en los inputs (Persistence UI)
    current_conf = load_configuration()

    return render_template('settings.html', message=message, current_conf=current_conf)

# -----------------------------------------------------------------------
if __name__ == '__main__':
    if not os.path.exists('logs'):
        os.makedirs('logs')
        
    nics = get_nics()
    
    print("\nInterficies de red disponibles:\n")
    for i ,(iface, ip) in enumerate(nics.items(),start=1):
        print(f"{i}. {iface} - {ip}")
    choice = int(input("\nSeleccione numero de interficie: ")) - 1
    iface, ip_interface = list(nics.items())[choice]
    
    set_port = int(input("Selecione un puerto (0-1023 pueden requerir de privilegios ROOT):\n"))
    print(f"\nIniciando 0xFlag en http://{ip_interface}:{set_port}")
    app.run(debug=False, use_reloader=False, host=ip_interface, port=set_port)