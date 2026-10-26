<!-- SPDX-License-Identifier: LicenseRef-ARP-Scan-Manpage -->
<!-- Complete AI-assistant translation; independent human review pending. -->
# arp-scan

## NOME

arp-scan — envia requisições ARP aos hosts de destino e exibe as respostas.

## SINOPSE

```text
arp-scan [options] [hosts...]
```

Os hosts de destino devem ser informados na linha de comando, exceto quando se usa a opção `--file` ou `--localnet`.

Os alvos podem ser endereços IPv4 ou nomes de host. Também são aceitas a notação CIDR, como 10.0.0.0/24, a notação rede:máscara, como 10.0.0.0:255.255.255.0, e intervalos de IPs, como 10.0.0.1-10.0.0.10. Por padrão, as notações CIDR e rede:máscara incluem os endereços de rede e de broadcast, a menos que --exclude-broadcast seja especificada.

## DESCRIÇÃO

O `arp-scan` envia pacotes de requisição ARP aos hosts especificados e exibe as respostas recebidas. A interface de rede pode ser escolhida com `--interface`. Se nenhuma interface for informada, o `arp-scan` selecionará a interface ativa e configurada de menor número, excluindo loopback.

O `arp-scan` usa sockets brutos, o que exige privilégios em alguns sistemas:

### Linux com suporte a capabilities POSIX.1e por meio da libcap:

O `arp-scan` reconhece capabilities. Ele exige `CAP_NET_RAW` no conjunto de capabilities permitidas e só a habilita nas funções que precisam dela. Use `setcap cap_net_raw+p /path/to/arp-scan` para acrescentar CAP_NET_RAW ao conjunto permitido do executável. Esse suporte também torna o uso de SUID root muito mais seguro, pois o `arp-scan` descarta todas as capabilities exceto CAP_NET_RAW e não executa com privilégios completos de root.

### BSD e macOS:

É necessário ter acesso de leitura e escrita a `/dev/bpf*`.

### Qualquer sistema operacional:

Executar como root ou com SUID root funciona em qualquer sistema operacional, mas outros métodos são preferíveis quando disponíveis.

ARP funciona somente na rede local e não pode ser roteado. Embora use endereços IPv4, não é um protocolo IP, e o `arp-scan` pode ser usado em interfaces sem endereço IPv4.

É enviada uma requisição ARP para cada alvo. Se um host não responder, a requisição será reenviada mais uma vez. O número de tentativas pode ser alterado com `--retry`. Reduzir esse número diminui o tempo de varredura, mas aumenta o risco de perder resultados devido à perda de pacotes.

A largura de banda usada pelo `arp-scan` pode ser definida com `--bandwidth`. O padrão é 256000 bits por segundo. Aumentá-la reduz o tempo da varredura, mas um valor excessivo pode gerar uma taxa elevada de pacotes de broadcast. Outra forma de definir a taxa de envio é usar `--interval`.

O tempo de uma varredura de passagem única, isto é, com `--retry`=1, é:

```text
time = n times i + t + o
```

Notação matemática equivalente: `time = n × i + t + o`.

Nessa expressão, `n` é o número de hosts; `i` é o intervalo entre pacotes, informado por `--interval` ou calculado a partir de `--bandwidth`; `t` é o tempo limite, definido por `--timeout`; e `o` é o tempo adicional necessário para carregar a lista de alvos e ler os arquivos de associação MAC/fabricante. Esse tempo adicional costuma ser desprezível, em torno de 100 ms, mas pode ser reduzido com `--quiet`. Em listas pequenas, o tempo limite é o fator predominante; em listas grandes, o intervalo entre pacotes é mais importante.

Qualquer parte da requisição ARP pode ser modificada com as opções `--arpXXX`, conforme a tabela:

Opções do pacote de requisição ARP

|Campo|Bits|Opção|Padrão|
|---|---|---|---|
|`ar$hrd`|`16`|`--arphrd`|`1 (ARPHRD_ETHER)`|
|`ar$pro`|`16`|`--arppro`|`0x0800`|
|`ar$hln`|`8`|`--arphln`|`6 (ETH_ALEN)`|
|`ar$pln`|`8`|`--arppln`|`4 (IPv4)`|
|`ar$op`|`16`|`--arpop`|`1 (ARPOP_REQUEST)`|
|`ar$sha`|`48`|`--arpsha`|endereço de hardware da interface|
|`ar$spa`|`32`|`--arpspa`|endereço IPv4 da interface|
|`ar$tha`|`48`|`--arptha`|`00:00:00:00:00:00`|
|`ar$tpa`|`32`|Nenhuma|endereço IPv4 do host de destino|

A opção mais comum é `--arpspa`, que define o endereço IPv4 de origem na requisição ARP. Ela permite usar um endereço de origem diferente daquele atribuído à interface e possibilita executar o `arp-scan` em interfaces sem endereço IPv4. Definir `ar$spa` como o IP do alvo faz alguns sistemas operacionais informarem um conflito de endereços quando recebem uma requisição ARP para seu próprio endereço.

Os valores do cabeçalho do quadro Ethernet também podem ser alterados:

Opções do cabeçalho Ethernet

|Campo|Bits|Opção|Padrão|
|---|---|---|---|
|Endereço de destino|`48`|`--destaddr`|`ff:ff:ff:ff:ff:ff`|
|Endereço de origem|`48`|`--srcaddr`|endereço da interface|
|Tipo de protocolo|`16`|`--prototype`|`0x0806 (ARP)`|

A opção `--destaddr`, que define o endereço Ethernet de destino, é a única desse grupo usada com frequência.

Por padrão, as respostas ARP são exibidas no seguinte formato:

```text
<IPv4 Address>	<MAC Address>	<Vendor Details>
```

Nesse formato, `IPv4 Address` é o endereço IP do alvo que respondeu; `MAC Address` é seu endereço de camada de enlace; e `Vendor Details` são os dados do fabricante obtidos a partir do endereço de hardware. Os campos são separados por um único caractere de tabulação. O formato de saída pode ser alterado com `--format`.

As respostas são exibidas na ordem de recebimento. Essa ordem pode ser diferente daquela em que as requisições foram enviadas, pois alguns hosts respondem mais rapidamente que outros.

A identificação do fabricante usa os arquivos `ieee-oui.txt` e `mac-vendor.txt`. O primeiro é gerado a partir dos registros IEEE `MA-L` (OUI), `MA-M`, `MA-S` (OUI36) e `IAB`. O arquivo `mac-vendor.txt` contém associações adicionais entre endereços MAC e fabricantes e permite incluir associações personalizadas. O `get-oui` atualiza `ieee-oui.txt` com os dados mais recentes dos registros IEEE.

Todos os hosts IPv4 devem responder a requisições ARP, inclusive aqueles com filtragem de pacotes, como firewalls. Isso torna o `arp-scan` útil para descobrir hosts IPv4 ativos na rede local.

## OPÇÕES

Quando uma opção recebe um valor, seu tipo é indicado por uma letra entre sinais de menor e maior. Essa letra representa o tipo de dado esperado:

### `<s>`

Cadeia de caracteres.

### `<i>`

Número inteiro decimal ou hexadecimal, se precedido por 0x; por exemplo, 2048 ou 0x800.

### `<f>`

Número decimal de ponto flutuante.

### `<m>`

Endereço MAC, como 01:23:45:67:89:ab ou 01-23-45-67-89-ab, sem distinção entre maiúsculas e minúsculas.

### `<a>`

Endereço IPv4, como 10.0.0.1.

### `<h>`

Dados binários codificados em hexadecimal, sem o prefixo 0x e sem distinção entre maiúsculas e minúsculas.

### `<x>`

Outro tipo; consulte a descrição da opção.

### Opções gerais

#### `--help or -h`

Exibe a mensagem de uso e encerra.

#### `--verbose or -v`

Exibe mensagens detalhadas de progresso. A opção pode ser repetida para aumentar o nível de detalhe, até o máximo de 3.

#### `--version or -V`

Exibe a versão do programa e encerra. Inclui detalhes da licença, a versão da libpcap e a indicação de suporte a capabilities POSIX.1e.

#### `--interface=<s> or -I <s>`

Usa a interface de rede `<s>`. Se ela não for especificada, o arp-scan procurará, na lista de interfaces do sistema, a interface ativa e configurada de menor número, excluindo loopback.

### Seleção de hosts

#### `--file=<s> or -f <s>`

Lê nomes de host ou endereços do arquivo especificado, com um nome ou padrão de endereços por linha. Use "-" para ler da entrada padrão, stdin.

#### `--localnet or -l`

Gera endereços a partir da configuração da interface. A lista é formada pelo endereço e pela máscara de rede da interface, incluindo rede e broadcast, salvo quando --exclude-broadcast é usada. Essa opção não pode ser combinada com `--file` nem com alvos informados na linha de comando. Use `--interface` para escolher outro adaptador que não seja o primeiro.

#### `--exclude-broadcast`

Exclui os endereços de rede e de broadcast dos intervalos gerados pelas notações rede/bits e rede:máscara e do intervalo obtido da configuração da interface com --localnet.

### Arquivos de associação MAC/fabricante

#### `--ouifile=<s> or -O <s>`

Usa o arquivo `<s>` de associações entre registros IEEE e fabricantes. O padrão é `ieee-oui.txt` no diretório atual. Se ele não for encontrado ou não puder ser aberto, será usado `@PKGDATADIR@/ieee-oui.txt`.

#### `--macfile=<s> or -m <s>`

Usa o arquivo personalizado `<s>` de associações de fabricantes. O padrão é `mac-vendor.txt` no diretório atual. Se ele não for encontrado ou não puder ser aberto, será usado `@PKGSYSCONFDIR@/mac-vendor.txt`.

### Controle do formato de saída

#### `--quiet or -q`

Exibe uma saída mínima para cada host que respondeu, mostrando apenas os endereços IP e MAC. Reduz o consumo de memória em cerca de 5 MB, pois os arquivos de fabricantes não são usados. Quando `--quiet` é especificada, somente os campos `${ip}` e `${mac}` ficam disponíveis para `--format`.

#### `--plain or -x`

Suprime os textos de cabeçalho e rodapé, exibindo apenas os detalhes dos hosts que responderam. É útil quando a saída será processada por um script.

#### `--ignoredups or -g`

Não exibe pacotes duplicados. Por padrão, eles são marcados com `(DUP: n)`, em que `n` é o número de respostas recebidas desse host.

#### `--rtt or -D`

Calcula e exibe o tempo de ida e volta dos pacotes, em milissegundos e frações de microssegundo. Disponibiliza o campo `${rtt}` para `--format`.

#### `--format=<s> or -F <s>`

Define a cadeia de formato emitida para cada host que respondeu. Os dados do host podem ser incluídos por referências a campos com a sintaxe "`${field[;width]}`". Os campos são alinhados à direita, exceto quando a largura é negativa; nesse caso, são alinhados à esquerda. Os nomes de campo abaixo não diferenciam maiúsculas e minúsculas:

|Campo|Descrição|
|---|---|
|`IP`|Endereço IPv4 do host em notação decimal pontuada|
|`Name`|Nome do host, quando `--resolve` é usada|
|`MAC`|Endereço MAC do host, no formato xx:xx:xx:xx:xx:xx|
|`HdrMAC`|Endereço Ethernet de origem, quando diferente|
|`Vendor`|Texto com os dados do fabricante|
|`Padding`|Preenchimento após o pacote ARP, em hexadecimal, quando diferente de zero|
|`Framing`|Tipo de enquadramento, quando diferente de Ethernet_II|
|`VLAN`|Identificador de VLAN 802.1Q, quando presente|
|`Proto`|Protocolo ARP, quando diferente de 0x0800|
|`DUP`|Número do pacote para respostas duplicadas, maior que 1|
|`RTT`|Tempo de ida e volta, quando `--rtt` é usada|
|`IPnum`|Endereço IPv4 do host como inteiro de 32 bits|

Somente os campos `${ip}` e `${mac}` ficam disponíveis quando `--quiet` é especificada.

Os caracteres que não representam campos são emitidos literalmente. A barra invertida "\" introduz sequências de escape:

|Campo|Descrição|
|---|---|
|`\n`|nova linha|
|`\r`|retorno de carro|
|`\t`|tabulação|
|`\`|suprimir o significado especial do caractere seguinte|

Coloque o argumento de `--format` entre aspas simples para proteger os caracteres especiais da interpretação pelo shell.

Exemplos:

Exemplos originais de formatação em notação da fonte tbl; os escapes foram preservados, sem tratá-los como uma receita de shell pronta para execução:

```text
--format='${ip}\\t${mac}\\t${vendor}'\n
--resolve --format='${ip}\\t${mac}\\t${name;20}\\t${vendor}'
```

### Embaralhamento da lista de hosts

#### `--random or -R`

Embaralha a lista de hosts de destino.

#### `--randomseed=<i>`

Define a semente do gerador de números pseudoaleatórios. É útil quando se deseja uma ordem reproduzível com `--random`.

### Temporização de saída e novas tentativas

#### `--retry=<i> or -r <i>`

Define o número total de tentativas por host como `<i>`. O padrão é 2.

#### `--backoff=<f> or -b <f>`

Define o fator de recuo como `<f>`, com padrão 1.50. O tempo limite é multiplicado por `<f>` a cada passagem.

#### `--timeout=<i> or -t <i>`

Define o tempo limite inicial de cada host como `<i>` milissegundos, com padrão 500. Esse valor vale para o primeiro pacote enviado a cada host. Os tempos seguintes são multiplicados pelo fator definido em `--backoff`.

#### `--interval=<x> or -i <x>`

Define o intervalo mínimo entre pacotes como `<x>`. Isso controla a largura de banda de saída por meio da taxa de envio. Para estabelecer diretamente uma largura de banda máxima, é mais simples usar --bandwidth. O intervalo é dado em milissegundos ou, se houver o sufixo "u", em microssegundos.

#### `--bandwidth=<x> or -B <x>`

Define a largura de banda de saída como `<x>`, com padrão 256000 bits por segundo. Acrescente `K` para quilobits ou `M` para megabits, usando múltiplos decimais. Não é possível especificar `--interval` e `--bandwidth` simultaneamente.

### Resolução DNS

#### `--numeric or -N`

Exige que os alvos sejam endereços IP, não nomes de host. Pode reduzir o tempo de inicialização de listas extensas.

#### `--resolve or -d`

Resolve os endereços que responderam para nomes de host. O formato padrão passa a exibir o nome em vez do endereço IPv4. Essa opção disponibiliza o campo `${name}` para `--format`.

### Pacote ARP de saída

#### `--arpsha=<m> or -u <m>`

Define o endereço Ethernet de origem do ARP, no campo `ar$sha` de 48 bits, sem modificar o endereço de hardware do cabeçalho do quadro. Para alterar esse outro endereço, use `--srcaddr`. O padrão é o endereço Ethernet da interface de saída.

#### `--arptha=<m> or -w <m>`

Define o endereço Ethernet de destino do ARP, no campo `ar$tha` de 48 bits. O padrão é zero, pois esse campo não é usado em requisições ARP.

#### `--arphrd=<i> or -H <i>`

Define o tipo de hardware do ARP, com padrão `1`, no campo `ar$hrd` de 16 bits. O valor padrão é `1` (`ARPHRD_ETHER`); muitos sistemas operacionais também respondem a `6` (`ARPHRD_IEEE802`).

#### `--arppro=<i> or -p <i>`

Define o tipo de protocolo do ARP, com padrão `0x0800`, no campo `ar$pro` de 16 bits. A maioria dos sistemas operacionais responde somente a `0x0800`, correspondente a IPv4.

#### `--arphln=<i> or -a <i>`

Define o comprimento do endereço de hardware, com padrão `6`, no campo `ar$hln` de 8 bits. Os comprimentos dos campos `ar$sha` e `ar$tha` não são alterados; somente `ar$hln` é modificado.

#### `--arppln=<i> or -P <i>`

Define o comprimento do endereço de protocolo, com padrão `4`, no campo `ar$pln` de 8 bits. Os comprimentos dos campos `ar$spa` e `ar$tpa` não são alterados; somente `ar$pln` é modificado.

#### `--arpop=<i> or -o <i>`

Define a operação ARP, com padrão `1`, no campo `ar$op` de 16 bits. A maioria dos sistemas operacionais responde somente ao valor 1, ARPOP_REQUEST.

#### `--arpspa=<a> or -s <a>`

Define o endereço IPv4 de origem em notação decimal pontuada. O valor também pode ser a cadeia "`dest`", que usa o endereço do host de destino como origem. O padrão é o endereço da interface de saída. A opção modifica `ar$spa`, de 32 bits. Alguns sistemas só respondem se a origem pertencer à rede da interface receptora. Definir `ar$spa` como o IP de destino pode provocar a indicação de conflito de endereços em alguns sistemas.

### Cabeçalho Ethernet de saída

#### `--srcaddr=<m> or -S <m>`

Define o endereço MAC Ethernet de origem, cujo padrão é o MAC da interface. Modifica o cabeçalho Ethernet, não o endereço dentro do pacote ARP; para este último, use `--arpsha`.

#### `--destaddr=<m> or -T <m>`

Define o endereço MAC de destino no cabeçalho Ethernet. O padrão é `ff:ff:ff:ff:ff:ff`, broadcast. Os hosts também respondem a requisições destinadas ao seu endereço unicast ou a um endereço multicast que estejam escutando.

#### `--prototype=<i> or -y <i>`

Define o tipo de protocolo no cabeçalho Ethernet, com padrão `0x0806`.

#### `--llc or -L`

Usa o encapsulamento LLC/SNAP da RFC 1042 para redes 802.2. Independentemente dessa opção, o `arp-scan` decodifica e exibe respostas ARP em Ethernet-II e IEEE 802.2.

#### `--vlan=<i> or -Q <i>`

Usa marcação 802.1Q com o identificador de VLAN `<i>`, que deve estar entre 0 e 4095. O arp-scan decodifica e exibe respostas ARP em 802.1Q independentemente dessa opção.

### Opções diversas

#### `--limit=<i> or -M <i>`

Encerra após o número especificado de hosts responder. O `arp-scan` retorna código 1 se a quantidade de respostas for menor que o limite. Isso permite verificar essa condição em scripts sem analisar a saída.

#### `--pcapsavefile=<s> or -W <s>`

Grava os pacotes recebidos no arquivo pcap `<s>`. As respostas ARP são salvas nesse arquivo, além de serem decodificadas e exibidas.

#### `--snap=<i> or -n <i>`

Define o tamanho de captura pcap, snap length, como `<i>`, com padrão 64. O tamanho inclui o cabeçalho Ethernet, e o padrão normalmente é suficiente.

#### `--retry-send=<i> or -Y <i>`

Define o número de tentativas de envio, com padrão 20.

#### `--retry-send-interval=<i> or -E <i>`

Define o intervalo entre tentativas de envio, em milissegundos ou em microssegundos se houver o sufixo "u". O padrão é 5.

#### `--padding=<h> or -A <h>`

Define um preenchimento após os dados do pacote. Acrescenta ao final da requisição ARP o valor hexadecimal <h>.

## CÓDIGO DE SAÍDA

O `arp-scan` retorna 0 quando termina com sucesso e um valor maior que 0 quando ocorre um erro.

Quando `--limit` é especificada, o `arp-scan` também retorna um código diferente de zero se a quantidade de hosts que responderam for menor que o limite.

## ARQUIVOS

### `@PKGDATADIR@/ieee-oui.txt`

Lista de associações entre identificadores OUI da IEEE, Organisationally Unique Identifier, e fabricantes.

### `@PKGSYSCONFDIR@/mac-vendor.txt`

Lista de outras associações entre endereços MAC Ethernet e fabricantes, incluindo acréscimos locais.

## EXEMPLOS

### Varredura simples

Varre a rede padrão, usando a configuração IPv4 da interface para gerar a lista de hosts.

```text
$ arp-scan --localnet
Interface: eth0, type: EN10MB, MAC: 50:65:f3:f0:6d:7c, IPv4: 10.0.0.106
Starting arp-scan 1.9.9 with 256 hosts (https://github.com/royhills/arp-scan)
10.0.0.14       a4:1f:72:7f:25:bb       Dell Inc.
10.0.0.22       10:60:4b:73:43:de       Hewlett Packard
10.0.0.74       00:0c:29:90:07:e9       VMware, Inc.
10.0.0.75       00:0c:29:66:9e:c2       VMware, Inc.
10.0.0.76       00:0c:29:d0:e1:ea       VMware, Inc.
10.0.0.82       9c:b6:54:bb:f3:ec       Hewlett Packard
10.0.0.84       00:21:9b:fd:b9:b3       Dell Inc.
10.0.0.85       00:02:b3:eb:5a:f8       Intel Corporation
10.0.0.91       00:9c:02:a5:7b:29       Hewlett Packard
10.0.0.92       d4:ae:52:d0:07:6f       Dell Inc.
10.0.0.93       d4:ae:52:d0:04:9b       Dell Inc.
10.0.0.96       9c:b6:54:bb:f5:35       Hewlett Packard
10.0.0.97       00:0c:29:0e:95:20       VMware, Inc.
10.0.0.104      50:65:f3:f0:70:a4       Hewlett Packard

15 packets received by filter, 0 packets dropped by kernel
Ending arp-scan 1.9.9: 256 hosts scanned in 1.532 seconds (167.10 hosts/sec). 14 responded
```

### Formatação de saída

Varre todos os hosts de `10.0.0.0/24` pela interface `eth0`, calcula o tempo de ida e volta e exibe colunas alinhadas com um formato personalizado.

```text
$ arp-scan -I eth0 --rtt --format='|${ip;-15}|${mac}|${rtt;8}|' 10.0.0.0/24
Interface: eth0, type: EN10MB, MAC: 50:65:f3:f0:6d:7c, IPv4: 10.0.0.106
Starting arp-scan 1.9.9 with 256 hosts (https://github.com/royhills/arp-scan)
|10.0.0.14      |a4:1f:72:7f:25:bb|   0.280|
|10.0.0.22      |10:60:4b:73:43:de|   0.293|
|10.0.0.74      |00:0c:29:90:07:e9|   0.380|
|10.0.0.75      |00:0c:29:66:9e:c2|   0.311|
|10.0.0.76      |00:0c:29:d0:e1:ea|   0.326|
|10.0.0.82      |9c:b6:54:bb:f3:ec|   0.216|
|10.0.0.84      |00:21:9b:fd:b9:b3|   0.244|
|10.0.0.85      |00:02:b3:eb:5a:f8|   0.244|
|10.0.0.91      |00:9c:02:a5:7b:29|   0.209|
|10.0.0.92      |d4:ae:52:d0:07:6f|   0.289|
|10.0.0.93      |d4:ae:52:d0:04:9b|   0.278|
|10.0.0.96      |9c:b6:54:bb:f5:35|   0.255|
|10.0.0.97      |00:0c:29:0e:95:20|   0.288|
|10.0.0.104     |50:65:f3:f0:70:a4|   0.263|

14 packets received by filter, 0 packets dropped by kernel
Ending arp-scan 1.9.9: 256 hosts scanned in 2.032 seconds (125.98 hosts/sec). 14 responded
```

### Saída CSV

`--plain` remove a saída adicional.

```text
$ arp-scan -I eth0 --plain --format='${ip},${mac},"${vendor}"' 10.0.0.0/24
10.0.0.14,a4:1f:72:7f:25:bb,"Dell Inc."
10.0.0.22,10:60:4b:73:43:de,"Hewlett Packard"
10.0.0.74,00:0c:29:90:07:e9,"VMware, Inc."
10.0.0.75,00:0c:29:66:9e:c2,"VMware, Inc."
10.0.0.76,00:0c:29:d0:e1:ea,"VMware, Inc."
10.0.0.82,9c:b6:54:bb:f3:ec,"Hewlett Packard"
10.0.0.84,00:21:9b:fd:b9:b3,"Dell Inc."
10.0.0.85,00:02:b3:eb:5a:f8,"Intel Corporation"
10.0.0.91,00:9c:02:a5:7b:29,"Hewlett Packard"
10.0.0.92,d4:ae:52:d0:07:6f,"Dell Inc."
10.0.0.93,d4:ae:52:d0:04:9b,"Dell Inc."
10.0.0.96,9c:b6:54:bb:f5:35,"Hewlett Packard"
10.0.0.97,00:0c:29:0e:95:20,"VMware, Inc."
10.0.0.104,50:65:f3:f0:70:a4,"Hewlett Packard"
```

## VEJA TAMBÉM

`get-oui`(1)

`arp-fingerprint`(1)

[https://github.com/royhills/arp-scan/wiki](https://github.com/royhills/arp-scan/wiki) — wiki do arp-scan.

[https://github.com/royhills/arp-scan](https://github.com/royhills/arp-scan) — página do projeto arp-scan.

## Aviso de licença original

```text
.\" Copyright (C) Roy Hills
.\"
.\" Copying and distribution of this file, with or without modification,
.\" are permitted in any medium without royalty provided the copyright
.\" notice and this notice are preserved.
.\"
```
