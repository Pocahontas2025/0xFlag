# 🚩 0xFlag - CTF Command Generator

**Versión:** Alpha v0.1
**Asignatura:** Introducció a la Programació / Tecnologies de la Productivitat
**Grupo:** 9

---

## 📖 Descripción del Proyecto

**0xFlag** es una herramienta web diseñada para facilitar la vida a los jugadores de **Capture The Flag (CTF)** y estudiantes de ciberseguridad. 

En competiciones o auditorías, recordar la sintaxis exacta de cada herramienta (Nmap, Gobuster, TTY upgrades, etc) añade una carga cognitiva innecesaria. Este proyecto, soluciona ese problema ofreciendo una interfaz gráfica sencilla que **genera automáticamente los comandos complejos** basándose en los parámetros que el usuario necesita, permitiéndole centrarse en la estrategia y no en la memorización.

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

## 📂 Estructura del Proyecto

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

## ⚠️ Estado del Proyecto

Actualmente en fase **Alpha**. Próximas funcionalidades para la **Release Final**:

  * Módulo de Reverse Shells.
  * Asistente de tratamiento de TTY.
  * Persistencia de configuración de usuario.
  * Servidor localhost.
  * Hosting web a la IP de la maquina, para conexiones remotas.

---
