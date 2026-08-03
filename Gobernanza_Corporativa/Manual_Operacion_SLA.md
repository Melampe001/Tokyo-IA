# MANUAL DE OPERACIÓN GLOBAL Y ACUERDO DE NIVEL DE SERVICIO (SLA) - MELAMPE001
Versión: 2026.1 - Alta Disponibilidad Continua

## 1. Mantenimiento Automático Eeterno (Estrategia 24/7)
La infraestructura del Rascacielos Digital opera de forma autónoma acoplada al Kernel de Windows.
*   **Vigencia del Proceso:** Monitoreado por el "Resource_Guardian.ps1" y el programador de tareas profunda bajo el usuario administrador oculto 'NT AUTHORITY\SYSTEM'.
*   **Protocolo de Caídas (Anti-Entropy):** Si un subproceso crítico (Python/Go) agota la memoria o sufre un bloqueo de red, el sistema operativo fuerza un reinicio limpio en caliente en menos de 60 segundos sin intervención humana.

## 2. Gestión de Tokens de Acceso
*   Cada token emitido de forma automatizada (TK-XXXXXXXXXXXX) posee una vigencia estricta en base de datos SQLite y es validado en microsegundos en cada petición HTTP por hilos ligeros de ejecución de Go (Go-routines).