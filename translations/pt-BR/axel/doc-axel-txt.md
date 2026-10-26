<!-- SPDX-License-Identifier: GPL-2.0 -->
<!-- Source: axel/doc/axel.txt at dc10ba0c8f8d804c1568df5dba3cdd6fa89572b1. -->
<!-- Translation by an AI assistant; independent human review remains pending. -->
# axel

## NOME

`axel` — acelerador leve de downloads pela linha de comando.

## SINOPSE

```text
 axel [OPTIONS] url1 [url2] [url...]
```

## DESCRIÇÃO

O `Axel` baixa um arquivo de um servidor `FTP` ou `HTTP` usando várias conexões. Cada conexão baixa sua própria parte do arquivo.

Ao contrário da maioria dos outros programas, o `Axel` grava todos os dados diretamente no arquivo de destino. Isso economiza tempo ao final, pois o programa não precisa concatenar as partes baixadas.

O `Axel` oferece suporte aos protocolos `HTTP`, `HTTPS`, `FTP` e `FTPS`.

## OPÇÕES

É necessário informar um argumento: a URL do arquivo a ser baixado. Em downloads por `FTP`, o nome do arquivo pode conter curingas, e o programa tentará determinar o nome completo. Também é possível especificar várias URLs de espelhos de um arquivo idêntico; nesse caso, o programa usará todas elas no download.

O programa não verifica se os arquivos são iguais.

Outras opções:

### `--max-speed=x, -s x`

Define uma velocidade, em bytes por segundo, em torno da qual o programa tentará manter a taxa média de transferência. Isso é útil para evitar que o programa consuma toda a largura de banda disponível.

### `--num-connections=x, -n x`

Define um número alternativo de conexões.

### `--max-redirect=x`

Define o limite de redirecionamentos seguidos ao estabelecer a conexão com o servidor. O padrão é 20.

### `--location-trusted`

Continua enviando os cabeçalhos que contêm credenciais quando um redirecionamento leva a um host diferente daquele solicitado inicialmente. Um cabeçalho `Cookie`, `Authorization` ou `Proxy-Authorization` fornecido com `--header` destina-se ao host informado na linha de comando. Por isso, ele é descartado quando um redirecionamento sai desse host ou abandona o `TLS`. Use esta opção somente quando todos os hosts para os quais o download possa ser redirecionado forem tão confiáveis quanto o primeiro.

### `--output=x, -o x`

Por padrão, os dados baixados são gravados em um arquivo local de mesmo nome. Esta opção permite escolher outro nome. Também é possível informar um diretório; nesse caso, o programa acrescentará o nome do arquivo ao caminho.

### `--search[=x], -S[x]`

O `Axel` pode procurar espelhos usando o mecanismo de busca filesearching.com. Essa busca é realizada quando esta opção é usada. Também é possível indicar quantos espelhos diferentes devem participar do download. A busca pode demorar, pois o programa testa a velocidade de cada servidor e verifica se o arquivo ainda está disponível.

### `--netrc[=x], -R[x]`

Obtém as credenciais do host a ser contatado a partir de um arquivo `.netrc`. Sem um argumento, usa o arquivo indicado pela variável de ambiente `NETRC` ou, se ela não estiver definida, `~/.netrc`. As credenciais fornecidas na URL têm precedência.

### `--no-netrc`

Não usa nenhum arquivo `.netrc`, sobrepondo a opção netrc do arquivo de configuração.

### `--ipv6, -6`

Usa somente o protocolo IPv6 ao estabelecer a conexão com o host.

### `--ipv4, -4`

Usa somente o protocolo IPv4 ao estabelecer a conexão com o host.

### `--no-proxy, -N`

Não usa um servidor proxy para baixar o arquivo. Isso não é possível quando há um proxy transparente ativo no caminho.

### `--insecure, -k`

Não verifica o certificado `SSL`. A documentação recomenda esta opção somente quando ocorrerem erros de certificado e houver certeza sobre a autenticidade do site.

### `--no-clobber, -c`

Ignora o download se já existir um arquivo de mesmo nome no diretório atual e nenhum arquivo de estado for encontrado.

### `--verbose, -v`

Exibe mais mensagens de estado. Repita a opção para obter mais detalhes.

### `--quiet, -q`

Não produz saída em stdout.

### `--alternate, -a`

Exibe um indicador de progresso alternativo. Uma barra mostra o progresso e o estado das diferentes threads, a velocidade atual e uma estimativa do tempo restante de download.

### `--progress, -p`

Exibe porcentagens simples, de 0 a 100, em vez de uma barra de progresso.

### `--header=x, -H x`

Adiciona um cabeçalho `HTTP`. O argumento deve ter o formato `"Header: Value"`. Consulte as seções 4.2 e 14 da RFC 2616 para detalhes sobre esse formato e os cabeçalhos padronizados.

### `--user-agent=x, -U x`

Define o agente de usuário `HTTP` usado nas requisições. Alguns sites fornecem conteúdo diferente conforme esse parâmetro. O valor padrão inclui "`Axel`", sua versão e a plataforma.

### `--help, -h`

Exibe um breve resumo de todas as opções.

### `--timeout=x, -T x`

Define o tempo limite das operações de entrada e saída, `I/O`, e da conexão.

### `--version, -V`

Exibe informações sobre a versão.

## NOTA

As opções longas, com dois hífens, só são aceitas quando a plataforma oferece a chamada `getopt_long`. Se isso não ocorrer, como no caso de *BSD citado pela fonte, somente as opções curtas poderão ser usadas.

## VALOR DE RETORNO

O programa retorna 0 quando o download é concluído com sucesso, 1 quando ocorre um erro e 2 quando o download é interrompido. Segundo o manual, qualquer outro valor indica um bug.

## EXEMPLOS

O uso básico para baixar um arquivo é semelhante a:

```text
    $ axel http://cdimage.debian.org/debian-cd/current/amd64/iso-cd/debian-9.1.0-amd64-netinst.iso
```

```text
    $ axel ftp://ftp.nl.kernel.org/pub/linux/kernel/v2.2/linux-2.2.20.tar.bz2
```

O comando a seguir usa os espelhos belga, holandês, inglês e alemão de kernel.org para baixar uma imagem do kernel Linux 2.4.17.

```text
    $ axel ftp://ftp.{be,nl,uk,de}.kernel.org/pub/linux/kernel/v2.4/linux-2.4.17.tar.bz2
```

O próximo comando procura o arquivo linux-2.4.17.tar.bz2 em filesearching.com e usa, se possível, os quatro espelhos mais rápidos para baixá-lo. ftp.kernel.org pode estar entre eles.

```text
    $ axel -S4 ftp://ftp.kernel.org/pub/linux/kernel/v2.4/linux-2.4.17.tar.bz2
```

## ARQUIVOS

### `/etc/axelrc`

Arquivo de configuração global do sistema.

### `~/.axelrc`

Arquivo de configuração pessoal.

### `~/.netrc`

Credenciais usadas somente quando `--netrc` é informado ou quando a opção netrc está habilitada no arquivo de configuração. O formato é o tradicional; consulte `ftp(1)`.

Esses arquivos não são descritos em uma página de manual, mas o arquivo de exemplo distribuído com o programa contém informações suficientes. A localização do arquivo de configuração global pode variar. No código-fonte, esse exemplo fica no diretório `doc/`. Em geral, ele é instalado em `/usr/share/doc/axel/examples/` ou no diretório equivalente da plataforma.

## DIREITOS AUTORAIS

O `Axel` foi originalmente escrito por `Wilmer van der Gaast` e recebeu contribuições de outros autores ao longo do tempo. Consulte os arquivos `AUTHORS` e `CREDITS`.

A página do projeto é <https://github.com/axel-download-accelerator/axel>.

## CONTRIBUA COM O PROJETO

Para contribuir, leia o arquivo `CONTRIBUTING.md`. Em sistemas Debian, ele fica disponível no diretório `/usr/share/doc/axel/`.
