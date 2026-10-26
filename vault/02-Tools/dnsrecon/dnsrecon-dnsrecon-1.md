---
title: "dnsrecon — manual de referência"
type: "official-documentation"
tool: "dnsrecon"
status: "source-checked"
reviewed: "2026-10-26"
language: "pt-BR"
tags: ["documentation", "tool/dnsrecon"]
cssclasses: ["fieldbook"]
source_url: "https://github.com/darkoperator/dnsrecon"
source_kind: "installed-kali-package"
package: "dnsrecon"
binary_version: "1.3.1-3"
source_package: "dnsrecon"
source_version: "1.3.1-3"
source_snapshot_sha256: "a7fbb986c2276a7e8503fa5a804c20ccf2b13619b29b942442ebda75cfcbf625"
source_sha256: "e57945a2a52ccca3d4200b41cfca13cbfb024ead0413ba373306211e1af00430"
license_spdx: "GPL-2.0-only"
human_review: "pending"
source_scope: "Complete installed English dnsrecon(1) manual only; upstream README, websites and additional documentation remain separate pending coverage"
binary: "dnsrecon"
source_manual_date: null
manual_section: "1"
test_status: "help-only"
tested_version: "dnsrecon 1.3.1-3"
---

> Tradução para português produzida por assistente de IA e conferida seção por seção contra a fonte. Revisão humana independente: pendente. Opções e exemplos originais foram preservados; nenhum exemplo foi executado automaticamente.

> **Compatibilidade observada:** dnsrecon 1.3.1-3. As opções do manual foram encontradas na ajuda instalada. Ela lista `--disable_check_nxdomain`, `--input-list`, `--loglevel`, `--verbose`, `--version`, `-iL`, ausente deste manual. A fonte fixada foi mantida sem trocar opções silenciosamente. Conferidas somente as duas formas de ajuda, versão do pacote e dnsrecon -V. Nenhum domínio, endereço, servidor DNS ou alvo foi fornecido; nenhuma consulta de enumeração foi solicitada. [Evidência e limites do teste](../../99-Assets/evidence/dnsrecon-help-tests.json).

<!-- SPDX-License-Identifier: GPL-2.0-only -->
# dnsrecon

<a id="name"></a>
## NOME

dnsrecon - ferramenta de enumeração e varredura DNS

<a id="synopsis"></a>
## SINOPSE

```text
dnsrecon [-h] [-d DOMAIN] [-n NS_SERVER] [-r RANGE] [-D DICTIONARY] [-f] [-a] [-s] [-b] [-k] [-w] [-z] [-y] [--threads THREADS] [--lifetime LIFETIME] [--tcp] [--db DB] [-x XML] [-c CSV] [-j JSON] [--iw] [--disable_check_recursion] [--disable_check_bindversion] [-v] [-V] [-t TYPE]
```

<a id="description"></a>
## DESCRIÇÃO

dsnrecon é um script Python simples que permite reunir informações relacionadas a DNS sobre um alvo especificado.

> **Nota editorial:** o original escreve "dsnrecon" nesta frase; o nome do programa, nas opções e na sinopse, é `dnsrecon`. A grafia da frase de origem foi mantida.

<a id="options"></a>
## OPÇÕES

### `-h, --help`

Mostra a mensagem de ajuda e encerra.

### `-d DOMAIN, --domain DOMAIN`

Domínio-alvo.

### `-n NS_SERVER, --name_server NS_SERVER`

Servidor de domínio a utilizar. Se nenhum for fornecido, será usado o SOA do alvo. Vários servidores podem ser especificados em uma lista separada por vírgulas.

### `-r RANGE, --range RANGE`

Intervalo de IPs para força bruta de consultas reversas, nos formatos (primeiro-último) ou (intervalo/máscara em bits).

### `-D DICTIONARY, --dictionary DICTIONARY`

Arquivo de dicionário de subdomínios e nomes de hosts a usar na força bruta. Ao salvar registros, filtra da consulta de domínio por força bruta os registros que resolvam para o endereço IP definido pelo wildcard.

### `-f`

Ao salvar registros, filtra da consulta de domínio por força bruta os registros que resolvam para o endereço IP definido pelo wildcard.

### `-a`

Executa AXFR junto com a enumeração padrão.

### `-b`

Executa enumeração pelo Bing junto com a enumeração padrão.

### `-s`

Executa consultas reversas dos intervalos IPv4 presentes no registro SPF junto com a enumeração padrão.

### `-y`

Executa enumeração pelo Yandex junto com a enumeração padrão.

### `-k`

Executa enumeração pelo crt.sh junto com a enumeração padrão.

### `-w`

Executa análise aprofundada dos registros whois e consulta reversa dos intervalos IP encontrados pelo Whois durante uma enumeração padrão.

### `-z`

Executa uma caminhada de zona DNSSEC junto com a enumeração padrão.

### `--threads THREADS`

Número de threads a usar em consultas reversas, consultas diretas, força bruta e enumeração de registros SRV.

### `--lifetime LIFETIME`

Tempo de espera pela resposta de um servidor a uma consulta. O padrão é 3.

### `--tcp`

Usa o protocolo TCP para executar consultas.

### `--db DB`

Arquivo SQLite 3 para salvar os registros encontrados.

### `-x XML, --xml XML`

Arquivo XML para salvar os registros encontrados.

### `-c CSV, --csv CSV`

Arquivo de valores separados por vírgulas.

### `-j JSON, --json JSON`

Arquivo JSON.

### `--iw`

Continua a força bruta de um domínio mesmo quando registros wildcard são descobertos.

### `--disable_check_recursion`

Desativa a verificação de recursão nos servidores de nomes.

### `--disable_check_bindversion`

Desativa a verificação da versão do BIND nos servidores de nomes.

### `-v`

Ativa a saída detalhada.

<a id="-v-1"></a>
### `-V`

Mostra a versão.

### `-t TYPE, --type TYPE`

Tipo de enumeração a executar. Há vários tipos possíveis:

- `std`: SOA, NS, A, AAAA, MX e SRV.

- `rvl`: consulta reversa de um CIDR ou intervalo de IPs especificado.

- `brt`: força bruta de domínios e hosts usando um dicionário especificado.

- `srv`: registros SRV.

- `axfr`: testa todos os servidores NS para uma transferência de zona.

- `bing`: pesquisa no Bing por subdomínios e hosts.

- `yand`: pesquisa no Yandex por subdomínios e hosts.

- `crt`: pesquisa no crt.sh por subdomínios e hosts.

- `snoop`: executa cache snooping em todos os servidores NS de um domínio especificado, testando cada um com um arquivo de domínios fornecido pela opção `-D`.

- `tld`: remove o TLD do domínio especificado e testa contra todos os TLDs registrados na IANA.

- `zonewalk`: executa uma caminhada de zona DNSSEC usando registros NSEC.

<a id="examples"></a>
## EXEMPLOS

Tenta uma transferência de zona (AXFR) no domínio zonetransfer.me

```text
dnsrecon -t axfr -d zonetransfer.me
```


---

## Procedência desta tradução

Fonte primária: [manual preservado](../../../sources/upstream/dnsrecon/dnsrecon.1.source), extraído de `/usr/share/man/man1/dnsrecon.1.gz`. Pacote `dnsrecon`, versão `1.3.1-3`; pacote-fonte `dnsrecon`, versão `1.3.1-3`. Aquisição de pacote instalado, sem atribuição de commit Git.

Licença: [GPL-2.0-only](../../99-Assets/upstream/dnsrecon/LICENSE.txt); [copyright e condições do pacote](../../99-Assets/upstream/dnsrecon/COPYRIGHT.package.txt). [Página de referência do pacote, não a origem exata do arquivo](https://github.com/darkoperator/dnsrecon). Hashes do original, gzip e avisos no registro de fontes. A data do manual é histórica; não implica que todos os serviços externos mantenham esse comportamento.
