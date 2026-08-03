# Sistema de Habla para IA - Explicación Completa

## ¿Qué es esto?
Es la arquitectura de un sistema que le da "habla real" a una IA.
No solo responde, sino que RECUERDA, ENTIENDE y HILA conversaciones.

---

## ¿Cómo funciona el flujo?

```
Usuario escribe algo
        ↓
[entendimiento/parser.py]
→ ¿Qué dijo exactamente?
        ↓
[entendimiento/intencion.py]
→ ¿Qué quiere lograr?
        ↓
[entendimiento/contexto.py]
→ ¿De qué va la conversación?
        ↓
[memoria/] - Los 3 tipos
→ ¿Qué recuerdo de antes?
        ↓
[razonamiento/procesador.py]
→ Genera las ideas de la respuesta
        ↓
[razonamiento/coherencia.py]
→ ¿Tiene sentido? ¿Se contradice?
        ↓
[razonamiento/hilacion.py]
→ Conecta con el pasado
        ↓
[respuesta/generador.py]
→ Construye el texto final
        ↓
[respuesta/tono.py]
→ Le da naturalidad
        ↓
Usuario recibe la respuesta
        ↓
[memoria/] Guarda lo importante
```

---

## Los 3 tipos de memoria

| Tipo | Dura | Guarda | Equivalente humano |
|---|---|---|---|
| Corta | Esta sesión | Todo el chat actual | Últimos minutos |
| Mediana | 7 días | Resúmenes de sesiones | Ayer, antier |
| Larga | Siempre | Lo más importante | Meses o años |

---

## ¿Qué hace cada carpeta?

- **/memoria** → Los 3 tipos de memoria + archivo JSON
- **/entendimiento** → Comprende lo que dice el usuario
- **/razonamiento** → Piensa y genera la lógica de la respuesta
- **/respuesta** → Construye y afina el texto final
- **/nucleo** → Configuración y herramientas generales
- **main.py** → El director que conecta todo

---

## Nota importante
Los archivos están en MACHOTE (plantilla).
Las funciones están definidas pero vacías (pass).
El siguiente paso es ir llenando cada función una por una.
