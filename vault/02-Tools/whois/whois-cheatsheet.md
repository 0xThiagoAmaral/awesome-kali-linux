---
title: "whois — cheatsheet"
type: "cheatsheet"
tool: "whois"
binary: "whois"
status: "source-checked"
reviewed: "2026-10-26"
language: "pt-BR"
tags: ["cheatsheet", "tool/whois", "category/information-gathering"]
cssclasses: ["fieldbook"]
test_status: "help-only"
tested_package_version: "whois 5.6.6"
license_spdx: "GPL-2.0-or-later"
---

# whois — cheatsheet

[Manual completo em português](whois-whois-1.md) · [Evidência local](../../99-Assets/evidence/whois-help-tests.json).

## Ajuda e versão — conferidas localmente

```bash
# Bash · diretório atual · Kali Linux/WSL · pacote whois instalado
whois --help
whois --version
```

Observado no pacote **5.6.6**: ambos encerraram com código 0. Os 31 nomes de opções do manual, incluindo os dois aliases longos de host/porta, constam na ajuda instalada. Não houve consulta de rede; a identidade do manual gzip permaneceu inalterada.

## Consulta e servidor explícito

As receitas abaixo são complementares, derivadas das opções do manual e **não executadas**. A documentação pode ser lida offline; consultar um servidor remoto exige conectividade.

```bash
# Bash · diretório atual · Kali Linux/WSL · whois instalado e acesso à rede
QUERY='example.org'
whois "$QUERY"
whois --verbose "$QUERY"
whois --no-recursion "$QUERY"
```

Para escolher servidor e porta, preencha os valores antes de executar:

```bash
# Bash · diretório atual · Kali Linux/WSL · whois instalado e servidor definido
HOST='whois.example.org'
PORT='43'
QUERY='example.org'
whois --host="$HOST" --port="$PORT" "$QUERY"
```

| Opção | Função |
|---|---|
| `-h HOST` / `--host=HOST` | Escolher o servidor |
| `-p PORT` / `--port=PORT` | Escolher a porta |
| `-I` | Consultar IANA primeiro e seguir o encaminhamento |
| `--no-recursion` | Não seguir do registro para o registrador |
| `-H` | Não mostrar os avisos legais enviados por alguns registros |
| `--verbose` | Mostrar informações detalhadas |
| `--` | Separar opções do cliente da string de consulta |

## Opções RIPE — não universais

Estas opções dependem do servidor consultado; o manual informa que opções específicas do RIPE são ignoradas por servidores que não são RIPE.

| Opção | Função |
|---|---|
| `-q sources` / `-q types` / `-q version` | Informações sobre o servidor |
| `-t TYPE` / `-v TYPE` | Modelo simples / detalhado de objeto |
| `-T TYPE[,TYPE]...` | Filtrar tipos de objetos |
| `-i ATTR[,ATTR]... OBJECT` | Busca inversa por atributo e valor |
| `-s SOURCE[,SOURCE]...` | Escolher fontes, na ordem especificada |
| `-x` | Correspondência exata do prefixo |
| `-l` / `-L` | Um nível / todos os níveis menos específicos |
| `-m` / `-M` | Um nível / todos os níveis mais específicos |

A lista integral, incluindo espelhamento e filtragem, está no manual — esta folha não o substitui.

## Configuração e reprodução

- `/etc/whois.conf`: seleção de servidor por expressão regular.
- `WHOIS_OPTIONS`: opções avaliadas antes da linha de comando.
- `WHOIS_SERVER`: servidor alternativo quando a seleção automática falha.
- `LANG` / `LC_MESSAGES`: configuração regional, inclusive comportamento das consultas japonesas.

Na raiz do repositório, este teste reproduz apenas ajuda/versão e identidade do manual, sem regravar as evidências congeladas:

```bash
# Bash · raiz do repositório · Kali Linux/WSL · Python 3 e whois instalados
python3 scripts/test_whois_help.py
```

## Procedência e limites

Fonte: manual `whois(1)` do pacote instalado `whois 5.6.6`, datado de **2019-12-30**. [Original preservado](../../../sources/upstream/whois/whois.1.source), [copyright do pacote](../../99-Assets/upstream/whois/COPYRIGHT.package.txt) e [GPL-2](../../99-Assets/upstream/whois/LICENSE.txt).

A licença específica do manual é **GPL-2.0-or-later**, declarada na seção AUTHOR e no identificador SPDX do original. Esta folha derivada mantém essa licença. Não se atribui commit Git ao pacote instalado. Comportamentos históricos de registros externos não foram validados; revisão humana independente permanece pendente.
