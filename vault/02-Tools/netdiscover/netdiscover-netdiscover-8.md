---
title: "netdiscover — manual de referência"
type: "official-documentation"
tool: "netdiscover"
status: "source-checked"
reviewed: "2026-10-26"
language: "pt-BR"
tags: ["documentation", "tool/netdiscover"]
cssclasses: ["fieldbook"]
source_url: "https://github.com/netdiscover-scanner/netdiscover"
source_kind: "installed-kali-package"
package: "netdiscover"
binary_version: "0.21-1"
source_package: "netdiscover"
source_version: "0.21-1"
source_snapshot_sha256: "9f683de948f8a332ad88282e445f640b44277fa7f895a3f3ca39f1ff49ede37c"
source_sha256: "94a0043626ac895ad1e235c1dae683a8f554a833b84420a621f1c523ceed8f82"
license_spdx: "GPL-3.0-or-later"
human_review: "pending"
source_scope: "Complete selected installed English manual netdiscover(8); upstream README, websites and other documentation remain pending coverage"
binary: "netdiscover"
source_manual_date: "14 Aug 2025"
manual_section: "8"
test_status: "help-only"
tested_version: "netdiscover; pacote netdiscover 0.21-1"
---

> Tradução para português produzida por assistente de IA e conferida seção por seção contra a fonte. Revisão humana independente: pendente. Opções e exemplos originais foram preservados; nenhum exemplo foi executado automaticamente.

> **Compatibilidade observada:** netdiscover; pacote netdiscover 0.21-1. As opções do manual foram encontradas na ajuda instalada. A fonte fixada foi mantida sem trocar opções silenciosamente. Conferida somente a ajuda -h (código 1 observado) e a versão dpkg. HOME temporário, nenhum alvo ou interface fornecido; nenhuma operação de envio, varredura ou captura foi solicitada. Ausência de uma opção na ajuda não demonstra sua rejeição pelo programa. [Evidência e limites do teste](../../99-Assets/evidence/netdiscover-help-tests.json).

<!-- SPDX-License-Identifier: GPL-3.0-or-later -->
# netdiscover

<a id="name"></a>
## NOME

netdiscover - ferramenta de reconhecimento ARP ativo/passivo

<a id="synopsis"></a>
## SINOPSE

```text
netdiscover [-i device] [-r range | -l file | -p] [-m file] [-F filter]
            [-s time] [-c count] [-n node] [-dfPLNS]
```

<a id="description"></a>
## DESCRIÇÃO

netdiscover é uma ferramenta de reconhecimento ARP ativo/passivo, desenvolvida inicialmente para obter informações sobre redes sem fio sem servidores DHCP em cenários de wardriving. Também pode ser usada em redes com switches. Construída sobre libnet e libpcap, pode detectar passivamente hosts online ou procurá-los enviando solicitações ARP.

Além disso, pode ser usada para inspecionar o tráfego ARP da sua rede ou encontrar endereços de rede usando o modo de varredura automática, que examina redes locais comuns.

<a id="options"></a>
## OPÇÕES

### `-i device`

A interface de rede para capturar e injetar pacotes. Se nenhuma interface for especificada, será usada a primeira disponível.

### `-r range`

Varre um intervalo especificado em vez de executar a varredura automática. Valores válidos de intervalo incluem, por exemplo: `192.168.0.0/24`, `192.168.2.0/23`, `192.168.0.0/12` e `192.168.0.0/8`. O netdiscover também é um scanner passivo, e todos os IPs detectados serão exibidos, além dos incluídos no intervalo especificado.

### `-l file`

Varre os intervalos contidos no arquivo especificado. Ele deve conter apenas um intervalo por linha.

### `-p`

Ativa o modo passivo. Nesse modo, o netdiscover não envia nada; apenas captura o tráfego.

### `-m file`

Varre uma lista de MACs e nomes de hosts conhecidos.

### `-F filter`

Personaliza a expressão de filtro pcap (padrão: "`arp`").

### `-s time`

Aguarda o tempo especificado, em milissegundos, entre as injeções de solicitações ARP. (Padrão: 1.)

### `-c count`

Número de vezes que cada solicitação ARP será enviada. Útil em redes com perda de pacotes: a varredura será repetida o número especificado de vezes para cada host. (Padrão: 1.)

### `-n node`

Último octeto do IP de origem usado para a varredura. Você pode alterá-lo se o host padrão (`x.x.x.67`) já estiver em uso. (Intervalo permitido: 2 a 253; padrão: 67.)

### `-d`

Ignora os arquivos de configuração no diretório pessoal (somente para os modos automático e rápido). Serão usados os intervalos e IPs padrão desses modos. Veja abaixo as informações sobre os arquivos de configuração.

### `-R`

Presume que o usuário é root ou possui as capacidades necessárias, sem executar verificações.

### `-f`

Ativa o modo de varredura rápida. Ele examina apenas `.1`, `.100` e `.254` em cada rede. É útil para procurar os intervalos em uso. Depois de encontrar um intervalo, você pode fazer uma varredura específica dele para encontrar máquinas online.

<a id="-p-1"></a>
### `-P`

Produz uma saída adequada para redirecionamento a um arquivo ou análise por outro programa, em vez de usar o modo interativo. Ao ativar esta opção, o netdiscover encerra após varrer os intervalos especificados.

### `-L`

Semelhante a `-P`, mas continua a execução para capturar pacotes ARP passivamente após a varredura ativa. Fase para capturar pacotes ARP passivamente.

### `-N`

Não imprime o cabeçalho. Só é válida quando `-P` ou `-L` está ativada.

### `-S`

(OBSOLETA) Ativa a supressão da espera entre solicitações. Se definida, o netdiscover aguardará após varrer 255 hosts em vez de aguardar após cada um. Esse modo era usado no netdiscover 0.3 beta4 e anteriores. Evite esta opção em redes com perda de pacotes ou redes sem fio com sinal fraco. (Também chamado de modo hardcore.)

<a id="usage"></a>
## USO

Se não estiverem ativadas as opções de modo passivo (`-p`), lista de varredura (`-l`) ou intervalo de varredura (`-r`), o netdiscover varrerá endereços LAN comuns (`192.168.0.0/16`, `172.16.0.0/12` e `10.0.0.0/8`).

Teclas de controle da tela:

|Tecla|Ação|
|---|---|
|`h`|Mostrar a tela de ajuda.|
|`j`|Rolar para baixo (ou seta para baixo).|
|`k`|Rolar para cima (ou seta para cima).|
|`.`|Rolar uma página para cima.|
|`,`|Rolar uma página para baixo.|
|`q`|Fechar a ajuda ou encerrar o aplicativo.|

Visualizações da tela:

|Tecla|Ação|
|---|---|
|`a`|Mostrar a lista de respostas ARP.|
|`r`|Mostrar a lista de solicitações ARP.|
|`u`|Mostrar os hosts únicos detectados.|

<a id="config-files"></a>
## ARQUIVOS DE CONFIGURAÇÃO

O netdiscover procura dois arquivos de configuração a cada execução. Se eles não existirem, usará os valores padrão. Você pode usar a opção `-d` para desativar a leitura e o carregamento desses arquivos.

### `~/.netdiscover/ranges`

Este arquivo contém uma lista de intervalos (um por linha) usados no modo de varredura automática em vez dos intervalos padrão. Por padrão, o netdiscover usa uma lista de intervalos comuns em redes locais.

Exemplo:

```text
    192.168.21.0/24
    172.24.0.0/14
    10.0.0.0/12
```

### `~/.netdiscover/fastips`

Lista que contém o último octeto dos IPs a varrer em cada sub-rede no modo rápido (`-f`); por padrão, (1,100,154). É necessário colocar um número por linha.

> **Nota editorial:** esta parte do original informa 154, enquanto a descrição de `-f` informa 254. Os dois valores foram preservados, sem escolher silenciosamente um deles; o comportamento de varredura não foi testado.

<a id="usage-examples"></a>
## EXEMPLOS DE USO

Varre endereços LAN comuns em eth0:

```text
    # netdiscover -i eth0
```

Varredura rápida de endereços LAN comuns em eth0 (procura apenas gateways):

```text
    # netdiscover -i eth0 -f
```

Varre alguns intervalos fixos:

```text
    # netdiscover -i eth0 -r 172.26.0.0/24
    # netdiscover -r 192.168.0.0/16
    # netdiscover -r 10.0.0.0/8
```

Varre endereços LAN comuns com espera de 0,5 milissegundo em vez do padrão 1:

```text
    # netdiscover -s 0.5
```

Varre um intervalo fixo no modo rápido com espera de 0,5 milissegundo em vez do padrão 1:

```text
    # netdiscover -r 192.168.0.0/16 -f -s 0.5
```

Varre um intervalo usando 101 como último octeto do IP de ORIGEM:

```text
    # netdiscover -r 10.1.0.0/16 -n 101
```

Apenas captura tráfego ARP, sem enviar nada:

```text
    # netdiscover -p
```

<a id="author"></a>
## AUTOR

netdiscover foi escrito por Jaime Penalba Estebanez <jpenalbae@gmail.com>.

Esta página de manual foi escrita originalmente por Nicolas Weyland para o projeto Debian. Ela foi incorporada ao projeto netdiscover e modificada a partir do original por Jaime Penalba e Joao Eriberto Mota Filho.


---

## Procedência desta tradução

Fonte primária: [manual preservado](../../../sources/upstream/netdiscover/netdiscover.8.source), extraído de `/usr/share/man/man8/netdiscover.8.gz`. Pacote `netdiscover`, versão `0.21-1`; pacote-fonte `netdiscover`, versão `0.21-1`. Aquisição de pacote instalado, sem atribuição de commit Git.

Licença: [GPL-3.0-or-later](../../99-Assets/upstream/netdiscover/LICENSE.txt); [copyright e condições do pacote](../../99-Assets/upstream/netdiscover/COPYRIGHT.package.txt). [Página de referência do pacote, não a origem exata do arquivo](https://github.com/netdiscover-scanner/netdiscover). Hashes do original, gzip e avisos no registro de fontes. A data do manual é histórica; não implica que todos os serviços externos mantenham esse comportamento.
