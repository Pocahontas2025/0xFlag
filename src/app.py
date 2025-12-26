import os
import pickle
from flask import Flask, render_template, request, url_for, redirect, jsonify
from libraries import logger
from libraries.config_manager import save_configuration, load_configuration
from src.libraries.utils import load_tty_data, load_nmap_data # Asumimos que estas existen en utils

app = Flask(__name__)

# ==========================================
# GESTIÓN DE DATOS (Carga de Binarios)
# ==========================================

def load_discovery_data():
    """Carga las herramientas de Discovery desde la carpeta raiz /data."""
    # Subimos un nivel desde src/ para encontrar la carpeta data
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    bin_path = os.path.join(base_dir, 'data', 'discovery_tools.bin')
    
    if os.path.exists(bin_path):
        with open(bin_path, 'rb') as f:
            return pickle.load(f)
    return {}

# ==========================================
# RUTAS DE LA APLICACIÓN
# ==========================================

@app.route('/')
def home():
    return render_template('index.html')

# --- Herramienta NMAP ---
@app.route('/nmap')
def nmap():
    # 1. Cargamos configuración (IP atacante, IP objetivo)
    current_conf = load_configuration()
    # 2. Cargamos base de datos de escaneos
    nmap_scans_db = load_nmap_data()
    return render_template('nmap.html', scans=nmap_scans_db, config=current_conf)

# --- Herramienta DISCOVERY ---
@app.route('/discovery')
def discovery():
    # 1. Cargamos configuración para rellenar los inputs automáticamente
    current_conf = load_configuration()
    # 2. Cargamos las herramientas desde el binario
    tools_db = load_discovery_data()
    return render_template('discovery.html', config=current_conf, tools=tools_db)

# --- Herramienta TTY ---
@app.route("/tty")
def tty_helper():
    tty_data = load_tty_data()
    # Pasamos config por si en el futuro queremos usar la IP en los comandos TTY
    current_conf = load_configuration()
    return render_template("tty.html", procedures=tty_data, config=current_conf)

# --- Herramienta REVERSE SHELL ---
@app.route("/reverse")
def reverse_shell():
    current_conf = load_configuration()
    return render_template("reverse.html", config=current_conf)

# ==========================================
# RUTAS DE API Y CONFIGURACIÓN
# ==========================================

@app.route('/settings', methods=['GET', 'POST'])
def settings():
    message = None
    if request.method == 'POST':
        ip = request.form.get('attacker_ip')
        interface = request.form.get('interface')
        target = request.form.get('target_ip')
        wordlist = request.form.get('wordlist') # Si decides guardar wordlist en settings también

        # Guardamos usando tu gestor de configuración
        if save_configuration(ip, interface, target):
            message = "¡Configuración guardada correctamente!"
        else:
            message = "Error al guardar la configuración."

    current_conf = load_configuration()
    return render_template('settings.html', message=message, current_conf=current_conf)

@app.route('/api/save_target', methods=['POST'])
def api_save_target():
    """API rápida para guardar solo el Target desde Nmap/Discovery"""
    data = request.json
    target_ip = data.get('ip')
    
    if target_ip:
        # Cargamos config actual para no perder la IP atacante
        current = load_configuration()
        # Guardamos actualizando solo el target
        save_configuration(current.get('attacker_ip'), current.get('interface'), target_ip)
        return jsonify({"status": "success", "ip": target_ip})
    
    return jsonify({"status": "error"}), 400

@app.route('/api/log_command', methods=['POST'])
def api_log_command():
    data = request.get_json()
    command = data.get('command')
    if command:
        logger.save_log(command)
        return jsonify({"status": "success"})
    return jsonify({"status": "error"}), 400

@app.route('/history')
def history():
    logs = logger.get_logs()
    return render_template('history.html', logs=logs)

@app.route('/clear_history', methods=['POST'])
def clear_history_route():
    logger.clear_logs()
    return redirect(url_for('history'))