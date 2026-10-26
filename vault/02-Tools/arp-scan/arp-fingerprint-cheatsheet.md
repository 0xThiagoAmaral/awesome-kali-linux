---
title: "arp-fingerprint — cheatsheet"
type: "cheatsheet"
tool: "arp-scan"
binary: "arp-fingerprint"
status: "source-checked"
reviewed: "2026-10-26"
language: "pt-BR"
tags: ["cheatsheet", "tool/arp-scan", "category/network"]
cssclasses: ["fieldbook"]
test_status: "help-only"
tested_package_version: "arp-scan 1.10.0"
---

# arp-fingerprint — cheatsheet

[Manual completo em português](arp-scan-arp-fingerprint-1.md) · [README do pacote](arp-scan-documentacao.md) · [Evidência da ajuda instalada](../../99-Assets/evidence/arp-scan-local-tests.json).

## Ajuda e identificação do pacote

```bash
# Bash · diretório atual · Kali Linux/WSL · pacote arp-scan instalado
arp-fingerprint -h
arp-scan --version
```

Ambos os comandos retornaram código 0. A versão observada foi **arp-scan 1.10.0**; a ajuda de `arp-fingerprint` não fornece uma versão própria.

## Um único host

Defina `TARGET` como um único endereço IP ou nome de host. A ferramenta não aceita listas, redes ou intervalos nessa posição.

```bash
# Bash · diretório atual · Kali Linux/WSL · arp-fingerprint
arp-fingerprint "${TARGET:?Defina TARGET como um único IP ou nome de host}"
```

## Interface específica, sem resolução DNS

```bash
# Bash · diretório atual · Kali Linux/WSL · arp-fingerprint
arp-fingerprint -o "-N -I ${INTERFACE:?Defina INTERFACE}" \
  "${TARGET:?Defina TARGET como um único endereço IP}"
```

`-o` repassa a cadeia de opções ao `arp-scan`. As aspas mantêm `-N -I INTERFACE` em um único argumento; `-N` desativa consultas DNS e `-I` escolhe a interface.

## Opções para consulta rápida

| Opção | Significado no manual fixado | Conferência local |
|---|---|---|
| `-h` | Exibir a ajuda e encerrar | Executada, código 0 |
| `-v` | Mensagens detalhadas de progresso | Listada na ajuda; operação não executada |
| `-o <option-string>` | Repassar opções ao arp-scan | Listada na ajuda; operação não executada |
| `-l` | Identificar todos os hosts da rede local | Listada na ajuda; operação não executada |
| `-m` | Incluir o endereço MAC na saída | Presente no manual, mas não listada na ajuda instalada |

As receitas com alvos acima são modelos derivados da documentação, não testes de rede realizados pelo projeto. A ausência de `-m` na ajuda não foi tratada como prova de que a implementação rejeita a opção.

## Interpretar o resultado

Cada posição da cadeia representa uma modalidade de requisição ARP: `1` indica resposta e `0` indica ausência de resposta. A cadeia é comparada com as referências conhecidas para sugerir um sistema operacional.

A correspondência não é uma identificação conclusiva: sistemas diferentes podem compartilhar a mesma cadeia, e a configuração de rede pode alterar o resultado. Os comandos e as saídas históricas originais foram preservados no manual.

## Reproduzir somente a conferência de ajuda

Na raiz do repositório:

```bash
# Bash · raiz do repositório · Kali Linux/WSL · Python 3 e arp-scan instalados
python3 scripts/test_arp_fingerprint_help.py
```

O script executa somente `arp-fingerprint -h` e `arp-scan --version`. Não fornece alvos, não solicita `-l` e não altera as evidências congeladas por padrão.

## Procedência e licença

Fonte: [arp-fingerprint.1 no commit fixado](https://github.com/royhills/arp-scan/blob/a0466d5fc7fa8a1e5625b7aae568ffb384e3f5a5/arp-fingerprint.1). O manual possui [aviso próprio de copyright e cópia](../../99-Assets/upstream/arp-scan/LICENSE.arp-fingerprint-manpage.txt), preservado integralmente. Não se atribuiu automaticamente a ele a licença GPL geral do repositório.
