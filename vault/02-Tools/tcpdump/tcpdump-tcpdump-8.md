---
title: "tcpdump — manual de referência"
type: "official-documentation"
tool: "tcpdump"
status: "source-checked"
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

> Tradução para português produzida por assistente de IA e conferida seção por seção contra a fonte. Revisão humana independente: pendente. Opções e exemplos originais foram preservados; nenhum exemplo foi executado automaticamente.

> **Compatibilidade observada:** tcpdump version 4.99.6. Ajuda/versão e leitura de PCAP sintético próprio verificadas. Filtros, contagem, gravação de cópia filtrada e rejeição de filtro inválido foram exercitados somente com -r. A ajuda compacta não foi tratada como lista integral de opções. Nenhuma captura ao vivo, interface ou envio foi solicitado. [Evidência e limites do teste](../../99-Assets/evidence/tcpdump-local-tests.json).

<!-- SPDX-License-Identifier: LicenseRef-Tcpdump-Manpage -->
> **Reconhecimento da licença:** This product includes software developed by the University of California, Lawrence Berkeley Laboratory and its contributors.

# tcpdump

<a id="name"></a>
## NOME

tcpdump - exibe o tráfego de uma rede

<a id="synopsis"></a>
## SINOPSE

```text
tcpdump [ -AbdDefghHIJKlLnNOpqStuUvxX# ] [ -B buffer_size ] [ -c count ] [ --count ] [ -C file_size ] [ -E spi@ipaddr algo:secret,... ] [ -F file ] [ -G rotate_seconds ] [ -i interface ] [ --immediate-mode ] [ -j tstamp_type ] [ -m module ] [ -M secret ] [ --number ] [ --print ] [ -Q in|out|inout ] [ -r file ] [ -s snaplen ] [ -T type ] [ --version ] [ -V file ] [ -w file ] [ -W filecount ] [ -y datalinktype ] [ -z postrotate-command ] [ -Z user ] [ --time-stamp-precision=tstamp_precision ] [ --micro ] [ --nano ] [ expression ]
```

<a id="description"></a>
## DESCRIÇÃO

`tcpdump` imprime uma descrição do conteúdo dos pacotes de uma interface de rede que correspondem à expressão booleana `expression` (veja a sintaxe de `expression` em `pcap-filter`(7)); essa descrição é precedida por uma marca temporal, exibida por padrão como horas, minutos, segundos e frações de segundo desde a meia-noite. Também pode ser executado com a opção `-w`, que salva os dados dos pacotes em um arquivo para análise posterior, e/ou com `-r`, que lê um arquivo de pacotes salvo em vez de ler de uma interface de rede. A opção `-V` permite ler uma lista de arquivos de pacotes salvos. Em todos os casos, o `tcpdump` processa apenas os pacotes que correspondem a `expression`.

Se executado sem a opção `-c`, o `tcpdump` continua capturando pacotes até ser interrompido por um sinal SIGINT (gerado, por exemplo, pelo caractere de interrupção, normalmente Ctrl-C) ou SIGTERM (normalmente gerado pelo comando `kill`(1)). Com `-c`, captura até receber SIGINT ou SIGTERM, ou até processar o número especificado de pacotes.

Ao terminar a captura, o `tcpdump` informa as contagens de:

pacotes “capturados”: o número de pacotes recebidos e processados pelo `tcpdump`;

pacotes “recebidos pelo filtro”: o significado depende do sistema operacional em que o `tcpdump` é executado e, possivelmente, de sua configuração. Quando há um filtro na linha de comando, alguns sistemas contam os pacotes independentemente de corresponderem à expressão e, mesmo quando correspondem, independentemente de o `tcpdump` já os ter lido e processado; outros contam apenas os que correspondem à expressão, independentemente de já terem sido lidos e processados; outros contam somente os que correspondem à expressão e foram processados pelo `tcpdump`;

pacotes “descartados pelo kernel”: o número de pacotes descartados, por falta de espaço em buffer, pelo mecanismo de captura do sistema operacional em que o `tcpdump` é executado, quando o sistema informa esse dado aos aplicativos. Caso contrário, a contagem informada é 0.

Em plataformas com suporte a SIGINFO, como a maioria dos BSDs (incluindo macOS) e Digital/Tru64 UNIX, essas contagens são informadas ao receber esse sinal, e a captura continua. O sinal pode ser gerado pelo caractere de “status”, normalmente Ctrl-T; em algumas plataformas, como macOS, esse caractere não é definido por padrão e precisa ser configurado com `stty`(1). Em plataformas sem SIGINFO, pode-se obter o mesmo resultado usando SIGUSR1.

Usar SIGUSR2 junto com a opção `-w` força a gravação do conteúdo do buffer de pacotes no arquivo de saída.

Ler pacotes de uma interface de rede pode exigir privilégios especiais; consulte `pcap`(3PCAP) para detalhes. Ler um arquivo de pacotes salvo não exige privilégios especiais.

<a id="options"></a>
## OPÇÕES

### `-A`

Imprime cada pacote em ASCII, sem o cabeçalho da camada de enlace. Útil para capturar páginas web. Não tem efeito quando são usadas as opções `-x[x]` ou `-X[X]`.

### `-b`

Imprime o número AS dos pacotes BGP na notação ASDOT em vez de ASPLAIN.

### `-B buffer_size`

### `--buffer-size=buffer_size`

Define o tamanho do buffer de captura do sistema operacional como `buffer_size`, em KiB (1024 bytes).

### `-c count`

Encerra após receber `count` pacotes.

### `--count`

Ao ler arquivos de captura, imprime em stdout apenas a contagem de pacotes, em vez de analisar/imprimir os pacotes. Se houver um filtro na linha de comando, o `tcpdump` conta somente os pacotes que correspondem à expressão.

### `-C file_size`

Antes de gravar um pacote bruto em um arquivo de captura, verifica se o arquivo já é maior que `file_size`; nesse caso, fecha o arquivo atual e abre outro. Os arquivos após o primeiro recebem o nome especificado por `-w` acrescido de um número, começando em 1 e aumentando a cada arquivo. A unidade padrão de `file_size` é um milhão de bytes (1.000.000, não 1.048.576 bytes).

Acrescentar os sufixos k/K, m/M ou g/G ao valor muda a unidade para 1.024 bytes (KiB), 1.048.576 bytes (MiB) ou 1.073.741.824 bytes (GiB), respectivamente.

Quando usada com `-Z` (ativada por padrão), a redução de privilégios ocorre antes da abertura do primeiro arquivo de captura.

### `-d`

Exibe o código compilado de correspondência de pacotes em formato legível na saída padrão e encerra.

Embora a compilação do código seja sempre específica de um DLT, normalmente é impossível e desnecessário especificar qual DLT usar nessa exibição: o `tcpdump` utiliza o DLT do arquivo pcap indicado por `-r`, o DLT padrão da interface indicada por `-i` ou o DLT específico indicado por `-y` e `-i`, respectivamente. Nesses casos, a saída mostra exatamente o código que filtraria o arquivo ou a interface sem `-d`.

Quando nem `-r` nem `-i` são especificadas, porém, `-d` impede que o `tcpdump` tente selecionar automaticamente uma interface adequada (veja `-i`). Nesse caso, o DLT padrão é EN10MB e pode ser alterado manualmente para outro valor válido com `-y`.

### `-dd`

Exibe o código de correspondência de pacotes como um fragmento de programa em `C`.

### `-ddd`

Exibe o código de correspondência de pacotes como números decimais, precedidos por uma contagem.

<a id="-d-1"></a>
### `-D`

### `--list-interfaces`

Imprime a lista das interfaces de rede disponíveis no sistema nas quais o `tcpdump` pode capturar. Para cada interface, imprime um número e um nome, possivelmente seguidos por uma descrição textual. O nome ou o número pode ser fornecido à opção `-i` para selecionar a interface de captura.

Isso pode ser útil em sistemas sem um comando para listar interfaces, como sistemas Windows ou UNIX sem `ifconfig -a`. O número pode ser útil no Windows 2000 e posteriores, em que o nome da interface é uma string relativamente complexa.

A opção `-D` não será compatível se o `tcpdump` tiver sido compilado com uma versão antiga da `libpcap` que não contenha a função `pcap_findalldevs`(3PCAP).

### `-e`

Imprime o cabeçalho da camada de enlace em cada linha de saída. Isso permite mostrar, por exemplo, endereços da camada MAC em protocolos como Ethernet e IEEE 802.11.

<a id="-e-1"></a>
### `-E`

Usa `spi@ipaddr algo:secret` para descriptografar pacotes IPsec ESP destinados a `addr` que contenham o valor `spi` no Security Parameter Index. Essa combinação pode ser repetida com separação por vírgulas ou quebras de linha.

No momento descrito pela fonte, há suporte à definição do segredo para pacotes ESP IPv4.

Os algoritmos podem ser `des-cbc`, `3des-cbc`, `blowfish-cbc`, `rc3-cbc`, `cast128-cbc` ou `none`. O padrão é `des-cbc`. A capacidade de descriptografar pacotes só está disponível quando o `tcpdump` é compilado com suporte a criptografia.

`secret` é o texto ASCII da chave secreta ESP. Se for precedido por 0x, será lido como um valor hexadecimal.

A opção pressupõe ESP da RFC 2406, não da RFC 1827. Destina-se somente à depuração, e seu uso com uma chave secreta real é desaconselhado. Informar a chave secreta IPsec na linha de comando a torna visível a outras pessoas, por meio de `ps`(1) e em outras situações.

Além da sintaxe acima, pode-se usar `file name` para fazer o tcpdump ler o arquivo fornecido. O arquivo é aberto quando chega o primeiro pacote ESP; nesse momento, quaisquer permissões especiais concedidas ao tcpdump já deverão ter sido abandonadas.

### `-f`

Imprime os endereços IPv4 “externos” numericamente em vez de simbolicamente. Essa opção contorna falhas graves do servidor NIS da Sun, que normalmente fica travado indefinidamente ao tentar traduzir endereços de redes não locais.

A identificação de endereços IPv4 “externos” usa o endereço IPv4 e a máscara de rede da interface em que a captura ocorre. Se esses dados não estiverem disponíveis — porque a interface não tem endereço ou máscara, ou porque é a pseudointerface “any” (veja `-i` abaixo) — a opção não funcionará corretamente.

### `-F file`

Usa `file` como entrada para a expressão do filtro. Uma expressão adicional fornecida na linha de comando é ignorada.

### `-g`

### `--ip-oneline`

Não insere uma quebra de linha após o cabeçalho IP no modo detalhado.

### `-G rotate_seconds`

Rotaciona o arquivo de captura indicado por `-w` a cada `rotate_seconds` segundos. Os arquivos recebem o nome especificado por `-w`, que deve incluir um formato de data/hora definido por `strftime`(3). Sem esse formato, cada arquivo novo sobrescreve o anterior. Sempre que o nome gerado não é único, o tcpdump sobrescreve os dados existentes; por isso, não se recomenda uma especificação temporal mais grosseira que o período da captura.

Quando usada com `-C`, os nomes dos arquivos assumem a forma ‘`file`<count>’.

Quando usada com `-Z` (ativada por padrão), a redução de privilégios ocorre antes da abertura do primeiro arquivo de captura.

### `-h`

### `--help`

Imprime as strings de versão de tcpdump e libpcap, mostra uma mensagem de uso e encerra.

### `--version`

Imprime as strings de versão de tcpdump e libpcap e encerra.

<a id="-h-1"></a>
### `-H`

Tenta detectar cabeçalhos de malha do rascunho 802.11s.

### `-i interface`

### `--interface=interface`

Escuta em `interface`, informa os tipos de camada de enlace ou de marcas temporais disponíveis, ou mostra o resultado da compilação de um filtro nessa interface. Se ela não for especificada e `-d` não for usada, o `tcpdump` procura na lista do sistema a interface de menor número que esteja configurada como ativa, excluindo loopback; ela pode ser, por exemplo, “eth0”.

Em todos os sistemas Linux compatíveis e nas versões recentes de macOS e Solaris descritas pela fonte, o argumento “any” de `interface` indica uma pseudointerface especial que captura de todas as interfaces de rede regulares do sistema. O que conta como interface regular é um detalhe de implementação do sistema operacional; no Linux, por exemplo, isso inclui dispositivos SocketCAN. Assim, pacotes capturados em “any” podem representar mais protocolos do que o esperado. As interfaces regulares também são apenas um subconjunto de todos os dispositivos de captura listados por `-D`. Essa lista pode incluir dispositivos implementados pela libpcap fora da pilha de rede do sistema: Bluetooth, DAG, D-Bus, SNF e USB. Capturas em “any” não são feitas em modo promíscuo.

Se houver suporte a `-D`, um número de interface exibido por essa opção pode ser usado como argumento `interface`, desde que nenhuma interface do sistema tenha esse número como nome.

### `-I`

### `--monitor-mode`

Coloca a interface em “modo monitor”; isso só é compatível com interfaces Wi-Fi IEEE 802.11 e apenas em alguns sistemas operacionais.

No modo monitor, o adaptador pode se desassociar da rede à qual está conectado, impedindo o uso de redes sem fio por esse adaptador. Se você não estiver conectado a outra rede por outro adaptador, isso pode impedir o acesso a arquivos de um servidor de rede ou a resolução de nomes de hosts e endereços de rede.

Esta opção afeta a saída de `-L`. Sem `-I`, são mostrados apenas os tipos de camada de enlace disponíveis fora do modo monitor; com `-I`, apenas os disponíveis nesse modo.

### `--immediate-mode`

Captura em “modo imediato”. Nele, os pacotes são entregues ao tcpdump assim que chegam, em vez de ficarem em buffer para melhorar a eficiência. Esse é o padrão ao imprimir pacotes em um terminal, em vez de salvá-los em um arquivo de captura ou imprimi-los em um arquivo ou pipe.

### `-j tstamp_type`

### `--time-stamp-type=tstamp_type`

Define o tipo de marca temporal da captura como `tstamp_type`. Os nomes dos tipos estão em `pcap-tstamp`(7); nem todos os tipos listados necessariamente são válidos para uma dada interface.

### `-J`

### `--list-time-stamp-types`

Lista os tipos de marcas temporais compatíveis com a interface e encerra. Se o tipo não puder ser definido para a interface, nenhum será listado.

### `--time-stamp-precision=tstamp_precision`

Durante a captura, define a precisão das marcas temporais como `tstamp_precision`. A disponibilidade de marcas de alta precisão (nanossegundos) e sua exatidão real dependem da plataforma e do hardware. Ao gravar capturas com precisão de nanossegundos em um arquivo, as marcas são salvas com resolução de nanossegundos e o arquivo recebe um magic number diferente, indicando segundos e nanossegundos. Nem todo programa leitor de pcap consegue ler esses arquivos.

Ao ler um arquivo de captura, converte as marcas temporais para a precisão indicada por `timestamp_precision` e as exibe nessa resolução. Se a precisão pedida for menor que a das marcas no arquivo, haverá perda de precisão.

Os valores compatíveis de `timestamp_precision` são `micro`, para resolução de microssegundos, e `nano`, para nanossegundos. O padrão é microssegundos.

### `--micro`

### `--nano`

Atalhos para `--time-stamp-precision=micro` ou `--time-stamp-precision=nano`, ajustando a precisão das marcas temporais. Ao ler um arquivo criado com precisão de nanossegundos, `--micro` trunca as marcas. Já em um arquivo com precisão de microssegundos, `--nano` acrescenta zeros à direita das marcas temporais.

### `-K`

### `--dont-verify-checksums`

Não tenta verificar os checksums de IP, TCP ou UDP. É útil em interfaces que calculam alguns ou todos esses checksums por hardware; caso contrário, todos os checksums TCP de saída serão sinalizados como incorretos.

### `-l`

Ativa o armazenamento de stdout em buffer por linha. Útil para acompanhar os dados durante a captura. Por exemplo:

```text
tcpdump -l | tee dat
```

ou

```text
tcpdump -l > dat & tail -f dat
```

No Windows, “buffer por linha” significa “sem buffer”; portanto, o WinDump grava cada caractere individualmente quando `-l` é especificada.

`-U` é semelhante a `-l`, mas usa buffer por pacote: a saída é gravada em stdout ao final de cada pacote, em vez de ao final de cada linha. Esse comportamento com buffer vale para todas as plataformas, inclusive Windows.

<a id="-l-1"></a>
### `-L`

### `--list-data-link-types`

Lista os tipos de enlace de dados conhecidos para a interface no modo especificado e encerra. A lista pode depender do modo: em algumas plataformas, por exemplo, uma interface Wi-Fi oferece certos tipos fora do modo monitor (como somente cabeçalhos Ethernet simulados, ou cabeçalhos 802.11 sem informações de rádio) e outro conjunto no modo monitor (como cabeçalhos 802.11, com ou sem informações de rádio, disponíveis somente nesse modo).

### `-m module`

Carrega do arquivo `module` as definições de um módulo MIB SMI. A opção pode ser repetida para carregar vários módulos MIB no `tcpdump`.

### `-M secret`

Usa `secret` como segredo compartilhado para validar os digests dos segmentos TCP que tenham a opção TCP-MD5 (RFC 2385).

### `-n`

Não converte endereços — como endereços de hosts e números de portas — em nomes.

<a id="-n-1"></a>
### `-N`

Não imprime a qualificação de domínio dos nomes de hosts. Por exemplo, com esta opção, o `tcpdump` imprime “nic” em vez de “nic.ddn.mil”.

### `-#`

### `--number`

Imprime um número de pacote no início da linha.

### `-O`

### `--no-optimize`

Não executa o otimizador do código de correspondência de pacotes. Só é útil se houver suspeita de um defeito no otimizador.

### `-p`

### `--no-promiscuous-mode`

Não coloca a interface em modo promíscuo (ênfase original: `Don't`). A interface pode já estar nesse modo por outro motivo; portanto, ‘-p’ não pode ser usada como abreviação de ‘ether host {local-hw-addr} or ether broadcast’.

### `--print`

Imprime a análise dos pacotes mesmo quando os pacotes brutos estão sendo salvos com `-w`.

### `-Q direction`

### `--direction=direction`

Escolhe a direção de envio/recebimento `direction` dos pacotes a capturar. Os valores possíveis são ‘in’, ‘out’ e ‘inout’. Não está disponível em todas as plataformas.

### `-q`

Saída rápida (silenciosa?): imprime menos informações de protocolo para encurtar as linhas.

### `-r file`

Lê os pacotes de `file`, criado com `-w` ou por outra ferramenta que grave pcap/pcapng. Se `file` for “-”, usa a entrada padrão.

### `-S`

### `--absolute-tcp-sequence-numbers`

Imprime números de sequência TCP absolutos em vez de relativos.

### `-s snaplen`

### `--snapshot-length=snaplen`

Captura `snaplen` bytes de dados de cada pacote em vez do padrão de 262144 bytes. Pacotes truncados pelo limite de captura são indicados na saída por “[|`proto`]”, em que `proto` é o protocolo no nível em que ocorreu o truncamento.

Capturas com snapshots maiores aumentam o tempo de processamento e reduzem, na prática, a quantidade de pacotes que cabe no buffer, podendo causar perdas. Snapshots menores descartam dados de protocolos acima da camada de transporte e podem eliminar informações importantes. Solicitações e respostas NFS e AFS, por exemplo, são muito grandes, e muitos detalhes ficam indisponíveis quando o tamanho capturado é curto demais.

Se for necessário reduzir o tamanho de captura abaixo do padrão, limite `snaplen` ao menor valor que preserve as informações de protocolo desejadas. Definir `snaplen` como 0 seleciona o padrão de 262144, por compatibilidade com versões anteriores recentes do `tcpdump`.

### `-T type`

Força a interpretação dos pacotes selecionados por “`expression`” como o `type` especificado. Os tipos conhecidos são `aodv` (Ad-hoc On-demand Distance Vector), `carp` (Common Address Redundancy Protocol), `cnfp` (Cisco NetFlow), `domain` (Domain Name System), `lmp` (Link Management Protocol), `pgm` (Pragmatic General Multicast), `pgm_zmtp1` (ZMTP/1.0 dentro de PGM/EPGM), `ptp` (Precision Time Protocol), `radius` (RADIUS), `resp` (REdis Serialization Protocol), `rpc` (Remote Procedure Call), `rtcp` (protocolo de controle de aplicações em tempo real), `rtp` (protocolo de aplicações em tempo real), `snmp` (Simple Network Management Protocol), `someip` (SOME/IP), `tftp` (Trivial File Transfer Protocol), `vat` (Visual Audio Tool), `vxlan` (Virtual eXtensible Local Area Network), `wb` (White Board distribuído) e `zmtp1` (ZeroMQ Message Transport Protocol 1.0).

O tipo `pgm` acima só afeta a interpretação de UDP; PGM nativo é sempre reconhecido como protocolo IP 113. PGM encapsulado em UDP costuma ser chamado de “EPGM” ou “PGM/UDP”.

O tipo `pgm_zmtp1` afeta simultaneamente a interpretação de PGM nativo e UDP. Na decodificação de PGM nativo, os dados da aplicação de um pacote ODATA/RDATA são decodificados como um datagrama ZeroMQ com quadros ZMTP/1.0. Na decodificação de UDP, além disso, qualquer pacote UDP é tratado como um pacote PGM encapsulado.

### `-t`

Não imprime uma marca temporal em cada linha de saída (ênfase original: `Don't`).

### `-tt`

Imprime em cada linha a marca temporal em segundos desde 1º de janeiro de 1970, 00:00:00 UTC, com suas frações de segundo.

### `-ttt`

Imprime em cada linha a diferença entre a linha atual e a anterior, com resolução de microssegundos ou nanossegundos conforme `--time-stamp-precision`. O padrão é microssegundos.

### `-tttt`

Imprime em cada linha uma marca temporal com horas, minutos, segundos e frações de segundo desde a meia-noite, precedida pela data.

### `-ttttt`

Imprime, em cada linha da saída, a diferença entre a marca temporal atual e a da primeira linha, com resolução de microssegundos ou nanossegundos conforme a opção `--time-stamp-precision`. A resolução padrão é de microssegundos.

### `-u`

Imprime os identificadores de arquivo (handles) NFS sem decodificá-los.

<a id="-u-1"></a>
### `-U`

### `--packet-buffered`

Se a opção `-w` não for especificada, ou se for especificada junto com a opção `--print`, usa buffer por pacote na saída impressa: à medida que a descrição do conteúdo de cada pacote é impressa, ela é enviada à saída padrão, em vez de, quando a saída não é um terminal, aguardar o preenchimento do buffer de saída.

Se a opção `-w` for especificada, usa buffer por pacote na saída de pacotes brutos salva: cada pacote é escrito no arquivo de saída assim que é salvo, em vez de aguardar o preenchimento do buffer de saída.

A opção `-U` não é suportada se o `tcpdump` tiver sido compilado com uma versão antiga da `libpcap` que não disponha da função `pcap_dump_flush`(3PCAP).

### `-v`

Ao analisar e imprimir, produz uma saída um pouco mais detalhada. Por exemplo, imprime o tempo de vida, a identificação, o comprimento total e as opções de um pacote IP. Também ativa verificações adicionais de integridade dos pacotes, como a conferência das somas de verificação dos cabeçalhos IP e ICMP.

Ao escrever em um arquivo com a opção `-w` sem, ao mesmo tempo, ler de um arquivo com a opção `-r`, informa na saída de erro padrão (stderr), uma vez por segundo, o número de pacotes capturados. No Solaris, no FreeBSD e possivelmente em outros sistemas operacionais, essa atualização periódica pode atualmente causar perda de pacotes capturados no trajeto do kernel até o tcpdump.

### `-vv`

Produz uma saída ainda mais detalhada. Por exemplo, imprime campos adicionais dos pacotes de resposta NFS e decodifica completamente os pacotes SMB.

### `-vvv`

Produz uma saída ainda mais detalhada. Por exemplo, imprime integralmente as opções telnet `SB` ... `SE`. Com `-X`, as opções Telnet também são impressas em hexadecimal.

### `-V file`

Lê uma lista de nomes de arquivos de `file`. Usa a entrada padrão se `file` for “-”.

### `-w file`

Escreve os pacotes brutos em `file`, em vez de analisá-los e imprimi-los. Eles podem ser impressos posteriormente com a opção -r. Usa a saída padrão se `file` for “-”.

Essa saída usa buffer quando é escrita em um arquivo ou pipe; portanto, um programa que leia desse arquivo ou pipe pode não receber os pacotes durante um intervalo arbitrário após sua recepção. Use a opção `-U` para que os pacotes sejam escritos assim que forem recebidos.

O tipo MIME `application/vnd.tcpdump.pcap` foi registrado na IANA para arquivos `pcap`. A extensão de nome de arquivo `.pcap` parece ser a mais usada, junto com `.cap` e `.dmp`. O próprio `tcpdump` não verifica a extensão ao ler arquivos de captura nem acrescenta uma extensão ao escrevê-los: usa, em seu lugar, números mágicos no cabeçalho do arquivo. Muitos sistemas operacionais e aplicativos, porém, usam a extensão quando ela está presente; recomenda-se acrescentar uma, como .pcap.

Consulte `pcap-savefile`(5) para obter uma descrição do formato do arquivo.

### `-W filecount`

Em conjunto com a opção `-C`, limita a quantidade de arquivos criados ao número especificado e passa a sobrescrevê-los a partir do primeiro, criando assim um buffer circular. Além disso, os nomes dos arquivos recebem zeros à esquerda em quantidade suficiente para acomodar o número máximo de arquivos, permitindo sua ordenação correta.

Em conjunto com a opção `-G`, limita o número de arquivos de captura criados pela rotação e encerra com status 0 ao atingir esse limite.

Se for usada em conjunto com `-C` e `-G,` a opção `-W` é atualmente ignorada e afeta apenas o nome do arquivo.

### `-x`

Ao analisar e imprimir, além dos cabeçalhos de cada pacote, imprime seus dados em hexadecimal, sem o cabeçalho da camada de enlace. Imprime o menor entre o pacote inteiro e `snaplen` bytes. Trata-se do pacote completo da camada de enlace; portanto, em camadas que acrescentam preenchimento, como Ethernet, os bytes de preenchimento também são impressos quando o pacote da camada superior é menor que o tamanho exigido pelo preenchimento. Na implementação atual, essa opção pode ter o mesmo efeito de `-xx` se o pacote estiver truncado. Não tem efeito quando a opção `-X[X]` é usada.

### `-xx`

Ao analisar e imprimir, além dos cabeçalhos de cada pacote, imprime seus dados em hexadecimal, incluindo o cabeçalho da camada de enlace (ênfase original: `including`). Não tem efeito quando a opção `-X[X]` é usada.

<a id="-x-1"></a>
### `-X`

Ao analisar e imprimir, além dos cabeçalhos de cada pacote, imprime seus dados em hexadecimal e ASCII, sem o cabeçalho da camada de enlace. Isso é muito útil para analisar novos protocolos. Na implementação atual, essa opção pode ter o mesmo efeito de `-XX` se o pacote estiver truncado.

<a id="-xx-1"></a>
### `-XX`

Ao analisar e imprimir, além dos cabeçalhos de cada pacote, imprime seus dados em hexadecimal e ASCII, incluindo o cabeçalho da camada de enlace (ênfase original: `including`).

### `-y datalinktype`

### `--linktype=datalinktype`

Define como `datalinktype` o tipo de enlace de dados usado na captura de pacotes (consulte `-L`) ou apenas na compilação e exibição do código de correspondência de pacotes (consulte `-d`).

### `-z postrotate-command`

Em conjunto com as opções `-C` ou `-G`, faz o `tcpdump` executar “ `postrotate-command file` ”, em que `file` é o arquivo de captura que está sendo fechado após cada rotação. Por exemplo, especificar `-z gzip` ou `-z bzip2` comprime cada arquivo de captura com gzip ou bzip2.

Essa opção só pode ser usada se houver implementação de criação de subprocessos por fork; por exemplo, não pode ser usada em sistemas Windows.

O tcpdump executa o comando em paralelo à captura, com a menor prioridade, para não perturbar o processo de captura.

Para usar um comando que receba suas próprias opções ou argumentos diferentes, escreva um script de shell que receba o nome do arquivo de captura como único argumento, organize as opções e os argumentos e execute o comando desejado.

### `-Z user`

### `--relinquish-privileges=user`

Se o `tcpdump` estiver sendo executado como root, depois de abrir o dispositivo de captura ou o arquivo de captura de entrada, mas antes de abrir qualquer arquivo de captura de saída, altera o ID de usuário para `user` e o ID de grupo para o grupo primário de `user`.

Esse comportamento é ativado por padrão (`-Z tcpdump`) e pode ser desativado com `-Z root`.

### ` expression`

Seleciona os pacotes que serão apresentados na saída. Se nenhuma `expression` for fornecida, todos os pacotes da rede serão apresentados. Caso contrário, somente os pacotes para os quais `expression` seja verdadeira serão apresentados.

Para a sintaxe de `expression`, consulte `pcap-filter`(7).

O argumento `expression` pode ser passado ao `tcpdump` como um único argumento do shell ou como vários argumentos, conforme for mais conveniente. Se a expressão contiver metacaracteres do shell, como barras invertidas usadas para escapar nomes de protocolos, costuma ser mais fácil passá-la como um único argumento entre aspas do que escapar os metacaracteres do shell. Vários argumentos são concatenados com espaços antes da análise.

<a id="examples"></a>
## EXEMPLOS

Para imprimir todos os pacotes que chegam a `sundown` ou saem dele:

```text
tcpdump host sundown
```

Para imprimir o tráfego entre `helios` e `hot` ou `ace`:

```text
tcpdump host helios and \( hot or ace \)
```

Para imprimir todos os pacotes IP entre `ace` e qualquer host, exceto `helios`:

```text
tcpdump ip host ace and not helios
```

Para imprimir todo o tráfego entre hosts locais e hosts em Berkeley:

```text
tcpdump net ucb-ether
```

Para imprimir todo o tráfego ftp que passa pelo gateway de internet `snup`: a expressão está entre aspas para impedir que o shell interprete incorretamente os parênteses.

```text
tcpdump 'gateway snup and (port ftp or ftp-data)'
```

Para imprimir o tráfego que não tem hosts locais como origem nem como destino: se você usa um gateway para outra rede, esse tráfego nunca deveria chegar à sua rede local.

```text
tcpdump ip and not net localnet
```

Para imprimir os pacotes de início e término, SYN e FIN, de cada comunicação TCP que envolva um host não local.

```text
tcpdump 'tcp[tcpflags] & (tcp-syn|tcp-fin) != 0 and not src and dst net localnet'
```

Para imprimir os pacotes TCP com os bits RST e ACK ativados simultaneamente: seleciona somente esses dois bits no campo de flags e considera que há correspondência se ambos estiverem ativados.

```text
tcpdump 'tcp[tcpflags] & (tcp-rst|tcp-ack) == (tcp-rst|tcp-ack)'
```

Para imprimir todos os pacotes HTTP IPv4 de ou para a porta 80, ou seja, somente pacotes que contenham dados, excluindo, por exemplo, pacotes SYN e FIN e pacotes que contenham apenas ACK. A versão IPv6 fica como exercício para o leitor.

```text
tcpdump 'tcp port 80 and (((ip[2:2] - ((ip[0]&0xf)<<2)) - ((tcp[12]&0xf0)>>2)) != 0)'
```

Para imprimir pacotes IP maiores que 576 bytes enviados pelo gateway `snup`:

```text
tcpdump 'gateway snup and ip[2:2] > 576'
```

Para imprimir pacotes IP de broadcast ou multicast que não tenham sido enviados por broadcast ou multicast Ethernet (ênfase original da negação: `not`):

```text
tcpdump 'ether[0] & 1 = 0 and ip[16] >= 224'
```

Para imprimir todos os pacotes ICMP que não sejam solicitações ou respostas de eco, isto é, que não sejam pacotes de ping:

```text
tcpdump 'icmp[icmptype] != icmp-echo and icmp[icmptype] != icmp-echoreply'
```

<a id="output-format"></a>
## FORMATO DA SAÍDA

A saída do `tcpdump` depende do protocolo. A seguir, são apresentadas uma breve descrição e exemplos da maioria dos formatos.

<a id="timestamps"></a>
### Marcas temporais

Por padrão, todas as linhas da saída são precedidas por uma marca temporal. Ela representa o horário atual do relógio no formato

```text
hh:mm:ss.frac
```

e tem a mesma precisão do relógio do kernel. A marca temporal reflete o instante em que o kernel a atribuiu ao pacote. Não se tenta compensar o intervalo entre o término da recepção do pacote pela interface de rede e a atribuição da marca temporal pelo kernel. Esse intervalo pode incluir tanto o atraso entre o término da recepção e a entrega ao kernel de uma interrupção para que ele leia o pacote quanto o atraso entre o atendimento da interrupção de “novo pacote” pelo kernel e a atribuição da marca temporal.

### Interface

Quando a interface `any` é selecionada para a captura, ou quando é lido um arquivo de captura com tipo de enlace `LINUX_SLL2`, o nome da interface é impresso após a marca temporal. Em seguida vem o tipo do pacote: `In` indica um pacote destinado a este host e `Out`, um pacote originado nele. Outros valores possíveis são `B` para pacotes de broadcast, `M` para pacotes multicast e `P` para pacotes destinados a outros hosts.

<a id="link-level-headers"></a>
### Cabeçalhos da camada de enlace

Se a opção '-e' for fornecida, imprime o cabeçalho da camada de enlace. Em redes Ethernet, imprime os endereços de origem e destino, o protocolo e o comprimento do pacote.

Em redes FDDI, a opção '-e' faz o `tcpdump` imprimir o campo de controle de quadro, os endereços de origem e destino e o comprimento do pacote. O campo de controle de quadro determina como interpretar o restante do pacote. Pacotes normais, como os que contêm datagramas IP, são pacotes assíncronos, com um valor de prioridade entre 0 e 7; por exemplo, `async4`. Presume-se que esses pacotes contenham um pacote 802.2 Logical Link Control (LLC); o cabeçalho LLC é impresso se não se tratar de um datagrama ISO nem de um pacote chamado SNAP (ênfase original da negação: `not`).

Em redes Token Ring, a opção '-e' faz o `tcpdump` imprimir os campos de controle de acesso e de controle de quadro, os endereços de origem e destino e o comprimento do pacote. Assim como em redes FDDI, presume-se que os pacotes contenham um pacote LLC. Para pacotes com roteamento pela origem, as informações desse roteamento são impressas independentemente de a opção '-e' ter sido especificada.

Em redes 802.11, a opção '-e' faz o `tcpdump` imprimir os campos de controle de quadro, todos os endereços do cabeçalho 802.11 e o comprimento do pacote. Assim como em redes FDDI, presume-se que os pacotes contenham um pacote LLC.

A descrição a seguir pressupõe familiaridade com o algoritmo de compressão SLIP descrito na RFC 1144.

Em enlaces SLIP, imprime um indicador de direção (“I” para entrada e “O” para saída), o tipo do pacote e informações de compressão. O tipo do pacote é impresso primeiro. Os três tipos são `ip`, `utcp` e `ctcp`. Para pacotes `ip`, não imprime outras informações do enlace. Para pacotes TCP, imprime o identificador da conexão após o tipo. Se o pacote estiver comprimido, imprime seu cabeçalho codificado. Os casos especiais são impressos como `*S+n` e `*SA+n`, em que `n` é a variação do número de sequência, ou do número de sequência e do ACK. Se não for um caso especial, imprime zero ou mais alterações. Cada alteração é indicada por U (ponteiro de urgência), W (janela), A (ACK), S (número de sequência) ou I (ID do pacote), seguido de uma diferença (+n ou -n) ou de um novo valor (=n). Por fim, imprime a quantidade de dados do pacote e o comprimento do cabeçalho comprimido.

Por exemplo, a linha a seguir mostra um pacote TCP comprimido de saída com um identificador de conexão implícito: o ACK variou em 6, o número de sequência em 49 e o ID do pacote em 6. Há 3 bytes de dados e 6 bytes de cabeçalho comprimido:

```text
O ctcp * A+6 S+49 I+6 3 (6)
```

<a id="arprarp-packets"></a>
### Pacotes ARP/RARP

A saída ARP/RARP mostra o tipo de solicitação e seus argumentos. O formato pretende ser autoexplicativo. A seguir, uma pequena amostra do início de um ‘rlogin’ do host `rtsg` para o host `csam`:

```text
arp who-has csam tell rtsg
arp reply csam is-at CSAM
```

A primeira linha informa que rtsg enviou um pacote ARP solicitando o endereço Ethernet do host de internet csam. Csam responde com seu endereço Ethernet. Neste exemplo, os endereços Ethernet estão em maiúsculas e os endereços de internet, em minúsculas.

A saída pareceria menos redundante se tivéssemos usado `tcpdump -n`:

```text
arp who-has 128.3.254.6 tell 128.3.254.68
arp reply 128.3.254.6 is-at 02:07:01:00:01:c4
```

Se tivéssemos usado `tcpdump -e`, ficaria visível que o primeiro pacote é de broadcast e o segundo é ponto a ponto:

```text
RTSG Broadcast 0806  64: arp who-has csam tell rtsg
CSAM RTSG 0806  64: arp reply csam is-at CSAM
```

Para o primeiro pacote, a saída informa que o endereço Ethernet de origem é RTSG, o destino é o endereço de broadcast Ethernet, o campo de tipo contém o valor hexadecimal 0806 (tipo ETHER_ARP) e o comprimento total é de 64 bytes.

<a id="ipv4-packets"></a>
### Pacotes IPv4

Se o cabeçalho da camada de enlace não estiver sendo impresso, imprime `IP` após a marca temporal para pacotes IPv4.

Se a opção `-v` for especificada, exibe informações do cabeçalho IPv4 entre parênteses após `IP` ou após o cabeçalho da camada de enlace. O formato geral dessas informações é:

```text
tos tos, ttl ttl, id id, offset offset, flags [flags], proto proto, length length, options (options)
```

`tos` é o campo de tipo de serviço; se os bits ECN não forem zero, são apresentados como `ECT(1)`, `ECT(0)` ou `CE`. `ttl` é o tempo de vida e não é apresentado se for zero. `id` é o campo de identificação IP. `offset` é o campo de deslocamento do fragmento e é impresso independentemente de o pacote fazer parte de um datagrama fragmentado. `flags` representa os bits MF e DF: imprime `+` se MF estiver ativado e `DF` se F estiver ativado, conforme o texto original. Se nenhum deles estiver ativado, imprime `.`. `proto` é o campo de identificação do protocolo. `length` é o campo de comprimento total; se o pacote for considerado um envio com TSO (TCP Segmentation Offload), imprime [was 0, presumed TSO]. `options` representa as opções IP, se houver.

Em seguida, para pacotes TCP e UDP, imprime os endereços IP de origem e destino e as portas TCP ou UDP, com um ponto entre cada endereço IP e sua porta correspondente e um > separando origem e destino. Para outros protocolos, imprime os endereços, com um > separando origem e destino. Depois disso, imprime as informações do protocolo de nível superior, se houver.

Em datagramas IP fragmentados, o primeiro fragmento contém o cabeçalho do protocolo de nível superior; os fragmentos seguintes não contêm esse cabeçalho. As informações de fragmentação só são impressas com a opção `-v`, nas informações do cabeçalho IP, conforme descrito acima.

<a id="tcp-packets"></a>
### Pacotes TCP

A descrição a seguir pressupõe familiaridade com o protocolo TCP descrito na RFC 793. Sem essa familiaridade, a descrição não será muito útil.

O formato geral de uma linha do protocolo TCP é:

```text
src > dst: Flags [tcpflags], seq data-seqno, ack ackno, win window, urg urgent, options [opts], length len
```

`Src` e `dst` são os endereços IP e as portas de origem e destino. `Tcpflags` é uma combinação de S (SYN), F (FIN), P (PSH), R (RST), U (URG), W (CWR), E (ECE) ou ‘.’ (ACK), ou ‘none’ se nenhum bit de controle estiver ativado. `Data-seqno` descreve a parte do espaço de sequência coberta pelos dados deste pacote; veja o exemplo abaixo. `Ackno` é o número de sequência dos próximos dados esperados no sentido oposto desta conexão. `Window` é a quantidade de bytes disponíveis no buffer de recepção no sentido oposto desta conexão. `Urg` indica que há dados urgentes no pacote. `Opts` são as opções TCP, como mss 1024. `Len` é o comprimento dos dados da carga útil.

`Iptype`, `Src`, `dst` e `flags` estão sempre presentes. Os demais campos dependem do conteúdo do cabeçalho TCP do pacote e só são apresentados quando apropriado.

A seguir está o início de um rlogin do host `rtsg` para o host `csam`.

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

A primeira linha informa que a porta TCP 1023 de rtsg enviou um pacote à porta `login` de csam. O `S` indica que o bit `SYN` estava ativado. O número de sequência do pacote era 768512 e ele não continha dados. A notação ‘first:last’ significa números de sequência de first até last, sem incluir last; a formulação original é `sequence numbers `first` up to but not including `last`'. Não havia ACK transportado junto ao pacote; a janela de recepção disponível era de 4096 bytes e havia uma opção de tamanho máximo de segmento solicitando um MSS de 1024 bytes.

Csam responde com um pacote semelhante, mas inclui nele um ACK para o SYN de rtsg. Rtsg então confirma o SYN de csam com um ACK. O ‘.’ significa que o bit ACK estava ativado. O pacote não continha dados, portanto não há número de sequência nem comprimento de dados. O número de sequência do ACK é um inteiro pequeno, 1. Quando o `tcpdump` vê uma comunicação TCP pela primeira vez, imprime o número de sequência do pacote. Nos pacotes seguintes da comunicação, imprime a diferença entre o número de sequência do pacote atual e esse número inicial. Assim, após o primeiro, os números de sequência podem ser interpretados como posições relativas de bytes no fluxo de dados da comunicação, sendo ‘1’ o primeiro byte de dados em cada sentido. A opção ‘-S’ desativa esse recurso e faz com que os números de sequência originais sejam apresentados.

Na 6ª linha, rtsg envia a csam 19 bytes de dados: os bytes de 2 a 20 no sentido rtsg → csam da comunicação. O bit PSH está ativado no pacote. Na 7ª linha, csam informa que recebeu os dados enviados por rtsg até o byte 21, sem incluí-lo. A maior parte desses dados aparentemente ainda está no buffer do socket, pois a janela de recepção de csam diminuiu 19 bytes. Nesse pacote, csam também envia um byte de dados a rtsg. Na 8ª e na 9ª linha, csam envia a rtsg dois bytes de dados urgentes com solicitação de entrega imediata (push).

Se o tamanho de captura por pacote for pequeno a ponto de o `tcpdump` não capturar o cabeçalho TCP completo, ele interpreta o máximo possível do cabeçalho e apresenta “[|`tcp`]” para indicar que o restante não pôde ser interpretado. Se o cabeçalho contiver uma opção inválida, cujo comprimento seja pequeno demais ou ultrapasse o final do cabeçalho, o `tcpdump` apresenta “[`bad opt`]” e não interpreta outras opções, pois é impossível saber onde começam. Se o comprimento do cabeçalho indicar a presença de opções, mas o comprimento do datagrama IP for insuficiente para contê-las, o `tcpdump` apresenta “[`bad hdr length`]”.

<a id="particular-tcp-flag-combinations-syn-ack-urg-ack-etc"></a>
### Combinações específicas de bits de controle TCP (SYN-ACK, URG-ACK etc.)

Há 8 bits na seção de bits de controle do cabeçalho TCP:

`CWR | ECE | URG | ACK | PSH | RST | SYN | FIN`

Suponha que queiramos observar os pacotes usados para estabelecer uma conexão TCP. O TCP usa uma negociação de três etapas, ou three-way handshake, ao iniciar uma nova conexão. A sequência de conexão, em relação aos bits de controle TCP, é

1) O iniciador envia SYN 2) O destinatário responde com SYN, ACK 3) O iniciador envia ACK

Agora queremos capturar pacotes que tenham somente o bit SYN ativado, como na etapa 1. Não queremos os pacotes da etapa 2, SYN-ACK, mas apenas um SYN inicial simples. Precisamos de uma expressão de filtro correta para o `tcpdump`.

Relembre a estrutura de um cabeçalho TCP sem opções:

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

Um cabeçalho TCP normalmente contém 20 octetos de dados, a menos que haja opções. A primeira linha do diagrama contém os octetos de 0 a 3; a segunda mostra os octetos de 4 a 7, e assim por diante.

Contando a partir de 0, os bits de controle TCP relevantes estão no octeto 13:

```text
 0             7|             15|             23|             31
----------------|---------------|---------------|----------------
|  HL   | rsvd  |C|E|U|A|P|R|S|F|        window size            |
----------------|---------------|---------------|----------------
|               |  13th octet   |               |               |
```

Examinemos mais de perto o octeto de número 13:

```text
                |               |
                |---------------|
                |C|E|U|A|P|R|S|F|
                |---------------|
                |7   5   3     0|
```

Esses são os bits de controle TCP que nos interessam. Numeramos os bits desse octeto de 0 a 7, da direita para a esquerda; portanto, PSH é o bit número 3 e URG é o bit número 5.

Queremos capturar pacotes em que apenas SYN esteja ativado. Vejamos o que acontece com o octeto 13 quando chega um datagrama TCP com o bit SYN ativado no cabeçalho:

```text
                |C|E|U|A|P|R|S|F|
                |---------------|
                |0 0 0 0 0 0 1 0|
                |---------------|
                |7 6 5 4 3 2 1 0|
```

Ao examinar a seção de bits de controle, vemos que somente o bit número 1, SYN, está ativado.

Considerando o octeto de número 13 como um inteiro de 8 bits sem sinal na ordem de bytes da rede, seu valor binário é

00000010

e sua representação decimal é

```text
   7     6     5     4     3     2     1     0
0*2 + 0*2 + 0*2 + 0*2 + 0*2 + 0*2 + 1*2 + 0*2  =  2
```

Estamos quase terminando: agora sabemos que, se somente SYN estiver ativado, o valor do octeto de índice 13 do cabeçalho TCP, interpretado como um inteiro de 8 bits sem sinal na ordem de bytes da rede, deve ser exatamente 2.

Essa relação pode ser expressa como

tcp[13] == 2

Podemos usar essa expressão como filtro do `tcpdump` para observar pacotes em que somente SYN esteja ativado:

tcpdump -i xl0 'tcp[13] == 2'

A expressão exige que o octeto de índice 13 de um datagrama TCP tenha o valor decimal 2, exatamente o que queremos.

Agora suponha que precisemos capturar pacotes SYN, independentemente de ACK ou qualquer outro bit de controle TCP estar ativado ao mesmo tempo. Vejamos o que acontece com o octeto 13 quando chega um datagrama TCP com SYN e ACK ativados:

```text
     |C|E|U|A|P|R|S|F|
     |---------------|
     |0 0 0 1 0 0 1 0|
     |---------------|
     |7 6 5 4 3 2 1 0|
```

Agora os bits 1 e 4 estão ativados no octeto de índice 13. O valor binário do octeto 13 é

00010010

que corresponde ao valor decimal

```text
   7     6     5     4     3     2     1     0
0*2 + 0*2 + 0*2 + 1*2 + 0*2 + 0*2 + 1*2 + 0*2   = 18
```

Agora não basta usar 'tcp[13] == 18' na expressão de filtro do `tcpdump`, pois isso selecionaria somente pacotes com SYN e ACK ativados, mas não aqueles em que apenas SYN está ativado. Não importa se ACK ou qualquer outro bit de controle estiver ativado, desde que SYN esteja ativado.

Para atingir nosso objetivo, precisamos aplicar a operação lógica AND entre o valor binário do octeto 13 e outro valor que preserve o bit SYN. Queremos que SYN esteja ativado em qualquer caso; por isso, aplicamos AND entre o valor do octeto de índice 13 e o valor binário de SYN:

```text
          00010010 SYN-ACK              00000010 SYN
     AND  00000010 (we want SYN)   AND  00000010 (we want SYN)
          --------                      --------
     =    00000010                 =    00000010
```

Vemos que essa operação AND produz o mesmo resultado independentemente de ACK ou de outro bit de controle TCP estar ativado. A representação decimal da máscara usada no AND e do resultado da operação é 2, ou 00000010 em binário. Portanto, para pacotes com SYN ativado, a relação a seguir deve ser verdadeira:

( ( valor do octeto 13 ) AND ( 2 ) ) == ( 2 )

Isso nos leva à expressão de filtro do `tcpdump`

tcpdump -i xl0 'tcp[13] & 2 == 2'

Alguns deslocamentos e valores de campos podem ser expressos por nomes em vez de valores numéricos. Por exemplo, tcp[13] pode ser substituído por tcp[tcpflags]. Também estão disponíveis os seguintes valores para o campo de bits de controle TCP: tcp-fin, tcp-syn, tcp-rst, tcp-push, tcp-ack, tcp-urg, tcp-ece e tcp-cwr.

Isso pode ser demonstrado assim:

tcpdump -i xl0 'tcp[tcpflags] & tcp-push != 0'

Use aspas simples ou uma barra invertida na expressão para proteger do shell o caractere especial AND ('&').

<a id="udp-packets"></a>
### Pacotes UDP

Este pacote rwho ilustra o formato UDP:

```text
actinide.who > broadcast.who: udp 84
```

Isso informa que a porta `who` do host `actinide` enviou um datagrama UDP à porta `who` do host `broadcast`, o endereço de broadcast da Internet. O pacote continha 84 bytes de dados do usuário.

Alguns serviços UDP são reconhecidos pelo número da porta de origem ou destino, e as informações do protocolo de nível superior são impressas. Em particular, são reconhecidas as solicitações ao serviço de nomes de domínio (RFC 1034/1035) e as chamadas Sun RPC (RFC 1050) para NFS.

<a id="tcp-or-udp-name-server-requests"></a>
### Solicitações a servidores de nomes por TCP ou UDP

A descrição a seguir pressupõe familiaridade com o protocolo de serviço de domínios descrito na RFC 1035. Sem essa familiaridade, a descrição parecerá escrita em grego.

As solicitações a servidores de nomes são formatadas assim:

```text
src > dst: id op? flags qtype qclass name (len)

h2opolo.1538 > helios.domain: 3+ A? ucbvax.berkeley.edu. (37)
```

O host `h2opolo` solicitou ao servidor de domínios em `helios` um registro de endereço (qtype=A) associado ao nome `ucbvax.berkeley.edu.`. O ID da consulta era ‘3’. O ‘+’ indica que o bit `recursion desired` estava ativado. O comprimento da consulta era de 37 bytes, excluindo os cabeçalhos TCP ou UDP e IP. A operação da consulta era a habitual, `Query`; por isso, o campo op foi omitido. Se op tivesse outro valor, seria impresso entre ‘3’ e ‘+’. Da mesma forma, qclass era a habitual, `C_IN`, e foi omitida. Qualquer outra qclass seria impressa imediatamente após ‘A’.

Algumas anomalias são verificadas e podem gerar campos adicionais entre colchetes. Se uma consulta contiver uma seção de respostas, de registros de autoridade ou de registros adicionais, `ancount`, `nscount` ou `arcount` são impressos como ‘[`n`a]’, ‘[`n`n]’ ou ‘[`n`au]’, em que `n` é a contagem correspondente. Se algum dos bits de resposta estiver ativado (AA, RA ou rcode), ou se algum dos bits que devem ser zero estiver ativado nos bytes dois e três, imprime ‘[b2&3=`x`]’, em que `x` é o valor hexadecimal dos bytes dois e três do cabeçalho.

<a id="tcp-or-udp-name-server-responses"></a>
### Respostas de servidores de nomes por TCP ou UDP

As respostas de servidores de nomes são formatadas assim:

```text
src > dst:  id op rcode flags a/n/au type class data (len)

helios.domain > h2opolo.1538: 3 3/3/7 A 128.32.137.3 (273)
helios.domain > h2opolo.1537: 2 NXDomain* 0/1/0 (97)
```

No primeiro exemplo, `helios` responde à consulta de ID 3 de `h2opolo` com 3 registros de resposta, 3 registros de servidores de nomes e 7 registros adicionais. O primeiro registro de resposta é do tipo A (endereço), e seus dados são o endereço de internet 128.32.137.3. O tamanho total da resposta era de 273 bytes, excluindo os cabeçalhos TCP ou UDP e IP. A operação (Query) e o código de resposta (NoError) foram omitidos, assim como a classe (C_IN) do registro A.

No segundo exemplo, `helios` responde à consulta 2 com um código de domínio inexistente (NXDomain), sem respostas, com um servidor de nomes e sem registros de autoridade. O ‘*’ indica que o bit `authoritative answer` estava ativado. Como não havia respostas, não foram impressos tipo, classe nem dados.

Outros caracteres indicadores que podem aparecer são ‘-’, que indica que RA (recursão disponível) não está ativado (ênfase original da negação: `not`), e ‘|’, que indica que TC (mensagem truncada) está ativado. Se a seção de perguntas não contiver exatamente uma entrada, imprime ‘[`n`q]’.

<a id="smbcifs-decoding"></a>
### Decodificação SMB/CIFS

O `tcpdump` agora inclui uma decodificação bastante abrangente de SMB/CIFS/NBT para dados em UDP/137, UDP/138 e TCP/139. Também realiza uma decodificação básica de dados SMB sobre IPX e NetBEUI.

Por padrão, realiza uma decodificação bastante reduzida; com -v, ela é muito mais detalhada. Com -v, um único pacote SMB pode ocupar uma página ou mais, portanto use essa opção somente se quiser todos os detalhes minuciosos.

Para obter informações sobre os formatos dos pacotes SMB e o significado de todos os campos, consulte https://download.samba.org/pub/samba/specs/ e outros recursos online. Os patches SMB foram escritos por Andrew Tridgell (tridge@samba.org).

<a id="nfs-requests-and-replies"></a>
### Solicitações e respostas NFS

As solicitações e respostas Sun NFS (Network File System) são impressas assim:

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

Na primeira linha, o host `sushi` envia a `wrl` uma transação com ID `26377`. A solicitação tinha 112 bytes, excluindo os cabeçalhos UDP e IP. A operação era `readlink`, leitura de link simbólico, no identificador de arquivo (`fh`) 21,24/10.731657119. Com sorte, como neste caso, o identificador de arquivo pode ser interpretado como um par de números de dispositivo major e minor, seguido do número do inode e do número de geração. Na segunda linha, `wrl` responde ‘ok’ com o mesmo ID de transação e o conteúdo do link.

Na terceira linha, `sushi` solicita a `wrl`, usando um novo ID de transação, que procure o nome ‘`xcolors`’ no arquivo de diretório 9,74/4096.6878. Na quarta linha, `wrl` envia uma resposta com o respectivo ID de transação.

Os dados impressos dependem do tipo de operação. O formato pretende ser autoexplicativo quando lido junto de uma especificação do protocolo NFS. Versões antigas do tcpdump imprimiam os pacotes NFS em um formato ligeiramente diferente: o ID de transação (xid) era impresso no lugar do número da porta não NFS do pacote.

Se a opção -v, de saída detalhada, for fornecida, imprime informações adicionais. Por exemplo:

```text
sushi.1023 > wrl.nfs: NFS request xid 79658
	148 read fh 21,11/12.195 8192 bytes @ 24576
wrl.nfs > sushi.1023: NFS reply xid 79658
	reply ok 1472 read REG 100664 ids 417/0 sz 29388
```

A opção -v também imprime os campos TTL, ID, comprimento e fragmentação do cabeçalho IP, omitidos deste exemplo. Na primeira linha, `sushi` solicita a `wrl` a leitura de 8192 bytes do arquivo 21,11/12.195, a partir do deslocamento de byte 24576. `Wrl` responde ‘ok’. O pacote mostrado na segunda linha é o primeiro fragmento da resposta e, por isso, tem apenas 1472 bytes. Os demais bytes vêm nos fragmentos seguintes, mas eles não têm cabeçalhos NFS nem mesmo UDP e, dependendo da expressão de filtro usada, podem não ser impressos. Como a opção -v foi fornecida, alguns atributos do arquivo, retornados além dos dados do arquivo, são impressos: o tipo de arquivo (“REG”, para arquivo regular), o modo do arquivo em octal, o UID, o GID e o tamanho do arquivo.

Se a opção -v for fornecida mais de uma vez, imprime ainda mais detalhes.

Os pacotes de resposta NFS não identificam explicitamente a operação RPC. Em vez disso, o `tcpdump` acompanha as solicitações recentes e as associa às respostas pelo ID de transação. Se uma resposta não vier logo após a solicitação correspondente, talvez não seja possível analisá-la.

<a id="afs-requests-and-replies"></a>
### Solicitações e respostas AFS

As solicitações e respostas Transarc AFS (Andrew File System) são impressas assim:

```text
src.sport > dst.dport: rx packet-type
src.sport > dst.dport: rx packet-type service call call-name args
src.sport > dst.dport: rx packet-type service reply call-name args


elvis.7001 > pike.afsfs:
	rx data fs call rename old fid 536876964/1/1 ".newsrc.new"
	new fid 536876964/1/1 ".newsrc"
pike.afsfs > elvis.7001: rx data fs reply rename
```

Na primeira linha, o host elvis envia um pacote RX a pike. Trata-se de um pacote de dados RX para o serviço fs (fileserver), que inicia uma chamada RPC. A chamada RPC era uma renomeação: o ID do arquivo do diretório antigo era 536876964/1/1 e o nome de arquivo antigo era ‘.newsrc.new’; o ID do arquivo do novo diretório era 536876964/1/1 e o novo nome de arquivo era ‘.newsrc’. O host pike responde à chamada de renomeação com uma resposta RPC. A operação foi bem-sucedida, pois a resposta era um pacote de dados, e não um pacote de abortamento.

Em geral, todas as RPCs AFS são decodificadas ao menos quanto ao nome da chamada RPC. Na maioria delas, pelo menos alguns argumentos são decodificados: normalmente apenas os considerados interessantes, conforme o critério adotado.

O formato pretende ser autoexplicativo, mas provavelmente não será útil para quem não conhece o funcionamento de AFS e RX.

Se a opção -v, de saída detalhada, for fornecida duas vezes, imprime pacotes de confirmação e informações adicionais do cabeçalho, como o ID de chamada RX, o número da chamada, o número de sequência, o número de série e os bits de controle do pacote RX.

Se a opção -v for fornecida duas vezes, imprime informações adicionais, como o ID de chamada RX, o número de série e os bits de controle do pacote RX. Também imprime as informações de negociação de MTU dos pacotes de confirmação RX.

Se a opção -v for fornecida três vezes, imprime o índice de segurança e o ID do serviço.

Imprime códigos de erro para pacotes de abortamento, exceto para os pacotes de sinalização periódica (beacon) Ubik, pois o protocolo Ubik usa pacotes de abortamento para indicar um voto afirmativo.

Os pacotes de resposta AFS não identificam explicitamente a operação RPC. Em vez disso, o `tcpdump` acompanha as solicitações recentes e as associa às respostas pelo número da chamada e pelo ID do serviço. Se uma resposta não vier logo após a solicitação correspondente, talvez não seja possível analisá-la.

<a id="kip-appletalk-ddp-in-udp"></a>
### KIP AppleTalk (DDP em UDP)

Os pacotes AppleTalk DDP encapsulados em datagramas UDP são desencapsulados e apresentados como pacotes DDP, descartando todas as informações do cabeçalho UDP. O arquivo `/etc/atalk.names` é usado para converter números de rede e de nó AppleTalk em nomes. As linhas desse arquivo têm o formato

```text
number	name

1.254		ether
16.1		icsd-net
1.254.110	ace
```

As duas primeiras linhas fornecem os nomes de redes AppleTalk. A terceira fornece o nome de um host específico. Um host se distingue de uma rede pelo terceiro octeto do número: um número de rede deve ter dois octetos e um número de host deve ter três octetos (ênfase original da obrigatoriedade: `must`). O número e o nome devem ser separados por espaços em branco, como espaços ou tabulações. O arquivo `/etc/atalk.names` pode conter linhas em branco ou de comentário, iniciadas por ‘#’.

Os endereços AppleTalk são impressos no formato

```text
net.host.port

144.1.209.2 > icsd-net.112.220
office.2 > icsd-net.112.220
jssmag.149.235 > icsd-net.2
```

Se `/etc/atalk.names` não existir ou não contiver uma entrada para algum número de host ou rede AppleTalk, os endereços são impressos em formato numérico. No primeiro exemplo, NBP, na porta DDP 2 do nó 209 da rede 144.1, envia para quem estiver escutando na porta 220 do nó 112 da rede icsd. A segunda linha é igual, exceto por ser conhecido o nome completo do nó de origem, ‘office’. A terceira linha é um envio da porta 235 do nó 149 da rede jssmag para o endereço de broadcast na porta NBP de icsd-net. O endereço de broadcast, 255, é indicado por um nome de rede sem número de host; por isso, convém manter distintos os nomes de nós e os nomes de redes em /etc/atalk.names.

O conteúdo dos pacotes NBP (Name Binding Protocol) e ATP (AppleTalk Transaction Protocol) é interpretado. Para outros protocolos, imprime somente o nome do protocolo, ou seu número se não houver nome registrado, e o tamanho do pacote.

<a id="nbp-packets"></a>
### Pacotes NBP

Os pacotes NBP são formatados como nos exemplos a seguir:

```text
icsd-net.112.220 > jssmag.2: nbp-lkup 190: "=:LaserWriter@*"
jssmag.209.2 > icsd-net.112.220: nbp-reply 190: "RM1140:LaserWriter@*" 250
techpit.2 > icsd-net.112.220: nbp-reply 190: "techpit:LaserWriter@*" 186
```

A primeira linha é uma solicitação de busca de nomes para laserwriters, enviada pelo host 112 da rede icsd e difundida por broadcast na rede jssmag. O ID NBP da busca é 190. A segunda linha mostra uma resposta a essa solicitação, com o mesmo ID, enviada pelo host jssmag.209, informando que ele tem um recurso laserwriter chamado “RM1140” registrado na porta 250. A terceira linha é outra resposta à mesma solicitação e informa que o host techpit tem um laserwriter chamado “techpit” registrado na porta 186.

<a id="atp-packets"></a>
### Pacotes ATP

O exemplo a seguir demonstra a formatação dos pacotes ATP:

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

Jssmag.209 inicia a transação de ID 12266 com o host helios solicitando até 8 pacotes, indicados por ‘<0-7>’. O número hexadecimal no final da linha é o valor do campo ‘userdata’ da solicitação.

Helios responde com 8 pacotes de 512 bytes. O ‘:digit’ após o ID da transação indica o número de sequência do pacote na transação; o número entre parênteses é a quantidade de dados do pacote, excluindo o cabeçalho ATP. O ‘*’ no pacote 7 indica que o bit EOM estava ativado.

Jssmag.209 solicita então a retransmissão dos pacotes 3 e 5. Helios os reenvia e, em seguida, jssmag.209 libera a transação. Por fim, jssmag.209 inicia a próxima solicitação. O ‘*’ na solicitação indica que XO, de ‘exactly once’ ou ‘exatamente uma vez’, não estava ativado (ênfase original da negação: `not`).

<a id="backward-compatibility"></a>
## COMPATIBILIDADE COM VERSÕES ANTERIORES

Os nomes de bits de controle TCP `tcp-ece` e `tcp-cwr` passaram a estar disponíveis ao vincular o programa à libpcap 1.9.0 ou posterior.

<a id="see-also"></a>
## CONSULTE TAMBÉM

`stty`(1), `pcap`(3PCAP), `bpf`(4), `nit`(4P), `pcap-savefile`(5), `pcap-filter`(7), `pcap-tstamp`(7)

`https://www.iana.org/assignments/media-types/application/vnd.tcpdump.pcap`

<a id="authors"></a>
## AUTORES

Os autores originais são:

Van Jacobson, Craig Leres e Steven McCanne, todos do Lawrence Berkeley National Laboratory, Universidade da Califórnia, Berkeley, CA.

Atualmente, o programa é mantido pelo The Tcpdump Group.

A versão atual está disponível via HTTPS:

`https://www.tcpdump.org/`

A distribuição original está disponível via FTP anônimo:

`ftp://ftp.ee.lbl.gov/old/tcpdump.tar.Z`

O suporte a IPv6/IPsec foi acrescentado pelo projeto WIDE/KAME. Este programa usa OpenSSL/LibreSSL em configurações específicas.

## BUGS

Para relatar um problema de segurança, envie um e-mail para security@tcpdump.org.

Para relatar bugs e outros problemas, contribuir com patches, solicitar funcionalidades, fornecer comentários gerais etc., consulte o arquivo `CONTRIBUTING.md` na raiz da árvore de código-fonte do tcpdump.

NIT não permite observar seu próprio tráfego de saída; BPF permite. Recomendamos usar BPF.

Deveria haver uma tentativa de remontar os fragmentos IP ou, ao menos, de calcular o comprimento correto para o protocolo de nível superior.

As consultas inversas a servidores de nomes não são apresentadas corretamente: imprime a seção de perguntas, vazia, em vez da consulta real na seção de respostas. Alguns consideram que as próprias consultas inversas são um bug e preferem corrigir o programa que as gera em vez do `tcpdump`.

Um rastreamento de pacotes que atravesse uma mudança de horário de verão apresentará marcas temporais incorretas, pois a mudança de horário é ignorada.

Expressões de filtro sobre campos que não pertençam aos cabeçalhos Token Ring não tratam corretamente pacotes Token Ring com roteamento pela origem.

Expressões de filtro sobre campos que não pertençam aos cabeçalhos 802.11 não tratam corretamente pacotes de dados 802.11 com To DS e From DS ativados simultaneamente.

`ip6 proto` deveria percorrer a cadeia de cabeçalhos, mas atualmente não o faz. Para esse comportamento, está disponível `ip6 protochain`.

Expressões aritméticas sobre cabeçalhos da camada de transporte, como `tcp[0]`, não funcionam com pacotes IPv6. Elas examinam somente pacotes IPv4.


---

## Procedência desta tradução

Fonte primária: [manual preservado](../../../sources/upstream/tcpdump/tcpdump.8.source), extraído de `/usr/share/man/man8/tcpdump.8.gz`. Pacote `tcpdump`, versão `4.99.6-2`; pacote-fonte `tcpdump`, versão `4.99.6-2`. Aquisição de pacote instalado, sem atribuição de commit Git.

Licença: [LicenseRef-Tcpdump-Manpage](../../99-Assets/upstream/tcpdump/LICENSE.txt); [copyright e condições do pacote](../../99-Assets/upstream/tcpdump/COPYRIGHT.package.txt). [Página de referência do pacote, não a origem exata do arquivo](https://www.tcpdump.org/). Hashes do original, gzip e avisos no registro de fontes. A data do manual é histórica; não implica que todos os serviços externos mantenham esse comportamento.
