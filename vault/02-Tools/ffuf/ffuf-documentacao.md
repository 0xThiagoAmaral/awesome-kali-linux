---
title: "ffuf — documentação oficial"
type: "official-documentation"
tool: "ffuf"
status: "translated-machine"
reviewed: "2026-10-26"
language: "pt-BR"
tags: ["documentation", "tool/ffuf"]
cssclasses: ["fieldbook"]
source_url: "https://github.com/ffuf/ffuf/blob/8d65e0373e5f223530174e5694285af849770078/README.md"
source_commit: "8d65e0373e5f223530174e5694285af849770078"
source_sha256: "2419b892f8a77ba3c5021300dcf5c37f2587ac9b7d579303c9add707fc0b93e4"
license_spdx: "MIT"
human_review: "pending"
source_scope: "Official English repository README/docs and available upstream Portuguese README; external manuals/wiki coverage tracked separately"
---

> Tradução automática local para português, ainda sem revisão humana integral. Estrutura e blocos de código preservados; referências externas não significam conteúdo espelhado.

![ffuf mascot](../../99-Assets/upstream/ffuf/_img/ffuf_run_logo_600.png)
# ffuf - Fuzz Faster U Fool

Uma web rápida fuzzer escrita em Go.

- [Instalação](#instalação)
- [Utilização do exemplo](#utilização-do-exemplo)
    - [Content discovery](#descoberta-de-diretórios-típica)
    - [Vhost discovery](#descoberta-virtual-da-máquina-sem-registos-dns)
    - [Parameter fuzzing](#get-parameter-fuzzing)
    - [POST data fuzzing](#dados-post-fuzzing)
    - [Using external mutator](#usando-mutante-externo-para-produzir-casos-de-teste)
    - [Configuration files](#arquivos-de-configuração)
- [Ajuda](#uso)
    - [Interactive mode](#modo-interativo)


## Instalação

- [Transferir](https://github.com/ffuf/ffuf/releases/latest) um binário pré-construído do [página de lançamentos](https://github.com/ffuf/ffuf/releases/latest), desempacote e execute!

_or_
- Se você estiver no Windows com [Scoop](https://scoop.sh/), ffuf pode ser instalado com: `scoop install ffuf`

_or_
- Se você estiver no Windows com [Winget](https://learn.microsoft.com/en-us/windows/package-manager/), ffuf pode ser instalado com: `winget install ffuf.ffuf`

_or_
- Se você estiver no macOS com [brew homebrew](https://brew.sh), ffuf pode ser instalado com: `brew install ffuf`
  
_or_
- Se você tiver o compilador ir instalado recentemente: `go install github.com/ffuf/ffuf/v2@latest` (o mesmo comando funciona para atualização)
  
_or_
- `git clone https://github.com/ffuf/ffuf ; cd ffuf ; go get ; go build`

1. Ffuf depende de Go 1.20 ou superior.
2. Uma compilação ir de um checkout mostra `git-<date>-<commit>` em vez da tag. Uma compilação local não é uma versão oficial, mesmo quando você está sentado em uma tag, e informações de compilação incorporadas do Go nos dá o commit, mas não o nome da tag — então nós superficiemos o commit exato de que foi construído. Os binários versionados autoritários são os da página de lançamentos.

## Utilização do exemplo

Os exemplos de uso abaixo mostram apenas as tarefas mais simples que você pode realizar usando `ffuf`.

Documentação mais elaborada que passa por muitos recursos com muitos exemplos é
disponível na wiki ffuf em [https://github.com/ffuf/ffuf/wiki](https://github.com/ffuf/ffuf/wiki)

Para uma documentação mais extensa, com exemplos e dicas de uso da vida real, confira o guia incrível:
"[Tudo o que você precisa saber sobre FFUF](https://codingo.io/tools/ffuf/bounty/2020/09/17/everything-you-need-to-know-about-ffuf.html)" por
Michael Skelton ([@ codingo](https://github.com/codingo)).

Você também pode praticar suas varreduras ffuf contra um host ao vivo com diferentes lições e usar casos localmente usando o recipiente de docker https://github.com/adamtlangley/ffufme ou contra a versão hospedada ao vivo no http://ffuf.me criado por Adam Langley [@adamtlangley](https://twitter.com/adamtlangley).

### Descoberta de diretórios típica

[asciicast](https://asciinema.org/a/211350)

Usando a palavra- chave FUZZ no final do URL (`-u`):

```text
ffuf -w /path/to/wordlist -u https://target/FUZZ
```

### Descoberta virtual da máquina (sem registos DNS)

[asciicast](https://asciinema.org/a/211360)

Assumindo que o tamanho padrão de resposta virtualhost é 4242 bytes, podemos filtrar todas as respostas desse tamanho (`-fs 4242`) enquanto fuzzing o Host - cabeçalho:

```text
ffuf -w /path/to/vhost/wordlist -u https://target -H "Host: FUZZ" -fs 4242
```

### GET parameter fuzzing

O nome do parâmetro GET fuzzing é muito semelhante à descoberta de diretórios, e funciona definindo a palavra-chave `FUZZ` como parte da URL. Isto também assume um tamanho de resposta de 4242 bytes para o nome do parâmetro GET inválido.

```text
ffuf -w /path/to/paramnames.txt -u https://target/script.php?FUZZ=test_value -fs 4242
```

Se o nome do parâmetro for conhecido, os valores podem ser fuzzed da mesma forma. Este exemplo assume um valor de parâmetro errado retornando HTTP código de resposta 401.

```text
ffuf -w /path/to/values.txt -u https://target/script.php?valid_name=FUZZ -fc 401
```

### Dados POST fuzzing

Esta é uma operação muito simples, novamente usando a palavra-chave `FUZZ`. Este exemplo é fuzzing apenas parte da solicitação POST. Estamos novamente filtrando as respostas 401.

```text
ffuf -w /path/to/postdata.txt -X POST -d "username=admin\&password=FUZZ" -u https://target/login.php -fc 401
```

### Tempo máximo de execução

Se você não quiser que o ffuf seja executado indefinidamente, você pode usar o `-maxtime`. Isto para o __ todo o processo __ após um determinado tempo (em segundos).

```text
ffuf -w /path/to/wordlist -u https://target/FUZZ -maxtime 60
```

Ao trabalhar com recursão, você pode controlar o trabalho do maxtime __per__ usando `-maxtime-job`. Isto irá parar o trabalho atual após um determinado tempo (em segundos) e continuar com o próximo. Novos trabalhos são criados quando a funcionalidade de recursão detecta um subdiretório.

```text
ffuf -w /path/to/wordlist -u https://target/FUZZ -maxtime-job 60 -recursion -recursion-depth 2
```

Também é possível combinar ambas as bandeiras limitando o tempo máximo de execução por tarefa, bem como o tempo total de execução. Se você não usar a recursão, então ambas as bandeiras se comportam igualmente.

### Usando mutante externo para produzir casos de teste

Para este exemplo, vamos fuzz JSON dados que é enviado sobre POST. [Radamsa](https://gitlab.com/akihe/radamsa) é usado como o mutador.

Quando o `--input-cmd` for usado, o ffuf irá mostrar as correspondências como a sua posição. Este mesmo valor de posição estará disponível para o chamado como uma variável de ambiente `$FFUF_NUM`. Vamos usar este valor de posição como a semente para o mutador. Os arquivos exemplo1.txt e exemplo2.txt contêm cargas válidas do JSON. Estamos a corresponder a todas as respostas, mas a filtrar o código de resposta `400 - Bad request`:

```text
ffuf --input-cmd 'radamsa --seed $FFUF_NUM example1.txt example2.txt' -H "Content-Type: application/json" -X POST -u https://ffuf.io.fi/FUZZ -mc all -fc 400
```

É claro que não é muito eficiente chamar o mutante para cada carga útil, então também podemos pré-gerar as cargas úteis, ainda usando [Radamsa](https://gitlab.com/akihe/radamsa) como exemplo:

```text
# Generate 1000 example payloads
radamsa -n 1000 -o %n.txt example1.txt example2.txt

# This results into files 1.txt ... 1000.txt
# Now we can just read the payload data in a loop from file for ffuf

ffuf --input-cmd 'cat $FFUF_NUM.txt' -H "Content-Type: application/json" -X POST -u https://ffuf.io.fi/ -mc all -fc 400
```

### Arquivos de configuração

Ao executar o ffuf, ele primeiro verifica se existe um arquivo de configuração padrão. O caminho padrão para um arquivo `ffufrc` é
`$XDG_CONFIG_HOME/ffuf/ffufrc`. Você pode configurar uma ou várias opções neste arquivo, e elas serão aplicadas em
todas as tarefas subsequentes do ffuf. Um exemplo de arquivo ffufrc pode ser encontrado
[Aqui.](https://github.com/ffuf/ffuf/blob/master/ffufrc.example).

Uma descrição mais detalhada sobre as localizações dos arquivos de configuração pode ser encontrada no wiki:
[https://github.com/ffuf/ffuf/wiki/Configuration](https://github.com/ffuf/ffuf/wiki/Configuration)

As opções de configuração fornecidas na linha de comando sobrepõem-se às carregadas a partir do arquivo `ffufrc` padrão.
Nota: isto não se aplica às bandeiras CLI que podem ser fornecidas mais de uma vez. Um desses exemplos é a bandeira `-H` (header).
Neste caso, os valores de `-H` fornecidos na linha de comando serão _appended_ para os do arquivo de configuração.

Além disso, no caso de você desejar usar vários arquivos de configuração para diferentes casos de uso, você pode fazer isso definindo
o caminho do arquivo de configuração usando o sinal de linha de comando `-config` que leva o caminho do arquivo para o arquivo de configuração como seu
parâmetro.

<p align="center">
  <img width="250" src="../../99-Assets/upstream/ffuf/_img/ffuf_juggling_250.png">
</p>

## Uso

Para definir o caso de teste para ffuf, use a palavra-chave `FUZZ` em qualquer lugar na URL (`-u`), cabeçalhos (`-H`), ou dados POST (`-d`).

```text
Fuzz Faster U Fool - v2.1.0

HTTP OPTIONS:
  -H                  Header `"Name: Value"`, separated by colon. Multiple -H flags are accepted.
  -X                  HTTP method to use
  -b                  Cookie data `"NAME1=VALUE1; NAME2=VALUE2"` for copy as curl functionality.
  -cc                 Client cert for authentication. Client key needs to be defined as well for this to work
  -ck                 Client key for authentication. Client certificate needs to be defined as well for this to work
  -d                  POST data
  -http2              Use HTTP2 protocol (default: false)
  -ignore-body        Do not fetch the response content. (default: false)
  -r                  Follow redirects (default: false)
  -raw                Do not encode URI (default: false)
  -recursion          Scan recursively. Only FUZZ keyword is supported, and URL (-u) has to end in it. (default: false)
  -recursion-depth    Maximum recursion depth. (default: 0)
  -recursion-strategy Recursion strategy: "default" for a redirect based, and "greedy" to recurse on all matches (default: default)
  -replay-proxy       Replay matched requests using this proxy.
  -sni                Target TLS SNI, does not support FUZZ keyword
  -timeout            HTTP request timeout in seconds. (default: 10)
  -u                  Target URL
  -x                  Proxy URL (SOCKS5 or HTTP). For example: http://127.0.0.1:8080 or socks5://127.0.0.1:8080

GENERAL OPTIONS:
  -V                  Show version information. (default: false)
  -ac                 Automatically calibrate filtering options (default: false)
  -acc                Custom auto-calibration string. Can be used multiple times. Implies -ac
  -ach                Per host autocalibration (default: false)
  -ack                Autocalibration keyword (default: FUZZ)
  -acs                Custom auto-calibration strategies. Can be used multiple times. Implies -ac
  -c                  Colorize output. (default: false)
  -config             Load configuration from a file
  -json               JSON output, printing newline-delimited JSON records (default: false)
  -maxtime            Maximum running time in seconds for entire process. (default: 0)
  -maxtime-job        Maximum running time in seconds per job. (default: 0)
  -noninteractive     Disable the interactive console functionality (default: false)
  -p                  Seconds of `delay` between requests, or a range of random delay. For example "0.1" or "0.1-2.0"
  -rate               Rate of requests per second (default: 0)
  -s                  Do not print additional information (silent mode) (default: false)
  -sa                 Stop on all error cases. Implies -sf and -se. (default: false)
  -scraperfile        Custom scraper file path
  -scrapers           Active scraper groups (default: all)
  -se                 Stop on spurious errors (default: false)
  -search             Search for a FFUFHASH payload from ffuf history
  -sf                 Stop when > 95% of responses return 403 Forbidden (default: false)
  -t                  Number of concurrent threads. (default: 40)
  -v                  Verbose output, printing full URL and redirect location (if any) with the results. (default: false)

MATCHER OPTIONS:
  -mc                 Match HTTP status codes, or "all" for everything. (default: 200-299,301,302,307,401,403,405,500)
  -ml                 Match amount of lines in response
  -mmode              Matcher set operator. Either of: and, or (default: or)
  -mr                 Match regexp
  -ms                 Match HTTP response size
  -mt                 Match how many milliseconds to the first response byte, either greater or less than. EG: >100 or <100
  -mw                 Match amount of words in response

FILTER OPTIONS:
  -fc                 Filter HTTP status codes from response. Comma separated list of codes and ranges
  -fl                 Filter by amount of lines in response. Comma separated list of line counts and ranges
  -fmode              Filter set operator. Either of: and, or (default: or)
  -fr                 Filter regexp
  -fs                 Filter HTTP response size. Comma separated list of sizes and ranges
  -ft                 Filter by number of milliseconds to the first response byte, either greater or less than. EG: >100 or <100
  -fw                 Filter by amount of words in response. Comma separated list of word counts and ranges

INPUT OPTIONS:
  -D                  DirSearch wordlist compatibility mode. Used in conjunction with -e flag. (default: false)
  -e                  Comma separated list of extensions. Extends FUZZ keyword.
  -enc                Encoders for keywords, eg. 'FUZZ:urlencode b64encode'
  -ic                 Ignore wordlist comments (default: false)
  -input-cmd          Command producing the input. --input-num is required when using this input method. Overrides -w.
  -input-num          Number of inputs to test. Used in conjunction with --input-cmd. (default: 100)
  -input-shell        Shell to be used for running command
  -mode               Multi-wordlist operation mode. Available modes: clusterbomb, pitchfork, sniper (default: clusterbomb)
  -request            File containing the raw http request
  -request-proto      Protocol to use along with raw request (default: https)
  -w                  Wordlist file path and (optional) keyword separated by colon. eg. '/path/to/wordlist:KEYWORD'

OUTPUT OPTIONS:
  -debug-log          Write all of the internal logging to the specified file.
  -o                  Write output to file
  -od                 Directory path to store matched results to.
  -of                 Output file format. Available formats: json, ejson, html, md, csv, ecsv (or, 'all' for all formats) (default: json)
  -or                 Don't create the output file if we don't have results (default: false)

EXAMPLE USAGE:
  Fuzz file paths from wordlist.txt, match all responses but filter out those with content-size 42.
  Colored, verbose output.
    ffuf -w wordlist.txt -u https://example.org/FUZZ -mc all -fs 42 -c -v

  Fuzz Host-header, match HTTP 200 responses.
    ffuf -w hosts.txt -u https://example.org/ -H "Host: FUZZ" -mc 200

  Fuzz POST JSON data. Match all responses not containing text "error".
    ffuf -w entries.txt -u https://example.org/ -X POST -H "Content-Type: application/json" \
      -d '{"name": "FUZZ", "anotherkey": "anothervalue"}' -fr "error"

  Fuzz multiple locations. Match only responses reflecting the value of "VAL" keyword. Colored.
    ffuf -w params.txt:PARAM -w values.txt:VAL -u https://example.org/?PARAM=VAL -mr "VAL" -c

  More information and examples: https://github.com/ffuf/ffuf
```

### Modo interativo

Ao pressionar o `ENTER` durante a execução do ffuf, o processo é pausado e o usuário é descartado para um modo interativo semelhante ao shell:
```text
entering interactive mode
type "help" for a list of commands, or ENTER to resume.
> help

available commands:
 afc  [value]             - append to status code filter 
 fc   [value]             - (re)configure status code filter 
 afl  [value]             - append to line count filter 
 fl   [value]             - (re)configure line count filter 
 afw  [value]             - append to word count filter 
 fw   [value]             - (re)configure word count filter 
 afs  [value]             - append to size filter 
 fs   [value]             - (re)configure size filter 
 aft  [value]             - append to time filter 
 ft   [value]             - (re)configure time filter 
 rate [value]             - adjust rate of requests per second (active: 0)
 queueshow                - show job queue
 queuedel [number]        - delete a job in the queue
 queueskip                - advance to the next queued job
 restart                  - restart and resume the current ffuf job
 resume                   - resume current ffuf job (or: ENTER) 
 show                     - show results for the current job
 savejson [filename]      - save current matches to a file
 help                     - you are looking at it
> 
```

neste modo, os filtros podem ser reconfigurados, gerenciados em filas e o estado atual salvo em disco.

Quando (re)configurando os filtros, eles são aplicados postumamente e todos os falsos positivos correspondências da memória que
teria sido filtrado pelos filtros recém-adicionados são excluídos.

O novo estado de correspondências pode ser impresso com um comando `show` que irá imprimir todas as correspondências como eles
teria sido encontrado pelo `ffuf`.

Como as partidas "negativas" não são armazenadas na memória, relaxar os filtros não pode, infelizmente, trazer de volta as partidas perdidas.
Para este tipo de cenário, o usuário é capaz de usar o comando `restart`, que reinicia o estado e inicia o atual
trabalho desde o início.

<p align="center">
  <img width="250" src="../../99-Assets/upstream/ffuf/_img/ffuf_waving_250.png">
</p>

## Contribuir

Relatórios de erros, requisições de recursos e requisições são bem- vindos. Veja
[CONTRIBUIÇÃO. md](https://github.com/ffuf/ffuf/blob/8d65e0373e5f223530174e5694285af849770078/CONTRIBUTING.md) para começar, e o
[Seção Contribuinte do wiki](https://github.com/ffuf/ffuf/wiki/Contributing) para
A documentação da arquitectura e dos ensaios.

## Licença

ffuf é lançado sob licença do MIT. Veja [LICENÇA](https://github.com/ffuf/ffuf/blob/master/LICENSE).


---

## Procedência desta tradução

Fonte: [https://github.com/ffuf/ffuf](https://github.com/ffuf/ffuf/blob/8d65e0373e5f223530174e5694285af849770078/README.md). Licença: [MIT](../../99-Assets/upstream/ffuf/LICENSE.txt). Commit: 8d65e0373e5f223530174e5694285af849770078.

O original preservado, a lista de mudanças de apresentação e os hashes constam no manifesto do projeto. Nenhum exemplo desta documentação foi executado automaticamente.
