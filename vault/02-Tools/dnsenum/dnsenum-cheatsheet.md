---
title: "dnsenum — cheatsheet"
type: "cheatsheet"
tool: "dnsenum"
binary: "dnsenum"
status: "source-checked"
reviewed: "2026-10-26"
language: "pt-BR"
tags: ["cheatsheet", "tool/dnsenum", "category/information-gathering"]
cssclasses: ["fieldbook"]
test_status: "help-only"
tested_package_version: "dnsenum 1.3.2-1"
license_spdx: "GPL-2.0-or-later"
---

# dnsenum — cheatsheet

[Manual completo em português](dnsenum-dnsenum-1.md) · [Evidência da ajuda instalada](../../99-Assets/evidence/dnsenum-help-tests.json).

## Ajuda — conferida sem domínio

```bash
# Bash · diretório atual · Kali Linux/WSL · pacote dnsenum instalado
dnsenum --help
dnsenum -h
```

As duas chamadas exibiram ajuda e retornaram **código 1**, capturado explicitamente pelo teste. O banner do executável e o manual dizem **1.3.1**; o pacote dpkg tem versão **1.3.2-1**. Versão do pacote e versão informada pelo programa não foram confundidas.

## Receita com parâmetros explícitos

As receitas abaixo **executam consultas e podem gravar resultados**; não foram executadas pelo projeto. Defina domínio e wordlist antes de usá-las:

```bash
# Bash · diretório atual · Kali Linux/WSL · dnsenum, DOMAIN e WORDLIST definidos
dnsenum --nocolor --noreverse --threads 5 --timeout 10 \
  --file "${WORDLIST:?Defina WORDLIST}" "${DOMAIN:?Defina DOMAIN}"
```

`--noreverse` pula consultas reversas; não transforma a ferramenta em uma consulta passiva. O manual descreve A, NS, MX, tentativas AXFR, extração de resultados do Google, força bruta e outras operações.

## Atalho de enumeração

```bash
# Bash · diretório atual · Kali Linux/WSL · dnsenum e DOMAIN definido
dnsenum --enum "${DOMAIN:?Defina DOMAIN}"
```

**Divergência preservada:** o manual expande `--enum` para `--threads 5 -s 20 -w`; a ajuda instalada mostra `--threads 5 -s 15 -w`. O manual informa **20 páginas** para `--pages`; a ajuda instalada informa **5**. Foram comparados os textos, não o comportamento de consultas reais. A tradução não substituiu um padrão pelo outro silenciosamente.

## Opções de consulta rápida

| Opção | Função descrita no manual |
|---|---|
| `--dnsserver <server>` | Servidor para A/NS/MX; AXFR/PTR usam os NS do domínio |
| `--noreverse` | Pular consultas reversas |
| `--threads <va>` | Threads; grafia do parâmetro preservada do manual |
| `-t, --timeout <value>` | Timeout TCP/UDP em segundos; padrão documentado 10 |
| `-f, --file <file>` | Arquivo de subdomínios para força bruta |
| `-r, --recursion` | Recursão em subdomínios descobertos com NS |
| `-u, --update <a|g|r|z>` | Atualizar a wordlist com resultados; altera o arquivo |
| `--subfile <file>` | Gravar subdomínios válidos |
| `-w, --whois` | Consultas whois nos intervalos de rede |
| `-d, --delay <value>` | Espera máxima entre consultas whois; padrão documentado 3 s |
| `-e, --exclude <regexp>` | Excluir PTRs que correspondam à expressão |
| `--private` | Incluir IPs privados no arquivo final |

A ajuda instalada também lista `-o` e `--output`, ausentes do manual adquirido. Elas são registradas como diferenças de cobertura, não inseridas como se fossem texto original.

## Arquivos e proxy

O manual documenta `domain_ips.txt` como saída de blocos IP não contíguos. A ajuda informa uma wordlist padrão em `/usr/share/dnsenum/dns.txt` ou `dns.txt` junto ao programa. A leitura offline destas notas não exige rede; enumeração e buscas externas exigem conectividade.

O manual descreve as variáveis `http_proxy` e `HTTP_PROXY` para o scraping do Google e registra que o serviço pode bloquear consultas. Não foi feito scraping no teste.

## Reproduzir somente a conferência local

Na raiz do repositório:

```bash
# Bash · raiz do repositório · Kali Linux/WSL · Python 3 e dnsenum instalados
python3 scripts/test_dns_help.py --tool dnsenum
```

Sem `--record`, as evidências congeladas não são reescritas. O teste fornece somente opções de ajuda, compara a identidade do manual e verifica o diretório temporário.

## Procedência

[Original preservado](../../../sources/upstream/dnsenum/dnsenum.1.source) · [copyright integral](../../99-Assets/upstream/dnsenum/COPYRIGHT.package.txt) · [GPL-2](../../99-Assets/upstream/dnsenum/LICENSE.txt).

Fonte `dnsenum(1)` do pacote `1.3.2-1`, com data de manual `2024-04-21`. O preâmbulo gerado por Pod::Man foi preservado como dados e não executado. Manual e esta folha derivada seguem **GPL-2.0-or-later**. Revisão humana independente: pendente.
