---
title: "ffuf — cheatsheet"
type: "cheatsheet"
status: "source-checked"
reviewed: "2026-10-26"
tags: ["category/web", "tool/ffuf"]
cssclasses: ["fieldbook"]
tool: "ffuf"
installed_version: "2.1.0-1+b11"
test_status: "partial-local"
tested_version: "2.1.0-dev"
---

# ffuf — cheatsheet

## Versão

```bash
# Bash · raiz do projeto · Kali/WSL2 · ffuf
ffuf -V
```

## Descoberta local com saída JSON

```bash
# Bash · raiz do projeto · Kali/WSL2 · ffuf
mkdir -p artifacts
ffuf -noninteractive -w vault/99-Assets/fixtures/paths.txt -u http://127.0.0.1:8000/FUZZ -mc 200 -t 1 -rate 5 -of json -o artifacts/ffuf-local.json
```

Espera-se encontrar `/admin` e `/health`; `/missing` retorna 404.
`-w` escolhe a lista, `-u` define a URL, `-t` limita concorrência e `-rate` limita requisições por segundo.
[Guia](ffuf-guia.md) · [fontes](ffuf-fontes.md).

[Evidência local sanitizada](../../99-Assets/evidence/local-tests.json). Escopo: versão, TCP/XML e receita ffuf limitada; demais receitas não foram executadas.
