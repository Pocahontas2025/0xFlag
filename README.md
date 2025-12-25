# 🚩 0xFlag - CTF Command Generator

**Versión:** Alpha v0.1
**Asignatura:** Introducció a la Programació / Tecnologies de la Productivitat
**Grupo:** 9

---

## 📖 Descripción del Proyecto

**0xFlag** es una herramienta web diseñada para facilitar la vida a los jugadores de **Capture The Flag (CTF)** y estudiantes de ciberseguridad. 

En competiciones o auditorías, recordar la sintaxis exacta de cada herramienta (Nmap, Gobuster, TTY upgrades, etc.) añade una carga cognitiva innecesaria. Este proyecto, soluciona ese problema ofreciendo una interfaz gráfica sencilla que **genera automáticamente los comandos complejos** basándose en los parámetros que el usuario necesita, permitiéndole centrarse en la estrategia y no en la memorización.

### 👥 Equipo de Desarrollo
* Xavier Conde
* Joel Díaz
* Oscar Ferre
* Gerard Soteras
* Adrià Trillo

---

## 🚀 Funcionalidades (Versión Alpha)

Esta entrega parcial (**Alpha**) implementa la arquitectura base del sistema y el primer módulo funcional:

1.  **Generador de Nmap:** Interfaz para crear escaneos de red (Rápido, Completo TCP y UDP) sin tocar la terminal.
2.  **Sistema de Logs:** Registro automático de todos los comandos generados en ficheros de texto para auditoría (`logs/history.txt`).
3.  **Arquitectura Modular:** Separación lógica entre interfaz web (Flask) y lógica de negocio (Python).

---

## 🛠️ Requisitos Previos

Para ejecutar este proyecto necesitas:

* **Python 3.8** o superior.
* **Pip** (Gestor de paquetes de Python).

---

## ⚙️ Instalación y Ejecución

Sigue estos pasos para desplegar la herramienta en tu entorno local:

### 1. Clonar el repositorio
```bash
git clone https://github.com/Pocahontas2025/0xFlag
cd 0XFlag
```

### 2. Instalar dependencias

El proyecto utiliza librerías externas para la gestión web. Instálalas con:

```bash
pip install -r requirements.txt
```

### 3. Ejecutar la aplicación

Lanza el servidor local ejecutando el punto de entrada principal:

```bash
python main.py
```

### 4. Acceder a la herramienta

Abre tu navegador web favorito y visita:

```
http://127.0.0.1:5000
```

---

## ⚙️ Personalización y Añadido de Comandos

**0xFlag** está diseñado para ser extensible. Los comandos de **Nmap** y los procedimientos de **TTY** no están "duros" en el código de la aplicación, sino que se generan a partir de una base de datos local.

Si deseas añadir tus propios escaneos personalizados o nuevos trucos de estabilización de shell, sigue estos pasos:

1. **Edita el archivo `generate_bins.py**`:
En la raíz del proyecto, abre este archivo. Verás dos diccionarios principales:
* `tty_procedures`: Contiene los métodos para mejorar la shell.
* `nmap_scans`: Contiene los "one-liners" de Nmap.

2. **Añade tu entrada**:
Sigue el formato existente (clave: valor).
* *Para Nmap:* Asegúrate de incluir el marcador `{ip}` donde quieras que se inserte la dirección IP objetivo.
* *Ejemplo:*
```python
"mi_scan": "nmap -p 80,443,8080 -sV {ip} -oN web_scan.txt"
```

3. **Regenera los binarios**:
Una vez guardado el archivo `.py`, ejecuta el script para actualizar la base de datos interna (`data/*.bin`):
```bash
python generate_bins.py

```

4. **Reinicia la aplicación**:
Si tenías `main.py` corriendo, ciérralo y vuélvelo a abrir para que cargue los nuevos cambios.

> **⚠️ Nota Importante:** Modifica `generate_bins.py` con cuidado. Asegúrate de respetar la sintaxis de diccionarios de Python (comillas, comas, llaves). Un error de sintaxis en este archivo impedirá la generación correcta de los binarios.

---

## 📂 Estructura del Proyecto

¡¡HAY QUE ACTUALIZARLO!!
El código sigue una arquitectura modular para facilitar la escalabilidad:

```text
PROYECTO-0XFLAG/
├── data/               # Almacenamiento de datos (placeholder)
├── logs/               # Registros de actividad (ficheros de texto)
│   └── history.txt     # Historial de comandos generados
├── src/                # Código fuente modular
│   ├── ctf_logic.py    # Lógica de generación de comandos
│   ├── logger.py       # Módulo de gestión de ficheros
│   ├── templates/      # Interfaz Web (HTML)
|   │   ├── index.html  # Landing Page de inicio
|   │   └── alpha.html  # Web provisional de la Alpha v0.1
|   └── static/         # Estilos e imágenes
│       ├── css/
│       │   └── styles.css
│       └── assets/
│           ├── favicon.ico
│           └── 0xFlag_Logo.png
├── main.py             # Punto de entrada (Servidor Flask)
├── requirements.txt    # Dependencias del proyecto
└── README.md           # Documentación
```

---

## 🛠️ Solución de Problemas (FAQ)

### ❌ Error al guardar la configuración ("Permission denied")
Si al intentar guardar tus ajustes en el apartado **Configuración** recibes un error o la aplicación se cierra, suele ser un problema de **permisos**.

**Causa:**
Probablemente ejecutaste la herramienta por primera vez usando `sudo` (root), lo que creó el archivo de guardado (`data/user_config.bin`) con permisos de administrador. Si ahora intentas ejecutarla como usuario normal, no tendrás permiso para sobrescribir ese archivo.

**Solución:**
Tienes dos opciones:
1.  **Ejecutar siempre con el mismo usuario** (recomendado usar usuario normal, no root, a menos que sea necesario).
2.  **Borrar el archivo de configuración bloqueado** para que se genere de nuevo con tu usuario actual:

```bash
sudo rm data/user_config.bin

```

### ❌ Error: ModuleNotFoundError: No module named 'flask'

Asegúrate de haber activado tu entorno virtual antes de iniciar la herramienta:

```bash
source venv/bin/activate  # En Linux/Mac
# o
pip install -r requirements.txt

```