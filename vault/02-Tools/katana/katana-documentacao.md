---
title: "katana — documentação oficial"
type: "official-documentation"
tool: "katana"
status: "translated-machine"
reviewed: "2026-10-26"
language: "pt-BR"
tags: ["documentation", "tool/katana"]
cssclasses: ["fieldbook"]
source_url: "https://github.com/projectdiscovery/katana/blob/4b41dd02a095df15ae0cd04cbb658af457d3c1ab/README.md"
source_commit: "4b41dd02a095df15ae0cd04cbb658af457d3c1ab"
source_sha256: "7f6cf81d98053ab01a802aecb0bf3f01fca797e7b0313b82f692625959188c5b"
license_spdx: "MIT"
human_review: "pending"
source_scope: "Official English repository README/docs and available upstream Portuguese README; external manuals/wiki coverage tracked separately"
---

> Tradução automática local para português, ainda sem revisão humana integral. Estrutura e blocos de código preservados; referências externas não significam conteúdo espelhado.

<h1 align="center">
  
  <br>
</h1>

<h4 align="center">A armação de rastejamento e aranha de próxima geração</h4>

<p align="center">
<a href="https://goreportcard.com/report/github.com/projectdiscovery/katana"></a>
<a href="https://github.com/projectdiscovery/katana/issues"></a>
<a href="https://github.com/projectdiscovery/katana/releases"></a>
<a href="https://twitter.com/pdiscoveryio"></a>
<a href="https://discord.gg/projectdiscovery"></a>
</p>

<p align="center">
<a href="#features">Características</a> •
<a href="#instalação">Instalação</a> •
<a href="#uso">Usage</a> •
<a href="#controlo-do-âmbito-de-aplicação">Scope</a> •
<a href="#configuração-do-crawler">Config</a> •
<a href="#filtros">Filters</a> •
<a href="https://discord.gg/projectdiscovery">Join Discord</a>
</p>


# Features

[Imagem/recurso externo: image](https://user-images.githubusercontent.com/8293321/199371558-daba03b6-bf9c-4883-8506-76497c6c3a44.png)

 - Rastreamento web rápido e totalmente configurável
 - Modo **Standard** e **Headless**
 - **JavaScript** análise / rastreamento
 - **preenchimento de formulário automático personalizável**
 - Controle **Scope** - Campo pré-configurado / Regex
 - **Knowledge base** - ML tipo de página / classificação de formulário (modelo baixado automaticamente)
 - **Saída personalizada** - Campos pré-configurados
 - INPUT - **STDIN**, **URL** e **LISTA**
 - OutPUT - **STDOUT**, **FILE** e **SON**


<a id="installation"></a>
## Instalação

katana requer Go 1.26.10+ para instalar com sucesso. Se você encontrar qualquer problema de instalação, recomendamos tentar com a versão mais recente disponível do Go, uma vez que a versão mínima necessária pode ter mudado. Execute o comando abaixo ou baixe um binário pré-compilado do [página de lançamento](https://github.com/projectdiscovery/katana/releases).

```console
CGO_ENABLED=1 go install github.com/projectdiscovery/katana/cmd/katana@latest
```

**Mais opções para instalar/ executar o katana-**

<details>
    <summary>Acoplamento</summary>

> Para instalar / atualizar docker para a última tag -

```sh
docker pull projectdiscovery/katana:latest
```

> Para executar katana no modo padrão usando docker -


```sh
docker run projectdiscovery/katana:latest -u https://tesla.com
```

> Para executar katana em modo sem cabeça usando docker -

```sh
docker run projectdiscovery/katana:latest -u https://tesla.com -system-chrome -headless
```

</details>

<details>
    <summary>Ubuntu</summary>

> Recomenda-se instalar os seguintes pré-requisitos -

```sh
sudo apt update
sudo apt install zip curl wget git snapd
sudo snap refresh
sudo snap install golang --classic

sudo install -d -m 0755 /etc/apt/keyrings
curl -fsSL https://dl.google.com/linux/linux_signing_key.pub \
  | sudo gpg --dearmor -o /etc/apt/keyrings/google-chrome.gpg

echo "deb [arch=amd64 signed-by=/etc/apt/keyrings/google-chrome.gpg] \
  http://dl.google.com/linux/chrome/deb/ stable main" \
  | sudo tee /etc/apt/sources.list.d/google-chrome.list > /dev/null

sudo apt update
sudo apt install google-chrome-stable
```

> instalar katana -


```sh
go install github.com/projectdiscovery/katana/cmd/katana@latest
```

</details>

<a id="usage"></a>
## Uso

```console
katana -h
```

Isto irá mostrar a ajuda para a ferramenta. Aqui estão todos os interruptores que suporta.

```console
Katana is a fast crawler focused on execution in automation
pipelines offering both headless and non-headless crawling.

Usage:
  ./katana [flags]

Flags:
INPUT:
   -u, -list string[]     target url / list to crawl
   -resume string         resume scan using resume.cfg
   -e, -exclude string[]  exclude host matching specified filter ('cdn', 'private-ips', cidr, ip, regex)

CONFIGURATION:
   -r, -resolvers string[]       list of custom resolver (file or comma separated)
   -d, -depth int                maximum depth to crawl (default 3)
   -jc, -js-crawl                enable endpoint parsing / crawling in javascript file
   -jsl, -jsluice                enable jsluice parsing in javascript file (memory intensive)
   -ct, -crawl-duration value    maximum duration to crawl the target for (s, m, h, d) (default s)
   -kf, -known-files string      enable crawling of known files (all,robotstxt,sitemapxml), a minimum depth of 3 is required to ensure all known files are properly crawled.
   -mrs, -max-response-size int  maximum response size to read (default 4194304)
   -timeout int                  time to wait for request in seconds (default 10)
   -aff, -automatic-form-fill    enable automatic form filling (experimental)
   -fx, -form-extraction         extract form, input, textarea & select elements in jsonl output
   -retry int                    number of times to retry the request (default 1)
   -proxy string                 http/socks5 proxy to use
   -td, -tech-detect             enable technology detection
   -H, -headers string[]         custom header/cookie to include in all http request in header:value format (file)
   -config string                path to the katana configuration file
   -fc, -form-config string      path to custom form configuration file
   -flc, -field-config string    path to custom field configuration file
   -s, -strategy string          Visit strategy (depth-first, breadth-first) (default "depth-first")
   -iqp, -ignore-query-params    Ignore crawling same path with different query-param values
   -fsu, -filter-similar         filter crawling of similar looking URLs (e.g., /users/123 and /users/456)
   -fst, -filter-similar-threshold int  number of distinct values before a path position is treated as parameter (default 10)
   -tlsi, -tls-impersonate       enable experimental client hello (ja3) tls randomization
   -dr, -disable-redirects       disable following redirects (default false)
   -pcs, -page-content-similar   enable page content similarity filtering (simhash|tfidf|bm25)
   -pcsm, -page-content-similar-mode string  similarity mode: simhash, tfidf, or bm25 (default simhash)
   -pcsd, -page-content-similar-distance int  simhash max hamming distance (default 3)
   -pcst, -page-content-similar-threshold float  tfidf/bm25 min score 0-1 (default 0.85)
   -pcsn, -page-content-similar-budget int  pages to fully process per similarity cluster (default 1)
   -sdd, -similarity-deduplication  alias for -pcs
   -kb, -knowledge-base          enable knowledge base classification
   -kb-secrets                   enable secrets extractor in the knowledge base
   -kb-validate-secrets          validate detected secrets against their provider (sends live API calls)
   -kb-endpoints                 enable endpoints extractor (classifies REST/GraphQL/SOAP/XHR requests)
   -mdp, -max-domain-pages int   maximum number of pages to crawl per domain (default unlimited)

DEBUG:
   -health-check, -hc        run diagnostic check up
   -elog, -error-log string  file to write sent requests error log
   -pprof-server             enable pprof server

HEADLESS:
   -hl, -headless                    enable headless hybrid crawling (experimental)
   -sc, -system-chrome               use local installed chrome browser instead of katana installed
   -sb, -show-browser                show the browser on the screen with headless mode
   -ho, -headless-options string[]   start headless chrome with additional options
   -nos, -no-sandbox                 start headless chrome in --no-sandbox mode
   -cdd, -chrome-data-dir string     path to store chrome browser data
   -scp, -system-chrome-path string  use specified chrome browser for headless crawling
   -noi, -no-incognito               start headless chrome without incognito mode
   -cwu, -chrome-ws-url string       use chrome browser instance launched elsewhere with the debugger listening at this URL
   -xhr, -xhr-extraction             extract xhr request url,method in jsonl output
   -pls, -page-load-strategy string  page load strategy (heuristic, load, domcontentloaded, networkidle, none) (default "heuristic")
   -dwt, -dom-wait-time int          time in seconds to wait after page load when using domcontentloaded strategy (default 5)
   -csp, -captcha-solver-provider string  captcha solver provider (e.g. capsolver)
   -csk, -captcha-solver-key string       captcha solver provider api key

SCOPE:
   -cs, -crawl-scope string[]       in scope url regex to be followed by crawler
   -cos, -crawl-out-scope string[]  out of scope url regex to be excluded by crawler
   -fs, -field-scope string         pre-defined scope field (dn,rdn,fqdn) or custom regex (e.g., '(company-staging.io|company.com)') (default "rdn")
   -ns, -no-scope                   disables host based default scope
   -do, -display-out-scope          display external endpoint from scoped crawling

FILTER:
   -mr, -match-regex string[]             regex or list of regex to match on output url (cli, file)
   -fr, -filter-regex string[]            regex or list of regex to filter on output url (cli, file)
   -f, -field string                      field to display in output (url,path,fqdn,rdn,rurl,qurl,qpath,file,ufile,key,value,kv,dir,udir) (Deprecated: use -output-template instead)
   -sf, -store-field string               field to store in per-host output (url,path,fqdn,rdn,rurl,qurl,qpath,file,ufile,key,value,kv,dir,udir)
   -em, -extension-match string[]         match output for given extension (eg, -em php,html,js,none)
   -ef, -extension-filter string[]        filter output for given extension (eg, -ef png,css)
   -ndef, -no-default-ext-filter bool     remove default extensions from the filter list
   -mdc, -match-condition string          match response with dsl based condition
   -fdc, -filter-condition string         filter response with dsl based condition
   -duf, -disable-unique-filter           disable duplicate content filtering
   -filter-page-type string[]      filter response with page type (e.g. error,captcha,parked)

RATE-LIMIT:
   -c, -concurrency int          number of concurrent fetchers to use (default 10)
   -p, -parallelism int          number of concurrent inputs to process (default 10)
   -rd, -delay int               request delay between each request in seconds
   -rl, -rate-limit int          maximum requests to send per second (default 150)
   -rlm, -rate-limit-minute int  maximum number of requests to send per minute
   -hrl, -host-rate-limit int    maximum requests to send per second per host
   -hrlm, -host-rate-limit-minute int  maximum number of requests to send per minute per host

UPDATE:
   -up, -update                 update katana to latest version
   -duc, -disable-update-check  disable automatic katana update check

OUTPUT:
   -o, -output string                file to write output to
   -output-template string      custom output template
   -sr, -store-response              store http requests/responses
   -srd, -store-response-dir string  store http requests/responses to custom directory
   -ncb, -no-clobber                 do not overwrite output file
   -sfd, -store-field-dir string     store per-host field to custom directory
   -or, -omit-raw                    omit raw requests/responses from jsonl output
   -ob, -omit-body                   omit response body from jsonl output
   -lof, -list-output-fields         list available fields for jsonl output format
   -eof, -exclude-output-fields      exclude fields from jsonl output
   -j, -jsonl                        write output in jsonl format
   -nc, -no-color                    disable output content coloring (ANSI escape codes)
   -silent                           display output only
   -v, -verbose                      display verbose output
   -debug                            display debug output
   -version                          display project version
```

<a id="running-katana"></a>
## A executar o Katana

<a id="input-for-katana"></a>
### Entrada para katana

**katana** requer **url** ou **endpoint** para rastejar e aceita entradas únicas ou múltiplas.

A URL de entrada pode ser fornecida usando a opção `-u`, e vários valores podem ser fornecidos usando a entrada separada por vírgulas, da mesma forma a entrada **file** é suportada usando a opção `-list` e adicionalmente a entrada (stdin) é suportada.

<a id="url-input"></a>
#### Entrada do URL

```sh
katana -u https://tesla.com
```

<a id="multiple-url-input-comma-separated"></a>
#### Entrada de URL múltipla (separada por vírgulas)

```sh
katana -u https://tesla.com,https://google.com
```

<a id="list-input"></a>
#### Input da Lista
```bash
$ cat url_list.txt

https://tesla.com
https://google.com
```

```text
katana -list url_list.txt
```

<a id="stdin-piped-input"></a>
#### Entrada de DSTIN (piped)

```sh
echo https://tesla.com | katana
```

```sh
cat domains | httpx | katana
```

<a id="page-content-similarity"></a>
### Similaridade do Conteúdo da Página

Filtragem opcional da camada-2 após o dedup de conteúdo MD5 exato.`nav`/`header`/`footer`/scripts), em seguida, um dos três modos decide se uma página é similar o suficiente para pular mais parse/enqueue (orçamento do cluster).`-fsu`) continua independente.

|Modo|Bandeira|Melhor para|
|------|------|----------|
|`simhash` (por omissão)|`-pcsm simhash`|Clones / modelo quase duplicados (Hamming via `-pcsd`)|
|`tfidf`|`-pcsm tfidf`|Semelhança cossena tópica (`-pcst`)|
|`bm25`|`-pcsm bm25`|Semelhança tópica com normalização de comprimento (`-pcst`)|

```sh
# Near-duplicate detection (default mode)
katana -u https://example.com -pcs

# TF-IDF topical filtering with higher budget
katana -u https://shop.example.com -pcs -pcsm tfidf -pcst 0.85 -pcsn 2

# BM25 mode
katana -u https://example.com -pcs -pcsm bm25

# Alias from older flag name
katana -u https://example.com -sdd -pcsm simhash
```

Estatísticas de conclusão de exemplo:
```console
[INF] Content similarity (simhash): 103 processed, 30 accepted, 73 filtered - 70.9% filter rate
[INF] Crawl completed in 14s. 21 endpoints found.
```

Exemplo em execução do katana -

```console
katana -u https://youtube.com

   __        __                
  / /_____ _/ /____ ____  ___ _
 /  '_/ _  / __/ _  / _ \/ _  /
/_/\_\\_,_/\__/\_,_/_//_/\_,_/ v0.0.1                     

      projectdiscovery.io

[WRN] Use with caution. You are responsible for your actions.
[WRN] Developers assume no liability and are not responsible for any misuse or damage.
https://www.youtube.com/
https://www.youtube.com/about/
https://www.youtube.com/about/press/
https://www.youtube.com/about/copyright/
https://www.youtube.com/t/contact_us/
https://www.youtube.com/creators/
https://www.youtube.com/ads/
https://www.youtube.com/t/terms
https://www.youtube.com/t/privacy
https://www.youtube.com/about/policies/
https://www.youtube.com/howyoutubeworks?utm_campaign=ytgen&utm_source=ythp&utm_medium=LeftNav&utm_content=txt&u=https%3A%2F%2Fwww.youtube.com%2Fhowyoutubeworks%3Futm_source%3Dythp%26utm_medium%3DLeftNav%26utm_campaign%3Dytgen
https://www.youtube.com/new
https://m.youtube.com/
https://www.youtube.com/s/desktop/4965577f/jsbin/desktop_polymer.vflset/desktop_polymer.js
https://www.youtube.com/s/desktop/4965577f/cssbin/www-main-desktop-home-page-skeleton.css
https://www.youtube.com/s/desktop/4965577f/cssbin/www-onepick.css
https://www.youtube.com/s/_/ytmainappweb/_/ss/k=ytmainappweb.kevlar_base.0Zo5FUcPkCg.L.B1.O/am=gAE/d=0/rs=AGKMywG5nh5Qp-BGPbOaI1evhF5BVGRZGA
https://www.youtube.com/opensearch?locale=en_GB
https://www.youtube.com/manifest.webmanifest
https://www.youtube.com/s/desktop/4965577f/cssbin/www-main-desktop-watch-page-skeleton.css
https://www.youtube.com/s/desktop/4965577f/jsbin/web-animations-next-lite.min.vflset/web-animations-next-lite.min.js
https://www.youtube.com/s/desktop/4965577f/jsbin/custom-elements-es5-adapter.vflset/custom-elements-es5-adapter.js
https://www.youtube.com/s/desktop/4965577f/jsbin/webcomponents-sd.vflset/webcomponents-sd.js
https://www.youtube.com/s/desktop/4965577f/jsbin/intersection-observer.min.vflset/intersection-observer.min.js
https://www.youtube.com/s/desktop/4965577f/jsbin/scheduler.vflset/scheduler.js
https://www.youtube.com/s/desktop/4965577f/jsbin/www-i18n-constants-en_GB.vflset/www-i18n-constants.js
https://www.youtube.com/s/desktop/4965577f/jsbin/www-tampering.vflset/www-tampering.js
https://www.youtube.com/s/desktop/4965577f/jsbin/spf.vflset/spf.js
https://www.youtube.com/s/desktop/4965577f/jsbin/network.vflset/network.js
https://www.youtube.com/howyoutubeworks/
https://www.youtube.com/trends/
https://www.youtube.com/jobs/
https://www.youtube.com/kids/
```


<a id="crawling-mode"></a>
## Modo de Rastejamento

<a id="standard-mode"></a>
### Modo Padrão

A modalidade de rastreamento padrão usa a biblioteca padrão ir http sob o capô para lidar com solicitações/respostas do HTTP. Esta modalidade é muito mais rápida, uma vez que não tem a sobrecarga do navegador. Ainda assim, ele analisa o corpo de respostas do HTTP como é, sem qualquer renderização de javascript ou DOM, terminais potencialmente ausentes pós-dom-rendered ou chamadas de endpoint assíncronas que podem acontecer em aplicações web complexas, dependendo, por exemplo, de eventos específicos do navegador.

<a id="headless-mode"></a>
### Modo sem cabeça

O modo sem cabeça liga chamadas internas sem cabeça para lidar com pedidos/respostas HTTP diretamente dentro do contexto do navegador. Isso oferece duas vantagens:
- A impressão digital HTTP (TLS e agente de usuário) identifica totalmente o cliente como um navegador legítimo
- Melhor cobertura uma vez que os endpoints são descobertos analisando a resposta bruta padrão, como na modalidade anterior, e também o navegador-renderizado com javascript habilitado.

O rastreamento sem cabeça é opcional e pode ser ativado usando a opção `-headless`.

Aqui estão outras opções de CLI sem cabeça -

```console
katana -h headless

Flags:
HEADLESS:
   -hl, -headless                    enable headless hybrid crawling (experimental)
   -sc, -system-chrome               use local installed chrome browser instead of katana installed
   -sb, -show-browser                show the browser on the screen with headless mode
   -ho, -headless-options string[]   start headless chrome with additional options
   -nos, -no-sandbox                 start headless chrome in --no-sandbox mode
   -cdd, -chrome-data-dir string     path to store chrome browser data
   -scp, -system-chrome-path string  use specified chrome browser for headless crawling
   -noi, -no-incognito               start headless chrome without incognito mode
   -cwu, -chrome-ws-url string       use chrome browser instance launched elsewhere with the debugger listening at this URL
   -xhr, -xhr-extraction             extract xhr requests
   -pls, -page-load-strategy string  page load strategy (heuristic, load, domcontentloaded, networkidle, none) (default "heuristic")
   -dwt, -dom-wait-time int          time in seconds to wait after page load when using domcontentloaded strategy (default 5)
   -csp, -captcha-solver-provider string  captcha solver provider (e.g. capsolver)
   -csk, -captcha-solver-key string       captcha solver provider api key
   -al, -auto-login string           automatic login with username:password (headless only)
   -rf, -recorded-flow string        chrome DevTools Recorder JSON (or explicit steps) to replay before crawl (headless only)
```

<a id="interactive-ui-exploration"></a>
### Exploração interactiva de IU

Use o `-interactive` para explorar estados clicáveis no navegador sem cabeça puro. Ele permite o modo sem cabeça, inicia na página de destino, clica primeiro na profundidade dos candidatos e restaura um estado pai antes de tentar o seu próximo controle. O `-interaction-depth` conta transições de estado bem- sucedidas, de modo que uma profundidade de 4 explora quatro cliques da página inicial. Este modo é mais lento do que o rastreamento sem cabeça normal porque uma ramificação pode precisar de ser reproduzida depois de um clique alterar a página.

```console
katana -u https://example.com/app -interactive -interaction-depth 4 \
  -interaction-max-states 500 -interaction-max-actions 2000 \
  -interaction-settle 2s -interaction-duration 5m -crawl-duration 20m
```

`-interaction-selector` e `-interaction-exclude` aceitam seletores de CSS. O conjunto de candidatos padrão inclui botões, links, controles comuns de ARIA, manipuladores de cliques em linha e ouvintes de cliques observados. Após a exploração de UI, Katana continua seu rastreamento de URL normal sem cabeça. Use `-interaction-duration` para reservar tempo para esse rastreamento dentro do `-crawl-duration`. Defina um limite de ação ou estado para `0` para remover esse limite.

A opção `-H` existente também se aplica ao rastreamento sem cabeça. Os valores do `Cookie` são semeados no navegador antes da navegação, e outros cabeçalhos são anexados às solicitações que o escopo de rastreamento aceita. Novas abas abertas por um clique são exploradas quando sua URL está no escopo. Seletores não podem alcançar cada controle de tela, raiz de sombra fechada, ou quadro de origem cruzada, então inspecione o resumo do rastreamento ao avaliar a cobertura.

*`-no-sandbox`*
----

Executa navegador cromo sem cabeça com **no-sandbox** opção, útil quando rodando como usuário root.

```console
katana -u https://tesla.com -headless -no-sandbox
```

*`-no-incognito`*
----

Executa navegador cromado sem cabeça sem modo incógnito, útil ao usar o navegador local.

```console
katana -u https://tesla.com -headless -no-incognito
```

Para preservar os cookies e outros dados de sessão do navegador através de corridas, combinar `-no-incognito` com `-chrome-data-dir` para Katana reutiliza seu diretório de perfil Chrome escolhido em vez de um temporário isolado.

```console
katana -u https://tesla.com -headless -no-incognito -chrome-data-dir /tmp/katana-profile
```

*`-headless-options`*
----

Ao rastejar em modo sem cabeça, opções adicionais de cromo podem ser especificadas usando `-headless-options`, por exemplo -


```console
katana -u https://tesla.com -headless -system-chrome -headless-options --disable-gpu,proxy-server=http://127.0.0.1:8080
```

*`-page-load-strategy`*
----

Controla como o katana espera que as páginas carreguem no modo sem cabeça. Estratégias diferentes são úteis para diferentes tipos de aplicações web:

|Estratégia|Designação das mercadorias|
|----------|-------------|
|`heuristic`|(padrão) Espera inteligente que se adapta ao comportamento da página - espera por evento de carga, rede ociosa e estabilidade DOM|
|`load`|Espera apenas pelo evento de carga do navegador|
|`domcontentloaded`|Espera pelo evento DOMContentLoaded mais tempo adicional (configurado via `-dwt`) para renderização em JavaScript|
|`networkidle`|Espera que a atividade da rede pare|
|`none`|Sem espera - retorna imediatamente após o início da navegação|

```console
katana -u https://tesla.com -headless -pls domcontentloaded
```

A estratégia `domcontentloaded` é particularmente útil para aplicações de página única (SPAs) que nunca completam completamente o carregamento devido a solicitações de fundo contínuas (websockets, votação, etc.).

*`-dom-wait-time`*
----

Ao usar a estratégia de carga da página `domcontentloaded`, esta opção especifica quantos segundos esperar após o incêndio do evento DOMContentLoaded. Isto permite que o JavaScript renderize elementos interativos. O padrão é de 5 segundos.

```console
katana -u https://tesla.com -headless -pls domcontentloaded -dwt 10
```


<a id="captcha-solving"></a>
### Resolução do Captcha

Katana suporta detecção e resolução de captchas automáticas durante o rastreamento sem cabeça. Quando uma página captcha é encontrada, o katana identifica o provedor captcha, resolve-o através de um serviço externo e continua rastejando.

Tipos de captcha suportados: **reCAPTCHA v2**, **reCAPTCHA v3**, **ReCAPTCHA Enterprise**, **Turno de chama em nuvem**, **hCaptcha**

*`-captcha-solver-provider`*
----

Opção para indicar o provedor de solução captcha. Atualmente suportado: `capsolver`.

*`-captcha-solver-key`*
----

Chave API para o provedor de solução captcha.

```console
katana -u https://example.com -headless -csp capsolver -csk YOUR_API_KEY
```

O provedor e a chave também podem ser definidos através de variáveis de ambiente:

```console
export CAPTCHA_SOLVER_PROVIDER=capsolver
export CAPTCHA_SOLVER_KEY=YOUR_API_KEY
katana -u https://example.com -headless
```

<a id="scope-control"></a>
## Controlo do âmbito de aplicação

Crawling pode ser interminável se não escopo, como tal katana vem com suporte múltiplo para definir o escopo de rastreamento.

*`-field-scope`*
----
Opção mais útil para definir escopo com nome de campo predefinido, `rdn` sendo a opção padrão para escopo de campo.

   - `rdn` - rastreando escopo para o nome de domínio root e todos os subdomínios (por exemplo, `*example.com`) (padrão)
   - `fqdn` - rastejando ao alcance de determinado sub(domínio) (por exemplo, `www.example.com` ou `api.example.com`)
   - `dn` - rastejando ao alcance da palavra-chave de nome de domínio (por exemplo, `example`)

```console
katana -u https://tesla.com -fs dn
```


*`-crawl-scope`*
------

Para controle de escopo avançado, a opção `-cs` pode ser usada que vem com suporte **regex**.

```console
katana -u https://tesla.com -cs login
```

Para várias regras de escopo, a entrada de arquivo com string / regex multilinha pode ser passada.

```bash
$ cat in_scope.txt

login/
admin/
app/
wordpress/
```

```console
katana -u https://tesla.com -cs in_scope.txt
```


*`-crawl-out-scope`*
-----

Para definir o que não rastejar, `-cos` opção pode ser usado e também suporta **regex** entrada.

```console
katana -u https://tesla.com -cos logout
```

Para várias regras fora do escopo, a entrada do arquivo com string / regex multilinha pode ser passada.

```bash
$ cat out_of_scope.txt

/logout
/log_out
```

```console
katana -u https://tesla.com -cos out_of_scope.txt
```

*`-no-scope`*
----

Katana é padrão para escopo `*.domain`, para desativar esta opção `-ns` pode ser usado e também para rastejar na internet.

```console
katana -u https://tesla.com -ns
```

*`-display-out-scope`*
----

Como padrão, quando a opção escopo é usada, ele também se aplica para os links para exibir como saída, como tal ** URLs externas são padrão para excluir** e para substituir este comportamento, `-do` opção pode ser usado para exibir todas as URLs externas que existem em alvos URL / Endpoint.

```text
katana -u https://tesla.com -do
```

Aqui estão todas as opções CLI para o controle de escopo -


```console
katana -h scope

Flags:
SCOPE:
   -cs, -crawl-scope string[]       in scope url regex to be followed by crawler
   -cos, -crawl-out-scope string[]  out of scope url regex to be excluded by crawler
   -fs, -field-scope string         pre-defined scope field (dn,rdn,fqdn) (default "rdn")
   -ns, -no-scope                   disables host based default scope
   -do, -display-out-scope          display external endpoint from scoped crawling
```


<a id="crawler-configuration"></a>
## Configuração do Crawler

Katana vem com várias opções para configurar e controlar o rastreamento como queremos.

*`-depth`*
----

Opção para definir o `depth` para seguir as urls para rastejar, mais profundidade o maior número de endpoint sendo rastreado + tempo para rastejar.

```text
katana -u https://tesla.com -d 5
```

*`-js-crawl`*
----

Opção para ativar a análise de arquivos JavaScript + rastreamento dos endpoints descobertos em arquivos JavaScript, desativados como padrão.

```text
katana -u https://tesla.com -jc
```

*`-crawl-duration`*
----

Opção para a duração predefinida do rastreamento, desabilitada como padrão.

```text
katana -u https://tesla.com -ct 2
```

*`-known-files`*
----
Opção para activar o arquivo `robots.txt` e `sitemap.xml`, desactivados por omissão.

```text
katana -u https://tesla.com -kf robotstxt,sitemapxml
```

*`-automatic-form-fill`*
----

Opção para habilitar preenchimento automático de formulários para campos conhecidos / desconhecidos, os valores de campos conhecidos podem ser personalizados conforme necessário, atualizando o arquivo de configuração de formulários no `$HOME/.config/katana/form-config.yaml`.

O preenchimento automático do formulário é uma característica experimental.

```text
katana -u https://tesla.com -aff
```

Os valores de configuração do formulário suportam as funções de ajuda DSL para a geração dinâmica de dados. Todas as funções `rand_*` da biblioteca [projectodescoberta/dsl](https://github.com/projectdiscovery/dsl) estão disponíveis:

```yaml
# $HOME/.config/katana/form-config.yaml
email: "rand_email()"
phone: "rand_phone()"
placeholder: "rand_first_name()"
password: 'rand_base(16, "")'
color: "#e66465"
```

*`-filter-similar`*
----

Uma opção para filtrar o rastreamento de URLs semelhantes, normalizando segmentos de caminhos variáveis. Isto detecta IDs, UUIDs, hashes, datas e outros valores dinâmicos, e também aprende padrões repetidos no tempo de execução. Por exemplo, `/users/123` e `/users/456` são tratados como o mesmo ponto final.

```text
katana -u https://tesla.com -fsu
```

O limiar de promoção (quantos valores distintos em uma posição de caminho antes de ser tratado como um parâmetro) pode ser sintonizado com `-fst`. Valores menores são mais agressivos (menos URLs rastreadas), valores maiores são mais permissivos. O padrão é `10`.

```text
katana -u https://tesla.com -fsu -fst 5
```

*`-max-domain-pages`*
----

Opção para limitar o número de páginas rastejadas por domínio. Impede qualquer domínio de consumir todo o orçamento de rastreamento, útil para grandes sites ou proteção armadilha rastreador.

```text
katana -u https://tesla.com -mdp 100
```

<a id="knowledge-base-classification"></a>
## Classificação da Base de Conhecimentos

Katana pode enriquecer os resultados de rastreamento com uma base **knowledge** — classificação machine-learning de cada página rastreada alimentado por [dit](https://github.com/HappyHackingSpace/dit). Quando habilitado, cada resposta é classificada por **page tipo** (por exemplo, `login`, `error`, `captcha`, `parked`) e quaisquer formulários na página são identificados, com o resultado anexado ao campo `knowledgebase` da saída JSONL. Isto funciona através de **all motores** (padrão e sem cabeça).

> **Note**: O modelo de classificação é ** baixado automaticamente** no primeiro uso para `~/.dit/model.json` (de [Abraçar o Rosto](https://huggingface.co/datasets/happyhackingspace/dit)). Este é um custo de uma vez, por máquina — as execuções subsequentes reutilizam o modelo em cache. Nenhuma instalação manual do `dit` é necessária.

*`-knowledge-base`*
----

Activar a classificação da base de conhecimentos. A classificação do tipo de página e do formulário é adicionada ao campo `knowledgebase` de cada resultado.

```console
katana -u https://example.com -kb -jsonl
```

```json
{
  "timestamp": "...",
  "request": { "...": "..." },
  "response": {
    "...": "...",
    "knowledgebase": {
      "PageType": "login",
      "Forms": [{ "type": "login", "fields": { "username": "username or email", "password": "password" } }]
    }
  }
}
```

*`-filter-page-type`*
----

Filtrar os resultados apenas para o( s) tipo( s) de página indicado( s). Habilitar isso implica `-kb` (o classificador é inicializado automaticamente).

```console
katana -u https://example.com -fpt login,error
```

*`-kb-secrets`*
----

Habilite o extrator de segredos na base de conhecimento, surfaceing detected secrets (API chaves, tokens, etc.) sob a chave `secrets`. Adicione `-kb-validate-secrets` para validar os segredos detectados contra seu provedor — note que **sends vive API calls**.

```console
katana -u https://example.com -kb-secrets
```

*`-kb-endpoints`*
----

Habilite o extrator de endpoints, que classifica as solicitações como REST, GraphQL, SOAP ou XHR sob a tecla `endpoints`.

```console
katana -u https://example.com -kb-endpoints
```

<a id="authenticated-crawling"></a>
## Rastejamento Autenticado

Katana suporta rastreamento autenticado de várias maneiras: cabeçalhos estáticos/cookies, anexando a uma sessão Chrome já registrada, login de formulário automático (`-auto-login`), e **fluxos de navegador gravados** (`-recorded-flow`) para logins multi-passo / SPA / SSO-estilo.

<a id="headers--cookies"></a>
### Cabeçalhos / cookies

O rastreamento autenticado pode incluir cabeçalhos personalizados ou cookies em pedidos HTTP para acessar recursos protegidos. Você pode especificar cabeçalhos diretamente na linha de comando ou fornecê-los como um arquivo.

> **Note**: Para a abordagem header/cookie, execute a autenticação manualmente uma vez e exporte o cookie/header da sessão para usar com katana.

*`-headers`*
----

Opção para adicionar um cabeçalho ou cookie personalizado à solicitação.
> Sintaxe de [cabeçalhos](https://datatracker.ietf.org/doc/html/rfc7230#section-3.2) na especificação HTTP

Aqui está um exemplo de adição de um cookie à solicitação:
```text
katana -u https://tesla.com -H 'Cookie: usrsess=AmljNrESo'
```

Também é possível fornecer cabeçalhos ou cookies como um arquivo. Por exemplo:

```text
$ cat cookie.txt

Cookie: PHPSESSIONID=XXXXXXXXX
X-API-KEY: XXXXX
TOKEN=XX
```

```text
katana -u https://tesla.com -H cookie.txt
```

<a id="automatic-login--auto-login"></a>
### Login automático (`-auto-login`)

No modo sem cabeça puro, o katana pode detectar um formulário de login e enviar credenciais automaticamente:

```console
katana -hl -u https://app.example.com -al 'user:password'
```

Isto é melhor para formas simples de nome de usuário/senha. Para logins multi-passo, SPA ou SSO preferem um fluxo gravado.

<a id="recorded-flow--recorded-flow"></a>
### Fluxo registado (`-recorded-flow`)

Fluxos gravados permitem exportar um login de navegador real de **Chrome DevTools → Gravador** e reproduzi-lo uma vez ** antes do crawl starts**. Cookies de sessão e armazenamento web de origem mesma ficar no contexto do navegador sem cabeça para o resto do crawl.

**1. Grave o login no Chrome**

1. Open Chrome DevTools → **Recorder**
2. Iniciar uma nova gravação e executar o login (navegar, digitar, clicar em Próximo, digitar senha, enviar, ...)
3. Exportar a gravação como JSON

**2. Reproduza com katana**

```console
katana -hl -u https://app.example.com/dashboard \
  -rf login.json \
  -al 'user:password'
```

Os literais credenciais na gravação são substituídos por `{{username}}` / `{{password}}` placeholders e preenchidos a partir de `-al`. Se a gravação (ou uma lista de passos explícita) ainda precisa desses placeholders, `-al` é necessário.

Katana também aceita um arquivo de passo explícito de autoria manual:

```json
{
  "steps": [
    {"action": "navigate", "value": "https://app.example.com/login"},
    {"action": "fill", "selector": "#email", "value": "{{username}}"},
    {"action": "fill", "selector": "#password", "value": "{{password}}"},
    {"action": "click", "selector": "#submit"}
  ]
}
```

Acções de acompanhamento: `navigate`, `fill`, `click`, `doubleclick`, `waitvisible`, `wait`, `press`, `submit`.

**Como funciona**

1. Katana lança Chrome sem cabeça
2. Captura o estado anônimo do navegador e, em seguida, reproduz o fluxo gravado uma vez
3. Verifica se um cookie ou o mesmo valor de armazenamento web de origem mudaram; caso contrário, tenta o `-auto-login` como um recurso
4. Inicia o rastreamento do `-u` com a sessão estabelecida
5. Ignora os URLs de saída enquanto autenticados

Para aplicações que mantêm a autenticação inteiramente do lado do servidor sem alterar
cookies ou armazenamento web, terminar um fluxo explícito com `waitvisible` visando um
elemento que só existe após o login. Uma verificação de visibilidade de terminal bem- sucedida é
tratado como a afirmação explícita de autenticação do fluxo.

> Fluxos gravados requerem **pure sem cabeça** (`-hl`). Híbrido (`-hh`) é desativado automaticamente quando `-rf` é definido.

Existem mais opções para configurar quando necessário, aqui estão todas as opções de CLI relacionadas à configuração -

```console
katana -h config

Flags:
CONFIGURATION:
   -r, -resolvers string[]       list of custom resolver (file or comma separated)
   -d, -depth int                maximum depth to crawl (default 3)
   -jc, -js-crawl                enable endpoint parsing / crawling in javascript file
   -ct, -crawl-duration int      maximum duration to crawl the target for
   -kf, -known-files string      enable crawling of known files (all,robotstxt,sitemapxml)
   -mrs, -max-response-size int  maximum response size to read (default 9223372036854775807)
   -timeout int                  time to wait for request in seconds (default 10)
   -aff, -automatic-form-fill    enable automatic form filling (experimental)
   -fx, -form-extraction         enable extraction of form, input, textarea & select elements
   -retry int                    number of times to retry the request (default 1)
   -proxy string                 http/socks5 proxy to use
   -H, -headers string[]         custom header/cookie to include in request
   -config string                path to the katana configuration file
   -fc, -form-config string      path to custom form configuration file
   -flc, -field-config string    path to custom field configuration file
   -s, -strategy string          Visit strategy (depth-first, breadth-first) (default "depth-first")
   -iqp, -ignore-query-params    Ignore crawling same path with different query-param values
   -fsu, -filter-similar         filter crawling of similar looking URLs (e.g., /users/123 and /users/456)
   -fst, -filter-similar-threshold int  number of distinct values before a path position is treated as parameter (default 10)
   -mdp, -max-domain-pages int   maximum number of pages to crawl per domain (default unlimited)
```

<a id="connecting-to-active-browser-session"></a>
### Conectando- se à Sessão de Navegador Activa

O Katana também pode conectar- se à sessão ativa do navegador onde o usuário já está conectado e autenticado. e usá- lo para rastrear. O único requisito para isso é iniciar o navegador com a depuração remota habilitada.

Aqui está um exemplo de iniciar o navegador cromado com a depuração remota ativada e usando- o com o katana -

**step 1) Primeiro local de localização do executável cromo**

|Sistema Operacional|Localização Executável de Crómio|Localização executável do Google Chrome|
|------------------|------------------------------|-----------------------------------|
|Janelas (64 bits)|`C:\Program Files (x86)\Google\Chromium\Application\chrome.exe`|`C:\Program Files (x86)\Google\Chrome\Application\chrome.exe`|
|Janelas (32 bits)|`C:\Program Files\Google\Chromium\Application\chrome.exe`|`C:\Program Files\Google\Chrome\Application\chrome.exe`|
|macOS|`/Applications/Chromium.app/Contents/MacOS/Chromium`|`/Applications/Google Chrome.app/Contents/MacOS/Google Chrome`|
|Linux|`/usr/bin/chromium`|`/usr/bin/google-chrome`|

**step 2) Inicie o cromo com a depuração remota ativada e ele retornará o url do websocker. Por exemplo, no MacOS, você pode iniciar o cromo com a depuração remota ativada usando o comando seguinte** -

```console
$ /Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9222


DevTools listening on ws://127.0.0.1:9222/devtools/browser/c5316c9c-19d6-42dc-847a-41d1aeebf7d6
```

> Agora faça login no site que você deseja rastejar e manter o navegador aberto.

**step 3) Agora use o url websocket com katana para se conectar à sessão do navegador ativo e rastejar para o site**

```console
katana -headless -u https://tesla.com -cwu ws://127.0.0.1:9222/devtools/browser/c5316c9c-19d6-42dc-847a-41d1aeebf7d6 -no-incognito
```

> **Note**: você pode usar `-cdd` opção para especificar diretório de dados cromo personalizado para armazenar dados do navegador e cookies, mas que não salva dados de sessão se o cookie está definido para `Session` apenas ou expira após determinado tempo.


<a id="filters"></a>
## Filtros

*`-field`*
----

> [!WARNING]
> Deprecado: use o [**`-output-template`**](#saída) em vez disso. A bandeira do campo ainda é suportada para compatibilidade com o backward.

Katana vem com campos embutidos que podem ser usados para filtrar a saída para a informação desejada, `-f` opção pode ser usado para especificar qualquer um dos campos disponíveis.

```text
   -f, -field string  field to display in output (url,path,fqdn,rdn,rurl,qurl,qpath,file,key,value,kv,dir,udir)
```

Aqui está uma tabela com exemplos de cada campo e saída esperada quando usado -


|CAMPO|DESCRIÇÃO|EXEMPLO|
| ------- | --------------------------- | ------------------------------------------------------------ |
|`url`|Ponto Final do URL|`https://admin.projectdiscovery.io/admin/login?user=admin&password=admin`|
|`qurl`|URL incluindo parâmetro de pesquisa|`https://admin.projectdiscovery.io/admin/login.php?user=admin&password=admin`|
|`qpath`|Localização, incluindo o parâmetro de pesquisa|`/login?user=admin&password=admin`|
|`path`|Localização do URL|`https://admin.projectdiscovery.io/admin/login`|
|`fqdn`|Nome de domínio totalmente qualificado|`admin.projectdiscovery.io`|
|`rdn`|Nome do domínio raiz|`projectdiscovery.io`|
|`rurl`|URL raiz|`https://admin.projectdiscovery.io`|
|`ufile`|URL com Arquivo|`https://admin.projectdiscovery.io/login.js`|
|`file`|Nome do arquivo em URL|`login.php`|
|`key`|Teclas de parâmetros em URL|`user,password`|
|`value`|Valores dos parâmetros em URL|`admin,admin`|
|`kv`|Chaves=Valores em URL|`user=admin&password=admin`|
|`dir`|Nome da pasta URL|`/admin/`|
|`udir`|URL com diretório|`https://admin.projectdiscovery.io/admin/`|

Aqui está um exemplo de usar a opção de campo para exibir apenas todos os urls com parâmetro de consulta nele -

```text
katana -u https://tesla.com -f qurl -silent

https://shop.tesla.com/en_au?redirect=no
https://shop.tesla.com/en_nz?redirect=no
https://shop.tesla.com/product/men_s-raven-lightweight-zip-up-bomber-jacket?sku=1740250-00-A
https://shop.tesla.com/product/tesla-shop-gift-card?sku=1767247-00-A
https://shop.tesla.com/product/men_s-chill-crew-neck-sweatshirt?sku=1740176-00-A
https://www.tesla.com/about?redirect=no
https://www.tesla.com/about/legal?redirect=no
https://www.tesla.com/findus/list?redirect=no
```

<a id="custom-fields"></a>
### Campos Personalizados

Você pode criar campos personalizados para extrair e armazenar informações específicas das respostas da página usando as regras de regex. Estes campos personalizados são definidos usando um arquivo de configuração YAML e são carregados a partir da localização padrão no `$HOME/.config/katana/field-config.yaml`. Em alternativa, você pode usar a opção `-flc` para carregar um arquivo de configuração de campo personalizado a partir de um local diferente.
Aqui está o exemplo de campo personalizado.

```yaml
- name: email
  type: regex
  regex:
  - '([a-zA-Z0-9._-]+@[a-zA-Z0-9._-]+\.[a-zA-Z0-9_-]+)'
  - '([a-zA-Z0-9+._-]+@[a-zA-Z0-9._-]+\.[a-zA-Z0-9_-]+)'

- name: phone
  type: regex
  regex:
  - '\d{3}-\d{8}|\d{4}-\d{7}'
```

Ao definir campos personalizados, são suportados os seguintes atributos:

- **name** (obrigatório)

> O valor do atributo **name** é usado como o valor da opção `-field` cli.

- **type** (obrigatório)

> O tipo de atributo personalizado, atualmente suportado opção - `regex`

- **part** (opcional)

> A parte da resposta para extrair a informação de. O valor padrão é `response`, que inclui tanto o cabeçalho quanto o corpo. Outros valores possíveis são `header` e `body`.

- grupo (opcional)

> Você pode usar este atributo para selecionar um grupo específico combinado no regex, por exemplo: `group: 1`

<a id="running-katana-using-custom-field"></a>
#### A executar o katana usando o campo personalizado:

```console
katana -u https://tesla.com -f email,phone
```

*`-store-field`*
---

Para complementar a opção `field` que é útil para filtrar a saída em tempo de execução, há `-sf, -store-fields` opção que funciona exatamente como opção de campo, exceto em vez de filtragem, ele armazena todas as informações no disco sob diretório `katana_field` ordenado por url alvo. Use `-sfd` ou `-store-field-dir` para armazenar dados em um local diferente.

```text
katana -u https://tesla.com -sf key,fqdn,qurl -silent
```

```bash
$ ls katana_field/

https_www.tesla.com_fqdn.txt
https_www.tesla.com_key.txt
https_www.tesla.com_qurl.txt
```

A opção `-store-field` pode ser útil para coletar informações para construir uma lista de palavras-alvo para vários fins, incluindo, mas não limitado a:

- Identificação dos parâmetros mais utilizados
- Descobrindo caminhos usados com frequência
- Encontrando arquivos comumente usados
- Identificando subdomínios relacionados ou desconhecidos

<a id="katana-filters"></a>
### Filtros Katana

*`-extension-match`*
---

A saída de rastejo pode ser facilmente combinada para uma extensão específica usando a opção `-em` para garantir a exibição apenas da saída contendo determinada extensão.

```text
katana -u https://tesla.com -silent -em js,jsp,json
```

Use o valor especial `none` para também incluir URLs sem uma extensão de arquivo na saída:

```text
katana -u https://tesla.com -silent -em js,jsp,json,none
```

*`-extension-filter`*
---

A saída de rastejo pode ser facilmente filtrada para extensão específica usando a opção `-ef` que garante a remoção de todos os urls que contêm determinada extensão.

```text
katana -u https://tesla.com -silent -ef css,txt,md

```
*`-no-default-ext-filter`*
---

O Katana filtra várias extensões por padrão. Isto pode ser desativado com a opção `-ndef`.

```text
katana -u https://tesla.com -silent -ndef
```

*`-match-regex`*
---
A opção `-match-regex` ou `-mr` permite- lhe filtrar URLs de saída usando expressões regulares. Ao usar esta opção, apenas URLs que correspondam à expressão regular indicada serão impressas na saída.

```text
katana -u https://tesla.com -mr 'https://shop\.tesla\.com/*' -silent
```
*`-filter-regex`*
---
A opção `-filter-regex` ou `-fr` permite- lhe filtrar URLs de saída usando expressões regulares. Ao usar esta opção, ela irá ignorar os URLs que correspondem à expressão regular indicada.

```text
katana -u https://tesla.com -fr 'https://www\.tesla\.com/*' -silent
```

<a id="advance-filtering"></a>
### Filtragem avançada

Katana suporta expressões baseadas em DSL para recursos avançados de correspondência e filtragem:

- Para corresponder aos parâmetros com um código de estado 200:
```shell
katana -u https://www.hackerone.com -mdc 'status_code == 200'
```
- Para corresponder aos parâmetros que contêm "padrão" e têm um código de estado diferente de 403:
```shell
katana -u https://www.hackerone.com -mdc 'contains(endpoint, "default") && status_code != 403'
```
- Para combinar os endpoints com as tecnologias PHP:
```shell
katana -u https://www.hackerone.com -mdc 'contains(to_lower(technologies), "php")'
```
- Para filtrar os endpoints em execução no Cloudflare:
```shell
katana -u https://www.hackerone.com -fdc 'contains(to_lower(technologies), "cloudflare")'
```
As funções DSL podem ser aplicadas a qualquer tecla na saída jsonl. Para mais informações sobre as funções DSL disponíveis, visite o [projeto dsl](https://github.com/projectdiscovery/dsl).

Aqui estão opções de filtro adicionais -

```console
katana -h filter

Flags:
FILTER:
   -mr, -match-regex string[]             regex or list of regex to match on output url (cli, file)
   -fr, -filter-regex string[]            regex or list of regex to filter on output url (cli, file)
   -f, -field string                      field to display in output (url,path,fqdn,rdn,rurl,qurl,qpath,file,ufile,key,value,kv,dir,udir)
   -sf, -store-field string               field to store in per-host output (url,path,fqdn,rdn,rurl,qurl,qpath,file,ufile,key,value,kv,dir,udir)
   -em, -extension-match string[]         match output for given extension (eg, -em php,html,js,none)
   -ef, -extension-filter string[]        filter output for given extension (eg, -ef png,css)
   -ndef, -no-default-ext-filter bool     remove default extensions from the filter list
   -mdc, -match-condition string          match response with dsl based condition
   -fdc, -filter-condition string         filter response with dsl based condition
   -duf, -disable-unique-filter           disable duplicate content filtering
```


<a id="rate-limit"></a>
## Limite de Taxa

É fácil ficar bloqueado / banido ao rastejar se não seguir os limites de sites de destino, katana vem com várias opções para ajustar o rastreamento para ir o mais rápido / lento que queremos.

*`-delay`*
-----

opção para introduzir um atraso em segundos entre cada nova requisição que o katana faz enquanto rasteja, desabilitado como padrão.

```text
katana -u https://tesla.com -delay 20
```

*`-concurrency`*
-----
opção para controlar o número de urls por alvo para obter ao mesmo tempo.

```text
katana -u https://tesla.com -c 20
```


*`-parallelism`*
-----
opção para definir o número de alvo a processar ao mesmo tempo a partir da entrada da lista.

```text
katana -u https://tesla.com -p 20
```

*`-rate-limit`*
-----
Solicitações máximas por segundo, aplicadas globalmente em todos os hosts.

```text
katana -u https://tesla.com -rl 100
```

*`-rate-limit-minute`*
-----
Solicitações máximas por minuto, aplicadas globalmente em todos os hosts.

```text
katana -u https://tesla.com -rlm 500
```

*`-host-rate-limit`*
-----
Requisições máximas por segundo por máquina. Cada máquina recebe o seu próprio balde de limite de taxa, para que uma máquina lenta não acelere as rápidas. Substitui o limite de taxa global quando estiver definido. O Katana também recua automaticamente com atraso exponencial e jitter quando uma máquina devolve 429 ou 503.

```console
katana -u https://tesla.com -hrl 50
```

*`-host-rate-limit-minute`*
-----
Máximo de pedidos por minuto por host.

```console
katana -u https://tesla.com -hrlm 200
```

Aqui está todas as opções CLI longo / curto para controle de limite de taxa -

```console
katana -h rate-limit

Flags:
RATE-LIMIT:
   -c, -concurrency int          number of concurrent fetchers to use (default 10)
   -p, -parallelism int          number of concurrent inputs to process (default 10)
   -rd, -delay int               request delay between each request in seconds
   -rl, -rate-limit int          maximum requests to send per second (default 150)
   -rlm, -rate-limit-minute int  maximum number of requests to send per minute
   -hrl, -host-rate-limit int    maximum requests to send per second per host
   -hrlm, -host-rate-limit-minute int  maximum number of requests to send per minute per host
```

<a id="output"></a>
## Saída

Katana suporta tanto a saída de arquivo em formato de texto simples, bem como JSON que inclui informações adicionais como, `source`, `tag`, e `attribute` nome para co-relacionar o endpoint descoberto.

*`-output`*
---

Por padrão, o katana produz os endpoints rastreados em formato de texto simples. Os resultados podem ser gravados em um arquivo usando a opção - output.


```console
katana -u https://example.com -no-scope -output example_endpoints.txt
```

*`-output-template`*
---

A opção `-output-template` permite- lhe personalizar o formato de saída usando o modelo, proporcionando flexibilidade na definição da estrutura de saída. Esta opção substitui a opção desactualizada `-field` para filtrar a saída. Em vez de confiar em campos predefinidos, você pode especificar um modelo personalizado diretamente na linha de comando para controlar como os dados extraídos são apresentados.

Exemplo de usar a opção `-output-template`:

```sh
katana -u https://example.com -output-template '{{email}} - {{url}}'
```

Neste exemplo, `email` representa um [campo personalizado](#campos-personalizados) que extrai e exibe endereços de e-mail encontrados dentro da fonte `url`.

> [!NOTA]
> Se um campo especificado não existe ou não contém um valor, ele simplesmente será omitido da saída.

Esta opção pode efetivamente estruturar a saída de uma forma que melhor se adapte ao seu caso de uso, tornando a extração de dados mais intuitiva e personalizável.

*`-jsonl`*
---

```console
katana -u https://example.com -jsonl | jq .
```

```json
{
  "timestamp": "2023-03-20T16:23:58.027559+05:30",
  "request": {
    "method": "GET",
    "endpoint": "https://example.com",
    "raw": "GET / HTTP/1.1\r\nHost: example.com\r\nUser-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36\r\nAccept-Encoding: gzip\r\n\r\n"
  },
  "response": {
    "status_code": 200,
    "headers": {
      "accept_ranges": "bytes",
      "expires": "Mon, 27 Mar 2023 10:53:58 GMT",
      "last_modified": "Thu, 17 Oct 2019 07:18:26 GMT",
      "content_type": "text/html; charset=UTF-8",
      "server": "ECS (dcb/7EA3)",
      "vary": "Accept-Encoding",
      "etag": "\"3147526947\"",
      "cache_control": "max-age=604800",
      "x_cache": "HIT",
      "date": "Mon, 20 Mar 2023 10:53:58 GMT",
      "age": "331239"
    },
    "body": "<!doctype html>\n<html>\n<head>\n    <title>Example Domain</title>\n\n    <meta charset=\"utf-8\" />\n    <meta http-equiv=\"Content-type\" content=\"text/html; charset=utf-8\" />\n    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\" />\n    <style type=\"text/css\">\n    body {\n        background-color: #f0f0f2;\n        margin: 0;\n        padding: 0;\n        font-family: -apple-system, system-ui, BlinkMacSystemFont, \"Segoe UI\", \"Open Sans\", \"Helvetica Neue\", Helvetica, Arial, sans-serif;\n        \n    }\n    div {\n        width: 600px;\n        margin: 5em auto;\n        padding: 2em;\n        background-color: #fdfdff;\n        border-radius: 0.5em;\n        box-shadow: 2px 3px 7px 2px rgba(0,0,0,0.02);\n    }\n    a:link, a:visited {\n        color: #38488f;\n        text-decoration: none;\n    }\n    @media (max-width: 700px) {\n        div {\n            margin: 0 auto;\n            width: auto;\n        }\n    }\n    </style>    \n</head>\n\n<body>\n<div>\n    <h1>Example Domain</h1>\n    <p>This domain is for use in illustrative examples in documents. You may use this\n    domain in literature without prior coordination or asking for permission.</p>\n    <p><a href=\"https://www.iana.org/domains/example\">More information...</a></p>\n</div>\n</body>\n</html>\n",
    "technologies": [
      "Azure",
      "Amazon ECS",
      "Amazon Web Services",
      "Docker",
      "Azure CDN"
    ],
    "raw": "HTTP/1.1 200 OK\r\nContent-Length: 1256\r\nAccept-Ranges: bytes\r\nAge: 331239\r\nCache-Control: max-age=604800\r\nContent-Type: text/html; charset=UTF-8\r\nDate: Mon, 20 Mar 2023 10:53:58 GMT\r\nEtag: \"3147526947\"\r\nExpires: Mon, 27 Mar 2023 10:53:58 GMT\r\nLast-Modified: Thu, 17 Oct 2019 07:18:26 GMT\r\nServer: ECS (dcb/7EA3)\r\nVary: Accept-Encoding\r\nX-Cache: HIT\r\n\r\n<!doctype html>\n<html>\n<head>\n    <title>Example Domain</title>\n\n    <meta charset=\"utf-8\" />\n    <meta http-equiv=\"Content-type\" content=\"text/html; charset=utf-8\" />\n    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\" />\n    <style type=\"text/css\">\n    body {\n        background-color: #f0f0f2;\n        margin: 0;\n        padding: 0;\n        font-family: -apple-system, system-ui, BlinkMacSystemFont, \"Segoe UI\", \"Open Sans\", \"Helvetica Neue\", Helvetica, Arial, sans-serif;\n        \n    }\n    div {\n        width: 600px;\n        margin: 5em auto;\n        padding: 2em;\n        background-color: #fdfdff;\n        border-radius: 0.5em;\n        box-shadow: 2px 3px 7px 2px rgba(0,0,0,0.02);\n    }\n    a:link, a:visited {\n        color: #38488f;\n        text-decoration: none;\n    }\n    @media (max-width: 700px) {\n        div {\n            margin: 0 auto;\n            width: auto;\n        }\n    }\n    </style>    \n</head>\n\n<body>\n<div>\n    <h1>Example Domain</h1>\n    <p>This domain is for use in illustrative examples in documents. You may use this\n    domain in literature without prior coordination or asking for permission.</p>\n    <p><a href=\"https://www.iana.org/domains/example\">More information...</a></p>\n</div>\n</body>\n</html>\n"
  }
}
```

*`-store-response`*
----

A opção `-store-response` permite gravar todas as requisições de endpoint e respostas para um arquivo de texto. Quando esta opção for usada, os arquivos de texto, incluindo a requisição e resposta, serão gravados para o diretório **katana_ response**. Se você quiser especificar uma pasta personalizada, você pode usar a opção `-store-response-dir`.

```console
katana -u https://example.com -no-scope -store-response
```

```bash
$ cat katana_response/index.txt

katana_response/example.com/327c3fda87ce286848a574982ddd0b7c7487f816.txt https://example.com (200 OK)
katana_response/www.iana.org/bfc096e6dd93b993ca8918bf4c08fdc707a70723.txt http://www.iana.org/domains/reserved (200 OK)
```

**Nota:**

*`-store-response` opção não é suportada no modo `-headless`.*

*`-list-output-fields`*
----

A bandeira `-list-output-fields` ou `-lof` exibe todos os campos disponíveis que podem ser usados no formato de saída JSONL. Isto é útil para entender quais dados estão disponíveis ao usar modelos de saída personalizados ou ao excluir campos específicos.

```console
katana -lof
```

*`-exclude-output-fields`*
----

A opção `-exclude-output-fields` ou `-eof` permite excluir campos específicos da saída JSONL. Isto é útil para reduzir o tamanho da saída ou focar em dados específicos removendo campos indesejados.

```console
katana -u https://example.com -jsonl -eof raw,body
```

Aqui estão as opções adicionais de CLI relacionadas à saída -

```console
katana -h output

OUTPUT:
   -o, -output string                file to write output to
   -sr, -store-response              store http requests/responses
   -srd, -store-response-dir string  store http requests/responses to custom directory
   -lof, -list-output-fields         list available fields for jsonl output format
   -eof, -exclude-output-fields      exclude fields from jsonl output
   -j, -json                         write output in JSON Lines format
   -nc, -no-color                    disable output content coloring (ANSI escape codes)
   -silent                           display output only
   -v, -verbose                      display verbose output
   -version                          display project version
```

<a id="katana-as-a-library"></a>
## Katana como uma biblioteca
`katana` pode ser usado como uma biblioteca criando uma instância da estrutura `Option` e povoando-a com as mesmas opções que seriam especificadas via CLI. Usando as opções que você pode criar `crawlerOptions` e assim padrão ou híbrido `crawler`.
O método `crawler.Crawl` deve ser chamado para rastrear a entrada.

```go
package main

import (
	"math"

	"github.com/projectdiscovery/gologger"
	"github.com/projectdiscovery/katana/pkg/engine/standard"
	"github.com/projectdiscovery/katana/pkg/output"
	"github.com/projectdiscovery/katana/pkg/types"
)

func main() {
	options := &types.Options{
		MaxDepth:     3,             // Maximum depth to crawl
		FieldScope:   "rdn",         // Crawling Scope Field
		BodyReadSize: math.MaxInt,   // Maximum response size to read
		Timeout:      10,            // Timeout is the time to wait for request in seconds
		Concurrency:  10,            // Concurrency is the number of concurrent crawling goroutines
		Parallelism:  10,            // Parallelism is the number of urls processing goroutines
		Delay:        0,             // Delay is the delay between each crawl requests in seconds
		RateLimit:    150,           // Maximum requests to send per second
		Strategy:     "depth-first", // Visit strategy (depth-first, breadth-first)
		OnResult: func(result output.Result) { // Callback function to execute for result
			gologger.Info().Msg(result.Request.URL)
		},
	}
	crawlerOptions, err := types.NewCrawlerOptions(options)
	if err != nil {
		gologger.Fatal().Msg(err.Error())
	}
	defer crawlerOptions.Close()
	crawler, err := standard.New(crawlerOptions)
	if err != nil {
		gologger.Fatal().Msg(err.Error())
	}
	defer crawler.Close()
	var input = "https://www.hackerone.com"
	err = crawler.Crawl(input)
	if err != nil {
		gologger.Warning().Msgf("Could not crawl %s: %s", input, err.Error())
	}
}
```

<a id="reporting-issues--feature-requests"></a>
## Relatar questões e pedidos de recursos

Para manter o rastreamento de problemas e melhorar a eficiência da triagem:

**Todos os relatórios começam como [Discussão do GitHub](https://github.com/projectdiscovery/katana/discussions)**

- **Bug Reports** → [Iniciar uma Discussão de Perguntas & Respostas](https://github.com/projectdiscovery/katana/discussions/new?category=q-a)
- **Pedidos de recursos** → [Iniciar uma Discussão de Ideias](https://github.com/projectdiscovery/katana/discussions/new?category=ideas)
- **Perguntas** → [Iniciar uma Discussão de Perguntas & Respostas](https://github.com/projectdiscovery/katana/discussions/new?category=q-a)

**Por que as discussões primeiro?**
- **Community pode ajudar** com perguntas rápidas e solução de problemas
- **Melhor triagem** - erros/caracteres confirmados tornam-se problemas rastreados
- **Cleaner issue tracker** - foco apenas em itens acionáveis

Os mantenedores converterão as discussões em questões quando apropriado após a revisão adequada.

--------

<div align="center">

O katana é feito com o [descoberta do projecto](https://projectdiscovery.io) e distribuído em [Licença MIT](../../99-Assets/upstream/katana/LICENSE.txt).


<a href="https://discord.gg/projectdiscovery"></a>

</div>


---

## Procedência desta tradução

Fonte: [https://github.com/projectdiscovery/katana](https://github.com/projectdiscovery/katana/blob/4b41dd02a095df15ae0cd04cbb658af457d3c1ab/README.md). Licença: [MIT](../../99-Assets/upstream/katana/LICENSE.txt). Commit: 4b41dd02a095df15ae0cd04cbb658af457d3c1ab.

O original preservado, a lista de mudanças de apresentação e os hashes constam no manifesto do projeto. Nenhum exemplo desta documentação foi executado automaticamente.
