---
title: "naabu — documentação oficial"
type: "official-documentation"
tool: "naabu"
status: "translated-machine"
reviewed: "2026-10-26"
language: "pt-BR"
tags: ["documentation", "tool/naabu"]
cssclasses: ["fieldbook"]
source_url: "https://github.com/projectdiscovery/naabu/blob/a4df9f40ba77bd08920bd47c2adf9f5939edcebb/README.md"
source_commit: "a4df9f40ba77bd08920bd47c2adf9f5939edcebb"
source_sha256: "f61b2cfdd205798a236715d3a20ef54ffaa2e7ac7f5880b0f9170b1bfcb62180"
license_spdx: "MIT"
human_review: "pending"
source_scope: "Official English repository README/docs and available upstream Portuguese README; external manuals/wiki coverage tracked separately"
---

> Tradução automática local para português, ainda sem revisão humana integral. Estrutura e blocos de código preservados; referências externas não significam conteúdo espelhado.

<h1 align="center">
  <img src="../../99-Assets/upstream/naabu/static/naabu-logo.png" alt="naabu" width="200px">
  <br>
</h1>

<p align="center">
<a href="https://opensource.org/licenses/MIT"></a>
<a href="https://github.com/projectdiscovery/naabu/issues"></a>
<a href="https://goreportcard.com/badge/github.com/projectdiscovery/naabu"></a>
<a href="https://github.com/projectdiscovery/naabu/releases"></a>
<a href="https://twitter.com/pdiscoveryio"></a>
<a href="https://discord.gg/projectdiscovery"></a>
</p>

<p align="center">
<a href="#features">Características</a> •
<a href="#installation-instructions">Instalação</a> •
<a href="#usage">Usage</a> •
<a href="#running-naabu">Running naabu</a> •
<a href="#configuration-file">Config</a> •
Integração <a href="#nmap-integration">NMAP</a> •
<a href="#cdnwaf-exclusion">CDN/WAF Exclusão</a> •
<a href="https://discord.gg/projectdiscovery">Discord</a>
</p>

Naabu é uma ferramenta de digitalização de portas escrita em Go que lhe permite enumerar portas válidas para máquinas de uma forma rápida e confiável. É uma ferramenta realmente simples que faz scans rápidas SYN/CONNECT/UDP na máquina/lista de máquinas e listas
Todas as portas que devolvem uma resposta.

# Features

<h1 align="center">
  
  <br>
</h1>

 - Pesquisa rápida e simples baseada em sonda **SYN/CONNECT/UDP**
 - Otimizado para facilidade de uso e **lightweight** em recursos
 - **DNS**
 - **Deduplicação IP automática** para varredura de portas DNS
 - **IPv4/IPv6** Port scan (**perimental**)
 - **Passive** enumeração da porta usando Shodan [Internetdb](https://internetdb.shodan.io)
 - **Host Discovery** (**perimental**)
 - Integração **NMAP** para descoberta de serviços
 - **Custom UDP cargas úteis** para exames CONNECT
 - Sondas **Native UDP de serviço** alimentadas por nmap-sondas de serviço
 - Suporte a múltiplas entradas - **STDIN/HOST/IP/CIDR/ASN**
 - Suporte a vários formatos de saída - **JSON/TXT/STDOUT**

# Usage

```sh
naabu -h
```

Isto irá mostrar a ajuda para a ferramenta. Aqui estão todos os interruptores que suporta.

```yaml
Usage:
  naabu [flags]

Flags:
INPUT:
   -host string[]              hosts to scan ports for (comma-separated)
   -list, -l string            list of hosts to scan ports (file)
   -exclude-hosts, -eh string  hosts to exclude from the scan (comma-separated)
   -exclude-file, -ef string   list of hosts to exclude from scan (file)

PORT:
   -port, -p string              ports to scan (80,443, 100-200)
   -top-ports, -tp string        top ports to scan (default 100) [full,100,1000]
   -exclude-ports, -ep string[]  ports to exclude from scan (file or comma-separated)
   -ports-file, -pf string[]     list of ports to scan (file or comma-separated)
   -port-threshold, -pts int     port threshold to skip port scan for the host
   -exclude-cdn, -ec             skip full port scans for CDN/WAF (only scan for port 80,443)
   -display-cdn, -cdn            display cdn in use

RATE-LIMIT:
   -c int                general internal worker threads (default 25)
   -rate int             packets to send per second (default 1000)
   -tw, -tx-workers int  parallel transmit workers for the fast SYN sender (default 1)

UPDATE:
   -up, -update                 update naabu to latest version
   -duc, -disable-update-check  disable automatic naabu update check

OUTPUT:
   -o, -output string                     file to write output to (optional)
   -lof, -list-output-fields              list of fields to output (comma separated)
   -eof, -exclude-output-fields string[]  exclude output fields output based on a condition
   -j, -json                              write output in JSON lines format
   -csv                                   write output in csv format
   -oX, -xml-output string                write nmap-compatible XML output to file (- for stdout)
   -oG, -grep-output string               write nmap-compatible greppable output to file (- for stdout)
   -oA, -output-all string                write json, xml and greppable output to <basename>.{json,xml,gnmap}

SERVICES-DISCOVERY:
   -sD, -service-discovery           identify services by port number
   -sV, -service-version             detect service versions using nmap-service-probes
   -sV-fast                          only probe port-hinted services (faster, skips fallback)
   -sV-timeout duration              timeout for service version probes (default 5s)
   -sV-workers int                   number of concurrent service version workers (default 25)
   -sV-probes string                 custom nmap-service-probes file path (auto-detected from local nmap install if empty)
   -uP, -udp-probes                  send protocol-specific payloads on UDP scans using nmap-service-probes

CONFIGURATION:
   -config string                   path to the naabu configuration file (default $HOME/.config/naabu/config.yaml)
   -scan-all-ips, -sa               scan all the IP's associated with DNS record
   -ip-version, -iv string[]        ip version to scan of hostname (4,6) - (default 4,6) (default ["4","6"])
   -scan-type, -s string            type of port scan (SYN/CONNECT) (default "c")
   -source-ip string                source ip and port (x.x.x.x:yyy - might not work on OSX) 
   -cp, -connect-payload string    payload to send in CONNECT scans (optional)
   -interface-list, -il             list available interfaces and public ip
   -interface, -i string            network Interface to use for port scan
   -nmap                            invoke nmap scan on targets (nmap must be installed) - Deprecated
   -nmap-cli string                 nmap command to run on found results (example: -nmap-cli 'nmap -sV')
   -r string                        list of custom resolver dns resolution (comma separated or from file)
   -proxy string                    socks5 proxy (ip[:port] / fqdn[:port]
   -proxy-auth string               socks5 proxy authentication (username:password)
   -dns-order string                dns resolution order (p/l/lp/pl) (default "l")
   -sr, -system-resolver            use system DNS as fallback resolver
   -resume                          resume scan using resume.cfg
   -stream                          stream mode (disables resume, nmap, verify, retries, shuffling, etc)
   -passive                         display passive open ports using shodan internetdb api (automatically enables stream mode)
   -irt, -input-read-timeout value  timeout on input read (default 3m0s)
   -no-stdin                        Disable Stdin processing

HOST-DISCOVERY:
   -sn, -host-discovery           Perform Only Host Discovery
   -show-dead                     show hosts that did not respond to host discovery (requires host discovery)
   -Pn, -skip-host-discovery      Skip Host discovery (Deprecated: use -wn/-with-host-discovery instead)
   -wn, -with-host-discovery      Enable Host discovery
   -ps, -probe-tcp-syn string[]   TCP SYN Ping (host discovery needs to be enabled)
   -pa, -probe-tcp-ack string[]   TCP ACK Ping (host discovery needs to be enabled)
   -pe, -probe-icmp-echo          ICMP echo request Ping (host discovery needs to be enabled)
   -pp, -probe-icmp-timestamp     ICMP timestamp request Ping (host discovery needs to be enabled)
   -pm, -probe-icmp-address-mask  ICMP address mask request Ping (host discovery needs to be enabled)
   -arp, -arp-ping                ARP ping (host discovery needs to be enabled)
   -nd, -nd-ping                  IPv6 Neighbor Discovery (host discovery needs to be enabled)
   -rev-ptr                       Reverse PTR lookup for input ips

OPTIMIZATION:
   -retries int                    number of retries for the port scan (default 3)
   -timeout value                  time to wait before timing out (e.g. 500ms, 2s; a bare number is milliseconds) (default 1s)
   -warm-up-time int               time in seconds between scan phases (default 2)
   -T, -timing int                 timing template, higher is faster (0-5) (default 3)
   -ping                           ping probes for verification of host
   -verify                         validate the ports again with TCP verification
   -ss, -smart-scan                predictive port scanning using port correlation model (not compatible with stream mode)
   -pt, -prediction-threshold int  minimum confidence for port predictions (0-100%) (default 20)
   -npp, -no-port-priority         disable tiered port ordering (scan the whole range in one uniform random order)
   -shard string                   distributed scan slice as index/total, 1-based (e.g. 1/4)
   -seed int                       seed for scan randomization, must match across shards (default random)

DEBUG:
   -health-check, -hc        run diagnostic check up
   -debug                    display debugging information
   -verbose, -v              display verbose output
   -no-color, -nc            disable colors in CLI output
   -silent                   display only results in output
   -version                  display version of naabu
   -stats                    display stats of the running scan (deprecated)
   -si, -stats-interval int  number of seconds to wait between showing a statistics update (deprecated) (default 5)
   -mp, -metrics-port int    port to expose naabu metrics on (default 63636)

CLOUD:
   -auth                           configure projectdiscovery cloud (pdcp) api key (default true)
   -ac, -auth-config string        configure projectdiscovery cloud (pdcp) api key credential file
   -pd, -dashboard                 upload / view output in projectdiscovery cloud (pdcp) UI dashboard
   -tid, -team-id string           upload asset results to given team id (optional)
   -aid, -asset-id string          upload new assets to existing asset id (optional)
   -aname, -asset-name string      assets group name to set (optional)
   -pdu, -dashboard-upload string  upload naabu output file (jsonl) in projectdiscovery cloud (pdcp) UI dashboard
```

# Installation Instructions

Baixe o pronto para executar [binário](https://github.com/projectdiscovery/naabu/releases/) / [docker](https://hub.docker.com/r/projectdiscovery/naabu) ou instalar com GO

Em distribuições baseadas em musl, como Alpine, use o arquivo de lançamento `linux_<arch>_musl`.

<a id="prerequisite"></a>
## Pré-requisito

> **Note**: antes de instalar o naabu, certifique-se de instalar a biblioteca `libpcap` para captura de pacotes.

Para instalar o libpcap **Linux**: `sudo apt install -y libpcap-dev`, em **Alpino**: `apk add libpcap`, em **Mac**: `brew install libpcap`, em **Janelas**: instalar [Npcap](https://npcap.com/)


<a id="installing-naabu"></a>
## Instalando o Naabu

```sh
go install -v github.com/projectdiscovery/naabu/v2/cmd/naabu@latest
```

# Running Naabu

Para executar a ferramenta em um alvo, basta usar o seguinte comando.
```sh
naabu -host hackerone.com
```

Isto irá executar a ferramenta contra o hackerone.com. Existem várias opções de configuração que você pode passar com este comando. O interruptor de verbose `-v` pode ser usado para exibir informações de verbose.

```console
naabu -host hackerone.com

                  __
  ___  ___  ___ _/ /  __ __
 / _ \/ _ \/ _ \/ _ \/ // /
/_//_/\_,_/\_,_/_.__/\_,_/ v2.0.3

    projectdiscovery.io

[WRN] Use with caution. You are responsible for your actions
[WRN] Developers assume no liability and are not responsible for any misuse or damage.
[INF] Running SYN scan with root privileges
[INF] Found 4 ports on host hackerone.com (104.16.100.52)

hackerone.com:80
hackerone.com:443
hackerone.com:8443
hackerone.com:8080
```

As portas a procurar na máquina podem ser especificadas através do parâmetro `-p` (as portas udp devem ser expressas como `u:port`). Ele leva nmap portas de formato e executa a enumeração nelas.

```sh
naabu -p 80,443,21-23,u:53 -host hackerone.com
```

Para as varreduras UDP, você pode especificar uma carga útil personalizada para enviar usando a bandeira `-cp` ou `--connect-payload`. Isto é particularmente útil para os serviços UDP que requerem dados específicos para responder:

```sh
naabu -p u:53 -host example.com -cp "DNS query payload"
```

Por padrão, o Naabu verifica as portas `Top 100` do nmap. Ele suporta as seguintes listas de portas integradas -

|Bandeira|Designação das mercadorias|
|-------------------|--------------------------------------|
|`-top-ports 100`|Analisar o topo do mapa **100**|
|`-top-ports 1000`|Analisar o topo do mapa **1000**|
|`-p - `|Procura por portas completas do **1-65535**|

Você também pode especificar portas específicas que você gostaria de excluir da varredura.

```sh
naabu -p - -exclude-ports 80,443
```

Para executar o naabu em uma lista de hosts, a opção `-list` pode ser usada.

```sh
naabu -list hosts.txt
```
Para executar o naabu em um ASN, a entrada AS pode ser usada. Ele pega o endereço IP disponível para determinado ASN e executa a enumeração sobre eles.

```console
echo AS14421 | naabu -p 80,443

216.101.17.249:80
216.101.17.249:443
216.101.17.248:443
216.101.17.252:443
216.101.17.251:80
216.101.17.251:443
216.101.17.250:443
216.101.17.250:80
```
Você também pode obter saída em formato json usando o switch `-json`. Este switch salva a saída no formato de linhas JSON.

```console
naabu -host 104.16.99.52 -json

{"ip":"104.16.99.52","port":443}
{"ip":"104.16.99.52","port":80}
```

As portas descobertas também podem ser canalizadas para outras ferramentas. Por exemplo, você pode canalizar as portas descobertas pelo naabu para o [httpx](https://github.com/projectdiscovery/httpx), que irá então encontrar os servidores http em execução na máquina.

```console
echo hackerone.com | naabu -silent | httpx -silent

http://hackerone.com:8443
http://hackerone.com:443
http://hackerone.com:8080
http://hackerone.com:80
```

A velocidade pode ser controlada alterando o valor da bandeira `rate` que representa o número de pacotes por segundo. Aumentando-a durante o processamento de hosts pode levar a taxas falsas-positivas aumentadas. Por isso, recomenda-se mantê-la a uma quantidade razoável.

# IPv4 and IPv6

Naabu suporta IPv4 e IPv6, e ambos estão habilitados por padrão. Se IPv6 for usado, a conectividade deve ser configurada corretamente, e a interface de rede deve ter um endereço IPv6 atribuído (`inet6`) e um gateway padrão.

```console
echo hackerone.com | naabu -p 80 -silent

104.16.99.52:80
104.16.100.52:80
2606:4700::6810:6434:80
2606:4700::6810:6334:80
```

A opção `-ip-version 6` faz com que a ferramenta use apenas endereços IPv6 ao resolver nomes de domínio.

```console
echo hackerone.com | ./naabu -p 80 -ip-version 6

                  __
  ___  ___  ___ _/ /  __ __
 / _ \/ _ \/ _ \/ _ \/ // /
/_//_/\_,_/\_,_/_.__/\_,_/ v2.0.8

      projectdiscovery.io

Use with caution. You are responsible for your actions
Developers assume no liability and are not responsible for any misuse or damage.
[INF] Running CONNECT scan with non root privileges
[INF] Found 1 ports on host hackerone.com (2606:4700::6810:6334)
hackerone.com:80
```

Para verificar todos os IPs de ambas as versões, a bandeira `-scan-all-ips` pode ser usada.

```console
echo hackerone.com | ./naabu -sa -p 80 -silent

[INF] Found 1 ports on host hackerone.com (104.16.100.52)
hackerone.com:80
[INF] Found 1 ports on host hackerone.com (104.16.99.52)
hackerone.com:80
[INF] Found 1 ports on host hackerone.com (2606:4700::6810:6334)
hackerone.com:80
[INF] Found 1 ports on host hackerone.com (2606:4700::6810:6434)
hackerone.com:80
```

# Host Discovery

Naabu opcionalmente suporta várias opções para executar a descoberta do host. A descoberta do host é opcional e pode ser ativada com a bandeira `-wn`. A bandeira `-sn` instrui a ferramenta para realizar apenas a descoberta do host.

Opções disponíveis para realizar a descoberta do host:

- **ARP** ping (`-arp`)
- TCP **SYN** ping (`-ps 80`)
- TCP **ACK** ping (`-pa 443`)
- ICMP **echo** ping (`-pe`)
- ICMP **timestamp** ping (`-pp`)
- ICMP **address mask** ping (`-pm`)
- IPv6 **neighbor discovery** (`-nd`)

# Configuration file

Naabu suporta arquivo de configuração como padrão localizado no `$HOME/.config/naabu/config.yaml`, Ele permite que você defina qualquer bandeira no arquivo de configuração e defina valores padrão para incluir para todas as varreduras.


# Nmap integration

Nós integramos suporte nmap para descoberta de serviço ou quaisquer varreduras adicionais suportadas pelo nmap nos resultados encontrados pelo Naabu, certifique-se de ter `nmap` instalado para usar este recurso.

Para usar,`nmap-cli` flag pode ser usado seguido pelo comando nmap, por exemplo:-

```console
echo hackerone.com | naabu -nmap-cli 'nmap -sV -oX nmap-output'
                  __       
  ___  ___  ___ _/ /  __ __
 / _ \/ _ \/ _ \/ _ \/ // /
/_//_/\_,_/\_,_/_.__/\_,_/ v2.0.0        

    projectdiscovery.io

[WRN] Use with caution. You are responsible for your actions
[WRN] Developers assume no liability and are not responsible for any misuse or damage.
[INF] Running TCP/ICMP/SYN scan with root privileges
[INF] Found 4 ports on host hackerone.com (104.16.99.52)

hackerone.com:443
hackerone.com:80
hackerone.com:8443
hackerone.com:8080

[INF] Running nmap command: nmap -sV -p 80,8443,8080,443 104.16.99.52

Starting Nmap 7.01 ( https://nmap.org ) at 2020-09-23 05:02 UTC
Nmap scan report for 104.16.99.52
Host is up (0.0021s latency).
PORT     STATE SERVICE       VERSION
80/tcp   open  http          cloudflare
443/tcp  open  ssl/https     cloudflare
8080/tcp open  http-proxy    cloudflare
8443/tcp open  ssl/https-alt cloudflare
```

# Service Version Detection

O Naabu tem a detecção integrada de versões de serviço usando o banco de dados de sondas de serviço do nmap. Isto é executado em paralelo com a digitalização de portas para obter o máximo desempenho.

```sh
naabu -host scanme.sh -sV
```

```console
scanme.sh:22 [ssh OpenSSH/6.6.1p1]
scanme.sh:80 [http Apache httpd/2.4.7]
scanme.sh:9929 [nping-echo Nping echo]

[INF] Found 3 ports on host scanme.sh (45.33.32.156) with 3 services identified
```

Bandeiras disponíveis:

|Bandeira|Designação das mercadorias|
|------|-------------|
|`-sV`|Activar a detecção da versão do serviço|
|`-sV-fast`|Apenas serviços de acesso à porta de sonda (periscópios de retorno mais rápidos, salta)|
|`-sV-timeout duration`|Tempo limite para sondas de versão de serviço (padrão 5s)|
|`-sV-workers int`|Número de trabalhadores de versão de serviço concorrente (padrão 25)|
|`-sV-probes string`|Localização personalizada do arquivo nmap- service- sobes (detectado automaticamente a partir da instalação local do nmap se estiver vazio)|
|`-sD`|Descobrimento do serviço (número da porta de correspondência para o nome do serviço, sem sondagem ativa)|

A bandeira `-sV` requer o arquivo de banco de dados `nmap-service-probes`. Naabu não envia este banco de dados em si (é licenciado sob a licença Nmap Public Source License copyleft, que é incompatível com a licença MIT do naabu), então ele lê o arquivo de uma instalação local do nmap, olhando automaticamente nos caminhos de instalação padrão do nmap. Para usar um arquivo personalizado, especifique o caminho com o `-sV-probes`.

# UDP Service Probes

Os serviços UDP normalmente ficam em silêncio quando recebem um datagram vazio, de modo que uma varredura cega da porta UDP falha a maioria deles. Com `-uP` (`-udp-probes`) o naabu escolhe uma carga útil específica do protocolo da base de dados `nmap-service-probes` para cada porta UDP sendo digitalizada (a consulta DNS para 53, pedido NTP para 123, pedido SNMPv1 GetRequest para 161, e assim por diante), então os serviços reais têm algo para responder e o naabu pode reportá- los como abertos.

```sh
naabu -host scanme.sh -p u:53,u:123,u:161 -uP
```

Notas:

- `-uP` é opte- in e aditivo. Quando desabilitado (o padrão) as varreduras UDP mantêm seu comportamento histórico de zero- comprimento- datagram.
- A sonda selecionada é a mais alta prioridade (mais baixa raridade) correspondente para a porta de destino; se nenhuma sonda for registrada para uma porta, a varredura cai de volta para o datagram vazio.
- Uma carga útil fornecida pelo usuário via `-cp` sempre ganha a sonda automática para essa porta.
- O `-uP` reutiliza o mesmo banco de dados da sonda que o `-sV`, para que possa combinar os dois sem pagar o custo de análise duas vezes. O arquivo da sonda é localizado automaticamente a partir de uma instalação local do nmap; use o `-sV-probes` para apontar para um arquivo personalizado. Se não for possível encontrar nenhum banco de dados, o `-uP` regista um aviso e está silenciosamente desactivado.

# CDN/WAF Exclusion

O Naabu também suporta excluir IPs CDN/WAF sendo digitalizados. Se usado, apenas as portas `80` e `443` são digitalizadas para esses IPs. Esta funcionalidade pode ser ativada usando a opção `exclude-cdn`.

Atualmente, os IPs `cloudflare`, `akamai`, `incapsula` e `sucuri` são suportados para exclusões.

# Scan Status
Naabu expõe informações de digitalização json em uma porta local vinculada ao localhost no `http://localhost:63636/metrics` (a porta pode ser alterada através da bandeira `-metrics-port`)

# Using naabu as library
O seguinte programa de amostra verifica o porto `80` do `scanme.sh`. Os resultados são devolvidos através do retorno de chamada `OnResult`:

```go
package main

import (
	"log"

	"context"
	"github.com/projectdiscovery/goflags"
	"github.com/projectdiscovery/naabu/v2/pkg/result"
	"github.com/projectdiscovery/naabu/v2/pkg/runner"
)

func main() {
	options := runner.Options{
		Host:      goflags.StringSlice{"scanme.sh"},
		ScanType: "s",
		OnResult: func(hr *result.HostResult) {
			log.Println(hr.Host, hr.Ports)
		},
		Ports: "80",
	}

	naabuRunner, err := runner.NewRunner(&options)
	if err != nil {
		log.Fatal(err)
	}
	defer naabuRunner.Close()

	naabuRunner.RunEnumeration(context.Background())
}
```

> **`OnResult`** é chamado uma vez depois que a varredura completa com resultados agregados. **em tempo real** como as portas são descobertas, use **`OnReceive`** em vez disso. `Stream` Option somente controla o carregamento do alvo async – ele não afeta quando os callbacks disparam.

# Notes

- Naabu permite a execução binária arbitrária como um recurso para suportar [integração do nmap](#nmap-integration).
- Naabu é projetado para verificar portas em vários hosts / varredura de porta de massa.
- Como padrão naabu é configurado com uma suposição de que você está executando-o a partir de VPS.
- Sugerimos afinar as bandeiras / taxa se executando naabu do sistema local.
- Para obter melhores resultados, execute naabu como usuário **root**.

-----

Naabu é feito com 🖤 pela equipe [descoberta do projecto](https://projectdiscovery.io). Contribuições comunitárias fizeram o projeto o que é.

Veja o arquivo **[Obrigado, md.](https://github.com/projectdiscovery/naabu/blob/master/THANKS.md)** para mais detalhes.


---

## Procedência desta tradução

Fonte: [https://github.com/projectdiscovery/naabu](https://github.com/projectdiscovery/naabu/blob/a4df9f40ba77bd08920bd47c2adf9f5939edcebb/README.md). Licença: [MIT](../../99-Assets/upstream/naabu/LICENSE.txt). Commit: a4df9f40ba77bd08920bd47c2adf9f5939edcebb.

O original preservado, a lista de mudanças de apresentação e os hashes constam no manifesto do projeto. Nenhum exemplo desta documentação foi executado automaticamente.
