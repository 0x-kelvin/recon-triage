#!/usr/bin/env python3
import argparse
import json
import urllib.request

OLLAMA_URL = "http://localhost:11434/api/generate"
MODELO = "llama3.2:3b"

def leer_hosts(archivo):
    with open(archivo) as f:
        return [l.strip() for l in f if l.strip()]

def preguntar_ia(prompt):
    datos = json.dumps({
        "model": MODELO,
        "prompt": prompt,
        "stream": False,
        "options": {"temperature": 0.2}
    }).encode("utf-8")
    req = urllib.request.Request(
        OLLAMA_URL, data=datos,
        headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read())["response"]

def construir_prompt(hosts):
    lista = "\n".join(hosts)
    return (
        "Eres un analista de seguridad haciendo triage de reconocimiento.\n"
        "Te doy subdominios de un objetivo autorizado. Marca SOLO los que vale la pena\n"
        "auditar primero (admin, paneles, dev, staging, api, ci/cd, jenkins, backups, vpn).\n"
        "Ignora los genéricos (www, cdn, blog, imágenes).\n"
        "Para cada uno interesante, UNA línea con este formato exacto:\n"
        "HOST | PRIORIDAD(alta/media) | razón corta\n"
        "Sin introducción ni conclusión.\n\n"
        f"Subdominios:\n{lista}"
    )

def guardar(archivo, texto):
    salida = f"{archivo}_triage.txt"
    with open(salida, "w") as f:
        f.write(texto)
    print(f"\n[+] Guardado en: {salida}")

def main():
    parser = argparse.ArgumentParser(description="recon-triage — prioriza hosts de recon con IA local")
    parser.add_argument("archivo", help="Archivo con hosts vivos (uno por línea)")
    args = parser.parse_args()

    hosts = leer_hosts(args.archivo)
    print(f"[*] {len(hosts)} hosts cargados")
    print("[*] Preguntando a la IA local...\n")

    resultado = preguntar_ia(construir_prompt(hosts))
    print(resultado)
    guardar(args.archivo, resultado)

if __name__ == "__main__":
    main()
