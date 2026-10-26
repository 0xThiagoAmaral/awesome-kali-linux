---
title: "dnsrecon — cheatsheet"
type: "cheatsheet"
tool: "dnsrecon"
binary: "dnsrecon"
status: "source-checked"
reviewed: "2026-10-26"
language: "pt-BR"
tags: ["cheatsheet", "tool/dnsrecon", "category/information-gathering"]
cssclasses: ["fieldbook"]
test_status: "help-only"
tested_package_version: "dnsrecon 1.3.1-3"
license_spdx: "GPL-2.0-only"
---

# dnsrecon — cheatsheet

[Manual completo em português](dnsrecon-dnsrecon-1.md) · [Evidência local](../../99-Assets/evidence/dnsrecon-help-tests.json).

## Ajuda e versão — conferidas sem alvo

```bash
# Bash · diretório atual · Kali Linux/WSL · pacote dnsrecon instalado
dnsrecon --help
dnsrecon -h
dnsrecon -V
```

As três chamadas encerraram com código 0 no pacote **1.3.1-3**. Nenhum domínio, endereço ou servidor foi fornecido. O manual não fornece uma data no cabeçalho; o campo de data foi mantido como desconhecido, sem inventar uma.

## Enumeração padrão e exportação

As receitas abaixo **consultam a rede** e, quando indicado, **gravam arquivos**. Não foram executadas pelo projeto:

```bash
# Bash · diretório atual · Kali Linux/WSL · dnsrecon e DOMAIN definido
dnsrecon -d "${DOMAIN:?Defina DOMAIN}" -t std
dnsrecon -d "${DOMAIN:?Defina DOMAIN}" -t std -j resultado.json
```

O manual define `std` como SOA, NS, A, AAAA, MX e SRV. Não interpreta a exibição da ajuda como prova de que esses backends foram exercitados.

## Dicionário, reverso e transferência de zona

```bash
# Bash · diretório atual · Kali Linux/WSL · dnsrecon e parâmetros definidos
dnsrecon -d "${DOMAIN:?Defina DOMAIN}" -t brt -D "${WORDLIST:?Defina WORDLIST}"
dnsrecon -r "${RANGE:?Defina RANGE como intervalo ou CIDR}" -t rvl
dnsrecon -d "${DOMAIN:?Defina DOMAIN}" -t axfr
```

O exemplo original com `zonetransfer.me` está preservado no manual como exemplo histórico, não como consulta realizada nesta máquina.

| Opção | Função |
|---|---|
| `-d DOMAIN` | Domínio |
| `-n NS_SERVER` | Servidor(es), separados por vírgulas |
| `-D DICTIONARY` | Dicionário de subdomínios/hosts |
| `-r RANGE` | Intervalo de consulta reversa |
| `-t TYPE` | Tipo de enumeração |
| `--threads THREADS` | Número de threads |
| `--lifetime LIFETIME` | Espera pela resposta; padrão documentado 3 |
| `--tcp` | Consultas por TCP |
| `--db DB` | Salvar em SQLite 3 |
| `-x XML` / `-c CSV` / `-j JSON` | Exportações XML / CSV / JSON |
| `-f` / `--iw` | Filtragem de wildcard / continuar apesar de wildcard |

Os tipos `srv`, `bing`, `yand`, `crt`, `snoop`, `tld` e `zonewalk` também estão documentados integralmente no manual. Seus serviços externos e resultados não foram testados.

## Diferenças da ajuda instalada

Todos os nomes de opções do manual aparecem na ajuda instalada. Esta acrescenta:

- `-iL` / `--input-list`;
- `--loglevel`;
- `--disable_check_nxdomain`;
- os aliases `--verbose` e `--version`.

Os identificadores com sublinhado e a opção curta multicaractere `-iL` foram comparados sem truncamento. Essas diferenças não foram enxertadas no texto original do manual.

## Reproduzir somente a conferência local

Na raiz do repositório:

```bash
# Bash · raiz do repositório · Kali Linux/WSL · Python 3 e dnsrecon instalados
python3 scripts/test_dns_help.py --tool dnsrecon
```

O teste não aceita domínio nem alvo, e não regrava as evidências sem `--record`.

## Procedência

[Original preservado](../../../sources/upstream/dnsrecon/dnsrecon.1.source) · [copyright do pacote](../../99-Assets/upstream/dnsrecon/COPYRIGHT.package.txt) · [GPL-2](../../99-Assets/upstream/dnsrecon/LICENSE.txt).

Esta importação e sua folha derivada usam **GPL-2.0-only**, sem inferir uma autorização “ou posterior” da licença dos arquivos de empacotamento. Originais, gzip, versão e hashes foram preservados. Revisão humana independente: pendente.
