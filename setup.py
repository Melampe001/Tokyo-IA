# TOKYO OS (c) 2026 - TODOS LOS DERECHOS RESERVADOS - MARCA REGISTRADA
import os
from setuptools import setup
from Extension import Extension
from Cython.Build import cythonize

# Definición de módulos premium a cerrar de forma inmutable contra robo de código
modulos_premium = [
    "internal/integration/ecuacion_autonoma.py",
    "internal/integration/okx_connector.py",
    "internal/integration/api_gateway.py"
]

setup(
    name="TokyoApps_Premium_Binaries",
    ext_modules=cythonize(modulos_premium, compiler_directives={'language_level': "3"}),
)
print("🏁 [Cython] Entorno preparado. Comando de compilación industrial: python setup.py build_ext --inplace")
