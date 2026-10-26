<!-- SPDX-License-Identifier: LicenseRef-Fping-Stanford-Variant -->
> **Reconhecimento da licença:** This software was developed by Stanford University.

# fping

## NOME

fping - envia pacotes ICMP ECHO_REQUEST a hosts de rede

## SINOPSE

```text
fping [ options ] [ systems... ]
```

## DESCRIÇÃO

fping é um programa semelhante ao ping que usa solicitações echo do Internet Control Message Protocol (ICMP) para determinar se um host-alvo está respondendo. Ele difere do ping por permitir qualquer quantidade de alvos na linha de comando ou um arquivo com listas de alvos. Em vez de enviar a um alvo até ele responder ou esgotar o tempo, o fping envia um pacote e passa ao próximo alvo, em rodízio (round-robin). No modo padrão, se um alvo responde, isso é registrado e ele é removido da lista a verificar; se não responde dentro dos limites de tempo e/ou tentativas, é marcado como inacessível. fping também permite enviar um número especificado de pings a um alvo ou repetir indefinidamente, como o ping. Diferentemente do ping, destina-se ao uso em scripts, por isso sua saída é projetada para facilitar a análise. Estatísticas atuais podem ser obtidas sem encerrar o processo, usando o sinal `SIGQUIT` (`^\` no teclado da maioria dos sistemas).

## OPÇÕES

### `-4, --ipv4`

Restringe a resolução de nomes e os IPs a endereços IPv4.

### `-6, --ipv6`

Restringe a resolução de nomes e os IPs a endereços IPv6.

### `-a, --alive`

Mostra os sistemas que estão ativos.

### `-A, --addr`

Exibe os alvos por endereço em vez do nome DNS. Combinada com `-d`, a saída conterá o IP e, quando disponível, o nome do host.

### `-b, --size=BYTES`

Número de bytes de dados do ping a enviar. O tamanho mínimo (normalmente 12) reserva espaço para o que o fping precisa para funcionar: número de sequência e marca temporal. O tamanho de dados recebidos informado inclui o cabeçalho IP (normalmente 20 bytes) e o cabeçalho ICMP (8 bytes), portanto o tamanho total mínimo é 40 bytes. O padrão é 56, como no ping. O máximo é o tamanho máximo teórico de um datagrama IP (64K), embora a maioria dos sistemas limite isso a um número menor, dependente do sistema.

### `-B, --backoff=N`

Fator de backoff. No modo padrão, o fping envia várias solicitações a um alvo antes de desistir, aguardando mais tempo pela resposta a cada nova solicitação. Este parâmetro é o valor pelo qual o tempo de espera (`-t`) é multiplicado em cada solicitação sucessiva; deve ser informado como número de ponto flutuante (x.y). O padrão é 1.5.

### `-c, --count=N`

Número de pacotes de solicitação a enviar para cada alvo. Neste modo, é exibida uma linha para cada resposta recebida (isso pode ser suprimido com `-q` ou `-Q`). As estatísticas de respostas de cada alvo também são exibidas quando todas as solicitações foram enviadas ou quando a execução é interrompida.

### `-C, --vcount=N`

Semelhante a `-c`, mas as estatísticas de cada alvo são exibidas em um formato destinado à coleta automatizada de tempos de resposta. Por exemplo:

```text
 $ fping -C 5 -q somehost
 somehost : 91.7 37.0 29.2 - 36.8
```

Mostra o tempo de resposta em milissegundos de cada uma das cinco solicitações; o `-` indica que a quarta solicitação não recebeu resposta.

### `-d, --rdns`

Usa DNS para resolver o endereço do alvo de ping. Isso permite fornecer ao fping uma lista de IPs e imprimir nomes de hosts na saída. É semelhante a `-n`/`--name`, mas força uma consulta DNS reversa mesmo quando o alvo é fornecido como nome de host (`NAME->IP->NAME`).

### `-D, --timestamp`

Acrescenta marcas temporais Unix no início das linhas de saída geradas nos modos de repetição ou contagem (`-l`, `-c` ou `-C`).

### `-e, --elapsed`

Mostra o tempo decorrido (ida e volta) dos pacotes.

### `-f, --file`

Lê uma lista de alvos de um arquivo. Esta opção só pode ser usada pelo usuário root. Usuários comuns devem fornecer o arquivo pela entrada padrão, usando redirecionamento:

```text
 $ fping < targets_file
```

### `-g, --generate addr/mask`

Gera uma lista de alvos a partir de uma máscara de rede IP ou de um IP inicial e final. Especifique a máscara ou o início/fim na parte de alvos da linha de comando. Se for fornecida uma rede com máscara, os endereços de rede e broadcast serão excluídos. Por exemplo, para enviar ping à rede 192.168.1.0/24, a linha de comando pode ter uma destas formas:

```text
 $ fping -g 192.168.1.0/24
```

ou

```text
 $ fping -g 192.168.1.1 192.168.1.254
```

### `-h, --help`

Imprime a mensagem de uso.

### `-H, --ttl=N`

Define o campo TTL do IP (tempo de vida em saltos).

### `-i, --interval=MSEC`

Tempo mínimo, em milissegundos, entre o envio de um pacote de ping e o seguinte para qualquer alvo (padrão: 10; mínimo: 1).

### `-I, --iface=IFACE`

Define a interface (requer suporte a `SO_BINDTODEVICE`).

### `-l, --loop`

Repete indefinidamente o envio de pacotes a cada alvo. Pode ser interrompido com Ctrl-C; as estatísticas de respostas de cada alvo são então exibidas.

### `-m, --all`

Envia pings a cada um dos vários endereços IP de um host-alvo (recomenda-se usar `-A`).

### `-M, --dontfrag`

Define o bit "Don't Fragment" no cabeçalho IP (usado para determinar/testar a MTU).

### `-n, --name`

Se os alvos forem especificados como IPs, faz consultas DNS reversas para imprimir seus nomes na saída.

### `-N, --netdata`

Formata a saída para netdata (requer `-l -Q`). Veja: <http://my-netdata.io/>

### `-o, --outage`

Calcula o tempo de indisponibilidade ("outage time") com base no número de pings perdidos e no intervalo usado (útil em testes de convergência de rede).

### `-O, --tos=N`

Define o sinalizador de tipo de serviço (TOS). `N` pode estar no formato decimal ou hexadecimal (0xh).

### `-p, --period=MSEC`

Nos modos de repetição ou contagem (`-l`, `-c` ou `-C`), define o tempo, em milissegundos, que o fping aguarda entre pacotes sucessivos para um mesmo alvo. O padrão é 1000 e o mínimo é 10.

### `-q, --quiet`

Silencioso. Não mostra resultados de cada tentativa, apenas o resumo final. Também não mostra mensagens de erro ICMP.

### `-Q, --squiet=SECS`

Como `-q`, mas também mostra resumos de resultados a cada `SECS` segundos.

### `-r, --retry=N`

Limite de novas tentativas (padrão: 3). É o número de novas tentativas de ping a um alvo, sem incluir a primeira.

### `-R, --random`

Gera bytes aleatórios em vez de usar dados de pacote inteiramente zerados. Pode ser usado para impedir, por exemplo, a compressão de dados no enlace.

### `-s, --stats`

Imprime estatísticas acumuladas ao encerrar.

### `-S, --src=addr`

Define o endereço de origem.

### `-t, --timeout=MSEC`

Timeout inicial do alvo em milissegundos. No modo padrão, sem repetição contínua, o timeout padrão é 500 ms e representa quanto o fping aguarda pela resposta à primeira solicitação. Os timeouts seguintes são multiplicados pelo fator de backoff especificado em `-B`.

No modo de repetição/contagem, o timeout padrão é ajustado automaticamente ao valor de "period" (mas limitado a 2000 ms). Ainda é possível ajustá-lo com esta opção, mas definir um valor maior que "period" produz resultados inconsistentes, pois o timeout só pode ser respeitado para o último ping.

Respostas recebidas com tempo maior que o timeout serão descartadas.

### `-T n`

Ignorada (para compatibilidade com fping 2.4).

### `-u, --unreach`

Mostra os alvos inacessíveis.

### `-v, --version`

Imprime as informações de versão do fping.

### `-x, --reachable=N`

Com uma lista de hosts, verifica se o número de hosts acessíveis é >= N e, nesse caso, encerra com resultado verdadeiro.

## EXEMPLOS

Gera 20 pings para dois hosts em aproximadamente 1 segundo (um ping a cada 50 ms para cada host) e informa todos os RTTs ao final:

```text
 $ fping --quiet --interval=1 --vcount=20 --period=50 127.0.0.1 127.0.0.2
```

## AUTORES

- Roland J. Schemers III, Stanford University, conceito e versões 1.x

- RL "Bob" Morgan, Stanford University, versões 2.x

- David Papp, versões 2.3x e posteriores

- David Schweikert, versões 3.0 e posteriores

Site do fping: <http://www.fping.org>

## DIAGNÓSTICOS

O código de saída é 0 se todos os hosts forem acessíveis, 1 se alguns forem inacessíveis, 2 se algum endereço IP não for encontrado, 3 para argumentos inválidos de linha de comando e 4 para falha em uma chamada de sistema.

## RESTRIÇÕES

Se o fping tiver sido configurado com `--enable-safe-limits`, os seguintes valores não são permitidos a usuários que não sejam root:

- `-i n`, em que `n` < 1 ms

- `-p n`, em que `n` < 10 ms

## VEJA TAMBÉM

ping(8)
