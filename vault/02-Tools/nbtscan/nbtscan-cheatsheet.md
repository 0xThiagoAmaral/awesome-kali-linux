---
title: "nbtscan — cheatsheet"
type: "cheatsheet"
tool: "nbtscan"
binary: "nbtscan"
status: "source-checked"
reviewed: "2026-10-26"
language: "pt-BR"
tags: ["cheatsheet", "tool/nbtscan", "category/information-gathering"]
cssclasses: ["fieldbook"]
test_status: "usage-only"
tested_package_version: "nbtscan 1.7.2-3"
license_spdx: "GPL-2.0-or-later"
---

# nbtscan — cheatsheet

[Manual completo em português](nbtscan-nbtscan-1.md) · [Evidência local](../../99-Assets/evidence/nbtscan-help-tests.json).

## Mensagem de uso — conferida sem alvo

```bash
# Bash · diretório atual · Kali Linux/WSL · pacote nbtscan instalado
nbtscan
```

No subprocesso de teste, a chamada sem argumentos exibiu a mensagem de uso e encerrou com **código 2**. Isso não é uma varredura bem-sucedida: faltou o alvo, intencionalmente. A versão do pacote foi conferida separadamente como **1.7.2-3**. As 12 opções do manual aparecem na mensagem instalada.

**`-h` não significa ajuda:** imprime nomes legíveis de serviços e só pode ser usada com `-v`.

## Receitas de consulta

Estas receitas derivadas do manual **enviam consultas NetBIOS** e não foram executadas. Defina `TARGET` como um IP ou intervalo da sua atividade de laboratório:

```bash
# Bash · diretório atual · Kali Linux/WSL · nbtscan e TARGET definido
nbtscan "${TARGET:?Defina TARGET como IP ou intervalo}"
nbtscan -v "${TARGET:?Defina TARGET como IP ou intervalo}"
nbtscan -v -h "${TARGET:?Defina TARGET como IP ou intervalo}"
nbtscan -v -s : "${TARGET:?Defina TARGET como IP ou intervalo}"
```

Formas documentadas: IP único (`192.168.1.1`), rede/prefixo (`192.168.1.0/24`) e intervalo do último octeto (`192.168.1.1-127`). Os endereços são exemplos do manual, não alvos consultados pelo projeto.

## Opções importantes

| Opção | Função |
|---|---|
| `-v` | Exibir a tabela completa de nomes NetBIOS |
| `-h` | Nomes legíveis de serviços, com `-v` |
| `-d` | Despejar pacotes; o manual exclui combinação com `-v`, `-s` e `-h` |
| `-e` / `-l` | Formato /etc/hosts / lmhosts |
| `-q` | Suprimir banners e erros |
| `-s separator` | Separador de campos, sem cabeçalhos |
| `-f filename` | Ler endereços de um arquivo |
| `-m retransmits` | Número de retransmissões; padrão 0 |
| `-b bandwidth` | Limitação em bps, segundo o manual |
| `-r` | Porta local 137; manual informa necessidade de root no Unix |

## Divergência de unidade em -t

O **manual instalado** descreve `-t` em **segundos, padrão 1**. A **mensagem de uso instalada** descreve **milissegundos, padrão 1000**.

Não trocamos o texto do manual silenciosamente. A divergência está registrada nas evidências e no aviso de compatibilidade. O teste não mediu o comportamento de timeout de uma consulta real; portanto não apresenta a comparação entre textos como prova de comportamento de rede.

## O que o resultado significa

O manual cobre nome do computador, indicação de servidor, usuário e MAC. A tabela dos **29 sufixos NetBIOS** e as quatro perguntas frequentes estão no manual completo, com comandos e saídas históricas preservados.

NBTscan não é um enumerador de compartilhamentos SMB: o manual distingue suas consultas UDP da busca por compartilhamentos via TCP. As afirmações sobre Windows 95/NT/2000 são históricas, oriundas desta edição.

## Reproduzir apenas a conferência local

Na raiz do repositório:

```bash
# Bash · raiz do repositório · Kali Linux/WSL · Python 3 e nbtscan instalados
python3 scripts/test_nbtscan_usage.py
```

O script não fornece alvo e não solicita envio de pacotes. Registra separadamente o código não zero do utilitário e o resultado das verificações; compara os hashes do manual instalado e preserva as evidências congeladas por padrão.

## Procedência

[Original preservado](../../../sources/upstream/nbtscan/nbtscan.1.source) · [copyright integral](../../99-Assets/upstream/nbtscan/COPYRIGHT.package.txt) · [GPL-2](../../99-Assets/upstream/nbtscan/LICENSE.txt).

O manual e esta folha derivada seguem **GPL-2.0-or-later**. A exceção BSD no copyright do pacote refere-se aos scripts geradores especificados, não é uma licença atribuída automaticamente ao manual. Revisão humana independente: pendente.
