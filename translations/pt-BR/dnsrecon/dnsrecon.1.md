<!-- SPDX-License-Identifier: GPL-2.0-only -->
# dnsrecon

## NOME

dnsrecon - ferramenta de enumeração e varredura DNS

## SINOPSE

```text
dnsrecon [-h] [-d DOMAIN] [-n NS_SERVER] [-r RANGE] [-D DICTIONARY] [-f] [-a] [-s] [-b] [-k] [-w] [-z] [-y] [--threads THREADS] [--lifetime LIFETIME] [--tcp] [--db DB] [-x XML] [-c CSV] [-j JSON] [--iw] [--disable_check_recursion] [--disable_check_bindversion] [-v] [-V] [-t TYPE]
```

## DESCRIÇÃO

dsnrecon é um script Python simples que permite reunir informações relacionadas a DNS sobre um alvo especificado.

> **Nota editorial:** o original escreve "dsnrecon" nesta frase; o nome do programa, nas opções e na sinopse, é `dnsrecon`. A grafia da frase de origem foi mantida.

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

## EXEMPLOS

Tenta uma transferência de zona (AXFR) no domínio zonetransfer.me

```text
dnsrecon -t axfr -d zonetransfer.me
```
