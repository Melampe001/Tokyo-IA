import urllib.request
import json

def query_local_ai(prompt, model="mistral"):
    url = "http://localhost:11434/api/generate"
    payload = json.dumps({"model": model, "prompt": prompt, "stream": False}).encode("utf-8")
    req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req) as response:
            res = json.loads(response.read().decode())
            return res.get("response", "")
    except Exception as e:
        return f"[AI_OFFLINE] No se pudo conectar al servidor local de IA: {e}"

if __name__ == "__main__":
    print("[🧠] AI Bridge Local Creado y Preparado.")
