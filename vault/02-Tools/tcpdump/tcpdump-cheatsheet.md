---
title: "tcpdump — cheatsheet offline"
type: "cheatsheet"
tool: "tcpdump"
binary: "tcpdump"
status: "source-checked"
reviewed: "2026-10-26"
language: "pt-BR"
tags: ["cheatsheet", "tool/tcpdump", "category/network", "offline"]
cssclasses: ["fieldbook"]
test_status: "offline-fixture"
tested_package_version: "tcpdump 4.99.6-2"
license_spdx: "LicenseRef-Tcpdump-Manpage"
---

# tcpdump — cheatsheet offline

> **Reconhecimento da licença:** This product includes software developed by the University of California, Lawrence Berkeley Laboratory and its contributors.

[Manual integral em português](tcpdump-tcpdump-8.md) · [PCAP sintético de exemplo](../../99-Assets/fixtures/tcpdump-demo.pcap) · [Evidência literal dos testes](../../99-Assets/evidence/tcpdump-local-tests.json).

O manual completo inclui protocolos e exemplos; sua primeira tradução é **automática local, ainda sem revisão editorial integral**. Esta folha complementar foi confrontada com os comandos do teste offline. Não confunda esse teste limitado com validação de todas as opções.

## Ler sem abrir uma interface

Execute **na raiz do repositório**:

```bash
# Bash · raiz do repositório · Kali Linux/WSL · tcpdump instalado
PCAP='vault/99-Assets/fixtures/tcpdump-demo.pcap'
tcpdump -nn -tt -r "$PCAP"
```

Saída observada para esse arquivo sintético:

```text
1700000000.000000 ARP, Request who-has 192.0.2.1 tell 192.0.2.10, length 28
1700000001.000000 IP 192.0.2.10.12345 > 198.51.100.20.80: Flags [S], seq 1, win 64240, length 0
1700000002.000000 IP 192.0.2.10.53000 > 198.51.100.53.53: 4660+ A? example.invalid. (33)
```

O arquivo tem **243 bytes e três pacotes construídos pelo script**: ARP, TCP SYN e UDP com uma consulta DNS codificada. Eles nunca foram transmitidos. Não é uma captura de tráfego pessoal. A mensagem `reading from file...` foi emitida em stderr; a saída acima é stdout.

- `-r`: ler um arquivo, em vez de capturar de uma interface.
- `-nn`: manter endereços e portas numéricos.
- `-tt`: timestamp numérico absoluto, usado para uma saída reproduzível.

## Filtros e contagens realmente conferidos

```bash
# Bash · raiz do repositório · Kali Linux/WSL · tcpdump e PCAP definido
tcpdump -nn --count -r "$PCAP" 'tcp port 80'
tcpdump -nn --count -r "$PCAP" 'udp port 53'
tcpdump -nn --count -r "$PCAP" 'arp'
tcpdump -nn --count -r "$PCAP" 'ip'
tcpdump -nn --count -r "$PCAP" '(tcp or udp) and port 53'
tcpdump -nn --count -r "$PCAP" 'not ip'
```

| Filtro | Quantidade observada |
|---|---|
| `tcp port 80` | 1 |
| `udp port 53` | 1 |
| `arp` | 1 |
| `ip` | 2 |
| `(tcp or udp) and port 53` | 1 |
| `not ip` | 1 |

Por exemplo, a primeira chamada produziu literalmente `1 packet`; `ip` produziu `2 packets`. Todos esses comandos terminaram com código 0.

As aspas protegem a expressão contra interpretação pelo shell. A gramática integral também é referenciada pelo manual em `pcap-filter(7)`; essa página externa ainda não faz parte desta importação.

## Gravar uma cópia filtrada

Escolha um arquivo de saída novo. Esta operação **grava no disco**; o teste fez isso somente no seu diretório temporário:

```bash
# Bash · raiz do repositório · Kali Linux/WSL · tcpdump, PCAP e OUTPUT definidos
test ! -e "${OUTPUT:?Defina OUTPUT como um arquivo novo}" &&
  tcpdump -nn -r "$PCAP" -w "$OUTPUT" 'tcp'
tcpdump -nn --count -r "$OUTPUT"
```

No teste, a cópia filtrada continha um pacote. O arquivo de entrada permaneceu byte a byte inalterado. O comando `-w` grava pacotes, não um relatório de texto.

## Inspecionar a compilação e um erro esperado

```bash
# Bash · raiz do repositório · Kali Linux/WSL · tcpdump e PCAP definido
tcpdump -nn -d -r "$PCAP" 'tcp'
tcpdump -nn -r "$PCAP" 'tcp and ('
```

A primeira chamada mostrou o filtro compilado. A segunda terminou com **código 1**, stdout vazio e a mensagem:

```text
tcpdump: can't parse filter expression: syntax error
```

Esse erro foi solicitado intencionalmente. As evidências preservam também a linha anterior de stderr com o nome do arquivo, sem esconder o código não zero.

## Opções de leitura frequentes

| Opção | Função descrita no manual |
|---|---|
| `-r file` / `-V file` | Ler uma captura / uma lista de arquivos |
| `--count` | Contar pacotes correspondentes ao filtro |
| `-c count` | Limitar o número de pacotes processados |
| `-n` / `-nn` | Nomes e serviços numéricos |
| `-e` | Mostrar cabeçalho de enlace |
| `-v` / `-vv` / `-vvv` | Mais detalhes de decodificação |
| `-A` | Conteúdo ASCII |
| `-x` / `-X` | Hexadecimal / hexadecimal e ASCII |
| `-w file` | Gravar pacotes no arquivo de saída |

As opções dessa tabela que não constam dos comandos exercitados acima continuam **não testadas operacionalmente**. Captura ao vivo, privilégios, rotação, decriptação e protocolos adicionais estão no manual; nenhum exemplo histórico foi executado automaticamente.

## Reproduzir o teste sem internet

Na raiz do repositório:

```bash
# Bash · raiz do repositório · Kali Linux/WSL · Python 3 e tcpdump instalados
python3 scripts/test_tcpdump_offline.py
```

O script gera seu próprio PCAP temporário, usa somente leitura com `-r`, verifica os filtros e grava uma cópia controlada. Não enumera interfaces, não abre captura ao vivo e não solicita envio. Sem `--record`, as evidências congeladas não são reescritas.

SHA-256 do PCAP de exemplo: `7005a7c9eb01b607624f745519e81e5df52147d1d3f9e8c59e4ba57a8bb157c9`.

## Procedência

[Original preservado](../../../sources/upstream/tcpdump/tcpdump.8.source) · [aviso específico do manual](../../99-Assets/upstream/tcpdump/LICENSE.txt) · [copyright integral do pacote](../../99-Assets/upstream/tcpdump/COPYRIGHT.package.txt).

Foi usada **LicenseRef-Tcpdump-Manpage**, com o aviso histórico integral e seu reconhecimento exigido, sem substituir silenciosamente as condições por uma licença BSD genérica. Esta folha derivada mantém as condições da fonte. O PCAP é um fixture sintético autoral, gerado pelo script MIT do projeto.
