<!-- SPDX-License-Identifier: GPL-2.0-or-later -->
# dnsenum

## NOME

dnsenum -- script multithread para enumerar informações sobre um domínio e descobrir blocos IP não contíguos

## VERSÃO

dnsenum versão 1.3.1

## SINOPSE

```text
dnsenum [options] <domain> -f dns.txt
```

## DESCRIÇÃO

Operações compatíveis: nslookup, transferência de zona, extração de resultados do Google, força bruta de domínios (também com recursão), whois de IPs e consultas reversas.

Operações:

- 1) Obtém o endereço do host (registro A).

- 2) Obtém os servidores de nomes (com threads).

- 3) Obtém o registro MX (com threads).

- 4) Executa consultas AXFR nos servidores de nomes (com threads).

- 5) Obtém nomes e subdomínios adicionais por extração de resultados do Google (consulta do Google = "`-www site:domain`").

- 6) Faz força bruta de subdomínios a partir de (OBRIGATÓRIO); também pode executar recursão em subdomínios que tenham registros NS (tudo com threads).

> **Nota editorial:** o original deixa em branco a origem após "from" nesta frase. A opção `-f`, descrita adiante, especifica o arquivo de subdomínios; a lacuna não foi preenchida silenciosamente.

- 7) Calcula intervalos de rede IP de classe C a partir dos resultados e executa consultas whois sobre eles (com threads).

- 8) Executa consultas reversas em intervalos de rede (classe C e/ou intervalos whois), com threads.

- 9) Grava os resultados de blocos IP não contíguos no arquivo `domain_ips.txt`.

## OPÇÕES

A opção de força bruta `-f` tem prioridade sobre o arquivo padrão `dns.txt`.

### OPÇÕES GERAIS:

### `--dnsserver <server>`

Usa este servidor DNS para executar todas as consultas A, NS e MX; as consultas AXFR e PTR são enviadas aos servidores NS do domínio.

### `--enum`

Atalho equivalente a `--threads 5 -s 20 -w`.

### `-h,  --help`

Imprime a mensagem de ajuda.

### `--noreverse`

Pula as operações de consulta reversa. Consultas reversas podem demorar bastante em intervalos de rede grandes.

### `--nocolor`

Desativa a saída ANSIColor. Esta opção destina-se apenas a consoles que não oferecem suporte à saída em cores.

### `--private`

Mostra e salva os IPs privados no final do arquivo `domain_ips.txt`.

### `--subfile <file>`

Grava todos os subdomínios válidos neste arquivo. Os subdomínios são obtidos de registros NS e MX, transferências de zona, extração de resultados do Google, força bruta e nomes de hosts de consultas reversas.

### `-t,  --timeout <value>`

Os valores de timeout TCP e UDP em segundos (padrão: 10 s).

### `--threads <va>`

O número de threads que executarão as diferentes consultas.

### `-v,  --verbose`

Exibe informações detalhadas (todo o progresso e todas as mensagens de erro).

Notas: nem o domínio padrão nem a lista de pesquisa do resolvedor são acrescentados a domínios que não contêm nenhum ponto.

### OPÇÕES DE EXTRAÇÃO DO GOOGLE:

Esta função extrai subdomínios da pesquisa do Google usando a consulta: `-www site:domain`.

### `-p,  --pages <value>`

O número de páginas de pesquisa do Google a processar ao extrair nomes; a opção `-s` deve ser especificada (padrão: 20 páginas).

### `-s,  --scrap <value>`

O número máximo de subdomínios a extrair do Google.

NOTAS: o Google pode bloquear nossas consultas com sua detecção de malware. As opções de proxy HTTP para a extração do Google são carregadas automaticamente do ambiente se as variáveis `http_proxy` ou `HTTP_PROXY` estiverem presentes: "`http_proxy=http://127.0.0.1:8118/`" ou "`HTTP_PROXY=http://127.0.0.1:8118/`". Em erros de E/S, o objeto de navegador mechanize chamará `die` automaticamente.

### OPÇÕES DE FORÇA BRUTA:

### `-f,  --file <file>`

Lê subdomínios deste arquivo para executar força bruta.

### `-u,  --update <a|g|r|z>`

Atualiza o arquivo especificado com a opção `-f` usando subdomínios válidos.

`-u a` — atualiza usando todos os resultados.

`-u g` — atualiza usando apenas resultados da extração do Google.

`-u r` — atualiza usando apenas resultados de consultas reversas.

`-u z` — atualiza usando apenas resultados de transferências de zona.

### `-r,  --recursion`

Recursão em subdomínios: executa força bruta em todos os subdomínios descobertos que tenham um registro NS.

NOTAS: para executar recursão, primeiro precisamos verificar se os resultados anteriores de subdomínios (transferência de zona, extração do Google e força bruta) contêm registros NS; depois executamos força bruta nos subdomínios válidos que tenham esses registros, e assim por diante. Os resultados de NS, MX e consultas reversas não são incluídos nesse processo.

### OPÇÕES DE WHOIS DE IP:

Executa consultas whois de IPs nos intervalos de rede de classe C descobertos pelas operações anteriores.

### `-d,  --delay <value>`

O valor máximo, em segundos, de espera entre consultas whois; o valor é definido aleatoriamente (padrão: 3 s).

NOTAS: servidores whois limitam o número de conexões.

### `-w,  --whois`

Executa consultas whois nos intervalos de rede de classe C. Aviso: isso pode gerar intervalos de rede muito grandes, e as consultas reversas levarão bastante tempo.

NOTAS: por padrão, a consulta whois deve consultar recursivamente os diversos provedores whois até obter as informações mais detalhadas, incluindo `TechPhone` ou `OrgTechPhone`. Veja: `perldoc Net::Whois::IP`. Em caso de erros, o intervalo de rede será uma rede de classe C `/24` padrão.

### OPÇÕES DE CONSULTA REVERSA:

### `-e,  --exclude <regexp>`

Exclui dos resultados de consulta reversa os registros PTR que correspondam à expressão regular; útil para nomes de host inválidos.

NOTAS: registros PTR que não correspondam ao domínio também são excluídos. O modo detalhado mostra todos os resultados.

## ARQUIVOS DE SAÍDA

Os blocos IP não contíguos finais são gravados no arquivo `domain_ips.txt`.

NOTAS: os blocos IP não contíguos finais são calculados:

- 1) A partir das consultas reversas executadas nos intervalos de rede (intervalos de classe C ou intervalos whois).

- 2) Se a opção `noreverse` for usada, são calculados a partir dos resultados das operações anteriores (nslookups, transferências de zona, extração do Google e força bruta).

## README

dnsenum: script multithread para enumerar informações sobre um domínio e descobrir blocos IP não contíguos.

## PRÉ-REQUISITOS

Módulos incluídos no Perl 5.28.0: `Getopt::Long`, `IO::File`, `Thread::Queue`.

Outros módulos necessários: obrigatórios: `Net::DNS`, `Net::IP`, `Net::Netmask`. Opcionais: `Net::Whois::IP`, `HTML::Parser`, `WWW::Mechanize`.

Módulos ithreads do Perl (o Perl precisa ser compilado com suporte a ithreads): `threads`, `threads::shared`.

## AUTORES

Filip Waeytens	<filip.waeytens[at]gmail.com>

tix tixxDZ	<tixxdz[at]gmail.com>

## MANTENEDOR

Network Silence

## COPYRIGHT

Este programa é software livre; você pode redistribuí-lo e/ou modificá-lo sob os termos da GNU General Public License, publicada pela Free Software Foundation, na versão 2 da licença ou, a seu critério, em qualquer versão posterior.

## CATEGORIAS DO SCRIPT

Redes DNS
