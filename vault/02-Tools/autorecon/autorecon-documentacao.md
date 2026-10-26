---
title: "autorecon — documentação oficial"
type: "official-documentation"
tool: "autorecon"
status: "translated-machine"
reviewed: "2026-10-26"
language: "pt-BR"
tags: ["documentation", "tool/autorecon"]
cssclasses: ["fieldbook"]
source_url: "https://github.com/Tib3rius/AutoRecon/blob/e7e98f60bdc5fb1695159c1bbcdfdf2746d30fa6/README.md"
source_commit: "e7e98f60bdc5fb1695159c1bbcdfdf2746d30fa6"
source_sha256: "0a42ce23038d6c5b767861414e9589329876ac68231653da46993eec431ce342"
license_spdx: "GPL-3.0"
human_review: "pending"
source_scope: "Repository root README and owned doc/docs/documentation Markdown or RST files; not a claim of full wiki/site coverage"
---

> Tradução automática local para português, ainda sem revisão humana integral. Estrutura e blocos de código preservados; referências externas não significam conteúdo espelhado.

> É como boliche com pára-choques. - [@ippsec](https://twitter.com/ippsec)

# AutoRecon

AutoRecon é uma ferramenta de reconhecimento de rede multi-threaded que executa a enumeração automatizada de serviços. Destina-se como uma ferramenta de economia de tempo para uso em CTFs e outros ambientes de teste de penetração (por exemplo, OSCP). Também pode ser útil em engajamentos do mundo real.

A ferramenta funciona realizando primeiramente varreduras de porta/detecção de serviço. A partir desses resultados iniciais, a ferramenta irá lançar mais varreduras de enumeração desses serviços usando um número de ferramentas diferentes. Por exemplo, se o HTTP for encontrado, o feroxbuster será lançado (assim como muitos outros).

Tudo na ferramenta é altamente configurável. A configuração padrão executa a exploração automatizada do **no** para manter a ferramenta de acordo com as regras do exame OSCP. Se você deseja adicionar ferramentas de exploração automáticas à configuração, você o faz por sua conta e risco. O autor não será responsabilizado por ações negativas que resultem da utilização incorreta desta ferramenta.

**Disclaimer: Enquanto o AutoRecon se esforça para realizar o máximo de identificação e enumeração de serviços possível, não há garantia de que cada serviço será identificado, ou que cada serviço será totalmente enumerado. Usuários do AutoRecon (especialmente estudantes) devem realizar sua própria enumeração manual ao lado do AutoRecon. Não confie nesta ferramenta sozinho para exames, CTFs, ou outros engajamentos.**

<a id="origin"></a>
## Origem

O AutoRecon foi inspirado em três ferramentas que o autor usou durante os laboratórios do OSCP: [Reconnoitre](https://github.com/codingo/Reconnoitre), [ReconScan](https://github.com/RoliSoft/ReconScan) e [bscan](https://github.com/welchbj/bscan). Embora todas as três ferramentas fossem úteis, nenhuma das três sozinho tinha a funcionalidade desejada. O AutoRecon combina as melhores características das ferramentas acima mencionadas, ao mesmo tempo em que implementa muitos novos recursos para ajudar os testadores com enumeração de alvos múltiplos.

<a id="features"></a>
## Características

* Suporta vários alvos na forma de endereços IP, intervalos IP (notação CIDR) e nomes de host resolváveis. IPv6 também é suportado.
* Pode digitalizar vários alvos simultaneamente, utilizando vários processadores se eles estão disponíveis.
* Sistema avançado de plugins permitindo a criação fácil de novas varreduras.
* Plugins de digitalização de portas personalizáveis para flexibilidade em suas varreduras iniciais.
* Plugins de digitalização de serviço personalizáveis para enumeração adicional.
* Comandos de acompanhamento manuais sugeridos para quando a automação faz pouco sentido.
* Capacidade de limitar a digitalização de portas a uma combinação de portas TCP/UDP.
* Capacidade de pular a fase de varredura de portas, fornecendo informações sobre serviços que devem estar abertos.
* Matching padrão global e per-scan que destaca e extrai informações importantes do ruído.
* Uma estrutura de diretório intuitiva para coleta de resultados.
* Registro completo de comandos que foram executados, juntamente com erros se eles falharem.
* Um arquivo de configuração poderoso permite que você use suas configurações favoritas sempre.
* Um sistema de marcação que permite incluir ou excluir certos plugins.
* Tempo limite global e por alvo, caso você tenha apenas tempo limitado.
* Quatro níveis de verbosidade, controláveis por opções de linha de comando, e durante as varreduras usando as setas para cima/baixo.
* Saída colorida para distinguir partes separadas de informação. Pode ser desligado por razões de acessibilidade.

<a id="installation"></a>
## Instalação

Existem três maneiras de instalar o AutoRecon: pipx, pip e manualmente. Antes de instalar usando qualquer um desses métodos, alguns requisitos precisam ser cumpridos. Se você não atualizou seu cache apt recentemente, execute o seguinte comando para que você esteja instalando os pacotes mais recentes disponíveis:

```bash
sudo apt update
```

### Python 3

AutoRecon requer o uso de Python 3.8+ e pip, que pode ser instalado no Kali Linux usando os seguintes comandos:

```bash
sudo apt install python3
sudo apt install python3-pip
```

<a id="supporting-packages"></a>
### Pacotes de Apoio

Vários comandos usados no AutoRecon referenciam o projeto SecLists, no diretório /usr/share/seclists/. Você pode baixar manualmente o projeto SecLists para este diretório (https://github.com/danielmiessler/SecLists), ou se você estiver usando Kali Linux (** altamente recomendado**) você pode executar os seguintes comandos:

```bash
sudo apt install seclists
```

AutoRecon ainda será executado se você não instalar SecLists, embora vários comandos possam falhar, e alguns comandos manuais também podem não ser executados.

Além disso, os seguintes comandos podem precisar ser instalados, dependendo do seu sistema operacional:

```text
curl
dnsrecon
enum4linux
feroxbuster
gobuster
impacket-scripts
nbtscan
nikto
nmap
onesixtyone
oscanner
redis-tools
smbclient
smbmap
snmpwalk
sslscan
svwar
tnscmd10g
whatweb
```

No Kali Linux, você pode garantir que todos eles estejam instalados usando os seguintes comandos:

```bash
sudo apt install seclists curl dnsrecon enum4linux feroxbuster gobuster impacket-scripts nbtscan nikto nmap onesixtyone oscanner redis-tools smbclient smbmap snmp sslscan sipvicious tnscmd10g whatweb
```

<a id="installation-method-1-pipx-recommended"></a>
### Método de Instalação # 1: pipx (Recomendado)

Recomenda-se que você use o `pipx` para instalar o AutoRecon. O pipx irá instalar o AutoRecon no seu próprio ambiente virtual e torná-lo disponível no contexto global, evitando dependências de pacotes conflitantes e a instabilidade resultante. Primeiro, instale o pipx usando os seguintes comandos:


```bash
sudo apt install python3-venv
python3 -m pip install --user pipx
python3 -m pipx ensurepath
```

Você terá que re-sourcear seu arquivo ~/.bashrc ou ~/.zshrc (ou abrir uma nova aba) após executar esses comandos para usar o pipx.

Instale o AutoRecon usando o seguinte comando:

```bash
pipx install git+https://github.com/Tib3rius/AutoRecon.git
```

Note que se você quiser executar AutoRecon usando sudo (obrigatório para digitalização mais rápida SYN e UDP), você tem que usar _one_ dos seguintes exemplos:

```bash
sudo env "PATH=$PATH" autorecon [OPTIONS]
sudo $(which autorecon) [OPTIONS]
```

<a id="installation-method-2-pip"></a>
### Método de instalação # 2: pip

Alternativamente, você pode usar `pip` para instalar o AutoRecon usando o seguinte comando:

```bash
python3 -m pip install git+https://github.com/Tib3rius/AutoRecon.git
```

Note que se você quiser executar o AutoRecon usando o sudo (obrigatório para uma digitalização mais rápida do SYN e do UDP), você terá que executar o comando acima como o usuário root (ou usando o sudo).

Da mesma forma que `pipx`, se instalado usando `pip` você pode executar AutoRecon simplesmente executando `autorecon`.

<a id="installation-method-3-manually"></a>
### Método de instalação # 3: Manualmente

Se preferir não usar o `pip` ou o `pipx`, poderá sempre instalar e executar o `autorecon.py` manualmente como um programa. De dentro do directório AutoRecon, instale as dependências:

```bash
python3 -m pip install -r requirements.txt
```

Você poderá então executar o script `autorecon.py`:

```bash
python3 autorecon.py [OPTIONS] 127.0.0.1
```

<a id="upgrading"></a>
## Atualizando

### pipx

Atualizar o AutoRecon quando ele foi instalado com o pipx é o mais fácil, e é por isso que o método é recomendado. Basta executar o seguinte comando:

```bash
pipx upgrade autorecon
```

### pip

Se você instalou o AutoRecon usando o pip, você primeiro terá que desinstalar o AutoRecon e, em seguida, re-instalar usando o mesmo comando de instalação:

```bash
python3 -m pip uninstall autorecon
python3 -m pip install git+https://github.com/Tib3rius/AutoRecon.git
```

<a id="manually"></a>
### Manualmente

Se você instalou AutoRecon manualmente, simplesmente mude para o diretório AutoRecon e execute o seguinte comando:

```bash
git pull
```

Assumindo que você não modificou nenhum dos conteúdos no diretório AutoRecon, isso deve puxar o código mais recente deste repo GitHub, após o qual você pode executar AutoRecon usando o script autorrecon.py como de costume.

<a id="plugins"></a>
### Plug-ins

Um processo de atualização do plugin está em funcionamento. Até lá, após atualizar, remova o diretório ~/.local/share/AutoRecon e execute o AutoRecon com qualquer argumento para repovoar com os arquivos mais recentes.

<a id="usage"></a>
## Uso

AutoRecon usa funcionalidades específicas do Python 3 e não suporta Python 2.

```text
usage: autorecon [-t TARGET_FILE] [-p PORTS] [-m MAX_SCANS] [-mp MAX_PORT_SCANS] [-c CONFIG_FILE] [-g GLOBAL_FILE] [--tags TAGS]
                 [--exclude-tags TAGS] [--port-scans PLUGINS] [--service-scans PLUGINS] [--reports PLUGINS] [--plugins-dir PLUGINS_DIR]
                 [--add-plugins-dir PLUGINS_DIR] [-l [TYPE]] [-o OUTPUT] [--single-target] [--only-scans-dir] [--no-port-dirs]
                 [--heartbeat HEARTBEAT] [--timeout TIMEOUT] [--target-timeout TARGET_TIMEOUT] [--nmap NMAP | --nmap-append NMAP_APPEND]
                 [--proxychains] [--disable-sanity-checks] [--disable-keyboard-control] [--force-services SERVICE [SERVICE ...]] [--accessible]
                 [-v] [--version] [--curl.path VALUE] [--dirbuster.tool {feroxbuster,gobuster,dirsearch,ffuf,dirb}]
                 [--dirbuster.wordlist VALUE [VALUE ...]] [--dirbuster.threads VALUE] [--dirbuster.ext VALUE]
                 [--onesixtyone.community-strings VALUE] [--global.username-wordlist VALUE] [--global.password-wordlist VALUE]
                 [--global.domain VALUE] [-h]
                 [targets ...]

Network reconnaissance tool to port scan and automatically enumerate services found on multiple targets.

positional arguments:
  targets               IP addresses (e.g. 10.0.0.1), CIDR notation (e.g. 10.0.0.1/24), or resolvable hostnames (e.g. foo.bar) to scan.

optional arguments:
  -t TARGET_FILE, --target-file TARGET_FILE
                        Read targets from file.
  -p PORTS, --ports PORTS
                        Comma separated list of ports / port ranges to scan. Specify TCP/UDP ports by prepending list with T:/U: To scan both
                        TCP/UDP, put port(s) at start or specify B: e.g. 53,T:21-25,80,U:123,B:123. Default: None
  -m MAX_SCANS, --max-scans MAX_SCANS
                        The maximum number of concurrent scans to run. Default: 50
  -mp MAX_PORT_SCANS, --max-port-scans MAX_PORT_SCANS
                        The maximum number of concurrent port scans to run. Default: 10 (approx 20% of max-scans unless specified)
  -c CONFIG_FILE, --config CONFIG_FILE
                        Location of AutoRecon's config file. Default: ~/.config/AutoRecon/config.toml
  -g GLOBAL_FILE, --global-file GLOBAL_FILE
                        Location of AutoRecon's global file. Default: ~/.config/AutoRecon/global.toml
  --tags TAGS           Tags to determine which plugins should be included. Separate tags by a plus symbol (+) to group tags together. Separate
                        groups with a comma (,) to create multiple groups. For a plugin to be included, it must have all the tags specified in
                        at least one group. Default: default
  --exclude-tags TAGS   Tags to determine which plugins should be excluded. Separate tags by a plus symbol (+) to group tags together. Separate
                        groups with a comma (,) to create multiple groups. For a plugin to be excluded, it must have all the tags specified in
                        at least one group. Default: None
  --port-scans PLUGINS  Override --tags / --exclude-tags for the listed PortScan plugins (comma separated). Default: None
  --service-scans PLUGINS
                        Override --tags / --exclude-tags for the listed ServiceScan plugins (comma separated). Default: None
  --reports PLUGINS     Override --tags / --exclude-tags for the listed Report plugins (comma separated). Default: None
  --plugins-dir PLUGINS_DIR
                        The location of the plugins directory. Default: ~/.local/share/AutoRecon/plugins
  --add-plugins-dir PLUGINS_DIR
                        The location of an additional plugins directory to add to the main one. Default: None
  -l [TYPE], --list [TYPE]
                        List all plugins or plugins of a specific type. e.g. --list, --list port, --list service
  -o OUTPUT, --output OUTPUT
                        The output directory for results. Default: results
  --single-target       Only scan a single target. A directory named after the target will not be created. Instead, the directory structure will
                        be created within the output directory. Default: False
  --only-scans-dir      Only create the "scans" directory for results. Other directories (e.g. exploit, loot, report) will not be created.
                        Default: False
  --no-port-dirs        Don't create directories for ports (e.g. scans/tcp80, scans/udp53). Instead store all results in the "scans" directory
                        itself. Default: False
  --heartbeat HEARTBEAT
                        Specifies the heartbeat interval (in seconds) for scan status messages. Default: 60
  --timeout TIMEOUT     Specifies the maximum amount of time in minutes that AutoRecon should run for. Default: None
  --target-timeout TARGET_TIMEOUT
                        Specifies the maximum amount of time in minutes that a target should be scanned for before abandoning it and moving on.
                        Default: None
  --nmap NMAP           Override the {nmap_extra} variable in scans. Default: -vv --reason -Pn -T4
  --nmap-append NMAP_APPEND
                        Append to the default {nmap_extra} variable in scans. Default:
  --proxychains         Use if you are running AutoRecon via proxychains. Default: False
  --disable-sanity-checks
                        Disable sanity checks that would otherwise prevent the scans from running. Default: False
  --disable-keyboard-control
                        Disables keyboard control ([s]tatus, Up, Down) if you are in SSH or Docker.
  --force-services SERVICE [SERVICE ...]
                        A space separated list of services in the following style: tcp/80/http tcp/443/https/secure
  --accessible          Attempts to make AutoRecon output more accessible to screenreaders. Default: False
  -v, --verbose         Enable verbose output. Repeat for more verbosity.
  --version             Prints the AutoRecon version and exits.
  -h, --help            Show this help message and exit.

plugin arguments:
  These are optional arguments for certain plugins.

  --curl.path VALUE     The path on the web server to curl. Default: /
  --dirbuster.tool {feroxbuster,gobuster,dirsearch,ffuf,dirb}
                        The tool to use for directory busting. Default: feroxbuster
  --dirbuster.wordlist VALUE [VALUE ...]
                        The wordlist(s) to use when directory busting. Separate multiple wordlists with spaces. Default: ['/root/.local/share/AutoRecon/wordlists/dirbuster.txt']
  --dirbuster.threads VALUE
                        The number of threads to use when directory busting. Default: 10
  --dirbuster.ext VALUE
                        The extensions you wish to fuzz (no dot, comma separated). Default: txt,html,php,asp,aspx,jsp
  --dirbuster.recursive
                        Enables recursive searching (where available). Warning: This may cause significant increases to scan times. Default: False
  --dirbuster.extras VALUE
                        Any extra options you wish to pass to the tool when it runs. e.g. --dirbuster.extras='-s 200,301 --discover-backup'
  --enum4linux.tool {enum4linux-ng,enum4linux}
                        The tool to use for doing Windows and Samba enumeration. Default: enum4linux-ng
  --onesixtyone.community-strings VALUE
                        The file containing a list of community strings to try. Default: /usr/share/seclists/Discovery/SNMP/common-snmp-community-strings-onesixtyone.txt
  --redirect-host-discovery.update-hosts
                        If set, discovered redirect hostnames will be added to /etc/hosts with the target IP
  --subdomain-enum.domain VALUE
                        The domain to use as the base domain (e.g. example.com) for subdomain enumeration. Default: None
  --subdomain-enum.wordlist VALUE [VALUE ...]
                        The wordlist(s) to use when enumerating subdomains. Separate multiple wordlists with spaces. Default: ['/usr/share/seclists/Discovery/DNS/subdomains-top1million-110000.txt']
  --subdomain-enum.threads VALUE
                        The number of threads to use when enumerating subdomains. Default: 10
  --vhost-enum.hostname VALUE
                        The hostname to use as the base host (e.g. example.com) for virtual host enumeration. Default: None
  --vhost-enum.wordlist VALUE [VALUE ...]
                        The wordlist(s) to use when enumerating virtual hosts. Separate multiple wordlists with spaces. Default: ['/usr/share/seclists/Discovery/DNS/subdomains-top1million-110000.txt']
  --vhost-enum.threads VALUE
                        The number of threads to use when enumerating virtual hosts. Default: 10
  --wpscan.api-token VALUE
                        An API Token from wpvulndb.com to help search for more vulnerabilities.

global plugin arguments:
  These are optional arguments that can be used by all plugins.

  --global.username-wordlist VALUE
                        A wordlist of usernames, useful for bruteforcing. Default: /usr/share/seclists/Usernames/top-usernames-shortlist.txt
  --global.password-wordlist VALUE
                        A wordlist of passwords, useful for bruteforcing. Default: /usr/share/seclists/Passwords/darkweb2017-top100.txt
  --global.domain VALUE
                        The domain to use (if known). Used for DNS and/or Active Directory. Default: None
```

<a id="verbosity"></a>
### Verbosidade

AutoRecon suporta quatro níveis de verbosidade:

* (nenhum) Saída mínima. AutoRecon anunciará quando os alvos de digitalização começarem / terminarem.
* (- v) Resultado verbose. AutoRecon irá anunciar adicionalmente quando os plugins começarem a correr, e relatar portas abertas e serviços identificados.
* (- vv) Resultado muito verboso. O AutoRecon irá adicionalmente especificar os comandos exatos que estão sendo executados pelos plug- ins, destacar quaisquer padrões que sejam combinados no resultado do comando e anunciar quando os plug- ins terminarem.
* (- vvv) Muito, muito verbose saída. AutoRecon irá produzir tudo. Literalmente cada linha de todos os comandos que estão em execução. Ao digitalizar vários alvos simultaneamente, isso pode levar a uma quantidade ridícula de saída. Não é aconselhável usar - vvv a menos que você precisa absolutamente de ver saída ao vivo de comandos.

Nota: Você pode alterar a verbosidade do AutoRecon mid-scan pressionando as teclas de seta para cima e para baixo.

<a id="results"></a>
### Resultados

Por padrão, os resultados serão armazenados na pasta ./results. Uma nova sub- pasta é criada para cada alvo. A estrutura desta sub- pasta é:

```text
.
├── exploit/
├── loot/
├── report/
│   ├── local.txt
│   ├── notes.txt
│   ├── proof.txt
│   └── screenshots/
└── scans/
	├── _commands.log
	├── _manual_commands.txt
	├── tcp80/
	├── udp53/
	└── xml/
```

O diretório exploit é destinado a conter qualquer código exploit que você baixar / escrever para o alvo.

O diretório de saque é destinado a conter qualquer saque (por exemplo hashes, arquivos interessantes) que você encontrar no alvo.

O diretório de relatórios contém alguns arquivos e diretórios gerados automaticamente que são úteis para relatórios:
* local.txt pode ser usado para armazenar a bandeira local.txt encontrada nos alvos.
* notes.txt deve conter um modelo básico onde você pode escrever notas para cada serviço descoberto.
* proof.txt pode ser usado para armazenar a bandeira proof.txt encontrada nos alvos.
* A pasta screenshots pretende conter as screenshots que você usa para documentar a exploração do alvo.

O diretório de varreduras é onde todos os resultados de varreduras realizadas pelo AutoRecon irão. Isto inclui varreduras de porta / serviços de detecção de varreduras, bem como qualquer exame de enumeração de serviço. Ele também contém dois outros arquivos:
* \_commands.log contém uma lista de todos os comandos AutoRecon executado contra o alvo. Isto é útil se um dos comandos falhar e você quiser executá-lo novamente com modificações.
* \_manual_commands.txt contém todos os comandos que são considerados "perigosos" para serem executados automaticamente, seja porque são muito intrusivos, requerem modificação com base na análise humana, ou apenas funcionam melhor quando há um humano monitorando-os.

Por padrão, os diretórios são criados para cada porta aberta (por exemplo, tcp80, udp53) e os resultados da varredura para os serviços encontrados nessas portas são armazenados em seus respectivos diretórios. Você pode desabilitar este comportamento usando a opção --no-port-dirs linha de comando, e os resultados da varredura serão armazenados no diretório de varreduras em si.

Se uma varredura resultar em um erro, um arquivo chamado \_errors.log também aparecerá no diretório de varreduras com alguns detalhes para alertar o usuário.

Se a saída corresponder a um padrão definido, um arquivo chamado \_patterns.log também aparecerá no diretório de varreduras com detalhes sobre a saída correspondente.

O diretório scans/xml armazena qualquer saída XML (por exemplo, de varreduras Nmap) separadamente das saídas principais da varredura, de modo que o diretório scans em si não fique muito desordenado.

<a id="testimonials"></a>
## Testemunhos

> AutoRecon foi inestimável durante o meu exame OSCP, em que ele me salvou do tédio de executar meus comandos de coleta de informação ativa. Eu fui capaz de começar em um alvo com todas as informações que eu precisava claramente colocado na minha frente. Eu recomendo fortemente este utilitário para qualquer um nos laboratórios PWK, o exame OSCP, ou outros ambientes como VulnHub ou HTB. É uma ótima ferramenta para ambas as pessoas apenas começando a sua jornada para OffSec e veteranos experientes. Apenas certifique-se de que em algum lugar entre esses dois pontos você tomar o tempo para aprender o que está acontecendo "debaixo do capô" e como / por que ele verifica o que ele faz.
>
>\- b0ats (hosts de exame 5/5 enraizados)

> Uau, que grande descoberta! Antes de usar o AutoRecon, o ReconScan foi o meu programa de enumeração de alvos porque ele executou automaticamente os comandos de enumeração depois de encontrar portas abertas. A única coisa que faltava foi a criação automática de pastas de chaves que um pentester poderia precisar durante um engajamento (exploração, saque, relatório, varredura). O Reconnoitre fez isso, mas não executou automaticamente esses comandos para você. Eu pensei que o ReconScan que era o joelho da abelha até que eu dei uma tentativa ao AutoRecon. É incrível! Ele combina as melhores características do Reconnoitre (criação de diretórios automáticos) e do ReconScan (executando automaticamente os comandos de enumeração). Tudo o que eu tenho que fazer é executá- lo em um alvo ou um conjunto de alvos e começar a trabalhar sobre as informações que já recolheu enquanto continua o restante da digitalização. A prova está no pudim :) Passei o exame OSCP! Kudos para Tib3rius!
>
>\- Werk0ut

> Um amigo me falou sobre AutoRecon, então eu dei-lhe uma tentativa nos laboratórios PWK. AutoRecon lança as ferramentas comuns que todos nós sempre usamos, quer seja nmap ou nikto, e também cria um bom sistema de subpastas baseado nos alvos que você está atacando. O recurso mais forte do AutoRecon é a velocidade; no exame OSCP eu deixei a ferramenta rodando em segundo plano enquanto eu comecei com outro alvo, e em questão de minutos eu tinha todo o resultado AutoRecon esperando por mim. AutoRecon cria um arquivo cheio de comandos que você deve tentar manualmente, alguns dos quais podem exigir ajustes (por exemplo, comandos Hydra bruteforcing). É bom ter essa lista de verificação extra.
>
>\- tr3mb0 (máquinas de testes 4/5 enraizadas)

> Ser introduzido no AutoRecon foi uma completa mudança de jogo para mim ao tomar o OSCP e estabelecer a minha metodologia de teste de penetração. AutoRecon é uma ferramenta de reconhecimento multi-threaded que combina e automatiza ferramentas de enumeração populares para fazer a maior parte do trabalho duro para você. Você não pode obter muito melhor do que isso! Depois de executar o AutoRecon em minhas máquinas de exame OSCP, foi-me dado um tesouro caixa cheio de informações que me ajudou a começar em cada máquina e passar na minha primeira tentativa. A melhor parte da ferramenta é que ele lança automaticamente mais varreduras de enumeração com base nas varreduras de porta iniciais (por exemplo, executar enum4linux se SMB é detectado). A única parte ruim é que eu não usar esta ferramenta mais cedo! Obrigado Tib3rius.
>
>\- rufy (enraizado 4/5 máquinas de exame)

> AutoRecon permite que um pesquisador de segurança digitalize iterativamente hosts e identifique potenciais vetores de ataque. Seu verdadeiro poder vem na forma de realizar varreduras em segundo plano enquanto o atacante está trabalhando em outro host. Eu fui capaz de iniciar minhas varreduras e terminar um host específico que eu estava trabalhando - e então retornar para encontrar todas as varreduras relevantes concluídas. Eu fui então capaz de imediatamente começar a tentar obter acesso inicial em vez de executar manualmente o processo de digitalização ativa. Eu vou continuar a usar AutoRecon em testes de penetração futuros e CTFs, e altamente recomendo que você faça o mesmo.
>
>\- waar (hosts de exame 4.99/5 enraizados)

> "Se você tem que fazer uma tarefa mais do que duas vezes por dia, você precisa automatizá-la." Esse é um conselho que um antigo chefe me deu. AutoRecon leva essa lição a sério. Se você está sentado no exame, ou nos laboratórios PWK, você pode disparar AutoRecon e deixá-lo trabalhar sua magia. Eu o tinha executado durante meu último exame enquanto eu trabalhava no buffer overflow. Quando eu terminei, todos os dados de enum que eu precisava estava lá para eu passar. 10/10 recomendaria para qualquer um entrar no CTF, e qualquer um que já esteve nisso por muito tempo.
>
>\- whoisflynn

> Eu amo esta ferramenta tanto que eu a escrevi.
>
>\- Tib3rius (anfitriões de exame 5/5 enraizados)

> Recomendo muito que alguém vá para o seu OSCP, fazendo CTFs ou em HTB para verificar esta ferramenta. Estou usando o AutoRecon em HTB há um mês antes de usá-lo nos laboratórios PWK e isso me ajudou a passar no meu exame OSCP. Se você está tendo dificuldade em se instalar com uma metodologia de enumeração, eu encorajo você a seguir o fluxo e as técnicas que este script usa. Ele tira um monte do trabalho tedioso que você provavelmente está acostumado enquanto, ao mesmo tempo, fornecer subdiretórios bem organizados para rapidamente olhar para que você não perca sua cabeça. Os comandos manuais que ele fornece são ótimos para essas situações específicas que precisam dele quando você tiver esgotado as opções. É uma ferramenta muito valiosa, não pode recomendar o suficiente.
>
>\- d0hnuts (anfitriões de exame 5/5 enraizados)

> Autorecon não é qualquer outra ferramenta, é um framweork de correlação de reconhecimento para engajamentos. Isso me ajudou a disparar um monte de varreduras enquanto eu estava trabalhando em outros alvos. Isso pode ajudar muito na gestão do tempo. Isso me ajudou a possuir 4/5 caixas no exame pwk! Resultado: Passado!
>
>\- Wh0ami (enraizado 4/5 máquinas de exame)

> A primeira vez que ouvi falar do AutoRecon eu perguntei se eu realmente precisava disso, minha enumeração estava OK... Eu tentei com uma mente aberta e imediatamente foi um pouco pisou na quantidade de informação que ele iria gerar. Uma vez que eu me acostumei com isso, e comecei a ler o resultado eu percebi o quanto eu estava faltando. Eu usei isso para o exame OSCP, e ele encontrou coisas que eu nunca teria encontrado de outra forma. Eu acredito firmemente, sem AutoRecon eu teria falhado. É uma ótima ferramenta, e eu estou muito impressionado o que Tib3rius foi capaz de criar. Definitivamente algo que eu já estou recomendando para os outros, incluindo você!
>
>\- othornew

> AutoRecon me ajudou a economizar tempo valioso no meu exame OSCP, permitindo-me gastar menos tempo escaneando sistemas e mais tempo invadindo-os. Este software vale o seu peso em ouro!
>
>\- TorHackr

> A ferramenta mágica que fez a enumeração de um pedaço de bolo, apenas acenda-o e veja a beleza de multi-threading cuspindo uma tonelada de informação que teria levado muitos comandos para executar. Eu certamente acredito que apenas usando AutoRecon no exame OSCP, metade do esforço já seria feito. Fortemente recomendado!
>
>\- Arman (solved máquinas de exame 4.5/5)


---

## Procedência desta tradução

Fonte: [https://github.com/Tib3rius/AutoRecon](https://github.com/Tib3rius/AutoRecon/blob/e7e98f60bdc5fb1695159c1bbcdfdf2746d30fa6/README.md). Licença: [GPL-3.0](../../99-Assets/upstream/autorecon/LICENSE.txt). Commit: e7e98f60bdc5fb1695159c1bbcdfdf2746d30fa6.

O original preservado, a lista de mudanças de apresentação e os hashes constam no manifesto do projeto. Nenhum exemplo desta documentação foi executado automaticamente.
