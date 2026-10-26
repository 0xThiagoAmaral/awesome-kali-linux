<!-- SPDX-License-Identifier: GPL-2.0-or-later -->
# whois

## NOME

whois - cliente para o serviço de diretório whois

## SINOPSE

```text
whois [ { -h | --host } HOST ] [ { -p | --port } PORT ] [ -abBcdGHIKlLmMrRx ] [ -g SOURCE:FIRST-LAST ] [ -i ATTR[,ATTR]... ] [ -s SOURCE[,SOURCE]... ] [ -T TYPE[,TYPE]... ] [ --verbose ] [ --no-recursion ] OBJECT

whois -q KEYWORD

whois -t TYPE

whois -v TYPE

whois --help

whois --version
```

## DESCRIÇÃO

`whois` procura um objeto em um banco de dados `RFC 3912`.

Esta versão do cliente whois tenta determinar o servidor correto para consultar o objeto especificado. Se não conseguir determiná-lo, conectará a `whois.networksolutions.com` para identificadores NIC ou a `whois.arin.net` para endereços IPv4 e nomes de redes.

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

### `-L`

Retorna todos os níveis de objetos menos específicos.

### `-m`

Retorna todos os objetos um nível mais específicos.

### `-M`

Retorna todos os níveis de objetos mais específicos.

### `-q` `KEYWORD`

Retorna informações sobre o servidor. `KEYWORD` pode ser `version` para a versão do servidor, `sources` para a lista de fontes de bancos de dados ou `types` para a lista de tipos de objetos compatíveis.

### `-r`

Desativa as consultas recursivas de informações de contato.

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

## ARQUIVOS

/etc/whois.conf

## AMBIENTE

### `LANG`

Ao consultar `whois.nic.ad.jp` e `whois.jprs.jp`, solicita-se texto em inglês, a menos que as variáveis de ambiente `LANG` ou `LC_MESSAGES` especifiquem uma configuração regional japonesa.

### `WHOIS_OPTIONS`

Uma lista de opções que serão avaliadas antes das especificadas na linha de comando.

### `WHOIS_SERVER`

Este servidor será consultado se o programa não conseguir determinar onde está localizado algum tipo de objeto. Se a variável não existir, `whois.arin.net` será consultado.

## VEJA TAMBÉM

`whois.conf`(5).

`RFC 3912`: especificação do protocolo WHOIS.

`RIPE Database Query Reference Manual`: <https://www.ripe.net/data-tools/support/documentation/ripe-database-query-reference-manual>

## BUGS

O programa pode apresentar estouros de buffer no analisador de linha de comando: certifique-se de não passar dados não confiáveis a ele. Ele deveria ser reescrito para usar uma biblioteca de strings dinâmicas.

## HISTÓRICO

Este programa acompanha de perto a interface de usuário do cliente whois desenvolvido no RIPE por Ambrose Magee e outros, com base no cliente BSD original.

## AUTOR

`Whois` e esta página de manual foram escritos por Marco d'Itri <`md@linux.it`> e são licenciados sob os termos da GNU General Public License, versão 2 ou posterior.
