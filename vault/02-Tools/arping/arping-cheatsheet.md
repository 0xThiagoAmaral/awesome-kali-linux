---
title: "arping — cheatsheet"
type: "cheatsheet"
tool: "arping"
binary: "arping"
status: "source-checked"
reviewed: "2026-10-26"
language: "pt-BR"
tags: ["cheatsheet", "tool/arping", "category/network"]
cssclasses: ["fieldbook"]
test_status: "help-only"
tested_package_version: "arping 2.28-1"
license_spdx: "GPL-2.0-or-later"
---

# arping — cheatsheet

[Manual completo em português](arping-arping-8.md) · [Evidência local](../../99-Assets/evidence/arping-help-tests.json).

## Ajuda — conferida sem alvo

```bash
# Bash · diretório atual · Kali Linux/WSL · pacote arping instalado
arping --help
arping -h
```

Ambos encerraram com código 0 no pacote **2.28-1**. As 33 opções curtas do manual aparecem na ajuda estendida. A própria listagem não enumera `--help`, mas o teste confirma que essa chamada funcionou. Nenhum alvo ou interface foi fornecido ao teste.

## Consulta com limite definido

As receitas abaixo **enviam pacotes**, não foram executadas e exigem uma interface com suporte a essas operações. A documentação continua legível offline; estas operações dependem da rede local.

Preencha `INTERFACE` e `TARGET_IP` antes de executar:

```bash
# Bash · diretório atual · Kali Linux/WSL · arping, interface e permissões de rede
arping -i "${INTERFACE:?Defina INTERFACE}" -c 3 "${TARGET_IP:?Defina TARGET_IP}"
arping -i "${INTERFACE:?Defina INTERFACE}" -c 3 -r "${TARGET_IP:?Defina TARGET_IP}"
```

| Opção | Função |
|---|---|
| `-i interface` | Selecionar a interface sem tentar determiná-la |
| `-c count` | Limitar o número de solicitações |
| `-C count` | Aguardar esse número de respostas, independentemente de `-c` e `-w` |
| `-w sec` | Tempo limite total |
| `-W sec` | Intervalo entre pings |
| `-r` / `-R` | Saída bruta de um / do outro endereço |
| `-q` / `-v` / `-vv` | Saída silenciosa / detalhada / mais detalhada |
| `-d` | Procurar respostas duplicadas; manual descreve código 1 para MACs diferentes |
| `-V vlan` / `-Q priority` | Tag VLAN e prioridade 802.1p |
| `-z` / `-Z` | Ativar / desativar seccomp |

## IP e MAC não usam a mesma consulta

Segundo o manual, consultar um IP envia ARP who-has; consultar um MAC envia ICMP Echo de broadcast direcionado. As opções de origem, destino e modo promíscuo, incluindo `-S`, `-s`, `-T`, `-t` e `-p`, estão explicadas no manual completo. Não foram testadas operacionalmente.

O manual histórico também documenta ARP não solicitado (`-U`), respostas ARP (`-P`), broadcast (`-B`) e endereços de origem especiais. Esses exemplos foram preservados como documentação, não como ações realizadas nesta máquina.

## WSL e limites do teste

A presença do executável e a exibição da ajuda **não demonstram** que a interface WSL oferece o mesmo acesso Ethernet de uma interface física. Nenhuma capacidade de envio ARP/ICMP foi medida aqui, e nenhuma configuração do WSL foi alterada.

Na raiz do repositório:

```bash
# Bash · raiz do repositório · Kali Linux/WSL · Python 3 e arping instalados
python3 scripts/test_arping_help.py
```

O teste compara a identidade do manual instalado, captura ajuda e versão do pacote e verifica que o diretório temporário permaneceu vazio. Não regrava as evidências sem `--record`.

## Procedência

Manual `arping(8)`, pacote `2.28-1`. [Original preservado](../../../sources/upstream/arping/arping.8.source) · [copyright do pacote](../../99-Assets/upstream/arping/COPYRIGHT.package.txt) · [GPL-2](../../99-Assets/upstream/arping/LICENSE.txt).

O original foi mantido byte a byte. Seis ajustes de apresentação, vinculados ao hash exato da fonte, fecham blocos malformados e separam comandos de prosa; o registro está no manifesto. Esta folha derivada mantém **GPL-2.0-or-later**. Revisão humana independente: pendente.
