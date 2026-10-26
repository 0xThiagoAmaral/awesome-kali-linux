---
title: "netdiscover — cheatsheet"
type: "cheatsheet"
tool: "netdiscover"
binary: "netdiscover"
status: "source-checked"
reviewed: "2026-10-26"
language: "pt-BR"
tags: ["cheatsheet", "tool/netdiscover", "category/network"]
cssclasses: ["fieldbook"]
test_status: "help-only"
tested_package_version: "netdiscover 0.21-1"
license_spdx: "GPL-3.0-or-later"
---

# netdiscover — cheatsheet

[Manual completo em português](netdiscover-netdiscover-8.md) · [Evidência local](../../99-Assets/evidence/netdiscover-help-tests.json).

## Ajuda — conferida sem iniciar varredura

```bash
# Bash · diretório atual · Kali Linux/WSL · pacote netdiscover instalado
netdiscover -h
```

Na instalação **0.21-1**, a chamada exibiu ajuda e retornou **código 1**. As 16 opções enumeradas pelo manual aparecem nessa listagem. O teste usou HOME temporário, sem alvo, interface ou pedido de captura.

**Executar sem `-p`, `-r` ou `-l` não é uma chamada de ajuda:** segundo o manual, inicia a busca em intervalos LAN comuns. Essa operação não foi executada pelo projeto.

## Captura passiva e intervalo explícito

As receitas abaixo **capturam tráfego ou enviam solicitações ARP**; não foram executadas. Defina os parâmetros da interface e do intervalo antes de usá-las:

```bash
# Bash · diretório atual · Kali Linux/WSL · interface e permissões de captura
netdiscover -i "${INTERFACE:?Defina INTERFACE}" -p
```

```bash
# Bash · diretório atual · Kali Linux/WSL · interface, intervalo e permissões de rede
netdiscover -i "${INTERFACE:?Defina INTERFACE}" -r "${RANGE:?Defina RANGE como rede/CIDR}"
netdiscover -i "${INTERFACE:?Defina INTERFACE}" -r "${RANGE:?Defina RANGE como rede/CIDR}" -P -N
```

O manual descreve `-p` como captura sem envio. `-P` produz saída não interativa e encerra após a varredura; `-L` continua capturando depois da etapa ativa. A presença da ajuda no WSL não comprova acesso Ethernet ou capacidade de captura naquela interface.

## Opções principais

| Opção | Função |
|---|---|
| `-i device` | Interface para captura/injeção |
| `-r range` / `-l file` | Intervalo explícito / arquivo com um intervalo por linha |
| `-p` | Modo passivo |
| `-m file` | Lista de MACs e nomes conhecidos |
| `-F filter` | Filtro pcap; padrão documentado `arp` |
| `-s time` | Espera entre solicitações, em milissegundos; padrão 1 |
| `-c count` | Repetições de cada solicitação; padrão 1 |
| `-n node` | Último octeto do IP de origem; padrão 67, permitido 2–253 |
| `-d` | Ignorar arquivos pessoais nos modos automático/rápido |
| `-f` | Varredura rápida |
| `-P` / `-L` / `-N` | Saída não interativa / continuar captura / sem cabeçalho |
| `-R` | Presumir as capacidades necessárias sem checá-las |
| `-S` | Opção obsoleta de supressão das esperas; detalhes no manual |

As nove teclas de controle/visualização estão em tabelas traduzidas no manual. Os caracteres das teclas foram preservados.

## Configuração e divergência do original

- `~/.netdiscover/ranges`: intervalos do modo automático, um por linha.
- `~/.netdiscover/fastips`: últimos octetos do modo rápido, um por linha.

O original informa **.1, .100 e .254** em `-f`, mas **1,100,154** na descrição de `fastips`. Ambos foram preservados e a divergência está sinalizada. Nenhuma varredura foi feita para decidir qual comportamento ocorre.

## Reproduzir somente a conferência local

Na raiz do repositório:

```bash
# Bash · raiz do repositório · Kali Linux/WSL · Python 3 e netdiscover instalados
python3 scripts/test_network_help.py --binary netdiscover
```

Sem `--record`, não regrava evidências congeladas. O teste usa apenas `-h` e metadados dpkg, comparando a identidade do manual e verificando o diretório temporário.

## Procedência

[Original preservado](../../../sources/upstream/netdiscover/netdiscover.8.source) · [copyright integral](../../99-Assets/upstream/netdiscover/COPYRIGHT.package.txt) · [GPL-3](../../99-Assets/upstream/netdiscover/LICENSE.txt).

Manual e esta folha derivada: **GPL-3.0-or-later**. As licenças diferentes de scripts auxiliares no pacote não foram aplicadas automaticamente ao manual. Revisão humana independente: pendente.
