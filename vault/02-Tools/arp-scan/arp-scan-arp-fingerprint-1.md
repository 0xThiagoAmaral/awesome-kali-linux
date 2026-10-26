---
title: "arp-fingerprint — manual de referência"
type: "official-documentation"
tool: "arp-scan"
status: "source-checked"
reviewed: "2026-10-26"
language: "pt-BR"
tags: ["documentation", "tool/arp-scan"]
cssclasses: ["fieldbook"]
source_url: "https://github.com/royhills/arp-scan/blob/a0466d5fc7fa8a1e5625b7aae568ffb384e3f5a5/arp-fingerprint.1"
source_commit: "a0466d5fc7fa8a1e5625b7aae568ffb384e3f5a5"
source_sha256: "2025a1f2ac8280a267f215816f9a9eac8ddb9698871f73d2fbd61ce40c6d5916"
license_spdx: "LicenseRef-ARP-Fingerprint-Manpage"
human_review: "pending"
source_scope: "Pinned README plus complete arp-fingerprint.1 and main arp-scan.1.dist manuals, each with its own preserved copying notice. Wiki, additional utilities and remaining sources still require coverage review."
binary: "arp-fingerprint"
source_manual_date: "January 07, 2023"
manual_section: "1"
test_status: "help-only"
tested_version: "arp-scan 1.10.0"
---

> Tradução para português produzida por assistente de IA e conferida seção por seção contra a fonte. Revisão humana independente: pendente. Opções e exemplos originais foram preservados; nenhum exemplo foi executado automaticamente.

> **Compatibilidade observada:** arp-scan 1.10.0. A ajuda dessa instalação não lista `-m`. A fonte fixada foi mantida sem trocar opções silenciosamente. Conferidas somente a ajuda do arp-fingerprint e a versão do pacote arp-scan; nenhum alvo foi informado e a opção -l não foi executada. [Evidência e limites do teste](../../99-Assets/evidence/arp-scan-local-tests.json).

<!-- SPDX-License-Identifier: LicenseRef-ARP-Fingerprint-Manpage -->
<!-- Source: arp-fingerprint.1 at a0466d5fc7fa8a1e5625b7aae568ffb384e3f5a5. -->
<!-- Translation by an AI assistant; independent human review remains pending. -->
# arp-fingerprint

<a id="name"></a>
## NOME

arp-fingerprint — identifica a impressão digital de um sistema usando ARP.

<a id="synopsis"></a>
## SINOPSE

```text
arp-fingerprint [options] target
```

O alvo deve ser um único endereço IP ou nome de host. Não é possível especificar vários alvos, redes IP ou intervalos de endereços.

Se o alvo for informado como endereço IP, a opção `-o` permite repassar `--numeric` ao `arp-scan`, impedindo tentativas de resolução DNS. Isso pode acelerar o processo de identificação, especialmente em sistemas com uma configuração DNS lenta ou defeituosa.

<a id="description"></a>
## DESCRIÇÃO

O `arp-fingerprint` identifica características do host de destino usando o protocolo ARP.

Ele envia diferentes tipos de requisições ARP ao alvo e registra a quais tipos o sistema responde. A partir disso, constrói uma cadeia de identificação: "1" indica resposta do alvo e "0" indica ausência de resposta. Um exemplo dessa cadeia é `01000100000`. Essa impressão digital é então usada para procurar o sistema operacional mais provável.

Vários sistemas operacionais compartilham muitas dessas cadeias, portanto nem sempre existe uma correspondência única entre a impressão digital e um sistema operacional. Uma correspondência com determinado sistema, ou com uma lista de sistemas, também não comprova que o alvo execute um deles, embora isso seja bastante provável. A lista de sistemas não é exaustiva: contém apenas os identificados pelo autor até a data da documentação, e certamente há sistemas não listados.

A impressão digital ARP de um sistema normalmente depende de seu kernel. Embora o processamento de ARP possa ser implementado em espaço de usuário, isso quase nunca ocorre.

Um mesmo sistema operacional pode produzir impressões digitais diferentes conforme sua configuração. Por exemplo, o Linux responde a um endereço IP de origem não local se esse endereço tiver uma rota pela interface que está sendo testada. Isso tem dois efeitos: torna a identificação mais complexa, mas também pode revelar aspectos da configuração do sistema.

O compartilhamento de uma mesma impressão digital ARP entre sistemas operacionais diferentes às vezes indica reutilização de código de rede. Windows NT e FreeBSD são um exemplo citado pela fonte.

O `arp-fingerprint` usa o `arp-scan` para enviar as requisições ARP e receber as respostas.

Existem outros métodos de identificação com `arp-scan` que podem complementar o `arp-fingerprint`. Eles não estão incluídos nessa ferramenta porque podem causar interrupções no sistema de destino ou porque exigem conhecimento de sua configuração que nem sempre está disponível.

A maioria das requisições ARP enviadas pelo `arp-fingerprint` não é padronizada. Por isso, elas podem afetar sistemas cuja pilha TCP/IP não seja robusta.

<a id="options"></a>
## OPÇÕES

### `-h`

Exibe uma breve mensagem de uso e encerra.

### `-v`

Exibe mensagens detalhadas de progresso.

### `-o <option-string>`

Repassa as opções especificadas ao arp-scan. Coloque a cadeia entre aspas se ela contiver espaços, como em `-o "-I eth1"`. As opções mais usadas são `--interface` (`-I`) e `--numeric` (`-N`).

### `-l`

Identifica todos os hosts da rede local. Quando esta opção é usada, não é necessário informar hosts de destino.

### `-m`

Inclui o endereço MAC do alvo na saída.

<a id="examples"></a>
## EXEMPLOS

```text
$ arp-fingerprint 192.168.0.1
192.168.0.1   01000100000     Linux 2.2, 2.4, 2.6
```

```text
$ arp-fingerprint -o "-N -I eth1" 192.168.0.202
192.168.0.202 11110100000     FreeBSD 5.3, Win98, WinME, NT4, 2000, XP, 2003
```

<a id="notes"></a>
## NOTAS

O `arp-fingerprint` é implementado em Perl. O interpretador Perl precisa estar instalado no sistema para executar a ferramenta.

<a id="see-also"></a>
## VEJA TAMBÉM

### `arp-scan`(1)

<https://github.com/royhills/arp-scan/wiki> — wiki do arp-scan.

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

Fonte: [https://github.com/royhills/arp-scan](https://github.com/royhills/arp-scan/blob/a0466d5fc7fa8a1e5625b7aae568ffb384e3f5a5/arp-fingerprint.1). Licença: [LicenseRef-ARP-Fingerprint-Manpage](../../99-Assets/upstream/arp-scan/LICENSE.arp-fingerprint-manpage.txt). Commit: a0466d5fc7fa8a1e5625b7aae568ffb384e3f5a5.

O original preservado, a lista de mudanças de apresentação e os hashes constam no manifesto do projeto. Nenhum exemplo desta documentação foi executado automaticamente.
