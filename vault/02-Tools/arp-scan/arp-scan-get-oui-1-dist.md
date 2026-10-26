---
title: "get-oui — manual de referência"
type: "official-documentation"
tool: "arp-scan"
status: "source-checked"
reviewed: "2026-10-26"
language: "pt-BR"
tags: ["documentation", "tool/arp-scan"]
cssclasses: ["fieldbook"]
source_url: "https://github.com/royhills/arp-scan/blob/a0466d5fc7fa8a1e5625b7aae568ffb384e3f5a5/get-oui.1.dist"
source_commit: "a0466d5fc7fa8a1e5625b7aae568ffb384e3f5a5"
source_sha256: "88cd4df36ba67aadfe42d7b2774aeada2b5984c763372f5aa71987bd02c776a7"
license_spdx: "LicenseRef-Get-OUI-Manpage"
human_review: "pending"
source_scope: "Pinned README plus full arp-scan, arp-fingerprint and get-oui manpages, with individual copying notices. Wiki and other sources remain a separate coverage review; IEEE data files are not mirrored by this acquisition."
binary: "get-oui"
source_manual_date: "October 28, 2022"
manual_section: "1"
test_status: "help-only"
tested_version: "arp-scan 1.10.0"
---

> Tradução para português produzida por assistente de IA e conferida seção por seção contra a fonte. Revisão humana independente: pendente. Opções e exemplos originais foram preservados; nenhum exemplo foi executado automaticamente.

> **Compatibilidade observada:** arp-scan 1.10.0. As opções do manual foram encontradas na ajuda instalada. A fonte fixada foi mantida sem trocar opções silenciosamente. Conferidas somente get-oui -h e a versão do pacote arp-scan; nenhuma atualização IEEE foi solicitada. [Evidência e limites do teste](../../99-Assets/evidence/get-oui-help-tests.json).

<!-- SPDX-License-Identifier: LicenseRef-Get-OUI-Manpage -->
<!-- Full translation by an AI assistant; independent human review pending. -->
# get-oui

<a id="name"></a>
## NOME

get-oui — obtém do site da IEEE o arquivo OUI usado pelo arp-scan.

<a id="synopsis"></a>
## SINOPSE

```text
get-oui [options]
```

<a id="description"></a>
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

<a id="options"></a>
## OPÇÕES

### `-h`

Exibe uma breve mensagem de uso e encerra.

### `-f <fn>`

Grava a saída no arquivo especificado em vez do padrão `ieee-oui.txt`.

### `-v`

Exibe mensagens detalhadas de progresso.

<a id="files"></a>
## ARQUIVOS

### `ieee-oui.txt`

Arquivo de saída padrão.

<a id="examples"></a>
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

<a id="notes"></a>
## NOTAS

O `get-oui` é implementado em Perl. O interpretador Perl precisa estar instalado no sistema para executar a ferramenta.

O `get-oui` usa os módulos Perl `LWP::UserAgent` e `Text::CSV` para obter e processar os registros IEEE. Esses módulos precisam estar instalados. Eles estão disponíveis na maioria das distribuições, normalmente nos pacotes `libwww-perl` e `libtext-csv-perl`, e também podem ser obtidos como código-fonte no CPAN.

Para usar um servidor proxy, defina a variável de ambiente `http_proxy`.

<a id="see-also"></a>
## VEJA TAMBÉM

### `arp-scan`(1)

### `arp-fingerprint`(1)

<a id="original-license-notice"></a>
## Aviso de licença original

```text
.\" Copyright (C) Roy Hills
.\"
.\" Copying and distribution of this file, with or without modification,
.\" are permitted in any medium without royalty provided the copyright
.\" notice and this notice are preserved.
.\"
```


---

## Procedência desta tradução

Fonte: [https://github.com/royhills/arp-scan](https://github.com/royhills/arp-scan/blob/a0466d5fc7fa8a1e5625b7aae568ffb384e3f5a5/get-oui.1.dist). Licença: [LicenseRef-Get-OUI-Manpage](../../99-Assets/upstream/arp-scan/LICENSE.get-oui-manpage.txt). Commit: a0466d5fc7fa8a1e5625b7aae568ffb384e3f5a5.

O original preservado, a lista de mudanças de apresentação e os hashes constam no manifesto do projeto. Nenhum exemplo desta documentação foi executado automaticamente.
