---
title: "Workflow — descoberta web local"
type: "workflow"
status: "source-checked"
reviewed: "2026-10-26"
tags: ["fieldbook"]
cssclasses: ["fieldbook"]
---

# Workflow — descoberta web local

## Preparar

Na raiz do projeto, terminal 1:

```bash
# Bash · raiz do projeto · Kali/WSL2 · Python 3
python3 scripts/local_fixture.py
```

## Executar e interpretar

No terminal 2, use [Nmap](../02-Tools/nmap/nmap-cheatsheet.md) para verificar a porta;
depois [ffuf](../02-Tools/ffuf/ffuf-cheatsheet.md) para consultar as rotas sintéticas.
Resultados esperados não são registros de execução. O script de teste da raiz produz a evidência real.

## Encerrar

Ctrl+C no terminal do fixture. As saídas pessoais ficam em `artifacts`, ignorado pelo Git.
