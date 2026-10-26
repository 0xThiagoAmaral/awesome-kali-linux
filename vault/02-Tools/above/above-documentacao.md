---
title: "above — documentação oficial"
type: "official-documentation"
tool: "above"
status: "translated-machine"
reviewed: "2026-10-26"
language: "pt-BR"
tags: ["documentation", "tool/above"]
cssclasses: ["fieldbook"]
source_url: "https://github.com/caster0x00/Above/blob/313f550ebb87d815aeece6792104b8c3f2a9db8f/README.md"
source_commit: "313f550ebb87d815aeece6792104b8c3f2a9db8f"
source_sha256: "7dec6e01263ed4064e2ba2428c1e6a011b0a17539db14b3c88da2df90d02633e"
license_spdx: "Apache-2.0"
human_review: "pending"
source_scope: "Official English repository README/docs and available upstream Portuguese README; external manuals/wiki coverage tracked separately"
---

> Tradução automática local para português, ainda sem revisão humana integral. Estrutura e blocos de código preservados; referências externas não significam conteúdo espelhado.

# Above

Sniffer de segurança de rede para encontrar vulnerabilidades na rede. Projetado para pentesters e engenheiros de segurança.

![](../../99-Assets/upstream/above/banner/banner.png)

```text
        ___    __                  
       /   |  / /_  ____ _   _____ 
      / /| | / __ \/ __ \ | / / _ \
     / ___ |/ /_/ / /_/ / |/ /  __/
    /_/  |_/_.___/\____/|___/\___/ 

    Above: Network Security Sniffer
    Developer: Mahama Bazarov (Caster)
    Contact: mahamabazarov@mailbox.org
    Version: 2.8.1
    Codename: Rubens Barrichello
    Documentation & Usage: https://github.com/caster0x00/Above
```

# Disclaimer

**Todas as informações contidas neste repositório são fornecidas apenas para fins educacionais e de pesquisa. O autor não é responsável por qualquer uso ilegal desta ferramenta**.

**It é uma ferramenta de segurança de rede especializada que ajuda tanto pentesters quanto profissionais de segurança**.

---

# Mechanics

Acima está um sniffer de segurança de rede para encontrar vulnerabilidades em equipamentos de rede. Ele é baseado inteiramente na análise de tráfego de rede, por isso não faz nenhum ruído no ar. Ele é invisível. Completamente baseado na biblioteca Scapy.

> Acima permite que os pentesters automatizem o processo de encontrar vulnerabilidades em hardware de rede. Protocolos de descoberta, roteamento dinâmico, 802.1Q, protocolos de resolução, ICS, FHRP, STP, LLMNR/NBT-NS, etc.

<a id="supported-protocols"></a>
## Protocolos suportados

Detecta até 28 protocolos:

```text
MACSec (802.1X AE)
EAPOL (Checking 802.1X versions)
ARP (Host Discovery)
CDP (Cisco Discovery Protocol)
DTP (Dynamic Trunking Protocol)
LLDP (Link Layer Discovery Protocol) 
VLAN (802.1Q)
S7COMM (Siemens) (SCADA)
OMRON (SCADA)
TACACS+ (Terminal Access Controller Access Control System Plus)
ModbusTCP (SCADA)
STP (Spanning Tree Protocol)
OSPF (Open Shortest Path First)
EIGRP (Enhanced Interior Gateway Routing Protocol)
BGP (Border Gateway Protocol)
VRRP (Virtual Router Redundancy Protocol)
HSRP (Host Standby Redundancy Protocol)
GLBP (Gateway Load Balancing Protocol)
IGMP (Internet Group Management Protocol)
LLMNR (Link Local Multicast Name Resolution)
NBT-NS (NetBIOS Name Service)
MDNS (Multicast DNS)
DHCP (Dynamic Host Configuration Protocol)
DHCPv6 (Dynamic Host Configuration Protocol v6)
ICMPv6 (Internet Control Message Protocol v6)
SSDP (Simple Service Discovery Protocol)
MNDP (MikroTik Neighbor Discovery Protocol)
SNMP (Simple Network Management Protocol)
```
<a id="operating-mechanism"></a>
## Mecanismo de funcionamento

Acima funciona em dois modos:

- Modo quente: Cheirando em sua interface especificando um timer
- Modo frio: Analisando lixões de tráfego

A ferramenta é muito simples em seu funcionamento e é impulsionada por argumentos:

- Interface: Especificando a interface de rede na qual será realizado o sniffing
- Temporizador: Tempo durante o qual a análise de tráfego será realizada
- Entrada: A ferramenta toma um `.pcap` já preparado como entrada e procura protocolos nele
- Saída: Acima irá gravar o tráfego escutado para o arquivo `.pcap`, seu nome que você especificar a si mesmo
- ARP passivo: Detectando hosts em um segmento usando ARP passivo
- Pesquisa VLAN: Procure segmentos VLAN extraindo IDs VLAN no tráfego

```text
usage: above.py [-h] [--interface INTERFACE] [--timer TIMER] [--output OUTPUT] [--input INPUT] [--passive-arp] [--search-vlan]

options:
  -h, --help            show this help message and exit
  --interface INTERFACE
                        Interface for traffic listening
  --timer TIMER         Time in seconds to capture packets, default: not set
  --output OUTPUT       File name where the traffic will be recorded, default: not set
  --input INPUT         File name of the traffic dump
  --passive-arp         Passive ARP (Host Discovery)
  --search-vlan         VLAN Search
```

---

<a id="information-about-protocols"></a>
## Informação sobre protocolos

As informações obtidas serão úteis não só para o pentester, mas também para o engenheiro de segurança, ele saberá o que precisa prestar atenção.

Quando acima detecta um protocolo, ele produz as informações necessárias para indicar o vetor de ataque ou problema de segurança:

- Impacto: Que tipo de ataque pode ser realizado neste protocolo;

- Ferramentas: Que ferramenta pode ser usada para lançar um ataque;

- Informações técnicas: Informações necessárias para o pentester, endereços MAC/IP do remetente, IDs de grupo FHRP, domínios OSPF/EIGRP, etc.

- Mitigação: Recomendações para a fixação dos problemas de segurança

- Endereços de destino: Para protocolos, acima exibe informações sobre os endereços de origem e destino MAC e endereços IP

---

# Installation

### Linux
Você pode instalar acima diretamente dos repositórios do Kali Linux
```bash
caster@kali:~$ sudo apt update && sudo apt install above
```

Ou:

```bash
:~$ sudo apt-get install python3-scapy python3-colorama python3-setuptools
:~$ git clone https://github.com/caster0x00/above
:~$ cd above/
:~/above$ sudo python3 setup.py install
```

### MacOS:
```bash
# Install python3 first
brew install python3
# Then install required dependencies
sudo pip3 install scapy colorama setuptools

# Clone the repo
git clone https://github.com/caster0x00/above
cd above/
sudo python3 setup.py install
```

Não se esqueça de **desativar** seu firewall no macOS!
<a id="settings--network--firewall"></a>
#### Configurações > Rede > Firewall
--------------------------

# How to Use

<a id="hot-mode"></a>
## Modo quente

> Acima requer acesso root para farejar

Acima pode ser executado com ou sem um timer:

```bash
caster@kali:~$ sudo above --interface eth0 --timer 120
```
> Para parar de farejar tráfego, pressione CTRL + С
>

Exemplo:

```bash
caster@kali:~$ sudo above --interface eth0 --timer 120
        ___    __                  
       /   |  / /_  ____ _   _____ 
      / /| | / __ \/ __ \ | / / _ \
     / ___ |/ /_/ / /_/ / |/ /  __/
    /_/  |_/_.___/\____/|___/\___/ 

    Above: Network Security Sniffer
    Developer: Mahama Bazarov (Caster)
    Contact: mahamabazarov@mailbox.org
    Version: 2.8.1
    Codename: Rubens Barrichello
    Documentation & Usage: https://github.com/caster0x00/Above

[*] Start Sniffing

[+] Detected STP Frame
[*] Attack Impact: Partial MITM
[*] Tools: Yersinia, Scapy
[*] STP Root Switch MAC: 00:11:22:33:44:55
[*] STP Root ID: 32768
[*] STP Root Path Cost: 0
[*] Mitigation: Enable BPDU Guard or Portfast
[*] Vendor: Routerboard.com
```

Se você precisar gravar o tráfego farejado, use o argumento `--output`

```bash
caster@kali:~$ sudo above --interface eth0 --timer 120 --output above.pcap
```
> Se você interromper a ferramenta com CTRL+C, o tráfego ainda é gravado no arquivo

<a id="cold-mode"></a>
## Modo frio

Se você já tem algum tráfego gravado, você pode usar o argumento `--input` para procurar possíveis problemas de segurança

```bash
caster@kali:~$ above --input hsrp.cap
```

Exemplo:

```bash
caster@kali:~$ sudo above --input hsrp.cap
        ___    __                  
       /   |  / /_  ____ _   _____ 
      / /| | / __ \/ __ \ | / / _ \
     / ___ |/ /_/ / /_/ / |/ /  __/
    /_/  |_/_.___/\____/|___/\___/ 

    Above: Network Security Sniffer
    Developer: Mahama Bazarov (Caster)
    Contact: mahamabazarov@mailbox.org
    Version: 2.8.1
    Codename: Rubens Barrichello
    Documentation & Usage: https://github.com/caster0x00/Above

    [+] Analyzing pcap file...


[+] Detected HSRP Packet
[*] HSRP Active Router Priority: 90
[+] Attack Impact: MITM
[*] Tools: Loki, Scapy, Yersinia
[*] HSRP Group Number: 10
[+] HSRP Virtual IP Address: 10.28.168.254
[*] HSRP Sender IP: 10.28.168.253
[*] HSRP Sender MAC: 00:00:0c:07:ac:0a
[!] Authentication: Plaintext Phrase: cisco
[*] Mitigation: Priority 255, Authentication, Extended ACL
[*] Vendor: Cisco Systems
```

# Passive ARP

Isto pode ser muito útil se um atacante não quiser fazer barulho no ar com as análises ARP e descobrir as máquinas silenciosamente. Esta função é executada com o `--passive-arp` e todas as máquinas encontradas serão gravadas no arquivo `above_passive_arp.txt`.

```bash
caster@kali:~$ sudo above --interface eth0 --passive-arp

[+] Starting Host Discovery...
[*] IP and MAC addresses will be saved to 'above_passive_arp.txt'
```

> Se você quiser, você pode especificar um timer por quanto tempo para ouvir os quadros ARP para encontrar hosts. Por padrão, nenhum timer está definido.

Uma vez iniciado, o terminal será completamente limpo e uma tabela composta por um mapeamento do endereço IP e do endereço MAC será exibida:

```bash
+--------------------+------------------------------+--------------------+
| IP Address         | MAC Address                   | ARP Type           |
+--------------------+------------------------------+--------------------+
| 172.16.120.12      | f0:27:65:ba:1c:42             | ARP Response       |
| 172.16.120.45      | 6d:9f:84:2b:33:ea             | ARP Request        |
| 172.16.120.78      | 3a:7c:19:d8:4e:21             | ARP Response       |
| 172.16.120.103     | c4:12:76:ae:50:bb             | ARP Request        |
| 172.16.120.127     | 89:3b:df:92:6a:54             | ARP Response       |
| 172.16.120.156     | b7:5d:49:cb:72:99             | ARP Request        |
| 172.16.120.189     | 1e:47:ac:3d:15:f8             | ARP Response       |
| 172.16.120.222     | 43:9a:df:e0:84:3c             | ARP Request        |
+--------------------+------------------------------+--------------------+

```

O conteúdo do arquivo `above_passive_arp.txt` será assim:

```bash
caster@kali:~$ cat above_passive_arp.txt 
Above: Passive ARP Host Discovery
Time: 2024-08-16 17:30:16
--------------------------------------------------
172.16.120.12 - f0:27:65:ba:1c:42
172.16.120.45 - 6d:9f:84:2b:33:ea
172.16.120.78 - 3a:7c:19:d8:4e:21
172.16.120.103 - c4:12:76:ae:50:bb
172.16.120.127 - 89:3b:df:92:6a:54
172.16.120.156 - b7:5d:49:cb:72:99
172.16.120.189 - 1e:47:ac:3d:15:f8
172.16.120.222 - 43:9a:df:e0:84:3c
```

É assim que acima com a aprendizagem de quadros ARP pode ajudar a descobrir hospedeiros em um segmento sem ruído no ar.

# VLAN Segments Search

Acima também pode encontrar IDs VLAN no tráfego. Esta é uma opção útil se o atacante estiver em uma porta de tronco em algumas circunstâncias durante o pentest. E o problema é que em uma porta de tronco, todo o tráfego é marcado com tags 802.1Q pertencentes a segmentos VLAN. Acima pode extrair todos os IDs VLAN do ar ou de uma descarga de tráfego:

```bash
caster@kali:~$ sudo above --interface eth0 --search-vlan 
```

Quando você executar esta função, o terminal também será limpo e uma tabela será exibida e atualizada:

```bash
+------------------------------+---------------+----------------------------------------+
|VLAN ID                       |Frames Count   |How to Jump                             |
+------------------------------+---------------+----------------------------------------+
|120                           |8              |sudo vconfig add eth0 120               |
|80                            |8              |sudo vconfig add eth0 80                |
|251                           |7              |sudo vconfig add eth0 251               |
|190                           |6              |sudo vconfig add eth0 190               |
+------------------------------+---------------+----------------------------------------+
```

Além disso, o resultado desta função será escrito para o arquivo `above_discovered_vlan.txt`:

```bash
caster@kali:~$ cat above_discovered_vlan.txt
Above: Discovered VLAN ID
Time: 2024-08-16 17:41:19
--------------------------------------------------------------------------------
VLAN ID                       Frames Count   How to Jump                             
--------------------------------------------------------------------------------
1                             208            sudo vconfig add eth0 1                 
5                             972            sudo vconfig add eth0 5                 
6                             904            sudo vconfig add eth0 6                 
10                            20             sudo vconfig add eth0 10                
12                            20             sudo vconfig add eth0 12                
13                            20             sudo vconfig add eth0 13                
11                            20             sudo vconfig add eth0 11                
2000                          1              sudo vconfig add eth0 2000              
1000                          2              sudo vconfig add eth0 1000              
--------------------------------------------------------------------------------
```

É assim que você pode encontrar informações sobre segmentos de VLAN com base apenas em operações de tráfego. Mas vale a pena considerar que este é um cenário específico, não é muitas vezes que um atacante estará em uma porta de tronco. Ou ele terá sorte com o DTP ou ele vai tropeçar em uma porta de switch esquecida pelo administrador.

# MAC Lookup

A partir da versão 2.8 Above é agora capaz de identificar o fornecedor pelo endereço MAC, especificamente pelos primeiros 24 bits. Isto é feito usando um [banco de dados baixado](https://standards-oui.ieee.org/), em seguida, convertendo-o para o módulo `above_oui_dict.py`, que é um dicionário que consiste de OUIS e nomes de fornecedores únicos.

# Copyright

Copyright (c) 2025 Mahama Bazarov. Este projeto está licenciado sob a Licença Apache 2.0

# Outro

Se você tiver alguma sugestão ou encontrar algum bug, sinta-se livre para criar problemas no repositório ou entre em contato comigo: [mahamabazarov@ mailbox.org](mailto:mahamabazarov@mailbox.org)






---

## Procedência desta tradução

Fonte: [https://github.com/caster0x00/Above](https://github.com/caster0x00/Above/blob/313f550ebb87d815aeece6792104b8c3f2a9db8f/README.md). Licença: [Apache-2.0](../../99-Assets/upstream/above/LICENSE.txt). Commit: 313f550ebb87d815aeece6792104b8c3f2a9db8f.

O original preservado, a lista de mudanças de apresentação e os hashes constam no manifesto do projeto. Nenhum exemplo desta documentação foi executado automaticamente.
