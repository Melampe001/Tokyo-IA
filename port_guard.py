import json
import os
import sys
import time
import psutil

REGISTRY_PATH = os.path.join(os.path.dirname(__file__), "port_registry.json")

def load_registry():
    if not os.path.exists(REGISTRY_PATH):
        return {"managed_ports": {}}
    with open(REGISTRY_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def is_port_in_use(port: int):
    for conn in psutil.net_connections(kind='inet'):
        if conn.laddr.port == port:
            return conn.pid
    return None

def audit_and_secure_port(port: int):
    registry = load_registry()
    port_str = str(port)
    managed_info = registry["managed_ports"].get(port_str)

    print(f"[*] [PORT GUARD] Analizando puerto {port}...")

    active_pid = is_port_in_use(port)
    if not active_pid:
        print(f"[✅] [PORT GUARD] Puerto {port} libre y disponible.")
        return True

    try:
        proc = psutil.Process(active_pid)
        proc_name = proc.name()
    except (psutil.NoSuchProcess, psutil.AccessDenied):
        proc_name = "Desconocido"

    print(f"[!] [PORT GUARD] Puerto {port} ocupado por PID {active_pid} ({proc_name})")

    if managed_info and managed_info.get('critical'):
        print(f"[❌] [PORT GUARD] BLOQUEO CRÍTICO: El puerto {port} pertenece a un núcleo protegido ({managed_info['service_name']}).")
        return False
    else:
        print(f"[*] [PORT GUARD] Liberando PID {active_pid} y esperando liberación del kernel...")
        try:
            proc.terminate()
            proc.wait(timeout=3)
        except Exception:
            pass

        # Espera activa hasta que el sistema operativo libere el socket (máximo 5 segundos)
        for _ in range(10):
            if not is_port_in_use(port):
                print(f"[✅] [PORT GUARD] Socket del puerto {port} liberado exitosamente por el OS.")
                return True
            time.sleep(0.5)
        
        print(f"[⚠️] [PORT GUARD] El socket sigue retenido, pero se intentará el arranque.")
        return True

if __name__ == "__main__":
    target_port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    success = audit_and_secure_port(target_port)
    sys.exit(0 if success else 1)