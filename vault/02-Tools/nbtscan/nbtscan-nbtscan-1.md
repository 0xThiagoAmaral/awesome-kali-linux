---
title: "nbtscan — manual de referência"
type: "official-documentation"
tool: "nbtscan"
status: "source-checked"
reviewed: "2026-10-26"
language: "pt-BR"
tags: ["documentation", "tool/nbtscan"]
cssclasses: ["fieldbook"]
source_url: "https://github.com/resurrecting-open-source-projects/nbtscan"
source_kind: "installed-kali-package"
package: "nbtscan"
binary_version: "1.7.2-3"
source_package: "nbtscan"
source_version: "1.7.2-3"
source_snapshot_sha256: "5d0690f9b6e12b9c0b1411486ca9cce62417ee78b43ecb57442c18cfd9a59f96"
source_sha256: "5a2e2690923164f8a7667f871ed6f476139aff943659b82a8e854afbcaa65f78"
license_spdx: "GPL-2.0-or-later"
human_review: "pending"
source_scope: "Complete English installed nbtscan(1) manual only; upstream README, FAQ, scripts and additional website coverage remain pending"
binary: "nbtscan"
source_manual_date: "13 Jan 2022"
manual_section: "1"
test_status: "usage-only"
tested_version: "nbtscan 1.7.2-3"
---

> Tradução para português produzida por assistente de IA e conferida seção por seção contra a fonte. Revisão humana independente: pendente. Opções e exemplos originais foram preservados; nenhum exemplo foi executado automaticamente.

> **Compatibilidade observada:** nbtscan 1.7.2-3. As opções do manual foram encontradas na ajuda instalada. A fonte fixada foi mantida sem trocar opções silenciosamente. Executado nbtscan sem argumentos: código 2 de uso capturado pelo subprocesso, sem alvo; -h significa nomes de serviços, não ajuda. Há divergência em -t: o manual diz segundos/padrão 1; a mensagem instalada diz milissegundos/padrão 1000. A tradução preserva o manual e registra a divergência; nenhum envio ou tempo de resposta de rede foi testado. [Evidência e limites do teste](../../99-Assets/evidence/nbtscan-help-tests.json).

<!-- SPDX-License-Identifier: GPL-2.0-or-later -->
# nbtscan

<a id="name"></a>
## NOME

nbtscan - varre redes em busca de informações de nomes NetBIOS

<a id="synopsis"></a>
## SINOPSE

```text
nbtscan [-v] [-d] [-e] [-l] [-t timeout] [-b bandwidth] [-r] [-q]
        [-s separator] [-h] [-m retransmits] [-f filename | target]
```

<a id="description"></a>
## DESCRIÇÃO

NBTscan é um programa para varrer redes IP em busca de informações de nomes NetBIOS. Ele envia uma consulta de status NetBIOS a cada endereço do intervalo fornecido e lista as informações recebidas em formato legível. Para cada host que responde, lista o endereço IP, o nome NetBIOS do computador, o nome do usuário conectado e o endereço MAC (como o Ethernet).

NBTscan produz um relatório como este:

```text
    IP address     NetBIOS Name  Server    User           MAC address
    -----------------------------------------------------------------------
    192.168.1.2    MYCOMPUTER              JDOE           00-a0-c9-12-34-56
    192.168.1.5    WIN98COMP     <server>  RROE           00-a0-c9-78-90-00
    192.168.1.123  DPTSERVER     <server>  ADMINISTRATOR  08-00-09-12-34-56
```

A primeira coluna lista o endereço IP do host que respondeu. A segunda coluna é o nome do computador. A terceira coluna indica se esse computador compartilha ou pode compartilhar arquivos ou impressoras. Em uma máquina NT, isso significa que o Serviço de Servidor está em execução. No Windows 95, significa que a caixa "Quero poder permitir que outras pessoas acessem meus arquivos" ou "Quero poder permitir que outras pessoas imprimam em minha(s) impressora(s)" está marcada (em Painel de Controle/Rede/Compartilhamento de Arquivos e Impressoras). Na maioria das vezes, significa que esse computador compartilha arquivos. A terceira coluna mostra o nome do usuário. Se ninguém estiver conectado a partir desse computador, ele será igual ao nome do computador. A última coluna mostra o endereço MAC do adaptador.

> **Nota editorial:** o original repete "terceira coluna" ao descrever o usuário. No relatório reproduzido acima, `User` é a quarta coluna. A redação original foi traduzida sem corrigir essa divergência silenciosamente.

Se executado com a opção `-v`, o NBTscan lista a tabela inteira de nomes NetBIOS de cada endereço que respondeu. A saída tem este aspecto:

```text
    NetBIOS Name Table for Host 192.168.1.123:

    Name             Service          Type
    ----------------------------------------
    DPTSERVER        <00>             UNIQUE
    DPTSERVER        <20>             UNIQUE
    DEPARTMENT       <00>             GROUP
    DEPARTMENT       <1c>             GROUP
    DEPARTMENT       <1b>             UNIQUE
    DEPARTMENT       <1e>             GROUP
    DPTSERVER        <03>             UNIQUE
    DEPARTMENT       <1d>             UNIQUE
    ??__MSBROWSE__?  <01>             GROUP
    INet~Services    <1c>             GROUP
    IS~DPTSERVER     <00>             UNIQUE
    DPTSERVER        <01>             UNIQUE

    Adapter address: 00-a0-c9-12-34-56
    ----------------------------------------
```

<a id="options"></a>
## OPÇÕES

Um resumo das opções está incluído abaixo.

### `-v`

Saída detalhada. Imprime todos os nomes recebidos de cada host.

### `-d`

Despeja os pacotes. Imprime todo o conteúdo dos pacotes. Não pode ser usado com as opções `-v`, `-s` ou `-h`.

### `-e`

Formata a saída no formato de `/etc/hosts`.

### `-l`

Formata a saída no formato lmhosts.

### `-t <timeout>`

Aguarda `timeout` segundos por uma resposta. O padrão é 1.

### `-b <bandwidth>`

Limitação da saída. Reduz a velocidade da saída para que não use mais que `bandwidth` bps. Útil em conexões lentas, para evitar o descarte das consultas enviadas.

### `-r`

Usa a porta local 137 para as varreduras. Máquinas Win95 só respondem a essa porta. É necessário ser root para usar esta opção.

### `-q`

Suprime banners e mensagens de erro.

### `-s <separator>`

Saída adequada para scripts. Não imprime cabeçalhos de colunas nem de registros; separa os campos com `separator`.

### `-h`

Imprime nomes legíveis para os serviços. Só pode ser usada com a opção `-v`.

### `-m <retransmits>`

Número de retransmissões (`retransmits`). O padrão é 0.

### `-f <filename>`

Obtém do arquivo "`filename`" os endereços IP a varrer.

### `target`

NBTscan é uma ferramenta de linha de comando. É necessário fornecer pelo menos um argumento: o intervalo de endereços, em uma destas três formas:

### `xxx.xxx.xxx.xxx`

IP único em notação decimal com pontos. Exemplo: `192.168.1.1`.

### `xxx.xxx.xxx.xxx/xx`

Endereço de rede e máscara de sub-rede. Exemplo: `192.168.1.0/24`.

### `xxx.xxx.xxx.xxx-xxx`

Intervalo de endereços. Exemplo: `192.168.1.1-127`. Isso varre todos os endereços de `192.168.1.1` a `192.168.1.127`.

<a id="examples"></a>
## EXEMPLOS

Varre toda a rede de classe C:

```text
    nbtscan 192.168.1.0/24
```

Varre toda a rede de classe C usando a porta 137:

```text
    nbtscan -r 192.168.1.0/24
```

Varre um intervalo de `192.168.1.25` a `192.168.1.137`:

```text
    nbtscan 192.168.1.25-137
```

Varre uma rede de classe C. Imprime os resultados em formato adequado para scripts, usando dois-pontos como separador de campos:

```text
    nbtscan -v -s : 192.168.1.0/24
```

O último comando produz uma saída como esta:

```text
    192.168.0.1:NT_SERVER:00U
    192.168.0.1:MY_DOMAIN:00G
    192.168.0.1:ADMINISTRATOR:03U
    192.168.0.2:OTHER_BOX:00U
    ...
```

Varre os endereços IP especificados no arquivo iplist:

```text
    nbtscan -f iplist
```

<a id="netbios-suffixes"></a>
## SUFIXOS NETBIOS

O sufixo NetBIOS, também conhecido como caractere final NetBIOS (endchar), indica o tipo de serviço do nome registrado. Os códigos mais conhecidos estão listados abaixo. (U = nome único, G = nome de grupo.)

|Nome|Número (hex.)|Tipo|Uso|
|---|---|---|---|
|`<computername>`|`00`|`U`|Serviço de estação de trabalho|
|`<computername>`|`01`|`U`|Serviço de mensagens|
|`<\--__MSBROWSE__>`|`01`|`G`|Navegador mestre|
|`<computername>`|`03`|`U`|Serviço de mensagens|
|`<computername>`|`06`|`U`|Serviço de servidor RAS|
|`<computername>`|`1F`|`U`|Serviço NetDDE|
|`<computername>`|`20`|`U`|Serviço de servidor de arquivos|
|`<computername>`|`21`|`U`|Serviço de cliente RAS|
|`<computername>`|`22`|`U`|Intercâmbio do Exchange (conector MSMail)|
|`<computername>`|`23`|`U`|Armazenamento do Exchange|
|`<computername>`|`24`|`U`|Diretório do Exchange|
|`<computername>`|`30`|`U`|Serviço de servidor de compartilhamento de modem|
|`<computername>`|`31`|`U`|Serviço de cliente de compartilhamento de modem|
|`<computername>`|`43`|`U`|Controle remoto de clientes SMS|
|`<computername>`|`44`|`U`|Ferramenta de controle remoto dos administradores SMS|
|`<computername>`|`45`|`U`|Chat remoto dos clientes SMS|
|`<computername>`|`46`|`U`|Transferência remota dos clientes SMS|
|`<computername>`|`87`|`U`|Microsoft Exchange MTA|
|`<computername>`|`6A`|`U`|Microsoft Exchange IMC|
|`<computername>`|`BE`|`U`|Agente do Monitor de Rede|
|`<computername>`|`BF`|`U`|Aplicativo Monitor de Rede|
|`<username>`|`03`|`U`|Serviço de mensagens|
|`<domain>`|`00`|`G`|Nome de domínio|
|`<domain>`|`1B`|`U`|Navegador mestre de domínio|
|`<domain>`|`1C`|`G`|Controladores de domínio|
|`<domain>`|`1D`|`U`|Navegador mestre|
|`<domain>`|`1E`|`G`|Eleições do serviço de navegação|
|`<INet~Services>`|`1C`|`G`|IIS|
|`<IS~computer name>`|`00`|`U`|IIS|

<a id="faq"></a>
## PERGUNTAS FREQUENTES

### `1.`

NBTscan lista minhas máquinas Windows normalmente, mas não lista meus sistemas Unix nem roteadores. Por quê?

R: É assim que ele deve funcionar. NBTscan usa NetBIOS para a varredura, e NetBIOS só é implementado pelo Windows (e por alguns programas em Unix, como o Samba).

### `2.`

Por que recebo erros "Connection reset by peer" no Windows 2000?

R: NBTscan usa a porta UDP 137 para enviar consultas. Se a porta estiver fechada no host de destino, ele responderá com uma mensagem ICMP "Port unreachable". A maioria dos sistemas operacionais ignora essa mensagem. O Windows 2000 a informa ao aplicativo como erro "Connection reset by peer". Basta ignorá-lo.

### `3.`

Por que o NBTscan não procura compartilhamentos? Vocês vão adicionar essa função ao NBTscan?

R: Não. NBTscan usa UDP para suas operações, o que o torna muito rápido. A busca por compartilhamentos exige TCP. Em primeiro lugar, isso tornaria o nbtscan mais lento. Além disso, adicionar essa busca significa acrescentar muito código novo ao nbtscan. Existem muitos bons scanners de compartilhamentos, portanto não há motivo para duplicar esse trabalho.

### `4.`

Por que recebo 00-00-00-00-00-00 em vez de um endereço MAC quando varro uma máquina Samba?

R: Porque é isso que o Samba envia em resposta à consulta. Nbtscan apenas imprime o que recebe.

<a id="author"></a>
## AUTOR

NBTscan foi criado por Alla Bezroutchko <alla@inetcat.org>. Atualmente é mantido por alguns voluntários em https://github.com/resurrecting-open-source-projects/nbtscan

Esta página de manual foi escrita inicialmente por Ryszard Lach <rla@debian.org> e reescrita do zero por Joao Eriberto Mota Filho <eriberto@debian.org> para o sistema Debian GNU/Linux (mas pode ser usada por outros).


---

## Procedência desta tradução

Fonte primária: [manual preservado](../../../sources/upstream/nbtscan/nbtscan.1.source), extraído de `/usr/share/man/man1/nbtscan.1.gz`. Pacote `nbtscan`, versão `1.7.2-3`; pacote-fonte `nbtscan`, versão `1.7.2-3`. Aquisição de pacote instalado, sem atribuição de commit Git.

Licença: [GPL-2.0-or-later](../../99-Assets/upstream/nbtscan/LICENSE.txt); [copyright e condições do pacote](../../99-Assets/upstream/nbtscan/COPYRIGHT.package.txt). [Página de referência do pacote, não a origem exata do arquivo](https://github.com/resurrecting-open-source-projects/nbtscan). Hashes do original, gzip e avisos no registro de fontes. A data do manual é histórica; não implica que todos os serviços externos mantenham esse comportamento.
