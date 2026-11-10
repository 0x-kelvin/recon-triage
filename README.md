# recon-triage

Prioriza hosts de reconocimiento usando una IA **local** (Ollama). Toma una lista de
hosts vivos y marca cuáles vale la pena auditar primero — sin que los datos salgan de tu máquina.

Compañero de [recon-kit](https://github.com/0x-kelvin/recon-kit): recon-kit descubre
los hosts, recon-triage decide por dónde empezar.

## Uso

```bash
python3 triage.py hosts.txt
```

Genera `hosts.txt_triage.txt` con el formato `HOST | PRIORIDAD | razón`.

## Cómo funciona

1. Lee los hosts del archivo.
2. Construye un prompt de triage y lo envía a un modelo local vía la API de Ollama (`localhost:11434`).
3. La IA marca los interesantes (admin, dev, staging, api, ci/cd, backups) e ignora el ruido.

Toda la inferencia ocurre en tu máquina: **ningún host se envía a terceros.**

## Requisitos

- Python 3
- [Ollama](https://ollama.com) con un modelo:
  ```bash
  ollama pull llama3.2:3b
  ```

## Nota

La IA es un primer filtro, no un oráculo: prioriza, tú verificas. Úsalo solo contra
objetivos tuyos o con autorización explícita.

---
por [0xkelvin](https://0xkelvin.sh)
