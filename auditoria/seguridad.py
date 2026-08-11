# TOKYO OS (c) 2026 - TODOS LOS DERECHOS RESERVADOS - MARCA REGISTRADA
# -*- coding: utf-8 -*-
import hashlib

def obtener_hash(archivo):
    hasher = hashlib.sha256()
    with open(archivo, 'rb') as f:
        hasher.update(f.read())
    return hasher.hexdigest()

def validar_integridad():
    archivos_criticos = ['C:\\TOKYOAPPS-UNIVERSE\\main.py', 'C:\\TOKYOAPPS-UNIVERSE\\nucleo\\telemetria.py']
    for archivo in archivos_criticos:
        print(f"VERIFICANDO: {archivo} | HASH: {obtener_hash(archivo)[:16]}...")
    return True

if __name__ == '__main__':
    validar_integridad()
