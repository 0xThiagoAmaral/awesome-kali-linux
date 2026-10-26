---
title: "arp-scan — cheatsheet"
type: "cheatsheet"
tool: "arp-scan"
binary: "arp-scan"
status: "source-checked"
reviewed: "2026-10-26"
language: "pt-BR"
tags: ["cheatsheet", "tool/arp-scan", "category/network"]
cssclasses: ["fieldbook"]
test_status: "help-only"
tested_version: "1.10.0"
---

# arp-scan — cheatsheet

[Manual principal completo](arp-scan-arp-scan-1-dist.md) · [Ferramenta complementar arp-fingerprint](arp-fingerprint-cheatsheet.md) · [Conferência da ajuda instalada](../../99-Assets/evidence/arp-scan-main-tests.json).

## Ajuda e versão

```bash
# Bash · diretório atual · Kali Linux/WSL · arp-scan instalado
arp-scan --help
arp-scan --version
```

Observado: **arp-scan 1.10.0**, com código 0 em ambos os comandos. As receitas de rede abaixo são modelos da documentação, não varreduras executadas pelo projeto.

## Um endereço IPv4, sem resolução DNS

```bash
# Bash · diretório atual · Kali Linux/WSL · arp-scan
arp-scan --interface="${INTERFACE:?Defina INTERFACE}" \
  --numeric "${TARGET_IP:?Defina TARGET_IP como um endereço IPv4}"
```

## Gerar a lista pela configuração da interface

```bash
# Bash · diretório atual · Kali Linux/WSL · arp-scan
arp-scan --interface="${INTERFACE:?Defina INTERFACE}" --localnet
```

Na fonte fixada, `--localnet` inclui rede e broadcast por padrão. A opção `--exclude-broadcast` aparece no manual, mas não na ajuda local verificada; essa diferença não foi ocultada.

## Ler alvos de um arquivo e limitar a largura de banda

```bash
# Bash · diretório atual · Kali Linux/WSL · arp-scan
arp-scan --interface="${INTERFACE:?Defina INTERFACE}" \
  --file="${TARGET_FILE:?Defina TARGET_FILE}" --bandwidth=256000 --retry=2
```

`--bandwidth` usa **bits por segundo**, não bytes. Não combine `--bandwidth` com `--interval`.

## Saída simples para processamento

```bash
# Bash · diretório atual · Kali Linux/WSL · arp-scan
arp-scan --interface="${INTERFACE:?Defina INTERFACE}" --plain --numeric \
  --format='${ip},${mac},"${vendor}"' \
  "${TARGET_IP:?Defina TARGET_IP como um endereço IPv4}"
```

As aspas simples preservam os marcadores de `--format` para o próprio programa, sem expansão pelo shell. `--quiet` disponibiliza somente `${ip}` e `${mac}`; para incluir o fabricante, não use essa opção.

## Opções essenciais

| Opção | Função |
|---|---|
| `--interface` / `-I` | Escolher a interface |
| `--numeric` / `-N` | Aceitar IPs, evitando resolução de nomes de entrada |
| `--localnet` / `-l` | Gerar alvos pela interface e máscara |
| `--file` / `-f` | Ler um alvo ou padrão por linha |
| `--bandwidth` / `-B` | Definir a largura de banda de saída |
| `--retry` / `-r` | Definir o total de tentativas por host |
| `--plain` / `-x` | Remover cabeçalho e rodapé |
| `--format` / `-F` | Escolher os campos e o formato |
| `--rtt` / `-D` | Calcular o tempo de ida e volta |

ARP atua na rede local e não é roteado. As exigências de permissões, capabilities e acesso a dispositivos estão detalhadas no manual; nenhuma configuração de privilégios foi alterada pelo projeto.

## Reproduzir somente a conferência de ajuda

Na raiz do repositório:

```bash
# Bash · raiz do repositório · Kali Linux/WSL · Python 3 e arp-scan instalados
python3 scripts/test_arp_scan_help.py
```

O script consulta apenas ajuda e versão, não informa alvos e não reescreve evidências por padrão.

## Procedência

As 42 opções, 6 tabelas, a fórmula de tempo e as transcrições históricas completas estão no [manual fixado](https://github.com/royhills/arp-scan/blob/a0466d5fc7fa8a1e5625b7aae568ffb384e3f5a5/arp-scan.1.dist). O [aviso próprio de cópia](../../99-Assets/upstream/arp-scan/LICENSE.arp-scan-manpage.txt) foi preservado, sem substituí-lo pela licença geral do repositório.
