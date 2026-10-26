---
title: "ffuf — guia"
type: "guide"
status: "source-checked"
reviewed: "2026-10-26"
tags: ["category/web", "tool/ffuf"]
cssclasses: ["fieldbook"]
tool: "ffuf"
installed_version: "2.1.0-1+b11"
test_status: "partial-local"
tested_version: "2.1.0-dev"
---

# ffuf — guia

Substitui `FUZZ` por entradas de uma wordlist. Neste piloto, o objetivo é localizar duas rotas conhecidas.
Execute na raiz do projeto, com o fixture local ativo em outro terminal.

`-mc 200` seleciona respostas HTTP 200. O teste não representa descoberta completa nem prova vulnerabilidades.
[Conceito](../../03-Concepts/fuzzing-e-filtros.md) · [cheatsheet](ffuf-cheatsheet.md) ·
[erros](ffuf-troubleshooting.md) · [fontes](ffuf-fontes.md).

[Evidência local sanitizada](../../99-Assets/evidence/local-tests.json). Escopo: versão, TCP/XML e receita ffuf limitada; demais receitas não foram executadas.
