---
title: "arping — manual de referência"
type: "official-documentation"
tool: "arping"
status: "source-checked"
reviewed: "2026-10-26"
language: "pt-BR"
tags: ["documentation", "tool/arping"]
cssclasses: ["fieldbook"]
source_url: "https://www.habets.pp.se/synscan/programs.php?prog=arping"
source_kind: "installed-kali-package"
package: "arping"
binary_version: "2.28-1"
source_package: "arping"
source_version: "2.28-1"
source_snapshot_sha256: "72e48dfb57a7a8f401a408124ca0295cae8f32eda0d4efb879735e99dc7ae71b"
source_sha256: "de74f6c4e808c9fb7003e4ad03c1fa0df98cf4c677b9cd4aeb647a3316f444d8"
license_spdx: "GPL-2.0-or-later"
human_review: "pending"
source_scope: "Complete English installed arping(8) manual only; upstream README, FAQ, scripts and additional website coverage remain pending"
binary: "arping"
source_manual_date: "21th June, 2003"
manual_section: "8"
test_status: "help-only"
tested_version: "arping 2.28-1"
---

> Tradução para português produzida por assistente de IA e conferida seção por seção contra a fonte. Revisão humana independente: pendente. Opções e exemplos originais foram preservados; nenhum exemplo foi executado automaticamente.

> **Compatibilidade observada:** arping 2.28-1. A ajuda dessa instalação não lista `--help`. A fonte fixada foi mantida sem trocar opções silenciosamente. Conferidas somente arping --help, arping -h e a versão dpkg. Embora não liste --help, a ajuda estendida foi obtida com essa opção e código 0. Nenhum endereço, interface ou alvo foi fornecido, e nenhuma operação de envio ARP/ICMP foi solicitada. [Evidência e limites do teste](../../99-Assets/evidence/arping-help-tests.json).

<!-- SPDX-License-Identifier: GPL-2.0-or-later -->
# arping

<a id="name"></a>
## NOME

arping - envia pings ARP e/ou IP a um host especificado

<a id="synopsis"></a>
## SINOPSE

```text
arping [-0aAbBdDeFhpqrRuUv] [-S host/ip] [-T host/ip] [-s MAC]    [-t MAC] [-c count] [-i interface] [ -w seconds ] [ -W seconds ] [ -V vlan ] [ -Q priority ] [ -g group ] <host | -B>

arping --help
```

<a id="description"></a>
## DESCRIÇÃO

O utilitário arping envia solicitações ARP e/ou ICMP ao host especificado e exibe as respostas. O host pode ser especificado pelo nome, pelo endereço IP ou pelo endereço MAC.

Uma solicitação é enviada a cada segundo.

Ao enviar ping a um IP, é enviada uma consulta ARP who-has. Ao enviar ping a um endereço MAC, é enviada uma solicitação ICMP Echo de broadcast direcionado. Para uma explicação mais técnica e perguntas frequentes, consulte o arquivo README.

Nota sobre temporização

Em uma LAN, os pacotes ARP normalmente recebem respostas tão rápidas que o escalonador de tarefas do sistema operacional não consegue acompanhá-las para obter uma temporização suficientemente exata. Em um sistema ocioso, os tempos de ida e volta serão bastante precisos, mas, com mais carga, a temporização perde exatidão.

Para obter uma temporização mais exata em um sistema que não esteja ocioso, ajuste a prioridade nice do arping para aproximadamente `-15`.

```text
# nice -n -15 arping foobar
```

Isso não é um problema apenas do arping; também ocorre com o ping normal (pelo menos no meu sistema). Mas não fica tão evidente com o ping, pois os pacotes do arping, ao consultar IPs, não atravessam a pilha IP ao serem recebidos e, por isso, recebem respostas mais rapidamente.

<a id="options"></a>
## OPÇÕES

### `--help`

Mostra a ajuda estendida. Não é tão extensa quanto esta página de manual, mas contém mais informações que `-h`.

### `-0`

Use esta opção para enviar ping com endereço IP de origem `0.0.0.0`. Use-a quando ainda não tiver configurado sua interface. Isso pode fazer com que o ping por MAC fique sem resposta. É um alias de `-S 0.0.0.0`.

### `-a`

Ping audível.

<a id="-a-1"></a>
### `-A`

Conta apenas os endereços que correspondem ao endereço solicitado (isso *VAI* prejudicar a maioria das operações. Só é útil ao usar arping em vários hosts ao mesmo tempo. Veja um exemplo em `arping-scan-net.sh`).

### `-b`

Como `-0`, mas com endereço de origem de broadcast (`255.255.255.255`). Isso pode deixar o arping sem resposta, pois não é um comportamento normal para um host.

<a id="-b-1"></a>
### `-B`

Use no lugar do host se quiser endereçar `255.255.255.255`.

### `-c count`

Envia apenas `count` solicitações.

<a id="-c-count-1"></a>
### `-C count`

Aguarda apenas `count` respostas, independentemente de `-c` e `-w`.

### `-d`

Encontra respostas duplicadas. Encerra com código 1 se houver respostas de dois endereços MAC diferentes.

<a id="-d-1"></a>
### `-D`

Exibe respostas como pontos de exclamação e pacotes ausentes como pontos. Como o flood ping de um equipamento Cisco.

### `-e`

Como `-a`, mas emite um sinal sonoro quando não há resposta.

### `-F`

Não tenta determinar automaticamente o nome da interface. Mesmo sem este sinalizador, `-i` desativa essa determinação automática.

### `-g group`

Executa `setgid()` para este grupo em vez do grupo nobody.

### `-h`

Exibe uma mensagem de ajuda e encerra.

### `-i interface`

Não tenta adivinhar: usa a interface especificada.

### `-m type`

Tipo de marca temporal a usar nos pacotes recebidos. Use `-vv` ao enviar ping para listar os tipos disponíveis.

### `-p`

Ativa o modo promíscuo na interface; use se você não "possuir" o endereço MAC que está usando.

<a id="-p-1"></a>
### `-P`

Envia respostas ARP em vez de solicitações. Útil com `-U`.

### `-q`

Não exibe mensagens, exceto mensagens de erro.

### `-Q priority`

Prioridade 802.1p a definir. Deve ser usada com uma tag 802.1Q (`-V`). O padrão é 0.

### `-r`

Saída bruta: exibe apenas o endereço MAC/IP de cada resposta.

<a id="-r-1"></a>
### `-R`

Saída bruta: como `-r`, mas mostra "o outro" endereço; pode ser combinada com `-r`.

### `-s MAC`

Define o endereço MAC de origem. Talvez seja necessário usar `-p` com esta opção.

### `-S IP`

Como `-b` e `-0`, mas com um endereço de origem definido. Isso pode deixar o arping sem resposta se o alvo não tiver uma rota para esse IP. Se você não possuir o IP que está usando, talvez precise ativar o modo promíscuo na interface (com `-p`). Com esta opção, é possível descobrir o endereço IP de um host sem atribuir a si próprio um endereço IP.

### `-t MAC`

Define o endereço MAC de destino a usar ao enviar ping a um endereço IP.

### `-T IP`

Usa `-T` como endereço de destino ao enviar ping a MACs que não respondam a um ping de broadcast, mas talvez respondam a um broadcast direcionado.

Exemplo: para verificar o endereço de MAC-A, use informações conhecidas sobre MAC-B e IP-B.

```text
$ arping -S <IP-B> -s <MAC-B> -p <MAC-A>
```

### `-u`

Mostra index=received/sent em vez de apenas index=received ao enviar ping a MACs.

<a id="-u-1"></a>
### `-U`

Envia ARP não solicitado. Isso define como broadcast o endereço MAC de destino no quadro ARP. O ARP não solicitado é usado para atualizar os caches ARP dos vizinhos.

Exemplo:

```text
$ arping -i <interface> -U <interface IP>
```

### `-v`

Saída detalhada. Use duas vezes para obter mais mensagens.

### `-V vlan`

Tag VLAN a definir. O padrão é não usar tag VLAN.

### `-w sec`

Especifica um tempo limite para o encerramento do ping, independentemente de quantos pacotes tenham sido enviados ou recebidos.

<a id="-w-sec-1"></a>
### `-W sec`

Tempo de espera entre os pings.

### `-z`

Ativa o seccomp (o estado padrão do seccomp depende das opções de compilação).

<a id="-z-1"></a>
### `-Z`

Desativa o seccomp (o estado padrão do seccomp depende das opções de compilação).

<a id="examples"></a>
## EXEMPLOS

```text
# arping -c 3 88.1.180.225
ARPING 88.1.180.225
60 bytes from 00:11:85:4c:01:01 (88.1.180.225): index=0 time=13.910 msec
60 bytes from 00:11:85:4c:01:01 (88.1.180.225): index=1 time=13.935 msec
60 bytes from 00:11:85:4c:01:01 (88.1.180.225): index=2 time=13.944 msec

--- 88.1.180.225 statistics ---
3 packets transmitted, 3 packets received,   0% unanswered

# arping -c 3 00:11:85:4c:01:01
ARPING 00:11:85:4c:01:01
60 bytes from 88.1.180.225 (00:11:85:4c:01:01): icmp_seq=0 time=13.367 msec
60 bytes from 88.1.180.225 (00:11:85:4c:01:01): icmp_seq=1 time=13.929 msec
60 bytes from 88.1.180.225 (00:11:85:4c:01:01): icmp_seq=2 time=13.929 msec

--- 00:11:85:4c:01:01 statistics ---
3 packets transmitted, 3 packets received,   0% unanswered

# arping -C 2 -c 10 -r 88.1.180.225
00:11:85:4c:01:01
00:11:85:4c:01:01
```

## BUGS

É necessário usar `-B` em vez de executar arping para `255.255.255.255`, e `-b` em vez de `-S 255.255.255.255`. Isso é uma falha da libnet.

<a id="see-also"></a>
## VEJA TAMBÉM

ping(8), arp(8), rarp(8)

<a id="author"></a>
## AUTOR

O Arping foi escrito por Thomas Habets <thomas@habets.se>.

http://www.habets.pp.se/synscan/

```text
git clone http://github.com/ThomasHabets/arping.git
```


---

## Procedência desta tradução

Fonte primária: [manual preservado](../../../sources/upstream/arping/arping.8.source), extraído de `/usr/share/man/man8/arping.8.gz`. Pacote `arping`, versão `2.28-1`; pacote-fonte `arping`, versão `2.28-1`. Aquisição de pacote instalado, sem atribuição de commit Git.

Licença: [GPL-2.0-or-later](../../99-Assets/upstream/arping/LICENSE.txt); [copyright e condições do pacote](../../99-Assets/upstream/arping/COPYRIGHT.package.txt). [Página de referência do pacote, não a origem exata do arquivo](https://www.habets.pp.se/synscan/programs.php?prog=arping). Hashes do original, gzip e avisos no registro de fontes. A data do manual é histórica; não implica que todos os serviços externos mantenham esse comportamento.
