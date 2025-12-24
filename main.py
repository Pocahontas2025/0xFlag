# WARNING - se tiene que instalar con pip (está especificado en el README)
from flask import Flask, render_template, request, url_for
from src import ctf_logic, logger
import os

# Definimos que busque templates en src/templates y estáticos en src/static
app = Flask(__name__, template_folder='src/templates', static_folder='src/static')

# Landing Page
@app.route('/')
def home():
    return render_template('index.html')

# Herramienta funcional (Alpha)
@app.route('/alpha')
def alpha_tool():
    return render_template('alpha.html')

# Procesa el formulario de la Alpha
@app.route('/generate', methods=['POST'])
def generate():
    ip = request.form.get('target_ip')
    scan_type = request.form.get('scan_type')
    
    # Lógica y Logs
    command = ctf_logic.generate_nmap_command(ip, scan_type)
    logger.save_log(command)
    
    # Al terminar, volvemos a mostrar alpha.html con el resultado
    return render_template('alpha.html', result=command)

if __name__ == '__main__':
    if not os.path.exists('logs'):
        os.makedirs('logs')
    print(" Iniciando 0xFlag Alpha en http://127.0.0.1:5000")
    app.run(debug=True, port=5000)