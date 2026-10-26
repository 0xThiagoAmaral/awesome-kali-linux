---
title: "Nmap — guia"
type: "guide"
status: "source-checked"
reviewed: "2026-10-26"
tags: ["category/network", "tool/nmap"]
cssclasses: ["fieldbook"]
tool: "nmap"
installed_version: "7.99+dfsg-1kali1"
test_status: "partial-local"
tested_version: "7.99"
---

# Nmap — guia

**Objetivo:** identificar portas e serviços. Não substitui a interpretação do protocolo nem prova vulnerabilidades.

## Pré-requisitos

Nmap instalado. Execute os exemplos na raiz do projeto. Para o fixture documentado,
inicie `python3 scripts/local_fixture.py` em outro terminal. O piloto usa `-sT`, sem root.

## Modelo mental

Em [TCP connect](../../03-Concepts/tcp-connect.md), `open` significa que a conexão foi aceita;
`closed` normalmente indica ausência de listener; `filtered` exige investigar filtros/ausência de resposta.
Em WSL, se localhost funciona mas um alvo remoto não, diagnostique rota/VPN separadamente.

## Consulta rápida

[Cheatsheet](nmap-cheatsheet.md) · [Troubleshooting](nmap-troubleshooting.md) · [Fontes](nmap-fontes.md).

## Versão e evidência

A propriedade `installed_version` veio do inventário. `evidence/local-tests.json` registra a versão
real do binário e os testes executados. Isso não valida todas as opções do Nmap.

[Evidência local sanitizada](../../99-Assets/evidence/local-tests.json). Escopo: versão, TCP/XML e receita ffuf limitada; demais receitas não foram executadas.
