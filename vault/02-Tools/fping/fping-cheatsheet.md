---
title: "fping — cheatsheet"
type: "cheatsheet"
tool: "fping"
binary: "fping"
status: "source-checked"
reviewed: "2026-10-26"
language: "pt-BR"
tags: ["cheatsheet", "tool/fping", "category/network"]
cssclasses: ["fieldbook"]
test_status: "help-only"
tested_package_version: "fping 5.1-1"
license_spdx: "LicenseRef-Fping-Stanford-Variant"
---

# fping — cheatsheet

> **Reconhecimento da licença:** This software was developed by Stanford University.

[Manual principal em português](fping-fping-8.md) · [Página de compatibilidade fping6](fping-fping6-8.md) · [Evidência do fping](../../99-Assets/evidence/fping-help-tests.json) · [Evidência do link fping6](../../99-Assets/evidence/fping6-help-tests.json).

## Ajuda e versão — conferidas sem alvos

```bash
# Bash · diretório atual · Kali Linux/WSL · pacote fping instalado
fping -h
fping -v
```

Ambos retornaram código 0; o programa informou **5.1**, no pacote **5.1-1**. `-h` funcionou, embora a própria saída não enumere `-h`, `--help` nem a opção antiga `-T`. Ausência na listagem não prova que uma opção é rejeitada; o manual descreve `-T` como ignorada por compatibilidade.

## Contagem limitada e coleta de tempos

As receitas abaixo **enviam ICMP** e não foram executadas pelo projeto:

```bash
# Bash · diretório atual · Kali Linux/WSL · fping e TARGET definido
fping -c 3 "${TARGET:?Defina TARGET}"
fping -C 5 -q "${TARGET:?Defina TARGET}"
```

`-c` mostra respostas e estatísticas; `-C` fornece um formato para coleta automatizada. No exemplo preservado do manual, `-` indica ausência de resposta. Os tempos e respostas históricos não são resultados desta máquina.

## Vários alvos e arquivo

```bash
# Bash · diretório atual · Kali Linux/WSL · fping e arquivo TARGETS_FILE definido
fping < "${TARGETS_FILE:?Defina TARGETS_FILE}"
```

O manual descreve também `-f` para arquivos e registra uma restrição histórica a root para essa opção. Ela não foi testada operacionalmente nem removida da tradução.

Para gerar alvos de uma rede explícita:

```bash
# Bash · diretório atual · Kali Linux/WSL · fping e RANGE definido
fping -g "${RANGE:?Defina RANGE como rede/CIDR}"
```

O manual informa exclusão dos endereços de rede e broadcast quando uma rede/máscara é fornecida.

## Parâmetros essenciais

| Opção | Função / unidade |
|---|---|
| `-4` / `-6` | Restringir a IPv4 / IPv6 |
| `-a` / `-u` | Mostrar acessíveis / inacessíveis |
| `-A` / `-n` / `-d` | Endereços / nomes por DNS reverso / forçar DNS reverso |
| `-i MSEC` | Intervalo mínimo entre pacotes para quaisquer alvos, em ms |
| `-p MSEC` | Intervalo entre pacotes do mesmo alvo, em ms |
| `-t MSEC` / `-B N` | Timeout inicial / fator de backoff |
| `-r N` | Novas tentativas, sem contar a primeira |
| `-q` / `-Q SECS` | Resumo final / resumos periódicos em segundos |
| `-I IFACE` / `-S addr` | Interface / endereço de origem |
| `-l` | Repetição indefinida, interrompida por Ctrl-C |

Os padrões, limites, opções adicionais e distinções entre modos estão no manual completo. Em particular, não confunda os milissegundos de `-i`, `-p` e `-t` com os segundos de `-Q`.

## Códigos de saída documentados

| Código | Significado segundo o manual |
|---|---|
| 0 | Todos os hosts acessíveis |
| 1 | Alguns hosts inacessíveis |
| 2 | Algum endereço IP não encontrado |
| 3 | Argumentos inválidos |
| 4 | Falha de chamada de sistema |

Esses resultados de sondagem não foram exercitados; o código 0 observado aqui pertence às chamadas de ajuda/versão.

## fping6: compatibilidade, não outro manual de opções

Nesta instalação, `/usr/bin/fping6` é um link simbólico para `fping` e resolve ao mesmo executável. Sua página própria explica a compatibilidade de configurações Smokeping. Ela foi traduzida separadamente, sem tratar a ausência de opções nessa página como omissão do manual principal.

A existência do link não valida envio IPv6 no WSL. Nenhuma sondagem IPv4/IPv6 foi solicitada pelo teste.

## Reproduzir somente a conferência local

Na raiz do repositório:

```bash
# Bash · raiz do repositório · Kali Linux/WSL · Python 3 e fping instalados
python3 scripts/test_network_help.py --binary fping
python3 scripts/test_network_help.py --binary fping6
```

## Procedência e licença específica

[Original fping](../../../sources/upstream/fping/fping.8.source) · [Original fping6](../../../sources/upstream/fping/fping6.8.source) · [Copyright e condições integrais](../../99-Assets/upstream/fping/COPYRIGHT.package.txt) · [Variante retida](../../99-Assets/upstream/fping/LICENSE.txt).

Não se atribuiu BSD-3-Clause padrão nem GPL a esta fonte. Foi usado **LicenseRef-Fping-Stanford-Variant**, preservando a redação original, o reconhecimento a Stanford e a condição de não endosso. Esta folha derivada mantém as condições da fonte. Revisão humana independente: pendente.
