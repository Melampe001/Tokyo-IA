# ============================================================
# contexto.py - EL QUE SABE DE QUÃ‰ VA LA CONVERSACIÃ“N
# ============================================================
# QUE HACE: Mantiene el hilo temÃ¡tico de la conversaciÃ³n.
# Sabe de quÃ© se estÃ¡ hablando en todo momento y
# conecta el mensaje actual con lo anterior.
#
# EQUIVALENTE HUMANO: La capacidad de saber que cuando
# alguien dice "eso" se refiere a algo que dijeron antes.
#
# EJEMPLO:
#   Usuario: "y eso cÃ³mo funciona?"
#   Sin contexto: Â¿QuÃ© es "eso"? No sÃ©.
#   Con contexto:  "eso" = memoria a corto plazo (tema anterior)
# ============================================================

def obtener_contexto(memoria_corta, texto_actual):
    """
    Combina la memoria reciente con el mensaje actual
    para entender el contexto completo.
    """
    pass

def resolver_referencias(texto, historial):
    """
    Resuelve palabras como 'eso', 'eso que dijiste',
    'lo anterior', etc. usando el historial.
    """
    pass

def identificar_tema_actual(historial):
    """Detecta el tema principal de la conversaciÃ³n"""
    pass
