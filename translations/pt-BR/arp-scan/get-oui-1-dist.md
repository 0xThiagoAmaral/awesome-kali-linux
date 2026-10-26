<!-- SPDX-License-Identifier: LicenseRef-Get-OUI-Manpage -->
<!-- Full translation by an AI assistant; independent human review pending. -->
# get-oui

## NOME

get-oui — obtém do site da IEEE o arquivo OUI usado pelo arp-scan.

## SINOPSE

```text
get-oui [options]
```

## DESCRIÇÃO

O `get-oui` obtém os registros de associação MAC/fabricante do site da IEEE e os converte para o formato usado pelo arp-scan. São baixados e processados os seguintes registros:

| Registro | Tamanho do prefixo | Descrição |
|---|---|---|
| `MA-L` | `24-bit` | Registro OUI original |
| `MA-M` | `28-bit` | Registro de blocos de endereços médios |
| `MA-S` | `36-bit` | Registro de blocos de endereços pequenos, OUI-36 |
| `IAB` | `36-bit` | Registro IAB, fechado para novas solicitações |

O script cria `ieee-oui.txt` a partir dos dados mais recentes disponíveis no site da IEEE. Execute `get-oui` periodicamente para manter esse arquivo atualizado.

Os dados OUI são obtidos das URLs definidas no script `get-oui`. Por padrão, a saída é gravada em `ieee-oui.txt` no diretório atual. O nome do arquivo pode ser alterado com `-f`.

O `arp-scan` usa o arquivo `ieee-oui.txt` produzido pelo script para identificar o fabricante de uma placa Ethernet a partir de seu endereço de hardware.

Primeiro, o `arp-scan` procura `ieee-oui.txt` no diretório atual. Se não o encontrar, usa o arquivo global do sistema, `@PKGDATADIR@/ieee-oui.txt`.

## OPÇÕES

### `-h`

Exibe uma breve mensagem de uso e encerra.

### `-f <fn>`

Grava a saída no arquivo especificado em vez do padrão `ieee-oui.txt`.

### `-v`

Exibe mensagens detalhadas de progresso.

## ARQUIVOS

### `ieee-oui.txt`

Arquivo de saída padrão.

## EXEMPLOS

```text
$ ./get-oui -v
Renaming ieee-oui.txt to ieee-oui.txt.bak
Opening ieee-oui.txt for output
Processing IEEE IAB registry data from https://standards-oui.ieee.org/iab/iab.csv
        Downloaded 381454 bytes
        4575 IAB entries written to ieee-oui.txt
Processing IEEE MAM registry data from https://standards-oui.ieee.org/oui28/mam.csv
        Downloaded 492756 bytes
        4477 MAM entries written to ieee-oui.txt
Processing IEEE OUI registry data from https://standards-oui.ieee.org/oui/oui.csv
        Downloaded 3051812 bytes
        32845 OUI entries written to ieee-oui.txt
Processing IEEE OUI36 registry data from https://standards-oui.ieee.org/oui36/oui36.csv
        Downloaded 466151 bytes
        5131 OUI36 entries written to ieee-oui.txt

Total of 47028 MAC/Vendor mappings written to ieee-oui.txt
```

## NOTAS

O `get-oui` é implementado em Perl. O interpretador Perl precisa estar instalado no sistema para executar a ferramenta.

O `get-oui` usa os módulos Perl `LWP::UserAgent` e `Text::CSV` para obter e processar os registros IEEE. Esses módulos precisam estar instalados. Eles estão disponíveis na maioria das distribuições, normalmente nos pacotes `libwww-perl` e `libtext-csv-perl`, e também podem ser obtidos como código-fonte no CPAN.

Para usar um servidor proxy, defina a variável de ambiente `http_proxy`.

## VEJA TAMBÉM

### `arp-scan`(1)

### `arp-fingerprint`(1)

## Aviso de licença original

```text
.\" Copyright (C) Roy Hills
.\"
.\" Copying and distribution of this file, with or without modification,
.\" are permitted in any medium without royalty provided the copyright
.\" notice and this notice are preserved.
.\"
```
