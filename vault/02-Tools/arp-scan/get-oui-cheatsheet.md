---
title: "get-oui — cheatsheet"
type: "cheatsheet"
tool: "arp-scan"
binary: "get-oui"
status: "source-checked"
reviewed: "2026-10-26"
language: "pt-BR"
tags: ["cheatsheet", "tool/arp-scan", "category/network"]
cssclasses: ["fieldbook"]
test_status: "help-only"
tested_package_version: "arp-scan 1.10.0"
---

# get-oui — cheatsheet

[Manual completo em português](arp-scan-get-oui-1-dist.md) · [arp-scan](arp-scan-cheatsheet.md) · [Evidência da ajuda e integridade local](../../99-Assets/evidence/get-oui-help-tests.json).

## Ajuda, sem solicitar atualização

```bash
# Bash · diretório atual · Kali Linux/WSL · pacote arp-scan instalado
get-oui -h
```

Observado: código 0. As opções `-h`, `-f` e `-v` do manual também aparecem na ajuda instalada. A versão do pacote foi conferida separadamente como **arp-scan 1.10.0**; o utilitário não informou uma versão própria.

## Atualizar em um arquivo escolhido

Esta receita **faz downloads e grava um arquivo**; não foi executada pelo projeto. Defina `OUTPUT` como o arquivo de destino.

```bash
# Bash · diretório atual · Kali Linux/WSL · get-oui e módulos Perl instalados
get-oui -v -f "${OUTPUT:?Defina OUTPUT como o arquivo de saída}"
```

| Opção | Função |
|---|---|
| `-h` | Exibir a ajuda e encerrar |
| `-f <fn>` | Escolher o arquivo de saída |
| `-v` | Exibir o progresso detalhado |

O nome padrão é `ieee-oui.txt` no diretório atual. A saída histórica completa, incluindo o backup exibido pelo exemplo upstream, está no manual; ela não foi apresentada como resultado de um download realizado nesta máquina.

## Dependências e proxy

O manual requer Perl e os módulos `LWP::UserAgent` e `Text::CSV`, normalmente fornecidos pelos pacotes `libwww-perl` e `libtext-csv-perl`. A variável `http_proxy` permite configurar um proxy.

Os registros processados são MA-L, MA-M, MA-S e IAB. A leitura desta documentação é offline; atualizar os dados da IEEE exige acesso à rede. O arp-scan consulta o arquivo local de fabricantes, conforme descrito no manual.

## Reproduzir somente a conferência de ajuda

Na raiz do repositório:

```bash
# Bash · raiz do repositório · Kali Linux/WSL · Python 3 e pacote arp-scan instalados
python3 scripts/test_get_oui_help.py
```

O script consulta somente ajuda e versão em diretório temporário, verifica se esse diretório continua vazio e compara os hashes dos arquivos de dados locais encontrados. Por padrão, não reescreve as evidências congeladas.

## Procedência

Fonte: [get-oui.1.dist no commit fixado](https://github.com/royhills/arp-scan/blob/a0466d5fc7fa8a1e5625b7aae568ffb384e3f5a5/get-oui.1.dist). O [aviso específico de copyright e cópia](../../99-Assets/upstream/arp-scan/LICENSE.get-oui-manpage.txt) foi preservado. Os bancos de dados IEEE não foram baixados nem redistribuídos nesta etapa.
