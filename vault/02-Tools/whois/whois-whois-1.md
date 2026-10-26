---
title: "whois — manual de referência"
type: "official-documentation"
tool: "whois"
status: "source-checked"
reviewed: "2026-10-26"
language: "pt-BR"
tags: ["documentation", "tool/whois"]
cssclasses: ["fieldbook"]
source_url: "https://www.kali.org/tools/whois/"
source_kind: "installed-kali-package"
package: "whois"
binary_version: "5.6.6"
source_package: "whois"
source_version: "5.6.6"
source_snapshot_sha256: "ecc5633af88fe2bb018cb587dc33832de15ec8060854de17806a008202eac19e"
source_sha256: "74ff8b3ae7c59193d366d679aad9d328c2917a38399bb7d73a39264604d038fc"
license_spdx: "GPL-2.0-or-later"
human_review: "pending"
source_scope: "Complete English whois(1) installed package manual only; whois.conf(5), mkpasswd(1), websites and other package documentation remain separate pending scope"
binary: "whois"
source_manual_date: "2019-12-30"
manual_section: "1"
test_status: "help-only"
tested_version: "whois 5.6.6"
---

> Tradução para português produzida por assistente de IA e conferida seção por seção contra a fonte. Revisão humana independente: pendente. Opções e exemplos originais foram preservados; nenhum exemplo foi executado automaticamente.

> **Compatibilidade observada:** whois 5.6.6. As opções do manual foram encontradas na ajuda instalada. A fonte fixada foi mantida sem trocar opções silenciosamente. Conferidas somente whois --help, whois --version e a versão dpkg; nenhum domínio, IP, servidor ou objeto foi consultado. [Evidência e limites do teste](../../99-Assets/evidence/whois-help-tests.json).

<!-- SPDX-License-Identifier: GPL-2.0-or-later -->
# whois

<a id="name"></a>
## NOME

whois - cliente para o serviço de diretório whois

<a id="synopsis"></a>
## SINOPSE

```text
whois [ { -h | --host } HOST ] [ { -p | --port } PORT ] [ -abBcdGHIKlLmMrRx ] [ -g SOURCE:FIRST-LAST ] [ -i ATTR[,ATTR]... ] [ -s SOURCE[,SOURCE]... ] [ -T TYPE[,TYPE]... ] [ --verbose ] [ --no-recursion ] OBJECT

whois -q KEYWORD

whois -t TYPE

whois -v TYPE

whois --help

whois --version
```

<a id="description"></a>
## DESCRIÇÃO

`whois` procura um objeto em um banco de dados `RFC 3912`.

Esta versão do cliente whois tenta determinar o servidor correto para consultar o objeto especificado. Se não conseguir determiná-lo, conectará a `whois.networksolutions.com` para identificadores NIC ou a `whois.arin.net` para endereços IPv4 e nomes de redes.

<a id="options"></a>
## OPÇÕES

### `-h` `HOST`, `--host=HOST`

Conecta a `HOST`.

### `-H`

Não exibe os avisos legais que alguns registros costumam mostrar.

### `-p` `PORT`, `--port=PORT`

Conecta à porta `PORT`.

### `-I`

Primeiro consulta `whois.iana.org` e depois segue seu encaminhamento ao servidor whois autoritativo para essa solicitação. Isso funciona para endereços IP, números AS e domínios. `BEWARE` (atenção): isso implica que o servidor IANA receberá sua consulta completa.

### `--no-recursion`

Desativa a recursão dos servidores de registro para os servidores dos registradores.

### `--verbose`

Exibe informações detalhadas.

### `--help`

Exibe a ajuda do programa.

### `--version`

Exibe a versão do programa.

As outras opções são sinalizadores reconhecidos por `whois.ripe.net` e por alguns outros servidores semelhantes ao RIPE:

### `-a`

Também pesquisa em todos os bancos de dados espelhados.

### `-b`

Retorna intervalos resumidos de endereços IP com contato para denúncias de abuso.

<a id="-b-1"></a>
### `-B`

Desativa a filtragem de objetos. (Mostra os endereços de e-mail.)

### `-c`

Retorna o menor intervalo de endereços IP com uma referência a um objeto irt.

### `-d`

Retorna também o objeto de delegação de DNS reverso.

### `-g` `SOURCE:FIRST-LAST`

Pesquisa atualizações no banco de dados `SOURCE` entre os números de série de atualização `FIRST` e `LAST`. É útil para obter o fluxo de espelhamento quase em tempo real (Near Real Time Mirroring).

### `-G`

Desativa o agrupamento de objetos associados.

### `-i` `ATTR`[,`ATTR`]...

Faz uma pesquisa inversa de objetos que tenham os atributos associados. `ATTR` é o nome do atributo, enquanto o argumento posicional `OBJECT` é o valor do atributo.

### `-K`

Retorna apenas atributos de chave primária. Uma exceção é o atributo `members` dos objetos `set`, que sempre é retornado. Outra exceção são todos os atributos dos objetos `organisation`, `person` e `role`, que nunca são retornados.

### `-l`

Retorna o objeto um nível menos específico.

<a id="-l-1"></a>
### `-L`

Retorna todos os níveis de objetos menos específicos.

### `-m`

Retorna todos os objetos um nível mais específicos.

<a id="-m-1"></a>
### `-M`

Retorna todos os níveis de objetos mais específicos.

### `-q` `KEYWORD`

Retorna informações sobre o servidor. `KEYWORD` pode ser `version` para a versão do servidor, `sources` para a lista de fontes de bancos de dados ou `types` para a lista de tipos de objetos compatíveis.

### `-r`

Desativa as consultas recursivas de informações de contato.

<a id="-r-1"></a>
### `-R`

Desativa o acompanhamento de encaminhamentos e força a exibição do objeto da cópia local no servidor.

### `-s` `SOURCE`[,`SOURCE`]...

Solicita ao servidor que pesquise objetos espelhados de `SOURCE`. As fontes são separadas por vírgula, e a ordem é significativa. Use o parâmetro `-q sources` para obter uma lista de fontes válidas.

### `-t` `TYPE`

Retorna o modelo para um objeto do tipo `TYPE`.

### `-T` `TYPE`[,`TYPE`]...

Restringe a pesquisa a objetos do tipo `TYPE`. Vários tipos são separados por vírgula.

### `-v` `TYPE`

Retorna o modelo detalhado para um objeto do tipo `TYPE`.

### `-x`

Pesquisa apenas correspondências exatas do prefixo de endereço de rede.

<a id="notes"></a>
## NOTAS

Ao consultar os servidores thin registry de gTLDs da Verisign (por exemplo, .com, .net...) sobre um domínio, o programa acrescentará automaticamente a palavra-chave `domain` no início para mostrar apenas registros de domínio. As palavras-chave `nameserver` ou `registrar` devem ser usadas para mostrar outros tipos de registros.

Ao consultar `whois.arin.net` sobre redes IPv4 ou IPv6, o comprimento da máscara de rede CIDR será removido automaticamente da string de consulta.

Ao consultar `whois.nic.ad.jp` sobre números AS, o programa converterá automaticamente a solicitação para o formato apropriado, inserindo um espaço após a string `AS`.

Ao consultar `whois.denic.de` sobre nomes de domínio sem especificar outros sinalizadores, o programa acrescentará automaticamente o sinalizador `-T dn`.

Ao consultar `whois.dk-hostmaster.dk` sobre nomes de domínio sem especificar outros sinalizadores, o programa acrescentará automaticamente o sinalizador `--show-handles`.

As opções de linha de comando específicas do RIPE são ignoradas ao consultar servidores que não são RIPE. Esse comportamento pode ou não corresponder ao pretendido pelo usuário. Ao usar parâmetros de consulta não padronizados, as opções de linha de comando que não devem ser interpretadas pelo cliente precisam vir após o separador `--` (que marca o início da string de consulta).

Se o arquivo de configuração `/etc/whois.conf` existir, ele será consultado para encontrar um servidor antes da aplicação das regras normais. Cada linha do arquivo deve conter uma expressão regular a ser comparada com o texto da consulta e o servidor whois a utilizar, separados por espaço em branco. Domínios IDN devem usar o formato ACE.

O protocolo whois não especifica uma codificação para caracteres que não podem ser representados em ASCII, e as implementações variam muito. Se o programa souber que determinado servidor usa uma certa codificação, quando necessário transcodificará a saída do servidor para a codificação especificada pela configuração regional atual do sistema.

Os argumentos de linha de comando sempre serão interpretados de acordo com a configuração regional atual do sistema e convertidos para a codificação compatível com ASCII dos IDNs.

<a id="files"></a>
## ARQUIVOS

/etc/whois.conf

<a id="environment"></a>
## AMBIENTE

### `LANG`

Ao consultar `whois.nic.ad.jp` e `whois.jprs.jp`, solicita-se texto em inglês, a menos que as variáveis de ambiente `LANG` ou `LC_MESSAGES` especifiquem uma configuração regional japonesa.

### `WHOIS_OPTIONS`

Uma lista de opções que serão avaliadas antes das especificadas na linha de comando.

### `WHOIS_SERVER`

Este servidor será consultado se o programa não conseguir determinar onde está localizado algum tipo de objeto. Se a variável não existir, `whois.arin.net` será consultado.

<a id="see-also"></a>
## VEJA TAMBÉM

`whois.conf`(5).

`RFC 3912`: especificação do protocolo WHOIS.

`RIPE Database Query Reference Manual`: <https://www.ripe.net/data-tools/support/documentation/ripe-database-query-reference-manual>

## BUGS

O programa pode apresentar estouros de buffer no analisador de linha de comando: certifique-se de não passar dados não confiáveis a ele. Ele deveria ser reescrito para usar uma biblioteca de strings dinâmicas.

<a id="history"></a>
## HISTÓRICO

Este programa acompanha de perto a interface de usuário do cliente whois desenvolvido no RIPE por Ambrose Magee e outros, com base no cliente BSD original.

<a id="author"></a>
## AUTOR

`Whois` e esta página de manual foram escritos por Marco d'Itri <`md@linux.it`> e são licenciados sob os termos da GNU General Public License, versão 2 ou posterior.


---

## Procedência desta tradução

Fonte primária: [manual preservado](../../../sources/upstream/whois/whois.1.source), extraído de `/usr/share/man/man1/whois.1.gz`. Pacote `whois`, versão `5.6.6`; pacote-fonte `whois`, versão `5.6.6`. Aquisição de pacote instalado, sem atribuição de commit Git.

Licença: [GPL-2.0-or-later](../../99-Assets/upstream/whois/LICENSE.txt); [copyright e condições do pacote](../../99-Assets/upstream/whois/COPYRIGHT.package.txt). [Página de referência do pacote, não a origem exata do arquivo](https://www.kali.org/tools/whois/). Hashes do original, gzip e avisos no registro de fontes. A data do manual é histórica; não implica que todos os serviços externos mantenham esse comportamento.
