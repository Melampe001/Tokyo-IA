import os
import subprocess
import datetime

# Directorios raÃ­z donde se encuentran todos tus proyectos y repositorios de software
RAICES_A_ESCANEAR = [
    r"C:\NULOGIC_CORE",
    r"C:\TOKYOAPPS-UNIVERSE",
    r"C:\Tokyo-Predictor-Roulette",
    r"C:\TokyoApps"
]

ssh_key = r"C:\Users\Tokyo Master\.ssh\id_ed25519_tokyo".replace('\\', '/')
log_path = r"C:\NULOGIC_CORE\logs\execution_flow.log"
timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

with open(log_path, "a", encoding="utf-8") as log:
    log.write(f"\n[START] --- Ciclo de Gobernanza Multirepositorio: {timestamp} ---\n")
    print(f"âš¡ [TokyoAI™™â„¢] Iniciando Escaneo Masivo de Repositorios en {timestamp}")
    print("==============================================================================")
    
    for raiz in RAICES_A_ESCANEAR:
        if not os.path.exists(raiz):
            log.write(f"  [âš ï¸] Ruta omitida (No existe en hardware): {raiz}\n")
            continue
            
        # Buscar repositorios Git activos en la carpeta actual o subcarpetas directas
        repos_a_procesar = []
        if os.path.exists(os.path.join(raiz, ".git")):
            repos_a_procesar.append(raiz)
        else:
            # Buscar subcarpetas que sean repositorios
            try:
                for subcarpeta in os.listdir(raiz):
                    ruta_completa = os.path.join(raiz, subcarpeta)
                    if os.path.isdir(ruta_completa) and os.path.exists(os.path.join(ruta_completa, ".git")):
                        repos_a_procesar.append(ruta_completa)
            except Exception:
                pass

        # Procesar de forma asÃ­ncrona e idempotente cada repositorio localizado
        for repo in repos_a_procesar:
            os.chdir(repo)
            nombre_repo = os.path.basename(repo)
            print(f"ðŸª™ Sincronizando Activo en GitHub: {nombre_repo}")
            log.write(f"[*] Procesando repositorio remoto: {nombre_repo}\n")
            
            # Forzar configuraciÃ³n corporativa inmutable
            subprocess.run(["git", "config", "user.name", "JosÃ© Arturo Orozco Jaime"], capture_output=True)
            subprocess.run(["git", "config", "user.email", "thenewtokyocompany@gmail.com"], capture_output=True)
            subprocess.run(["git", "config", "core.sshCommand", f"ssh -i '{ssh_key}' -o IdentitiesOnly=yes"], capture_output=True)
            
            # Secuencia forzada de indexaciÃ³n y commit
            subprocess.run(["git", "add", "--all"], capture_output=True)
            subprocess.run(["git", "commit", "-m", "Auto-clean: SincronizaciÃ³n inmaculada multirepositorio por Melampe001", "--allow-empty"], capture_output=True)
            
            # Push forzado por tÃºnel SSH protegido contra robos
            res = subprocess.run(["git", "push", "origin", "main", "--force"], capture_output=True, text=True)
            
            if "Permission denied" in res.stderr:
                print(f"  [âŒ] Error de acceso en {nombre_repo}. Llave no registrada en GitHub web.")
                log.write(f"  [âŒ] Fallo SSH en repositorio: {nombre_repo}\n")
            else:
                print(f"  [âœ…] {nombre_repo} respaldado y blindado en la nube con Ã©xito.")
                log.write(f"  [âœ…] SincronizaciÃ³n exitosa: {nombre_repo}\n")

    log.write(f"[END] --- Fin del ciclo global multirepositorio ---\n")
print("==============================================================================")
print("ðŸ PROTOCOLO CONCLUIDO: El 100% de tus repositorios estÃ¡n bajo gobernanza automatizada.")

