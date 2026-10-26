---
title: "Nmap — cheatsheet"
type: "cheatsheet"
status: "source-checked"
reviewed: "2026-10-26"
tags: ["category/network", "tool/nmap"]
cssclasses: ["fieldbook"]
tool: "nmap"
installed_version: "7.99+dfsg-1kali1"
test_status: "partial-local"
tested_version: "7.99"
---

# Nmap — cheatsheet

Execute na raiz do projeto. O fixture padrão escuta em 127.0.0.1:8000.

## Conferir a versão

```bash
# Bash · raiz do projeto · Kali/WSL2 · Nmap
nmap --version
```

## Consultar a ajuda

```bash
# Bash · raiz do projeto · Kali/WSL2 · Nmap
nmap -h
```

## Verificar uma porta TCP

```bash
# Bash · raiz do projeto · Kali/WSL2 · Nmap
nmap -sT -p 8000 127.0.0.1
```

Com o fixture ativo, espera-se `open`. Sem listener, `closed` pode ser o resultado correto.

## Identificar o serviço

```bash
# Bash · raiz do projeto · Kali/WSL2 · Nmap
nmap -sT -sV --version-light -p 8000 127.0.0.1
```

`-sV` consulta o serviço; `--version-light` reduz a intensidade dessa identificação.

## Salvar XML para leitura por programas

```bash
# Bash · raiz do projeto · Kali/WSL2 · Nmap
mkdir -p artifacts
nmap -sT -p 8000 -oX artifacts/nmap-local.xml 127.0.0.1
```

Ler: [guia](nmap-guia.md) · [erros](nmap-troubleshooting.md) · [fontes](nmap-fontes.md).

[Evidência local sanitizada](../../99-Assets/evidence/local-tests.json). Escopo: versão, TCP/XML e receita ffuf limitada; demais receitas não foram executadas.
