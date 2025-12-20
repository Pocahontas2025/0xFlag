# WARNING - se tiene que instalar con pip (está especificado en el README)
from flask import Flask, render_template, request, url_for
from src import logger
from utils import get_nics
import os
import utils

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
    command = utils.generate_nmap_command(ip, scan_type)
    logger.save_log(command)
    
    # Al terminar, volvemos a mostrar alpha.html con el resultado
    return render_template('alpha.html', result=command)

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
    print(f"\nIniciando 0xFlag Alpha en http://{ip_interface}:{set_port}")
    app.run(debug=False, use_reloader=False, host=ip_interface, port=set_port)



