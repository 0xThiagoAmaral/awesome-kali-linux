---
title: "tcpdump — manual de referência"
type: "official-documentation"
tool: "tcpdump"
status: "translated-machine"
reviewed: "2026-10-26"
language: "pt-BR"
tags: ["documentation", "tool/tcpdump"]
cssclasses: ["fieldbook"]
source_url: "https://www.tcpdump.org/"
source_kind: "installed-kali-package"
package: "tcpdump"
binary_version: "4.99.6-2"
source_package: "tcpdump"
source_version: "4.99.6-2"
source_snapshot_sha256: "4795035df33af0b8c303eaf540d06cc989773ce69199e31320ac4a15d9917964"
source_sha256: "a683c08e923292a49006a2efe59eddddb64616bf684c55f56eb5c1a4c0bd3a91"
license_spdx: "LicenseRef-Tcpdump-Manpage"
human_review: "pending"
source_scope: "Complete installed English tcpdump(8) manual; separately referenced pcap-filter(7), pcap(3PCAP), libraries and upstream website documentation remain pending coverage"
binary: "tcpdump"
source_manual_date: "30 June 2025"
manual_section: "8"
test_status: "offline-fixture"
tested_version: "tcpdump version 4.99.6"
---

> Tradução automática local para português, ainda sem revisão humana integral. Estrutura e blocos de código preservados; referências externas não significam conteúdo espelhado.

> **Reconhecimento da licença:** This product includes software developed by the University of California, Lawrence Berkeley Laboratory and its contributors.

> **Compatibilidade observada:** tcpdump version 4.99.6. Ajuda/versão e leitura de PCAP sintético próprio verificadas. Filtros, contagem, gravação de cópia filtrada e rejeição de filtro inválido foram exercitados somente com -r. A ajuda compacta não foi tratada como lista integral de opções. Nenhuma captura ao vivo, interface ou envio foi solicitado. [Evidência e limites do teste](../../99-Assets/evidence/tcpdump-local-tests.json).

# tcpdump

<a id="name"></a>
## NOME

tcpdump - descarga de tráfego em uma rede

<a id="synopsis"></a>
## SINOPSIA

```text
tcpdump [ -AbdDefghHIJKlLnNOpqStuUvxX# ] [ -B buffer_size ] [ -c count ] [ --count ] [ -C file_size ] [ -E spi@ipaddr algo:secret,... ] [ -F file ] [ -G rotate_seconds ] [ -i interface ] [ --immediate-mode ] [ -j tstamp_type ] [ -m module ] [ -M secret ] [ --number ] [ --print ] [ -Q in|out|inout ] [ -r file ] [ -s snaplen ] [ -T type ] [ --version ] [ -V file ] [ -w file ] [ -W filecount ] [ -y datalinktype ] [ -z postrotate-command ] [ -Z user ] [ --time-stamp-precision=tstamp_precision ] [ --micro ] [ --nano ] [ expression ]
```

<a id="description"></a>
## DESCRIÇÃO

`tcpdump` imprime uma descrição do conteúdo dos pacotes numa interface de rede que corresponde ao Booleano `expression` (ver `pcap-filter`7) para a `expression` sintaxe); a descrição é precedida por um selo de tempo, impresso, por padrão, como horas, minutos, segundos e frações de um segundo desde a meia-noite. `-w` flag, que faz com que ele salve os dados do pacote em um arquivo para análise posterior, e/ou com `-r` flag, que faz com que ele leia de um arquivo de pacote salvo em vez de ler pacotes de uma interface de rede. Ele também pode ser executado com o `-V` flag, o que faz com que ele leia uma lista de arquivos de pacotes salvos. Em todos os casos, apenas pacotes que correspondam `expression` será processado por `tcpdump`.

`tcpdump` irá, se não correr com a bandeira `-c`, continuar a capturar pacotes até que seja interrompido por um sinal SIGINT (gerado, por exemplo, digitando seu caractere de interrupção, tipicamente controle-C) ou um sinal SIGTERM (tipicamente gerado com o comando `kill`(1)); se executado com a bandeira `-c`, ele irá capturar pacotes até que seja interrompido por um sinal SIGINT ou SIGTERM ou o número especificado de pacotes tenha sido processado.

Quando o `tcpdump` terminar de capturar pacotes, ele relatará contagens de:

pacotes “capturados” (este é o número de pacotes que o `tcpdump` recebeu e processou);

pacotes “recebidos por filtro” (o significado disto depende do sistema operacional no qual você está executando `tcpdump`, e possivelmente da forma como o sistema operacional foi configurado - se um filtro foi especificado na linha de comando, em alguns sistemas operacionais conta pacotes independentemente se eles foram pareados pela expressão do filtro e, mesmo se eles foram pareados pela expressão do filtro, independentemente de `tcpdump` ter lido e processado eles ainda, em outros sistemas operacionais conta apenas pacotes que foram pareados pela expressão do filtro, independentemente de `tcpdump` tê-los lido e processado ainda, e em outros sistemas operacionais conta apenas pacotes que foram pareados pela expressão do filtro e foram processados pelo `tcpdump`);

pacotes “dropped by kernel” (este é o número de pacotes que foram deixados cair, devido à falta de espaço de buffer, pelo mecanismo de captura de pacotes no sistema operacional no qual o `tcpdump` está em execução, se o sistema operacional reporta essa informação para aplicativos; se não, ele será relatado como 0).

Nas plataformas que suportam o sinal SIGINFO, como a maioria dos BSDs (incluindo o macOS) e o Digital/Tru64 UNIX, ele irá relatar essas contagens quando receber um sinal SIGINFO (gerado, por exemplo, digitando seu caractere “status”, tipicamente control-T, embora em algumas plataformas, como o macOS, o caractere “status” não esteja definido por padrão, então você deve configurá-lo com o `stty`(1) para usá-lo) e continuará capturando pacotes. Em plataformas que não suportam o sinal SIGINFO, o mesmo pode ser alcançado usando o sinal SIGUSR1.

Usando o sinal SIGUSR2 juntamente com a bandeira `-w` irá forçar a descarga do buffer de pacotes no arquivo de saída.

A leitura de pacotes de uma interface de rede pode exigir que você tenha privilégios especiais; veja a página de manual do `pcap`(3PACP) para detalhes. Ler um arquivo de pacotes salvo não requer privilégios especiais.

<a id="options"></a>
## OPÇÕES

### `-A`

Imprime cada pacote (menos o cabeçalho de nível de ligação) no ASCII. Habilidoso para capturar páginas Web. Sem efeito quando as opções `-x[x]` ou `-X[X]` são usadas.

### `-b`

Imprima o número AS nos pacotes BGP na notação ASDOT em vez de notação ASPLAIN.

### `-B buffer_size`

### `--buffer-size=buffer_size`

Defina o tamanho do buffer de captura do sistema operacional em `buffer_size`, em unidades de KiB (1024 bytes).

### `-c count`

Sair após receber pacotes `count`.

### `--count`

Imprime apenas no 'stdout' a contagem de pacotes ao ler os arquivos de captura em vez de processar/imprimir os pacotes. Se for indicado um filtro na linha de comando, o `tcpdump` só conta os pacotes que foram correspondentes à expressão do filtro.

### `-C file_size`

Antes de escrever um pacote em bruto para um arquivo de salvamento, verifique se o arquivo é atualmente maior do que o `file_size` e, se for o caso, feche o arquivo de salvamento atual e abra um novo. Os arquivos de salvamento após o primeiro arquivo de salvamento terão o nome especificado com a bandeira `-w`, com um número depois dele, iniciando em 1 e continuando para cima. A unidade padrão do `file_size` é de milhões de bytes (1.000.000 de bytes, não 1.048.576 bytes).

Ao adicionar um sufixo de k/K, m/M ou g/G ao valor, a unidade pode ser alterada para 1.024 (KiB), 1.048.576 (MiB), ou 1.073.741.824 (GiB), respectivamente.

Note que, quando usado com a opção `-Z` (permitido por padrão), os privilégios são deixados de lado antes de abrir o primeiro arquivo de salvamento.

### `-d`

Descarte o código compilado de correspondência de pacotes em uma forma legível humana para saída padrão e pare.

Por favor, lembre-se de que embora a compilação de código seja sempre específica para DLT, normalmente é impossível (e desnecessário) especificar qual DLT usar para o dump porque `tcpdump` usa o DLT do arquivo pcap de entrada especificado com `-r`, ou o DLT padrão da interface de rede especificada com `-i`, ou o DLT particular da interface de rede especificada com `-y` e `-i`, respectivamente. Nestes casos, o dump mostra o mesmo código exato que filtraria o arquivo de entrada ou a interface de rede sem `-d`.

No entanto, quando nem `-r` nem `-i` é especificado, especificando `-d` impede `tcpdump` de adivinhar uma interface de rede adequada (veja `-i`). Neste caso, o padrão DLT é EN10MB e pode ser configurado para outro valor válido manualmente com `-y`.

### `-dd`

Descarte o código de correspondência de pacotes como um fragmento do programa `C`.

### `-ddd`

Dump packet-matching código como números decimais (precedida com uma contagem).

<a id="-d-1"></a>
### `-D`

### `--list-interfaces`

Imprime a lista das interfaces de rede disponíveis no sistema e no qual o `tcpdump` pode capturar pacotes. Para cada interface de rede, um número e um nome de interface, possivelmente seguido de uma descrição de texto da interface, são impressos. O nome da interface ou o número podem ser fornecidos para a opção `-i` para especificar uma interface na qual capturar.

Isso pode ser útil em sistemas que não têm um comando para listá-los (por exemplo, sistemas Windows, ou sistemas UNIX faltando `ifconfig -a`); o número pode ser útil no Windows 2000 e sistemas posteriores, onde o nome da interface é uma string um tanto complexa.

A bandeira `-D` não será suportada se `tcpdump` foi construída com uma versão mais antiga do `libpcap` que não possui a função `pcap_findalldevs`(3PCAP).

### `-e`

Imprime o cabeçalho de nível de ligação em cada linha de descarga. Isto pode ser usado, por exemplo, para imprimir endereços de camadas MAC para protocolos como Ethernet e IEEE 802.11.

<a id="-e-1"></a>
### `-E`

Use `spi@ipaddr algo:secret` para descriptografar pacotes IPsec ESP que são endereçados ao `addr` e conter o valor do índice de parâmetros de segurança `spi`. Esta combinação pode ser repetida com vírgula ou separação de novas linhas.

Note que a configuração do segredo para pacotes IPv4 ESP é suportada neste momento.

Os algoritmos podem ser `des-cbc`, `3des-cbc`, `blowfish-cbc`, `rc3-cbc`, `cast128-cbc` ou `none`. O padrão é `des-cbc`. A capacidade de descodificar pacotes só está presente se o `tcpdump` foi compilado com criptografia habilitada.

`secret` é o texto ASCII para a chave secreta ESP. Se precedido por 0x, então um valor hexadecimal será lido.

A opção assume RFC 2406 ESP, não RFC 1827 ESP. A opção é apenas para fins de depuração, e o uso desta opção com uma verdadeira chave ‘secreto’ é desencorajado. Ao apresentar a chave secreta IPsec na linha de comando, você a torna visível para outros, através do `ps`(1) e outras ocasiões.

Além da sintaxe acima, a sintaxe `file name` pode ser usada para fazer com que o tcpdump leia o arquivo fornecido. O arquivo é aberto ao receber o primeiro pacote ESP, de modo que quaisquer permissões especiais que o tcpdump possa ter sido dado já deveriam ter sido dadas.

### `-f`

Imprima endereços IPv4 ‘estrangeiros’ numericamente em vez de simbolicamente (esta opção é destinada a contornar sérios danos cerebrais no servidor NIS da Sun — geralmente, ele fica para sempre traduzindo números de internet não-local).

O teste para endereços ‘estrangeiros’ IPv4 é feito usando o endereço IPv4 e a máscara de rede da interface nessa captura está sendo feita. Se esse endereço ou máscara de rede não estiverem disponíveis, seja porque a interface na captura está sendo feita não tem endereço ou máscara de rede ou porque é a pseudo- interface "qualquer" (veja a bandeira `-i` abaixo), esta opção não funcionará corretamente.

### `-F file`

Use o `file` como entrada para a expressão do filtro. Uma expressão adicional dada na linha de comando é ignorada.

### `-g`

### `--ip-oneline`

Não insira uma quebra de linha após o cabeçalho IP no modo verbose.

### `-G rotate_seconds`

Se especificado, roda o arquivo de descarga especificado com a opção `-w` a cada segundo `rotate_seconds`. Os arquivos de salvamento terão o nome especificado pelo `-w` que deverá incluir um formato de tempo, conforme definido pelo `strftime`(3). Se nenhum formato de tempo for especificado, cada novo arquivo substituirá o anterior. Sempre que um nome de arquivo gerado não for único, o tcpdump substituirá os dados preexistentes; fornecendo uma especificação de tempo que seja mais grosseira do que o período de captura não é, portanto, aconselhado.

Se usado em conjunto com a opção `-C`, os nomes de arquivos assumirão a forma de «`file`<count>».

Note que, quando usado com a opção `-Z` (permitido por padrão), os privilégios são deixados de lado antes de abrir o primeiro arquivo de salvamento.

### `-h`

### `--help`

Imprima as strings de versão tcpdump e libpcap, imprima uma mensagem de uso e saia.

### `--version`

Imprime as strings de versão tcpdump e libpcap e sai.

<a id="-h-1"></a>
### `-H`

Tente detectar cabeçalhos de malha de rascunho 802.11s.

### `-i interface`

### `--interface=interface`

Ouça, relate a lista de tipos de camada de links, relate a lista de tipos de carimbos de tempo ou relate os resultados da compilação de uma expressão de filtro no `interface`. Se não for especificado e se a bandeira `-d` não for indicada, o `tcpdump` pesquisa a lista de interface do sistema para a interface mais baixa numerada, configurada (excluindo loopback), que pode ser, por exemplo, “et0”.

Em todos os sistemas Linux suportados, bem como nas versões recentes do macOS e Solaris, um argumento `interface` de “qualquer” significa uma pseudo- interface especial, que captura pacotes de todas as interfaces de rede regulares do sistema operacional. O que é considerado uma interface de rede regular é um detalhe de implementação do sistema operacional (por exemplo, no Linux, isto inclui dispositivos SocketCAN), de modo que os pacotes capturados no “qualquer” pseudo- interface podem representar protocolos de rede mais diferentes do que o esperado. Também todas as interfaces de rede regulares são um subconjunto de todos os dispositivos de captura disponíveis como impresso pela bandeira `-D`. Estes últimos também podem incluir dispositivos de captura que a libpcap implementa por outros meios que não a pilha de rede do sistema operacional: Bluetooth, DAG, D- Bus, SNF e USB. Note que captura no “qualquer” pseudo- interface não será feito em modo promíscuo.

Se a bandeira `-D` é suportada, um número de interface como impresso por essa bandeira pode ser usado como argumento `interface`, se nenhuma interface no sistema tem esse número como um nome.

### `-I`

### `--monitor-mode`

Coloque a interface em "modo monitor"; isso é suportado apenas em interfaces IEE 802.11 Wi-Fi, e suportado apenas em alguns sistemas operacionais.

Note que no modo monitor, o adaptador pode se dissociar da rede com a qual está associado, de modo que você não será capaz de usar nenhuma rede sem fio com esse adaptador. Isto pode impedir o acesso a arquivos em um servidor de rede, ou a resolução de nomes de host ou endereços de rede, se você estiver capturando no modo monitor e não estiver conectado a outra rede com outro adaptador.

Esta opção irá afectar o resultado da opção `-L`. Se o `-I` não for especificado, só serão mostrados os tipos de camada de ligação disponíveis quando não estiverem no modo de monitor; se o `-I` for indicado, só serão mostrados os tipos de camada de ligação disponíveis quando estiverem no modo de monitor.

### `--immediate-mode`

Capture em "modo imediato". Neste modo, os pacotes são entregues ao tcpdump assim que chegam, em vez de serem tamponados para obter eficiência. Este é o padrão ao imprimir pacotes em vez de salvar pacotes para um "arquivo de salvamento" se os pacotes estiverem sendo impressos em um terminal em vez de em um arquivo ou pipe.

### `-j tstamp_type`

### `--time-stamp-type=tstamp_type`

Define o tipo de carimbo de tempo para a captura em `tstamp_type`. Os nomes a usar para os tipos de carimbo de tempo são indicados em `pcap-tstamp`( 7); nem todos os tipos listados serão necessariamente válidos para uma dada interface.

### `-J`

### `--list-time-stamp-types`

Listar os tipos de carimbos de tempo suportados para a interface e sair. Se o tipo de carimbo de tempo não puder ser definido para a interface, não serão listados os tipos de carimbo de tempo.

### `--time-stamp-precision=tstamp_precision`

Ao capturar, defina a precisão do selo de tempo para a captura para `tstamp_precision`. Observe que a disponibilidade de selos de tempo de alta precisão (nanossegundos) e sua precisão real é dependente de plataforma e hardware. Também note que, ao escrever capturas feitas com precisão de nanossegundos para um arquivo de salvamento, os selos de tempo são escritos com resolução de nanossegundos, e o arquivo é escrito com um número mágico diferente, para indicar que os selos de tempo são em segundos e nanossegundos; nem todos os programas que lêem pcap savefiles serão capazes de ler essas capturas.

Ao ler um arquivo de salvamento, converta os selos de tempo para a precisão especificada pelo `timestamp_precision`, e exiba-os com essa resolução. Se a precisão especificada for menor do que a precisão dos selos de tempo no arquivo, a conversão perderá a precisão.

Os valores suportados para `timestamp_precision` são `micro` para resolução de microsegundos e `nano` para resolução de nanossegundos. O padrão é resolução de microsegundos.

### `--micro`

### `--nano`

Shorthands para `--time-stamp-precision=micro` ou `--time-stamp-precision=nano`, ajustando a precisão do carimbo de tempo em conformidade. Ao ler os pacotes de um arquivo de salvamento, usando `--micro` trunca os selos de tempo se o arquivo de salvamento foi criado com precisão de nanossegundos. Em contraste, um arquivo de salvamento criado com precisão de microssegundos terá zeros de rastreamento adicionados ao selo de tempo quando o `--nano` for usado.

### `-K`

### `--dont-verify-checksums`

Não tente verificar as somas de verificação IP, TCP ou UDP. Isto é útil para interfaces que executam alguns ou todos esses cálculos de soma de verificação em hardware; caso contrário, todas as somas de verificação TCP de saída serão marcadas como ruins.

### `-l`

Faça o buffer da linha 'stdout'. Útil se quiser ver os dados enquanto o captura. Por exemplo,

```text
tcpdump -l | tee dat
```

ou

```text
tcpdump -l > dat & tail -f dat
```

Observe que no Windows, "linha buffered" significa "não tampão", de modo que WinDump irá escrever cada caractere individualmente se `-l` é especificado.

`-U` é semelhante ao `-l` em seu comportamento, mas fará com que a saída seja “packet-buffered”, de modo que a saída seja escrita em stdout no final de cada pacote em vez de no final de cada linha; isso é buffered em todas as plataformas, incluindo Windows.

<a id="-l-1"></a>
### `-L`

### `--list-data-link-types`

Listar os tipos de links de dados conhecidos para a interface, no modo especificado e sair. A lista de tipos de links de dados conhecidos pode ser dependente do modo especificado; por exemplo, em algumas plataformas, uma interface Wi-Fi pode suportar um conjunto de tipos de links de dados quando não estiver no modo monitor (por exemplo, pode suportar apenas cabeçalhos Ethernet falsos, ou pode suportar cabeçalhos 802.11 mas não suporta cabeçalhos 802.11 com informações de rádio) e outro conjunto de tipos de links de dados quando estiver no modo monitor (por exemplo, pode suportar cabeçalhos 802.11, ou cabeçalhos 802.11 com informações de rádio, apenas no modo monitor).

### `-m module`

Carregar as definições do módulo MIB do arquivo `module`. Esta opção pode ser usada várias vezes para carregar vários módulos MIB no `tcpdump`.

### `-M secret`

Use `secret` como um segredo compartilhado para validar os digestos encontrados nos segmentos TCP com a opção TCP-MD5 (RFC 2385), se presente.

### `-n`

Não converta endereços (ou seja, endereços de host, números de portas, etc.) para nomes.

<a id="-n-1"></a>
### `-N`

Não imprima a qualificação do nome de domínio de nomes de host. Por exemplo, se você der esta bandeira, então `tcpdump` irá imprimir “nic” em vez de “nic.ddn.mil”.

### `-#`

### `--number`

Imprime um número de pacote no início da linha.

### `-O`

### `--no-optimize`

Não execute o otimizador de código compatível com pacotes. Isto só é útil se suspeitar de um erro no otimizador.

### `-p`

### `--no-promiscuous-mode`

`Don't` colocou a interface no modo promíscuo. Note que a interface pode estar no modo promíscuo por alguma outra razão; portanto, ‘- p’ não pode ser usado como uma abreviatura para ‘éter host {local- hw- addr} ou transmissão de éter’.

### `--print`

Imprime a saída do pacote analisado, mesmo que os pacotes brutos estejam sendo salvos em um arquivo com a bandeira `-w`.

### `-Q direction`

### `--direction=direction`

Escolha a direção de envio/receção `direction` para os quais os pacotes devem ser capturados. Os valores possíveis são ‘in’, ‘out’ e ‘inout’. Não estão disponíveis em todas as plataformas.

### `-q`

Saída rápida (quiet?). Imprima menos informações de protocolo para que as linhas de saída sejam mais curtas.

### `-r file`

Leia pacotes do `file` (que foi criado com a opção `-w` ou por outras ferramentas que escrevem arquivos pcap ou pcapng). Entrada padrão é usada se `file` é “-”.

### `-S`

### `--absolute-tcp-sequence-numbers`

Imprima números absolutos, em vez de relativos, de sequência TCP.

### `-s snaplen`

### `--snapshot-length=snaplen`

Snarf `snaplen` bytes de dados de cada pacote em vez do padrão de 262144 bytes. Pacotes truncados por causa de um instantâneo limitado são indicados na saída com “[ .`proto`]”, onde `proto` é o nome do nível de protocolo em que a truncação ocorreu.

Note que tirar instantâneos maiores aumenta a quantidade de tempo que leva para processar pacotes e, efetivamente, diminui a quantidade de buffering de pacotes. Isto pode fazer com que pacotes sejam perdidos. Lembre- se também que tirar instantâneos menores irá descartar dados de protocolos acima da camada de transporte, o que perde informações que podem ser importantes. As solicitações e respostas do NFS e do AFS, por exemplo, são muito grandes, e muito do detalhe não estará disponível se um tamanho de instantâneo muito curto estiver selecionado.

Se você precisa reduzir o tamanho do instantâneo abaixo do padrão, você deve limitar `snaplen` ao menor número que irá capturar as informações de protocolo que você está interessado. Configurando `snaplen` para 0 o define para o padrão de 262144, para compatibilidade para trás com versões mais antigas recentes do `tcpdump`.

### `-T type`

Forçar os pacotes seleccionados por "`expression`" para ser interpretado o especificado `type`. Os tipos actualmente conhecidos são `aodv` (Protocolo ad hoc a pedido de Vector de Distância), `carp` (Protocolo Comum de Redundância de Endereços), `cnfp` (Protocolo Cisco NetFlow), `domain` (Sistema de Nomes de Domínio), `lmp` (Protocolo de Gestão de Ligações), `pgm` (Pragmático General Multicast), `pgm_zmtp1` (ZMTP/1.0 dentro de PGM/EPGM), `ptp` (Protocolo sobre o Tempo de Precisão), `radius` (RADIUS), `resp` (Protocolo de Serialização REDIS), `rpc` (Chamada de Procedimento Remoto), `rtcp` (Protocolo de controlo de aplicações em tempo real), `rtp` (Protocolo de Aplicações em Tempo Real), `snmp` (Protocolo de Gestão da Rede Simples), `someip` (SOMA/PI), `tftp` (Protocolo de Transferência de arquivos Triviais), `vat` (Ferramenta de Áudio Visual), `vxlan` (Rede Virtual eXtensível de Área Local), `wb` (divulgado White Board) e `zmtp1` (Protocolo de Transporte de Mensagem ZeroMQ) 1.0).

Note que o tipo `pgm` acima afeta apenas a interpretação UDP, o PGM nativo é sempre reconhecido como protocolo IP 113 independentemente. O PGM encapsulado por UDP é frequentemente chamado de "EPGM" ou "PGM/UDP".

Note que o tipo `pgm_zmtp1` acima afeta a interpretação tanto do PGM nativo quanto do UDP ao mesmo tempo. Durante a decodificação PGM nativa, os dados da aplicação de um pacote ODATA/RDATA seriam decodificados como um datagrama ZeroMQ com quadros ZMTP/1.0. Durante a decodificação UDP, além de que qualquer pacote UDP seria tratado como um pacote PGM encapsulado.

### `-t`

`Don't` imprimir um timestamp em cada linha de descarga.

### `-tt`

Imprima o timestamp, como segundos desde 1 de janeiro de 1970, 00:00:00, UTC, e frações de um segundo desde então, em cada linha de despejo.

### `-ttt`

Imprime um delta (resolução de microsegundo ou nanosegundo dependendo da opção `--time-stamp-precision`) entre a linha atual e a linha anterior em cada linha de descarga. O padrão é a resolução de microsegundo.

### `-tttt`

Imprima um timestamp, como horas, minutos, segundos e frações de um segundo desde meia-noite, precedido pela data, em cada linha de despejo.

### `-ttttt`

Imprime um delta (resolução de microsegundo ou nanosegundo dependendo da opção `--time-stamp-precision`) entre a linha atual e a primeira em cada linha de descarga. O padrão é a resolução de microsegundo.

### `-u`

Imprime manipuladores NFS não codificados.

<a id="-u-1"></a>
### `-U`

### `--packet-buffered`

Se a opção `-w` não for especificada, ou se for especificada, mas a bandeira `--print` também for especificada, faça com que a saída impressa do pacote “packet-buffered”; ou seja, como a descrição do conteúdo de cada pacote é impressa, ela será escrita para a saída padrão, ao invés de, ao não escrever em um terminal, ser escrita apenas quando o buffer de saída preencher.

Se a opção `-w` for especificada, faça com que a saída do pacote "packet-buffered" seja salva; ou seja, como cada pacote é salvo, será escrita no arquivo de saída, ao invés de ser escrita apenas quando o buffer de saída preencher.

A bandeira `-U` não será suportada se `tcpdump` foi construída com uma versão mais antiga do `libpcap` que não possui a função `pcap_dump_flush`(3PCAP).

### `-v`

Ao analisar e imprimir, produz (um pouco mais) o resultado verbose. Por exemplo, o tempo de vida, identificação, comprimento total e opções em um pacote IP são impressos. Também permite verificações adicionais de integridade do pacote, como a verificação do IP e a verificação do cabeçalho ICMP.

Ao escrever para um arquivo com a opção `-w` e ao mesmo tempo não ler de um arquivo com a opção `-r`, informe ao stderr, uma vez por segundo, o número de pacotes capturados. No Solaris, no FreeBSD e possivelmente em outros sistemas operacionais, esta atualização periódica atualmente pode causar perda de pacotes capturados no seu caminho do kernel para o tcpdump.

### `-vv`

Ainda mais texto de saída. Por exemplo, campos adicionais são impressos a partir de pacotes de resposta NFS, e os pacotes SMB são totalmente decodificados.

### `-vvv`

Ainda mais verbose saída. Por exemplo, telnet `SB` ... `SE` opções são impressas na íntegra. Com `-X` opções Telnet são impressas em hex também.

### `-V file`

Leia uma lista de nomes de arquivos do `file`. A entrada padrão é usada se o `file` for “-”.

### `-w file`

Escreva os pacotes brutos para `file` em vez de analisá-los e imprimi-los para fora. Eles podem mais tarde ser impressos com a opção -r. Saída padrão é usado se `file` é “-”.

Esta saída será buffered se escrita em um arquivo ou pipe, assim que uma leitura do programa do arquivo ou pipe pode não ver pacotes por um período arbitrário após eles serem recebidos. Use a opção `-U` para fazer com que os pacotes sejam escritos assim que forem recebidos.

O tipo MIME `application/vnd.tcpdump.pcap` foi registrado com o IANA para os arquivos `pcap`. A extensão do nome de arquivo `.pcap` parece ser a mais comumente usada junto com `.cap` e `.dmp`. O `tcpdump` em si não verifica a extensão ao ler os arquivos de captura e não adiciona uma extensão ao escrevê- los (utiliza números mágicos no cabeçalho do arquivo). No entanto, muitos sistemas operacionais e aplicativos usarão a extensão se estiver presente e adicionar um (por exemplo, . pcap) é recomendado.

Veja `pcap-savefile`(5) para uma descrição do formato do arquivo.

### `-W filecount`

Usado em conjunto com a opção `-C`, isto irá limitar o número de arquivos criados ao número indicado, e começar a sobrescrever os arquivos desde o início, criando assim um buffer 'rotatório'. Além disso, irá nomear os arquivos com 0s que cheguem para suportar o número máximo de arquivos, permitindo- lhes classificar correctamente.

Usado em conjunto com a opção `-G`, isso limitará o número de arquivos de descarga girados que são criados, saindo com o status 0 ao atingir o limite.

Se usado em conjunto com `-C` e `-G,`, a opção `-W` será ignorada e afetará apenas o nome do arquivo.

### `-x`

Ao processar e imprimir, para além de imprimir os cabeçalhos de cada pacote, imprime os dados de cada pacote (menos o cabeçalho do nível de ligação) em hexadecimal. O menor dos bytes inteiros do pacote ou do `snaplen` será impresso. Lembre- se que este é o pacote inteiro da camada de ligação, por isso, para as camadas de ligação que o bloco de ligação (por exemplo, Ethernet), os bytes de enchimento também serão impressos quando o pacote de camada superior for mais curto do que o necessário. Na implementação actual, esta opção poderá ter o mesmo efeito que o `-xx` se o pacote for truncado. Sem efeito quando for usada a opção `-X[X]`.

### `-xx`

Ao analisar e imprimir, além de imprimir os cabeçalhos de cada pacote, imprima os dados de cada pacote, `including` seu cabeçalho de nível de ligação, em hex. Sem efeito quando a opção `-X[X]` é usada.

<a id="-x-1"></a>
### `-X`

Ao analisar e imprimir, para além de imprimir os cabeçalhos de cada pacote, imprima os dados de cada pacote (menos o cabeçalho de nível de ligação) no Hex e no ASCII. Isto é muito útil para analisar novos protocolos. Na implementação actual, esta opção poderá ter o mesmo efeito que o `-XX` se o pacote for truncado.

<a id="-xx-1"></a>
### `-XX`

Ao analisar e imprimir, além de imprimir os cabeçalhos de cada pacote, imprima os dados de cada pacote, `including` seu cabeçalho de nível de ligação, em hex e ASCII.

### `-y datalinktype`

### `--linktype=datalinktype`

Defina o tipo de link de dados para usar durante a captura de pacotes (veja `-L`) ou apenas compilando e despejando código de correspondência de pacotes (veja `-d`) para `datalinktype`.

### `-z postrotate-command`

Usado em conjunto com as opções `-C` ou `-G`, isto fará com que `tcpdump` execute " `postrotate-command file` " onde `file` é o arquivo de salvamento que está sendo fechado após cada rotação. Por exemplo, especificando `-z gzip` ou `-z bzip2` irá comprimir cada arquivo de salvamento usando gzip ou bzip2.

Esta opção só pode ser usada se for implementado subprocesso fork (por exemplo, não em sistemas Windows).

Note que o tcpdump executará o comando em paralelo à captura, usando a menor prioridade para que isso não perturbe o processo de captura.

E no caso de você gostaria de usar um comando que em si leva bandeiras ou argumentos diferentes, você sempre pode escrever um script shell que vai tomar o nome savefile como o único argumento, fazer os arranjos de bandeiras & argumentos e executar o comando que você deseja.

### `-Z user`

### `--relinquish-privileges=user`

Se o `tcpdump` estiver rodando como root, depois de abrir o dispositivo de captura ou o arquivo de entrada, mas antes de abrir qualquer arquivo de salvamento para saída, mude o ID do usuário para `user` e o ID do grupo para o grupo primário do `user`.

Este comportamento é ativado por padrão (`-Z tcpdump`), e pode ser desativado pelo `-Z root`.

### ` expression`

selecciona os pacotes que serão largados. Se não for dado `expression`, todos os pacotes na rede serão largados. Caso contrário, apenas os pacotes para os quais o `expression` é ‘verdadeiro’ serão largados.

Para a sintaxe `expression`, veja `pcap-filter`(7).

O argumento `expression` pode ser passado para o `tcpdump` como um único argumento de Shell, ou como vários argumentos de Shell, o que for mais conveniente. Geralmente, se a expressão contém metacaracteres de Shell, tais como contra- linhas usadas para escapar dos nomes dos protocolos, é mais fácil passá- lo como um único argumento citado em vez de escapar aos metacaracteres de Shell. Vários argumentos são concatenados com espaços antes de serem analisados.

<a id="examples"></a>
## EXEMPLOS

Para imprimir todos os pacotes que chegam ou partem do `sundown`:

```text
tcpdump host sundown
```

Para imprimir o tráfego entre `helios` e `hot` ou `ace`:

```text
tcpdump host helios and \( hot or ace \)
```

Para imprimir todos os pacotes IP entre o `ace` e qualquer máquina, excepto o `helios`:

```text
tcpdump ip host ace and not helios
```

Para imprimir todo o tráfego entre anfitriões locais e anfitriões em Berkeley:

```text
tcpdump net ucb-ether
```

Para imprimir todo o tráfego de ftp através do gateway de internet `snup`: (note que a expressão é citada para evitar que o shell de (mis-)interprete os parênteses):

```text
tcpdump 'gateway snup and (port ftp or ftp-data)'
```

Para imprimir o tráfego não originado nem destinado a hosts locais (se você gateway para uma outra rede, este material nunca deve fazê-lo em sua rede local).

```text
tcpdump ip and not net localnet
```

Para imprimir os pacotes de início e fim (os pacotes SYN e FIN) de cada conversa TCP que envolve um host não-local.

```text
tcpdump 'tcp[tcpflags] & (tcp-syn|tcp-fin) != 0 and not src and dst net localnet'
```

Para imprimir os pacotes TCP com bandeiras RST e ACK ambos definidos. (i.e., selecione apenas as bandeiras RST e ACK no campo bandeiras, e se o resultado for "RST e ACK ambos definidos", combinar)

```text
tcpdump 'tcp[tcpflags] & (tcp-rst|tcp-ack) == (tcp-rst|tcp-ack)'
```

Para imprimir todos os pacotes IPv4 HTTP de e para a porta 80, ou seja, imprimir apenas pacotes que contenham dados, não, por exemplo, pacotes SYN e FIN e pacotes apenas ACK. (IPv6 é deixado como um exercício para o leitor.)

```text
tcpdump 'tcp port 80 and (((ip[2:2] - ((ip[0]&0xf)<<2)) - ((tcp[12]&0xf0)>>2)) != 0)'
```

Para imprimir pacotes IP maiores que 576 bytes enviados através do gateway `snup`:

```text
tcpdump 'gateway snup and ip[2:2] > 576'
```

Para imprimir pacotes de transmissão IP ou multicast que foram enviados `not` via transmissão Ethernet ou multicast:

```text
tcpdump 'ether[0] & 1 = 0 and ip[16] >= 224'
```

Para imprimir todos os pacotes ICMP que não são requisições/respostas de eco (isto é, pacotes de ping não):

```text
tcpdump 'icmp[icmptype] != icmp-echo and icmp[icmptype] != icmp-echoreply'
```

<a id="output-format"></a>
## FORMATO DE NOTIFICAÇÃO

O resultado do `tcpdump` é dependente do protocolo. O seguinte dá uma breve descrição e exemplos da maioria dos formatos.

### Timestamps

Por padrão, todas as linhas de saída são precedidas por uma data- horário. A hora- horário é a hora atual do relógio no formulário

```text
hh:mm:ss.frac
```

e é tão preciso quanto o relógio do kernel. O timestamp reflete o tempo em que o kernel aplicou um selo de tempo no pacote. Nenhuma tentativa é feita para contabilizar o intervalo de tempo entre quando a interface de rede terminou de receber o pacote da rede e quando o kernel aplicou um selo de tempo no pacote; esse defasamento de tempo poderia incluir um atraso entre o tempo em que a interface de rede terminou de receber um pacote da rede e o tempo em que uma interrupção foi entregue ao kernel para fazê- lo ler o pacote e um atraso entre o tempo em que o kernel servia a interrupção do ‘novo pacote’ e o tempo em que ele aplicou um selo de tempo no pacote.

### Interface

Quando a interface `any` é selecionada na captura ou quando um arquivo de captura `LINUX_SLL2` do tipo link é lido, o nome da interface é impresso após o timestamp. Isto é seguido pelo tipo de pacote com `In` e `Out` denotando um pacote destinado a esta máquina ou originado desta máquina, respectivamente. Outros valores possíveis são `B` para pacotes de transmissão, `M` para pacotes multicast e `P` para pacotes destinados a outras máquinas.

<a id="link-level-headers"></a>
### Cabeçalhos de Nível de Ligação

Se a opção '-e' for dada, o cabeçalho de nível de ligação é impresso. Nas Ethernets, os endereços de origem e destino, protocolo e comprimento do pacote são impressos.

Nas redes FDDI, a opção '-e' faz com que o `tcpdump` imprima o campo ‘controlo de quadros’, os endereços de origem e destino e o comprimento do pacote. (O campo ‘controlo de quadros’ governa a interpretação do resto do pacote. Os pacotes normais (como os que contêm datagramas IP) são pacotes ‘assincronizados’, com um valor prioritário entre 0 e 7; por exemplo, ‘`async4`’. Supõe-se que esses pacotes contenham um pacote 802.2 Logical Link Control (LLC); o cabeçalho LLC é impresso se for `not` um datagrama ISO ou um pacote chamado SNAP.

Nas redes Token Ring, a opção '-e' faz com que `tcpdump` imprima os campos 'controlo de acesso' e 'controlo de frame', os endereços de origem e destino e o comprimento do pacote. Como nas redes FDDI, os pacotes são assumidos para conter um pacote LLC. Independentemente se a opção '-e' é especificada ou não, a informação de roteamento de origem é impressa para pacotes roteados.

Nas redes 802.11, a opção '-e' faz com que `tcpdump` imprima os campos de 'controle de quadros', todos os endereços no cabeçalho 802.11 e o comprimento do pacote. Como nas redes FDDI, os pacotes são assumidos para conter um pacote LLC.

(N.B.: A seguinte descrição assume familiaridade com o algoritmo de compressão SLIP descrito na RFC 1144.)

Nas ligações SLIP, um indicador de direcção (“I” para a entrada, “O” para a saída), tipo de pacote e informação de compressão são impressos. O tipo de pacote é impresso primeiro. Os três tipos são `ip`, `utcp` e `ctcp`. Não são impressas outras informações de ligação para os pacotes `ip`. Para os pacotes TCP, o identificador de ligação é impresso seguindo o tipo. Se o pacote for comprimido, o cabeçalho codificado é impresso. Os casos especiais são impressos como `*S+n` e `*SA+n`, onde `n` é a quantidade pela qual o número de sequência (ou número de sequência e ack) foi alterado. Se não for um caso especial, são impressas zero ou mais alterações. Uma alteração é indicada por U (urgente ponteiro), W (window), A (ack), S (número de sequência) e I (pacote ID), seguida por um delta (+n) ou por um novo valor impresso (ou o valor do pacote).

Por exemplo, a seguinte linha mostra um pacote TCP comprimido de saída, com um identificador de conexão implícito; o ack mudou em 6, o número de sequência em 49, e o ID de pacote em 6; existem 3 bytes de dados e 6 bytes de cabeçalho comprimido:

```text
O ctcp * A+6 S+49 I+6 3 (6)
```

<a id="arprarp-packets"></a>
### Pacotes ARP/RARP

O resultado do ARP/RARP mostra o tipo de requisição e os seus argumentos. O formato destina- se a ser autoexplicativo. Aqui está uma amostra curta recolhida desde o início de um 'rlogin' do `rtsg` da máquina para o `csam` da máquina:

```text
arp who-has csam tell rtsg
arp reply csam is-at CSAM
```

A primeira linha diz que rtsg enviou um pacote ARP pedindo o endereço Ethernet do csam do host da internet. Csam responde com o seu endereço Ethernet (neste exemplo, endereços Ethernet estão em caps e endereços de internet em minúsculas).

Isso pareceria menos redundante se tivéssemos feito `tcpdump -n`:

```text
arp who-has 128.3.254.6 tell 128.3.254.68
arp reply 128.3.254.6 is-at 02:07:01:00:01:c4
```

Se tivéssemos feito `tcpdump -e`, o fato de que o primeiro pacote é transmitido e o segundo é ponto-a-ponto seria visível:

```text
RTSG Broadcast 0806  64: arp who-has csam tell rtsg
CSAM RTSG 0806  64: arp reply csam is-at CSAM
```

Para o primeiro pacote isto diz que o endereço de origem Ethernet é RTSG, o destino é o endereço de transmissão Ethernet, o campo de tipo continha hex 0806 (tipo ETHER_ARP) e o comprimento total era de 64 bytes.

<a id="ipv4-packets"></a>
### Pacotes IPv4

Se o cabeçalho da camada de links não estiver sendo impresso, para pacotes IPv4, `IP` é impresso após o carimbo de tempo.

Se a opção `-v` for indicada, as informações do cabeçalho IPv4 são mostradas entre parênteses após o cabeçalho `IP` ou a camada de ligação. O formato geral desta informação é:

```text
tos tos, ttl ttl, id id, offset offset, flags [flags], proto proto, length length, options (options)
```

`tos` é o tipo de campo de serviço; se os bits ECN não forem zero, estes são reportados como `ECT(1)`, `ECT(0)`, ou `CE`. `ttl` é o tempo de vida; não é reportado se for zero. `id` é o campo de identificação IP. `offset` é o campo offset do fragmento; é impresso se isto faz parte de um datagram fragmentado ou não. `flags` são os pavilhões MF e DF; `+` é reportado se o MF estiver definido, e `DF` é reportado se F estiver definido. Se nenhum dos dois estiver definido, `.` foi reportado. `proto` é o campo de identificação do protocolo. `length` é o campo de comprimento total; se o pacote for um ORT presumido (TCP Segmentação Offload) enviar, [foi 0, presumível ORT] é comunicado. `options` são as opções IP, se houver.

Em seguida, para os pacotes TCP e UDP, os endereços IP de origem e destino e as portas TCP ou UDP, com um ponto entre cada endereço IP e sua porta correspondente, serão impressos, com um > separando a fonte e o destino. Para outros protocolos, os endereços serão impressos, com um > separando a fonte e o destino. Informações de protocolo de nível superior, se houver, serão impressas depois disso.

Para os datagramas IP fragmentados, o primeiro fragmento contém o cabeçalho do protocolo de nível superior; os fragmentos após o primeiro não contêm nenhum cabeçalho do protocolo de nível superior. As informações de fragmentação serão impressas apenas com a opção `-v`, na informação do cabeçalho IP, conforme descrito acima.

<a id="tcp-packets"></a>
### Pacotes TCP

(N.B.:A seguinte descrição assume familiaridade com o protocolo TCP descrito em RFC 793. Se você não estiver familiarizado com o protocolo, esta descrição não será muito útil para você.)

O formato geral de uma linha de protocolo TCP é:

```text
src > dst: Flags [tcpflags], seq data-seqno, ack ackno, win window, urg urgent, options [opts], length len
```

`Src` e `dst` são os endereços IP de origem e destino e as portas. `Tcpflags` são uma combinação de S (SYN), F (FIN), P (PSH), R (RST), U (URG), W (CWR), E (ECE) ou «.» (ACK), ou «nenhuma» se não forem fixados pavilhões. `Data-seqno` descreve a parte do espaço de sequência coberta pelos dados neste pacote (ver exemplo abaixo). `Ackno` é o número de sequência dos próximos dados esperados para a outra direção nesta conexão. `Window` é o número de bytes de espaço de buffer de recebimento disponíveis na outra direção nesta conexão. `Urg` indica que existem dados «urgentes» no pacote. `Opts` are TCP opções (por exemplo, mss 1024). `Len` é o comprimento dos dados de carga útil.

`Iptype`, `Src`, `dst` e `flags` estão sempre presentes. Os outros campos dependem do conteúdo do cabeçalho do protocolo TCP do pacote e só são de saída se apropriado.

Aqui está a parte de abertura de um rlogin da máquina `rtsg` para a máquina `csam`.

```text
IP rtsg.1023 > csam.login: Flags [S], seq 768512:768512, win 4096, opts [mss 1024]
IP csam.login > rtsg.1023: Flags [S.], seq, 947648:947648, ack 768513, win 4096, opts [mss 1024]
IP rtsg.1023 > csam.login: Flags [.], ack 1, win 4096
IP rtsg.1023 > csam.login: Flags [P.], seq 1:2, ack 1, win 4096, length 1
IP csam.login > rtsg.1023: Flags [.], ack 2, win 4096
IP rtsg.1023 > csam.login: Flags [P.], seq 2:21, ack 1, win 4096, length 19
IP csam.login > rtsg.1023: Flags [P.], seq 1:2, ack 21, win 4077, length 1
IP csam.login > rtsg.1023: Flags [P.], seq 2:3, ack 21, win 4077, urg 1, length 1
IP csam.login > rtsg.1023: Flags [P.], seq 3:4, ack 21, win 4077, urg 1, length 1
```

A primeira linha diz que a porta TCP 1023 no rtsg enviou um pacote para o `login` no csam. O `S` indica que a bandeira `SYN` foi definida. O número de sequência do pacote foi 768512 e não continha dados. (A notação é ‘primeiro:último’, o que significa `sequence numbers `first` up to but not including `last`'.) Não houve nenhum ACK com suporte de piggy, a janela de recepção disponível foi de 4096 bytes e havia uma opção de tamanho de segmento máximo solicitando um MSS de 1024 bytes.

O Csam responde com um pacote semelhante, exceto que inclui um ACK com suporte de piggy para o SYN do rtsg. Rtsg então ACKs Csam's SYN. O ‘.’ significa que a opção ACK foi definida. O pacote não contém dados, de modo que não há nenhum número de sequência de dados ou comprimento. Lembre- se que o número de sequência ACK é um número inteiro pequeno (1). A primeira vez que o `tcpdump` vê uma ‘conversação’ do TCP, imprime o número de sequência do pacote. Nos pacotes subsequentes da conversa, a diferença entre o número de sequência do pacote atual e este número de sequência inicial é impressa. Isto significa que os números de sequência após o primeiro podem ser interpretados como posições de byte relativas no fluxo de dados da conversação (com o primeiro byte cada direção sendo ‘1’). O ‘- S’ irá substituir esta funcionalidade, fazendo com que os números de sequência originais sejam obtidos.

Na 6a linha, o rtsg envia ao csam 19 bytes de dados (bytes 2 a 20 no lado rtsg → csam da conversa). A opção PSH está definida no pacote. Na 7a linha, o csam diz que recebeu dados enviados pelo rtsg até mas não incluindo o byte 21. A maioria destes dados está aparentemente no buffer do socket desde que a janela de recepção do csam ficou 19 bytes menor. O Csam também envia um byte de dados para o rtsg neste pacote. Nas 8 e 9 linhas, o csam envia dois bytes de urgência, empurrando os dados para o rtsg.

Se o snapshot foi pequeno o suficiente para que o `tcpdump` não capturasse o cabeçalho completo do TCP, ele interpreta tanto do cabeçalho quanto pode e então relata “[□`tcp`]” para indicar que o restante não poderia ser interpretado. Se o cabeçalho contém uma opção falsa (uma com um comprimento que é demasiado pequeno ou além do final do cabeçalho), `tcpdump` o relata como “[`bad opt`]” e não interpreta quaisquer outras opções (já que é impossível dizer onde eles começam). Se o comprimento do cabeçalho indica opções estão presentes, mas o comprimento do datagrama IP não é suficiente para as opções estarem realmente lá, `tcpdump` relata como “[`bad hdr length`]”.

<a id="particular-tcp-flag-combinations-syn-ack-urg-ack-etc"></a>
### Combinações particulares de bandeira TCP (SYN-ACK, URG-ACK, etc.)

Existem 8 bits na seção de bits de controle do cabeçalho TCP:

`CWR | ECE | URG | ACK | PSH | RST | SYN | FIN`

Vamos supor que queremos assistir pacotes usados para estabelecer uma conexão TCP. Lembre-se que TCP usa um protocolo de aperto de mão de 3 vias quando ele inicializa uma nova conexão; a sequência de conexão com relação aos bits de controle TCP é

1) Chamador envia SYN 2) Destinatário responde com SYN, ACK 3) Chamador envia ACK

Agora estamos interessados em capturar pacotes que têm apenas o conjunto de bits SYN (Passo 1). Note que não queremos pacotes do passo 2 (SYN-ACK), apenas um SYN inicial simples. O que precisamos é de uma expressão de filtro correta para `tcpdump`.

Lembre-se da estrutura de um cabeçalho TCP sem opções:

```text
 0                            15                              31
-----------------------------------------------------------------
|          source port          |       destination port        |
-----------------------------------------------------------------
|                        sequence number                        |
-----------------------------------------------------------------
|                     acknowledgment number                     |
-----------------------------------------------------------------
|  HL   | rsvd  |C|E|U|A|P|R|S|F|        window size            |
-----------------------------------------------------------------
|         TCP checksum          |       urgent pointer          |
-----------------------------------------------------------------
```

Um cabeçalho TCP normalmente contém 20 octets de dados, a menos que as opções estejam presentes. A primeira linha do gráfico contém 0 - 3, a segunda linha mostra os octets 4 - 7, etc.

Começando a contar com 0, os bits de controle TCP relevantes estão contidos no octeto 13:

```text
 0             7|             15|             23|             31
----------------|---------------|---------------|----------------
|  HL   | rsvd  |C|E|U|A|P|R|S|F|        window size            |
----------------|---------------|---------------|----------------
|               |  13th octet   |               |               |
```

Vamos dar uma olhada mais de perto no octeto no 13:

```text
                |               |
                |---------------|
                |C|E|U|A|P|R|S|F|
                |---------------|
                |7   5   3     0|
```

Estes são os bits de controle TCP em que estamos interessados. Nós numeramos os bits neste octeto de 0 a 7, da direita para a esquerda, então o bit PSH é o número 3, enquanto o bit URG é o número 5.

Lembre-se que queremos capturar pacotes com apenas o conjunto SYN. Vamos ver o que acontece com o octet 13 se um datagram TCP chega com o bit SYN definido em seu cabeçalho:

```text
                |C|E|U|A|P|R|S|F|
                |---------------|
                |0 0 0 0 0 0 1 0|
                |---------------|
                |7 6 5 4 3 2 1 0|
```

Olhando para a seção de bits de controle vemos que apenas o bit número 1 (SYN) está definido.

Assumindo que octet número 13 é um inteiro de 8 bits não assinado na ordem de byte de rede, o valor binário deste octet é

00000010

e a sua representação decimal é

```text
   7     6     5     4     3     2     1     0
0*2 + 0*2 + 0*2 + 0*2 + 0*2 + 0*2 + 1*2 + 0*2  =  2
```

Estamos quase terminados, porque agora sabemos que se apenas SYN é definido, o valor do 13o octeto no cabeçalho TCP, quando interpretado como um inteiro de 8 bits não assinado na ordem byte de rede, deve ser exatamente 2.

Esta relação pode ser expressa como

tcp[13] == 2

Podemos usar esta expressão como o filtro para `tcpdump`, a fim de assistir pacotes que têm apenas SYN definido:

tcpdump -i xl0 'tcp[13] == 2'

A expressão diz "deixar o 13o octeto de um datagrama TCP ter o valor decimal 2", que é exatamente o que queremos.

Agora, vamos assumir que precisamos capturar pacotes SYN, mas não nos importa se ACK ou qualquer outro bit de controle TCP é definido ao mesmo tempo. Vamos ver o que acontece com o octeto 13 quando um datagrama TCP com o conjunto SYN-ACK chega:

```text
     |C|E|U|A|P|R|S|F|
     |---------------|
     |0 0 0 1 0 0 1 0|
     |---------------|
     |7 6 5 4 3 2 1 0|
```

Agora os bits 1 e 4 são definidos no 13o octeto. O valor binário do octeto 13 é

00010010

que se traduz em decimal

```text
   7     6     5     4     3     2     1     0
0*2 + 0*2 + 0*2 + 1*2 + 0*2 + 0*2 + 1*2 + 0*2   = 18
```

Agora não podemos usar apenas 'tcp[13] == 18' na expressão do filtro `tcpdump`, porque isso selecionaria apenas os pacotes que têm o conjunto SYN-ACK, mas não aqueles com apenas o conjunto SYN. Lembre-se que não nos importa se o ACK ou qualquer outro bit de controle é definido enquanto o SYN estiver definido.

Para alcançar nosso objetivo, precisamos logicamente E o valor binário do octeto 13 com algum outro valor para preservar o bit SYN. Sabemos que queremos que o SYN seja definido em qualquer caso, então logicamente E o valor no 13o octeto com o valor binário de um SYN:

```text
          00010010 SYN-ACK              00000010 SYN
     AND  00000010 (we want SYN)   AND  00000010 (we want SYN)
          --------                      --------
     =    00000010                 =    00000010
```

Vemos que esta operação AND oferece o mesmo resultado, independentemente se ACK ou outro bit de controle TCP está definido. A representação decimal do valor AND, bem como o resultado desta operação é 2 (m00000/10 binário), então sabemos que para pacotes com SYN definido a seguinte relação deve manter true:

( ( valor de octeto 13 ) E ( 2 ) ) == ( 2 )

Isto indica- nos a expressão do filtro `tcpdump`

tcpdump -i xl0 'tcp[13] & 2 == 2'

Alguns deslocamentos e valores de campo podem ser expressos como nomes em vez de como valores numéricos. Por exemplo, o tcp[ 13] pode ser substituído por tcp[ tcpflags]. Os seguintes valores de campo de bandeira TCP também estão disponíveis: tcp- fin, tcp- syn, tcp- rst, tcp- push, tcp- ack, tcp- urg, tcp- ece e tcp- cwr.

Tal pode ser demonstrado como:

tcpdump - i xl0 'tcp[ tcpflags] & tcp- push != 0'

Note que você deve usar aspas simples ou uma barra na expressão para ocultar o caractere especial AND ('&') da shell.

<a id="udp-packets"></a>
### Pacotes UDP

O formato UDP é ilustrado por este pacote rwho:

```text
actinide.who > broadcast.who: udp 84
```

Isto diz que a porta `who` no host `actinide` enviou um datagram UDP para o porto `who` no host `broadcast`, o endereço de transmissão da Internet. O pacote continha 84 bytes de dados do usuário.

Alguns serviços UDP são reconhecidos (a partir da fonte ou número do porto de destino) e as informações de protocolo de nível superior impressas. Em particular, pedidos de serviço de Nome de Domínio (RFC 1034/1035) e chamadas RPC Sun (RFC 1050) para NFS.

<a id="tcp-or-udp-name-server-requests"></a>
### Pedidos de Servidor de Nomes TCP ou UDP

(N.B.:A seguinte descrição assume familiaridade com o protocolo Domain Service descrito na RFC 1035. Se você não estiver familiarizado com o protocolo, a seguinte descrição parecerá escrita em grego.)

Os pedidos do servidor de nomes são formatados como

```text
src > dst: id op? flags qtype qclass name (len)

h2opolo.1538 > helios.domain: 3+ A? ucbvax.berkeley.edu. (37)
```

O servidor `h2opolo` pediu ao servidor de domínio no `helios` para um registo de endereços (qtype=A) associado ao nome `ucbvax.berkeley.edu.` O ID da consulta foi ‘3’. O ‘+’ indica que a opção `recursion desired` foi definida. O comprimento da consulta foi de 37 bytes, excluindo os cabeçalhos do protocolo TCP ou UDP e IP. A operação de consulta foi a normal, `Query`, por isso o campo de operação foi omitido. Se a opção tivesse sido outra coisa, teria sido impressa entre o ‘3’ e o ‘+’. Da mesma forma, o qclass era o normal, o `C_IN`, e omitido. Qualquer outro qclass teria sido impresso imediatamente após o ‘A’.

Algumas anomalias são verificadas e podem resultar em campos adicionais fechados entre parênteses rectos: Se uma consulta contiver uma resposta, registos de autoridade ou secção de registos adicionais, `ancount`, `nscount`, ou `arcount` são impressos sob a forma de «[`n`a]’, ‘[`n`n]» ou «[`n`au]» onde `n` Se algum dos bits de resposta estiver definido (AA, RA ou rcode) ou qualquer dos bits de ‘deve ser zero’ estiver definido em bytes dois e três, ‘[b2&3=`x`]» é impressa, em que `x` é o valor hexadecimal dos bytes de cabeçalho dois e três.

<a id="tcp-or-udp-name-server-responses"></a>
### Respostas ao Servidor de Nomes TCP ou UDP

As respostas do servidor de nomes são formatadas como

```text
src > dst:  id op rcode flags a/n/au type class data (len)

helios.domain > h2opolo.1538: 3 3/3/7 A 128.32.137.3 (273)
helios.domain > h2opolo.1537: 2 NXDomain* 0/1/0 (97)
```

No primeiro exemplo, o `helios` responde à consulta id 3 do `h2opolo` com 3 registros de respostas, 3 registros de servidores de nomes e 7 registros adicionais. O primeiro registro de respostas é o tipo A (endereço) e seus dados são o endereço de internet 128.32.137.3. O tamanho total da resposta foi 273 bytes, excluindo o TCP ou os cabeçalhos UDP e IP. O op (Query) e o código de resposta (NoErro) foram omitidos, assim como a classe (C_IN) do registro A.

No segundo exemplo, o `helios` responde à consulta 2 com um código de resposta de domínio inexistente (NXDomain) sem respostas, um servidor de nome e nenhum registro de autoridade. O ‘*’ indica que o bit `authoritative answer` foi definido. Como não havia respostas, nenhum tipo, classe ou dados foram impressos.

Outros caracteres de bandeira que podem aparecer são “-” (recursão disponível, RA, `not` set) e “ !" (mensagem truncada, TC, set). Se a seção de “questão” não contém exatamente uma entrada, “[`n`q]” é impresso.

<a id="smbcifs-decoding"></a>
### Decodificação SMB/CIFS

`tcpdump` agora inclui bastante extensa decodificação SMB/CIFS/NBT para dados em UDP/137, UDP/138 e TCP/139. Alguns dados primitivos de decodificação de IPX e NetBEUI SMB também é feito.

Por padrão, um decodificador bastante mínimo é feito, com um decodificador muito mais detalhado feito se -v for usado. Esteja avisado que com -v um único pacote SMB pode pegar uma página ou mais, então só use -v se você realmente quiser todos os detalhes sangrentos.

Para obter informações sobre os formatos de pacotes SMB e o que todos os campos significam ver https://download.samba.org/pub/samba/specs/ e outros recursos online. Os patches SMB foram escritos por Andrew Tridgell (tridge@samba.org).

<a id="nfs-requests-and-replies"></a>
### Pedidos e Respostas NFS

Os pedidos e respostas do Sun NFS (Sistema de arquivos de Rede) são impressos como:

```text
src.sport > dst.nfs: NFS request xid xid len op args
src.nfs > dst.dport: NFS reply xid xid reply stat len op results


sushi.1023 > wrl.nfs: NFS request xid 26377
	112 readlink fh 21,24/10.73165
wrl.nfs > sushi.1023: NFS reply xid 26377
	reply ok 40 readlink "../var"
sushi.1022 > wrl.nfs: NFS request xid 8219
	144 lookup fh 9,74/4096.6878 "xcolors"
wrl.nfs > sushi.1022: NFS reply xid 8219
	reply ok 128 lookup fh 9,74/4134.3150
```

Na primeira linha, o servidor `sushi` envia uma transacção com o id `26377` para o `wrl`. A requisição foi de 112 bytes, excluindo os cabeçalhos UDP e IP. A operação foi um `readlink` (ligação simbólica de leitura) no identificador de arquivos (`fh`) 21,24/10.731657119. (Se alguém tiver sorte, como neste caso, o identificador de arquivos pode ser interpretado como um par de números maior, menor do dispositivo, seguido do número de inodo e número de geração.) Na segunda linha, o `wrl` responde ‘ok’ com o mesmo ID de transacção e o conteúdo do link.

Na terceira linha, `sushi` pede (usando um novo ID de transação) `wrl` para pesquisar o nome ‘`xcolors`’ no arquivo de diretório 9,74/4096.6878. Na quarta linha, `wrl` envia uma resposta com o respectivo ID de transação.

Note que os dados impressos dependem do tipo de operação. O formato destina- se a ser autoexplicativo se lido em conjunto com uma especificação de protocolo NFS. Lembre- se também que as versões mais antigas dos pacotes NFS impressos tcpdump num formato ligeiramente diferente: o ID de transação (xid) seria impresso em vez do número de porta não- NFS do pacote.

Se a opção - v (verbose) for indicada, serão impressas informações adicionais. Por exemplo:

```text
sushi.1023 > wrl.nfs: NFS request xid 79658
	148 read fh 21,11/12.195 8192 bytes @ 24576
wrl.nfs > sushi.1023: NFS reply xid 79658
	reply ok 1472 read REG 100664 ids 417/0 sz 29388
```

(-v também imprime os campos de TTL, ID, comprimento e fragmentação do cabeçalho IP, que foram omitidos deste exemplo.) Na primeira linha, `sushi` pede ao `wrl` para ler 8192 bytes do arquivo 21,11/12.195, no byte offset 24576. `Wrl` responde ‘ok’; o pacote mostrado na segunda linha é o primeiro fragmento da resposta, e, portanto, é apenas 1472 bytes longos (os outros bytes seguirão em fragmentos subsequentes, mas estes fragmentos não têm NFS ou mesmo os cabeçalhos UDP e assim podem não ser impressos, dependendo da expressão do filtro usada). Dado que a opção -v é dada, alguns dos atributos do arquivo (que são devolvidos em adição aos dados do arquivo) são impressos: o tipo de arquivo (“REG”, para o arquivo regular), o modo de arquivo (em octal), o UID e o GID e o tamanho do arquivo.

Se a bandeira -v é dada mais de uma vez, ainda mais detalhes são impressos.

Os pacotes de resposta NFS não identificam explicitamente a operação RPC. Em vez disso, o `tcpdump` mantém o controle de pedidos “recentes” e corresponde às respostas usando o ID da transação. Se uma resposta não seguir de perto a solicitação correspondente, ela pode não ser processável.

<a id="afs-requests-and-replies"></a>
### Pedidos e Respostas AFS

Os pedidos e respostas do Transarc AFS (Andrew File System) são impressos como:

```text
src.sport > dst.dport: rx packet-type
src.sport > dst.dport: rx packet-type service call call-name args
src.sport > dst.dport: rx packet-type service reply call-name args


elvis.7001 > pike.afsfs:
	rx data fs call rename old fid 536876964/1/1 ".newsrc.new"
	new fid 536876964/1/1 ".newsrc"
pike.afsfs > elvis.7001: rx data fs reply rename
```

Na primeira linha, o elvis da máquina envia um pacote RX para o pike. Este era um pacote de dados RX para o serviço fs (fileserver), e é o início de uma chamada RPC. A chamada RPC foi um renome, com o id do arquivo de diretório antigo de 536876964/1/1 e um nome de arquivo antigo de ‘.newsrc.new’, e um novo ID do arquivo de diretório de 536876964/1/1 e um novo nome de arquivo de ‘.newsrc’. O pike da máquina responde com uma resposta RPC para a chamada de renome (que foi bem sucedido, porque era um pacote de dados e não um pacote de abortar).

Em geral, todos os RPCs AFS são decodificados pelo menos pelo nome de chamada RPC. A maioria dos RPCs AFS têm pelo menos alguns dos argumentos decodificados (geralmente apenas os argumentos "interessantes", para alguma definição de interessante).

O formato destina-se a ser auto-descritivo, mas provavelmente não será útil para pessoas que não estão familiarizados com o funcionamento de AFS e RX.

Se a bandeira -v (verbose) for dada duas vezes, pacotes de reconhecimento e informações adicionais do cabeçalho são impressos, como o RX call ID, número de chamada, número de sequência, número de série e as bandeiras do pacote RX.

Se a bandeira -v for dada duas vezes, são impressas informações adicionais, tais como o ID de chamada RX, o número de série e as bandeiras de pacotes RX. A informação de negociação MTU também é impressa a partir de pacotes RX ack.

Se a bandeira -v for dada três vezes, o índice de segurança e o ID de serviço são impressos.

Códigos de erro são impressos para abortar pacotes, com a exceção de pacotes de baliza Ubik (porque os pacotes de abortar são usados para significar um voto sim para o protocolo Ubik).

Os pacotes de resposta AFS não identificam explicitamente a operação RPC. Em vez disso, `tcpdump` mantém o controle de pedidos “recentes”, e corresponde às respostas usando o número de chamada e ID de serviço. Se uma resposta não segue de perto o pedido correspondente, pode não ser processável.

<a id="kip-appletalk-ddp-in-udp"></a>
### KIP AppleTalk (DDP em UDP)

Os pacotes DDP do AppleTalk encapsulados nos datagramas do UDP são desencapsulados e largados como pacotes DDP (isto é, todas as informações do cabeçalho do UDP são descartadas). O arquivo `/etc/atalk.names` é usado para traduzir os números da rede e do nó do AppleTalk para os nomes. As linhas neste arquivo têm o formulário

```text
number	name

1.254		ether
16.1		icsd-net
1.254.110	ace
```

As duas primeiras linhas dão os nomes das redes do AppleTalk. A terceira linha dá o nome de uma máquina em particular (uma máquina distingue- se de uma rede pelo terceiro octeto no número - um número de rede `must` tem dois octets e um número de máquina `must` tem três octets.) O número e o nome devem ser separados por espaços em branco (em branco ou tabulações). O arquivo `/etc/atalk.names` pode conter linhas em branco ou linhas de comentários (linhas que começam com um '#").

Os endereços AppleTalk são impressos no formulário

```text
net.host.port

144.1.209.2 > icsd-net.112.220
office.2 > icsd-net.112.220
jssmag.149.235 > icsd-net.2
```

(Se o `/etc/atalk.names` não existir ou não contiver uma entrada para algum número da máquina/rede AppleTalk, os endereços são impressos em forma numérica.) No primeiro exemplo, o NBP (porta DDP 2) no nó Net 144.1 209 está a enviar para o que quer que esteja a ouvir na porta 220 do nó net icsd 112. A segunda linha é a mesma, excepto o nome completo do nó de origem é conhecido (“office”). A terceira linha é um envio da porta 235 no nó net jsssmag 149 para transmitir na porta icsd-net NBP (note que o endereço de transmissão (255) é indicado por um nome de rede sem número de máquina - por esta razão é uma boa ideia manter os nomes de nós e os nomes de rede distintos em /etc/atalk.names).

Os pacotes NBP (nome binding protocol) e ATP (AppleTalk transaction protocol) têm seu conteúdo interpretado. Outros protocolos simplesmente descartam o nome do protocolo (ou número se nenhum nome estiver registrado para o protocolo) e o tamanho do pacote.

<a id="nbp-packets"></a>
### Pacotes NBP

Os pacotes NBP são formatados como os seguintes exemplos:

```text
icsd-net.112.220 > jssmag.2: nbp-lkup 190: "=:LaserWriter@*"
jssmag.209.2 > icsd-net.112.220: nbp-reply 190: "RM1140:LaserWriter@*" 250
techpit.2 > icsd-net.112.220: nbp-reply 190: "techpit:LaserWriter@*" 186
```

A primeira linha é um pedido de procura de nomes para laserwriters enviados pela net icsd host 112 e transmitidos na net jssmag. O nbp id para a pesquisa é 190. A segunda linha mostra uma resposta para esta requisição (note que ela tem o mesmo id) da host jssmag. 209 dizendo que ela tem um recurso de laserwriter chamado "RM1140" registrado na porta 250. A terceira linha é outra resposta à mesma requisição dizendo que o host techpit tem laserwriter "techpit" registrado na porta 186.

<a id="atp-packets"></a>
### Pacotes ATP

A formatação de pacotes ATP é demonstrada pelo seguinte exemplo:

```text
jssmag.209.165 > helios.132: atp-req  12266<0-7> 0xae030001
helios.132 > jssmag.209.165: atp-resp 12266:0 (512) 0xae040000
helios.132 > jssmag.209.165: atp-resp 12266:1 (512) 0xae040000
helios.132 > jssmag.209.165: atp-resp 12266:2 (512) 0xae040000
helios.132 > jssmag.209.165: atp-resp 12266:3 (512) 0xae040000
helios.132 > jssmag.209.165: atp-resp 12266:4 (512) 0xae040000
helios.132 > jssmag.209.165: atp-resp 12266:5 (512) 0xae040000
helios.132 > jssmag.209.165: atp-resp 12266:6 (512) 0xae040000
helios.132 > jssmag.209.165: atp-resp*12266:7 (512) 0xae040000
jssmag.209.165 > helios.132: atp-req  12266<3,5> 0xae030001
helios.132 > jssmag.209.165: atp-resp 12266:3 (512) 0xae040000
helios.132 > jssmag.209.165: atp-resp 12266:5 (512) 0xae040000
jssmag.209.165 > helios.132: atp-rel  12266<0-7> 0xae030001
jssmag.209.133 > helios.132: atp-req* 12267<0-7> 0xae030002
```

Jssmag.209 inicia a transação id 12266 com helios host solicitando até 8 pacotes (o ‘<0-7>’). O número hex no final da linha é o valor do campo ‘usuáriodata’ na solicitação.

Helios responde com 8 pacotes 512-byte. O ‘:digite’ após o ID da transação dá o número da sequência do pacote na transação e o número em parens é a quantidade de dados no pacote, excluindo o cabeçalho ATP. O ‘*’ no pacote 7 indica que o bit EOM foi definido.

Jssmag.209 então solicita que os pacotes 3 e 5 sejam retransmitidos. Helios reenvia-os então jssmag.209 libera a transação. Finalmente, jssmag.209 inicia o próximo pedido. O ‘*’ na solicitação indica que o XO (“exatamente uma vez”) foi o conjunto `not`.

<a id="backward-compatibility"></a>
## COMPATIBILIDADE DA CONCORRÊNCIA

A bandeira TCP nomes `tcp-ece` e `tcp-cwr` tornou-se disponível ao ligar com libppap 1.9.0 ou mais tarde.

<a id="see-also"></a>
## VER TAMBÉM

`stty`(1), `pcap`(3PACP), `bpf`(4), `nit`(4P), `pcap-savefile`(5), `pcap-filter`(7), `pcap-tstamp`(7)

`https://www.iana.org/assignments/media-types/application/vnd.tcpdump.pcap`

<a id="authors"></a>
## AUTORES

Os autores originais são:

Van Jacobson, Craig Leres e Steven McCanne, todos do Lawrence Berkeley National Laboratory, Universidade da Califórnia, Berkeley, CA.

Atualmente é mantido pelo Grupo Tcpdump.

A versão atual está disponível via HTTPS:

`https://www.tcpdump.org/`

A distribuição original está disponível via ftp anônimo:

`ftp://ftp.ee.lbl.gov/old/tcpdump.tar.Z`

O suporte ao IPv6/IPsec é adicionado pelo projeto WIDE/KAME. Este programa usa OpenSSL/LibreSSL, em configurações específicas.

<a id="bugs"></a>
## BUGES

Para relatar um problema de segurança, envie um e-mail para security@tcpdump.org.

Para relatar erros e outros problemas, contribuir com patches, solicitar um recurso, fornecer feedback genérico, etc. consulte o arquivo `CONTRIBUTING.md` na raiz da árvore de origem tcpdump.

NIT não deixa você assistir seu próprio tráfego de saída, BPF vai. Recomendamos que você use o último.

Algumas tentativas devem ser feitas para remontar fragmentos IP ou, pelo menos para calcular o comprimento certo para o protocolo de nível superior.

As consultas inversas do servidor de nomes não são descartadas corretamente: a seção de perguntas (vazio) é impressa em vez de uma consulta real na seção de respostas. Alguns acreditam que as consultas inversas são eles mesmos um erro e preferem corrigir o programa gerando-os em vez de `tcpdump`.

Um traço de pacote que atravessa uma mudança de horário de verão dará selos de tempo distorcidos (a mudança de hora é ignorada).

Filtrar expressões em campos diferentes daqueles nos cabeçalhos do Token Ring não irá lidar corretamente com os pacotes Token Ring direcionados pelo código fonte.

Filtrar expressões em campos diferentes daqueles em cabeçalhos 802.11 não manejará corretamente pacotes de dados 802.11 com o conjunto To DS e From DS.

`ip6 proto` deve perseguir a cadeia de cabeçalho, mas neste momento não faz. `ip6 protochain` é fornecido para este comportamento.

A expressão aritmética contra cabeçalhos de camadas de transporte, como o `tcp[0]`, não funciona contra pacotes IPv6. Ele só olha para pacotes IPv4.



---

## Procedência desta tradução

Fonte primária: [manual preservado](../../../sources/upstream/tcpdump/tcpdump.8.source), extraído de `/usr/share/man/man8/tcpdump.8.gz`. Pacote `tcpdump`, versão `4.99.6-2`; pacote-fonte `tcpdump`, versão `4.99.6-2`. Aquisição de pacote instalado, sem atribuição de commit Git.

Licença: [LicenseRef-Tcpdump-Manpage](../../99-Assets/upstream/tcpdump/LICENSE.txt); [copyright e condições do pacote](../../99-Assets/upstream/tcpdump/COPYRIGHT.package.txt). [Página de referência do pacote, não a origem exata do arquivo](https://www.tcpdump.org/). Hashes do original, gzip e avisos no registro de fontes. A data do manual é histórica; não implica que todos os serviços externos mantenham esse comportamento.
