---
title: "aflplusplus — documentação oficial"
type: "official-documentation"
tool: "aflplusplus"
status: "translated-machine"
reviewed: "2026-10-26"
language: "pt-BR"
tags: ["documentation", "tool/aflplusplus"]
cssclasses: ["fieldbook"]
source_url: "https://github.com/AFLplusplus/AFLplusplus/blob/d0070729206a80a9af297b2341edd63f68fdac35/docs/afl-fuzz_approach.md"
source_commit: "d0070729206a80a9af297b2341edd63f68fdac35"
source_sha256: "ae8fd56c1e27c993be8ff88e412871e6881e91709bc64f8f19097fe81028eb10"
license_spdx: "AGPL-3.0-or-later"
human_review: "pending"
source_scope: "Repository root README and owned doc/docs/documentation Markdown or RST files; not a claim of full wiki/site coverage"
---

> Tradução automática local para português, ainda sem revisão humana integral. Estrutura e blocos de código preservados; referências externas não significam conteúdo espelhado.

# The afl-fuzz approach

AFL++ é um fuzzer de força bruta acoplado a um extremamente simples, mas sólido em rocha
algoritmo genético guiado por instrumentação. Ele usa uma forma modificada de borda
cobertura para sem esforço pegar mudanças sutis em escala local para o controle do programa
Fluxo.

Nota: Se você está interessado em um mergulho profundo mais atual atual como AFL++
funciona então recomendamos este post do blog:
[https://blog.ritsec.club/posts/afl-under-hood/](https://blog.ritsec.club/posts/afl-under-hood/)

Simplificando um pouco, o algoritmo geral pode ser resumido como:

1) Carregar os casos de teste iniciais fornecidos pelo usuário na fila.

2) Pegue o próximo arquivo de entrada da fila.

3) Tentar aparar o caso de teste para o menor tamanho que não altera o
comportamento medido do programa.

4) Mutar repetidamente o arquivo usando uma variedade equilibrada e bem pesquisada de
estratégias tradicionais fuzzing.

5) Se alguma das mutações geradas resultou numa nova transição de estado registada
pela instrumentação, adicione o resultado mutado como uma nova entrada na fila.

6) Go a 2.

Os casos de teste descobertos também são periodicamente cortados para eliminar aqueles que
foram obsoletas por descobertas mais recentes e de maior cobertura; e passaram por várias outras
Passos de minimização do esforço orientado para instrumentação.

Como resultado lateral do processo fuzzing, a ferramenta cria um pequeno,
corpus auto-contido de casos de teste interessantes. Estes são extremamente úteis para
outros regimes de teste intensivos em trabalho ou recursos - por exemplo, para
navegadores de teste de stress, aplicações de escritório, suites gráficas ou código fechado
Ferramentas.

O fuzzer é cuidadosamente testado para fornecer desempenho fora da caixa de longe
superior a fuzzing cego ou apenas ferramentas de cobertura.

<a id="understanding-the-status-screen"></a>
## Compreender a tela de status

Esta seção fornece uma visão geral da tela de status - mais dicas para
Resolução de problemas de avisos e texto vermelho mostrados na UI.

Para o manual geral de instruções, consulte [README.md](aflplusplus-docs-readme-md.md).

<a id="a-note-about-colors"></a>
### Uma nota sobre as cores

A tela de status e as mensagens de erro usam cores para manter as coisas legíveis e
atrair sua atenção para os detalhes mais importantes.
significa sempre "consultar este doc" :-)

Infelizmente, a UI só irá renderizar corretamente se o seu terminal estiver usando
paleta tradicional un* x (texto branco no fundo preto) ou algo próximo
Isso.

Se você estiver usando vídeo inverso, você pode querer alterar suas configurações, diga:

- Para o Terminal GNOME, vá para as preferências `Edit > Profile`, selecione as "colores"
tab, e a partir da lista de esquemas embutidos, escolha "branco no preto".
- Para o aplicativo MacOS X Terminal, abra uma nova janela usando o esquema "Pro" via
Menu `Shell > New Window` (ou faça "Pro" o seu padrão).

Alternativamente, se você realmente gosta de suas cores atuais, você pode editar config.h para
Comente fora USO_COLORS, em seguida, faça `make clean all`.

Não estamos cientes de qualquer outra maneira simples de fazer este trabalho sem causar outros
efeitos colaterais - desculpe por isso.

Com isso fora do caminho, vamos falar sobre o que está realmente no tela...

<a id="the-status-bar"></a>
### A barra de status

```text
american fuzzy lop ++3.01a (default) [fast] {0}
```

A linha superior mostra em que modo o afl-fuzz está a correr (normal: "americano
fuzzy lop", modo de exploração de crash: "modo coelho peruano") e a versão de
AFL++. Ao lado da versão está o banner, que, se não for definido com - T à mão,
mostrará o nome binário sendo fuzzed, ou o nome principal -M/-S/secundário
para fuzzing paralelo. Segundo para o último é o modo de programação de energia a ser executado
(padrão: rápido). Finalmente, o último item é o ID da CPU.

<a id="process-timing"></a>
### Temporização do processo

```text
  +----------------------------------------------------+
  |        run time : 0 days, 8 hrs, 32 min, 43 sec    |
  |   last new find : 0 days, 0 hrs, 6 min, 40 sec     |
  | last uniq crash : none seen yet                    |
  |  last uniq hang : 0 days, 1 hrs, 24 min, 32 sec    |
  +----------------------------------------------------+
```

Esta secção é bastante auto-explicativa: diz-lhe quanto tempo o fuzzer tem
tem estado em execução e quanto tempo se passou desde as suas descobertas mais recentes.
dividido em "caminhos" (uma abreviação para casos de teste que desencadeiam nova execução
padrões), quebras, e enforcamentos.

Quando se trata de tempo: não há regra difícil, mas a maioria dos trabalhos fuzzing deve ser
Prevê-se que funcione durante dias ou semanas; de facto, para um projecto de moderada complexidade,
o primeiro passe provavelmente levará um dia ou assim. De vez em quando, alguns trabalhos
Serão autorizados a correr durante meses.

Há uma coisa importante para se ter cuidado: se a ferramenta não está encontrando novo
caminhos dentro de vários minutos do início, você provavelmente não está invocando o
alvo binário corretamente e ele nunca começa a analisar os arquivos de entrada que são
lançado nele; outras explicações possíveis são que o limite de memória padrão
(`-m`) é muito restritivo e o programa sai após não alocar um
buffer muito cedo; ou que os arquivos de entrada são manifestamente inválidos e sempre
falhou uma verificação básica do cabeçalho.

Se não houver novos caminhos aparecendo por um tempo, você vai eventualmente ver um grande
alerta vermelho nesta seção, também :-)

<a id="overall-results"></a>
### Resultados globais

```text
  +-----------------------+
  |  cycles done : 0      |
  |  total paths : 2095   |
  | uniq crashes : 0      |
  |   uniq hangs : 19     |
  +-----------------------+
```

O primeiro campo nesta seção lhe dá a contagem de passes de fila feitos até agora
- ou seja, o número de vezes que o fuzzer passou por todo o teste interessante
Casos descobertos até agora, fuzzed-los, e voltou ao início.
Cada sessão do fuzzing deve ser autorizada a completar pelo menos um ciclo; e
idealmente, deve correr muito mais tempo do que isso.

Como observado anteriormente, a primeira passagem pode levar um dia ou mais, por isso sente-se e
Relaxa.

Para ajudar a fazer a chamada em quando bater `Ctrl-C`, o contador de ciclo é codificado em cores.
É mostrado em magenta durante a primeira passagem, progride para amarelo se novos achados
ainda estão sendo feitas em rodadas subsequentes, em seguida, azul quando isso termina - e
finalmente, fica verde depois que o fuzzer não tem visto nenhuma ação por mais tempo
Enquanto isso.

Os campos restantes nesta parte da tela devem ser bastante óbvios:
há o número de casos de teste ("caminhos") descobertos até agora, e o número de
falhas únicas. Os casos de teste, quebras e travas podem ser explorados em tempo real
navegando no diretório de saída, veja
[#interpretação-saída](#interpretar-o-resultado).

<a id="cycle-progress"></a>
### Progresso do ciclo

```text
  +-------------------------------------+
  |  now processing : 1296 (61.86%)     |
  | paths timed out : 0 (0.00%)         |
  +-------------------------------------+
```

Esta caixa diz- lhe a que distância está o fuzzer com o ciclo da fila actual:
mostra o ID do caso de teste em que está actualmente a trabalhar, mais o número de
inputs decidiu abandonar porque eles eram persistentemente timing out.

O sufixo "*" às vezes mostrado na primeira linha significa que o
o caminho processado não é "favorecido" (uma propriedade discutida mais tarde).

<a id="map-coverage"></a>
### Cobertura do mapa

```text
  +--------------------------------------+
  |    map density : 10.15% / 29.07%     |
  | count coverage : 4.03 bits/tuple     |
  +--------------------------------------+
```

A secção fornece algumas perguntas sobre a cobertura observada pelo
instrumentação incorporada no binário alvo.

A primeira linha na caixa diz-lhe quantas tuplas de ramo já foram atingidas, em
proporção com o quanto o mapa de bits pode manter. O número à esquerda descreve o
entrada atual; a entrada à direita é o valor para todo o corpus de entrada.

Cuidado com os extremos:

- Números absolutos abaixo de 200 mais ou menos sugerem uma de três coisas: que o programa
é extremamente simples; que não é instrumentado corretamente (por exemplo, devido a ser
ligado a uma cópia não-instrumentada da biblioteca alvo); ou que seja
Saindo prematuramente em seus casos de teste de entrada. O fuzzer tentará marcar
Isto em rosa, só para que saibas.
- Percentagens acima de 70% podem muito raramente acontecer com programas muito complexos que
fazer uso pesado do código gerado por modelos. Porque a alta densidade de bitmap faz
é mais difícil para o fuzzer discernir de forma confiável novos estados do programa, recomendamos
recompilando o binário com `AFL_INST_RATIO=10` ou assim e tentando novamente (ver
[env_variables.md](aflplusplus-docs-env-variables-md.md)). O fuzzer assinalará percentagens elevadas
no vermelho. As chances são, você nunca verá que a menos que você é fuzzing extremamente
software peludo (por exemplo, v8, perl, ffmpeg).

A outra linha lida com a variabilidade nas contagens de pancadas tuplas vistas no
binário. Em essência, se cada ramo tomado é sempre tomado um número fixo de
vezes para todas as entradas que foram tentados, isso vai ler `1.00`.
gatilho outras contagens de hit para cada ramo, a agulha começará a mover- se para
`8.00` (cada pedaço no mapa de 8 bits atingido), mas provavelmente nunca alcançará isso
Extremo.

Em conjunto, os valores podem ser úteis para comparar a cobertura de vários
diferentes tarefas fuzzing que dependem do mesmo binário instrumentado.

<a id="stage-progress"></a>
### Progresso da fase

```text
  +-------------------------------------+
  |  now trying : interest 32/8         |
  | stage execs : 3996/34.4k (11.62%)   |
  | total execs : 27.4M                 |
  |  exec speed : 891.7/sec             |
  +-------------------------------------+
```

Esta parte dá-lhe uma olhada em profundidade no que o fuzzer está realmente fazendo direito
Agora. Ele fala sobre o estágio atual, que pode ser qualquer um de:

- calibração - uma fase pré-fuzzing onde o caminho de execução é examinado para
detectar anomalias, estabelecer a velocidade de execução de base, e assim por diante.
breve sempre que uma nova descoberta está a ser feita.
- aparar L/S - outra fase pré-fuzzing onde o caso de teste é aparado para o
forma mais curta que ainda produz o mesmo caminho de execução. O comprimento (L) e
stepover (S) são escolhidos em relação geral ao tamanho do arquivo.
- bitflip L/S - flips de bits determinísticos. Existem bits L alternados em qualquer dado
tempo, percorrendo o arquivo de entrada com incrementos de S-bit. As variantes L/S atuais
são: `1/1`, `2/1`, `4/1`, `8/8`, `16/8`, `32/8`.
- arith L/8 - aritmética determinística. O fuzzer tenta subtrair ou adicionar
pequenos números inteiros para valores de 8-, 16- e 32-bit. O passover é sempre de 8 bits.
- interesse L/8 - valor determinístico sobrescrever. O fuzzer tem uma lista de conhecidos
"interessante" 8-, 16-, e 32-bit valores para tentar. O stepover é 8 bits.
- extras - injeção determinística dos termos do dicionário. Isto pode ser mostrado como
"usuário" ou "auto", dependendo se o fuzzer está usando um usuário fornecido
dicionário (`-x`) ou um criado automaticamente. Você também verá " acima" ou
"inserir", dependendo se as palavras do dicionário sobrescrever dados existentes ou
são inseridos compensando os restantes dados para acomodar o seu comprimento.
- caos - uma espécie de ciclo de comprimento fixo com ajustes aleatórios empilhados.
as operações tentadas durante esta fase incluem bit flips, sobrescritas com
inteiros aleatórios e "interessantes", exclusão de blocos, duplicação de blocos, mais
operações relacionadas com o dicionário (se um dicionário for fornecido no
primeiro lugar).
- splice - uma estratégia de último recurso que inicia após o primeiro ciclo completo da fila
sem novos caminhos. É equivalente a 'havoc', exceto que ele primeiro splices
em conjunto duas entradas aleatórias da fila em alguns arbitrariamente selecionados
Ponto médio.
- sync - uma fase usada apenas quando `-M` ou `-S` estiver definida (ver
[fuzzing_in_profund.md:3c) Usando vários núcleos](aflplusplus-docs-fuzzing-in-depth-md.md#c-using-multiple-cores)).
Nenhum fuzzing real está envolvido, mas a ferramenta verifica a saída de outros fuzzers
A primeira vez que isto é feito, pode levar
alguns minutos, mais ou menos.

Os campos restantes devem ser bastante evidentes: há a contagem executiva
indicador de progresso para a fase actual, um contador executivo global e um índice de referência
para a velocidade de execução atual do programa. Isto pode variar a partir de um caso de teste
para outro, mas o índice de referência deve ser idealmente mais de 500 executivos/seg a maior parte dos
tempo - e se ficar abaixo de 100, o trabalho provavelmente vai demorar muito tempo.

O fuzzer irá avisá-lo explicitamente sobre alvos lentos, também. Se isto acontecer,
ver [best_práticas.md#melhorar a velocidade](aflplusplus-docs-best-practices-md.md#improving-speed)
para ideias sobre como acelerar as coisas.

<a id="findings-in-depth"></a>
### Resultados em profundidade

```text
  +--------------------------------------+
  | favored paths : 879 (41.96%)         |
  |  new edges on : 423 (20.19%)         |
  | total crashes : 0 (0 unique)         |
  |  total tmouts : 24 (19 unique)       |
  +--------------------------------------+
```

Isso lhe dá várias métricas que são de interesse principalmente para completar nerds.
A seção inclui o número de caminhos que o fuzzer mais gosta com base em
um algoritmo de minimização colocado no código (estes obterão consideravelmente mais
tempo de ar), e o número de casos de teste que realmente resultou em melhor borda
cobertura (contra apenas empurrando os contadores de hit branch para cima). Existem também
adicional, contadores mais detalhados para quebras e timeouts.

Note que o contador de tempo- limite é um pouco diferente do contador de tempo- limite; este
um inclui todos os casos de teste que excederam o tempo- limite, mesmo que não
Exceda-a por uma margem suficiente para ser classificada como enforcamento.

<a id="fuzzing-strategy-yields"></a>
### Rendimentos da estratégia fuzzing

```text
  +-----------------------------------------------------+
  |   bit flips : 57/289k, 18/289k, 18/288k             |
  |  byte flips : 0/36.2k, 4/35.7k, 7/34.6k             |
  | arithmetics : 53/2.54M, 0/537k, 0/55.2k             |
  |  known ints : 8/322k, 12/1.32M, 10/1.70M            |
  |  dictionary : 9/52k, 1/53k, 1/24k                   |
  |havoc/splice : 1903/20.0M, 0/0                       |
  |py/custom/rq : unused, 53/2.54M, unused              |
  |    trim/eff : 20.31%/9201, 17.05%                   |
  +-----------------------------------------------------+
```

Esta é apenas mais uma secção orientada para os nerds a controlar quantos caminhos estavam
líquido, proporcionalmente ao número de executivos tentados, para cada um dos fuzzing
as estratégias discutidas anteriormente, o que serve para validar de forma convincente
pressupostos sobre a utilidade das várias abordagens tomadas pela afl-fuzz.

As estatísticas de estratégia de aparar nesta seção são um pouco diferentes do que o resto.
o primeiro número nesta linha mostra a proporção de bytes removidos dos arquivos de entrada;
o segundo corresponde ao número de executivos necessários para atingir esse objetivo.
Finalmente, o terceiro número mostra a proporção de bytes que, embora não
possível de remover, foram considerados não ter efeito e foram excluídos de alguns dos
os passos determinísticos mais caros fuzzing.

Note que quando o modo determinístico de mutação está desligado (que é o padrão porque
não é muito eficiente) as cinco primeiras linhas exibem "desactivado (padrão,
habilitar com -D)".

Somente o que é ativado terá mostrado o contador.

<a id="path-geometry"></a>
### Geometria do caminho

```text
  +---------------------+
  |    levels : 5       |
  |   pending : 1570    |
  |  pend fav : 583     |
  | own finds : 0       |
  |  imported : 0       |
  | stability : 100.00% |
  +---------------------+
```

O primeiro campo nesta seção rastreia a profundidade do caminho alcançado através do guiado
Processo fuzzing. Em essência: os casos de teste iniciais fornecidos pelo usuário são
considerados "nível 1". Os casos de teste que podem ser derivados disso através
fuzzing tradicional são considerados "nível 2"; os derivados usando estes como
entradas para rodadas fuzzing subsequentes são "nível 3"; e assim por diante.
profundidade é, portanto, um proxy áspero para quanto valor você está recebendo fora do
Abordagem orientada para a instrumentação adoptada pelo afl-fuzz.

O campo seguinte mostra o número de entradas que não passaram por nenhuma
fuzzing ainda. A mesma estatística também é dada para os itens "favorecidos" que o fuzzer
realmente quer chegar a este ciclo de fila (os itens não favoritos podem ter que
esperar um par de ciclos para ter a sua oportunidade).

Próximo é o número de novos caminhos encontrados durante esta seção fuzzing e importados
de outras instâncias fuzzer ao fazer fuzzing paralelizado; e a extensão a
que entradas idênticas parecem às vezes produzir comportamento variável na
binário testado.

Esta última parte é, na verdade, bastante interessante: mede a coerência de
traços observados. Se um programa se comportar sempre do mesmo modo para os mesmos dados de entrada,
ele vai ganhar uma pontuação de 100%. Quando o valor é menor, mas ainda mostrado em roxo,
o processo fuzzing é improvável ser afetado negativamente. Se ele entra em vermelho,
você pode estar em apuros, uma vez que AFL++ terá dificuldade em discernir entre
efeitos significativos e "fantom" de ajustar o arquivo de entrada.

Agora, a maioria dos alvos vai ter uma pontuação de 100%, mas quando você vê números mais baixos,
há várias coisas para ver:

- O uso da memória não inicializada em conjunto com algumas fontes intrínsecas de
entropia no binário testado. Inofensiva para AFL, mas poderia ser indicativo de uma
Insecto de segurança.
- Tenta manipular recursos persistentes, como arquivos temporários
ou objetos de memória compartilhados. Isto geralmente é inofensivo, mas você pode querer
Verifique novamente para ter certeza de que o programa não está a sair prematuramente.
fora do espaço em disco, manipula SHM, ou outros recursos globais podem desencadear isso,
Também.
- Bater em alguma funcionalidade que é realmente projetada para se comportar aleatoriamente.
Geralmente inofensivo. Por exemplo, quando fuzzing sqlite, uma entrada como `select
random();` irá desencadear um caminho de execução variável.
- Múltiplos threads que executam de uma só vez em ordem semi- aleatória. Isto é inofensivo quando
a métrica 'estabilidade' permanece acima de 90% ou mais, mas pode se tornar um problema se não.
Aqui está o que tentar:
  * Use afl-clang-fast de [instrumentação](https://github.com/AFLplusplus/AFLplusplus/blob/d0070729206a80a9af297b2341edd63f68fdac35/instrumentation) - ele usa um
    thread-local tracking model that is less prone to concurrency issues,
  * Veja se o alvo pode ser compilado ou executado sem threads.
    `./configure` options include `--without-threads`, `--disable-pthreads`, or
    `--disable-openmp`.
  * Substituir pthreads pelo GNU Pth (https://www.gnu.org/software/pth/), que
    allows you to use a deterministic scheduler.
- No modo persistente, pequenas gotas na métrica de "estabilidade" podem ser normais,
porque nem todo o código se comporta de forma idêntica quando reentrada; mas as principais diferenças
pode significar que o código dentro de `__AFL_LOOP()` não está se comportando corretamente em
iterações subsequentes (por exemplo, devido a limpeza incompleta ou reinici
o estado) e que a maioria do esforço fuzzing vai para o lixo.

<a id="cpu-load"></a>
### Carregamento da CPU

```text
  [cpu: 25%]
```

Este pequeno elemento mostra a utilização aparente da CPU no sistema local. É
calculado tomando o número de processos no estado "runnable", e então
comparando-o com o número de núcleos lógicos no sistema.

Se o valor é mostrado em verde, você está usando menos núcleos de CPU do que disponível em
seu sistema e pode provavelmente paralelizar para melhorar o desempenho; para dicas sobre como
para fazer isso, veja
[fuzzing_in_profund.md:3c) Usando vários núcleos](aflplusplus-docs-fuzzing-in-depth-md.md#c-using-multiple-cores).

Se o valor é mostrado em vermelho, sua CPU é *possibly* sobreassinado, e executando
Fuzzers adicionais podem não lhe dar quaisquer benefícios.

Claro, este benchmark é muito simplista; ele diz-lhe quantos processos
estão prontos para correr, mas não como eles podem estar com fome de recursos.
distinguir entre núcleos físicos, núcleos lógicos e CPUs virtualizados;
características de desempenho de cada um destes irá diferir bastante.

Se você quiser uma medição mais precisa, você pode executar o utilitário `afl-gotcpu`
da linha de comando.

<a id="interpreting-output"></a>
## Interpretar o resultado

Ver [# Entendendo-o-estrato-tela](#compreender-a-tela-de-status) para
informações sobre como interpretar as estatísticas exibidas e monitorar a saúde de
o processo. Certifique-se de consultar este arquivo especialmente se quaisquer elementos de UI são
destacado em vermelho.

O processo fuzzing continuará até que você pressione Ctrl-C. No mínimo, você deseja
para permitir que o fuzzer para pelo menos um ciclo de fila sem novas descobertas, que pode
Levar de umas duas horas a uma semana ou mais.

Existem três subdiretórios criados dentro do diretório de saída e atualizados
em tempo real:

- fila/ - casos de teste para cada caminho de execução distintivo, mais todos os
             starting files given by the user. This is the synthesized corpus.

             Before using this corpus for any other purposes, you can shrink
             it to a smaller size using the afl-cmin tool. The tool will find
             a smaller subset of files offering equivalent edge coverage.

- quebras / - casos de teste únicos que fazem com que o programa testado receba uma fatal
             signal (e.g., SIGSEGV, SIGILL, SIGABRT). The entries are grouped by
             the received signal.

- pendura/ - casos de teste únicos que fazem com que o programa testado cronometre.
             default time limit before something is classified as a hang is the
             larger of 1 second and the value of the -t parameter. The value can
             be fine-tuned by setting AFL_HANG_TMOUT, but this is rarely
             necessary.

Acidentes e enforcamentos são considerados "únicos" se os caminhos de execução associados
envolver quaisquer transições de estado não vistas em falhas previamente gravadas.
um único erro pode ser alcançado de várias maneiras, haverá alguma inflação de contagem
no início do processo, mas isto deve diminuir rapidamente.

Os nomes dos arquivos para falhas e falhas estão correlacionados com o pai,
entradas de fila não- falhas. Isto deverá ajudar na depuração.

<a id="visualizing"></a>
## Visualizando

Se você tem gnuplot instalado, você também pode gerar alguns gráficos bonitos para qualquer
tarefa fuzzing ativa usando afl-plot. Para um exemplo de como isso se parece, veja
[https://lcamtuf.coredump.cx/afl/plot/](https://lcamtuf.coredump.cx/afl/plot/).

Você também pode construir e instalar manualmente afl-plot-ui, que é um utilitário auxiliar
para mostrar os gráficos gerados pelo afl-plot em uma janela gráfica usando GTK.
Você pode compilá-lo e instalá-lo como segue:

```shell
sudo apt install libgtk-3-0 libgtk-3-dev pkg-config
cd utils/plot_ui
make
cd ../../
sudo make install
```

Para saber mais sobre monitoramento remoto e visualização de métricas com o StatsD, consulte
[rpc_statsd.md](aflplusplus-docs-rpc-statsd-md.md).

<a id="addendum-status-and-plot-files"></a>
### Addendum: status e plot files

Para a operação sem vigilância, algumas das informações da tela de status da chave também podem ser
encontrado em um formato legível por máquina no arquivo fuzzer_stats na saída
diretório. Isto inclui:

- `start_time` - tempo unix indicando a hora inicial do afl-fuzz
- `last_update` - unix time correspondente à última atualização deste arquivo
- `run_time` - tempo de execução em segundos para a última atualização deste arquivo
- `fuzzer_pid` - PID do processo fuzzer
- `cycles_done` - ciclos de fila concluídos até agora
- `cycles_wo_finds` - número de ciclos sem novos caminhos encontrados
- `time_wo_finds` - maior tempo em segundos nenhum novo caminho foi encontrado
- `fuzz_time` - tempo em segundos gasto na verdade fuzzing (run_time menos calibração, cmplog, sincronização, aparamento e construção de tabelas)
- `calibration_time` - tempo cumulativo em segundos gasto calibrando casos de teste
- `cmplog_time` - tempo cumulativo em segundos passados no estágio cmplog/redqueen
- `cmplog_tightness` - não- zero se o escalonamento de aperto do cmplog estiver ativado (`-l` com `M`)
- `cmplog_tight_new` - número de entradas na fila que produziram um novo resultado de aperto do cmplog
- `cmplog_size_derive`- não- zero se a derivação do tamanho do operando do cmplog estiver activada (`-l` com `Z`)
- `sync_time` - tempo cumulativo em segundos gasto sincronizando com outras instâncias fuzzer
- `trim_time` - tempo cumulativo em segundos gastos aparando casos de teste
- `table_time` - tempo acumulado em segundos gasto construindo a tabela de agendamento alias
- `execs_done` - número de chamadas executivas () tentadas
- `execs_per_sec` - número total de executivos por segundo
- `execs_ps_last_min` - número de executivos por segundo, em média no último minuto
- `corpus_count` - número total de entradas na fila
- `corpus_favored` - número de entradas de fila que são favorecidas
- `corpus_found` - número de entradas descobertas através do fuzzing local
- `corpus_imported` - número de entradas importadas de outras instâncias
- `max_depth` - número de níveis no conjunto de dados gerados
- `cur_item` - número de entrada atualmente processado
- `pending_favs` - número de entradas favoritas ainda esperando para ser fuzzed
- `pending_total` - número de todas as entradas à espera de serem fuzzed
- `corpus_variable` - número de casos de teste mostrando comportamento variável
- `stability` - porcentagem de bytes de bitmap que se comportam de forma consistente
- `bitmap_cvg` - porcentagem de cobertura de borda encontrada no mapa até agora
- `saved_crashes` - número de falhas únicas gravadas
- `saved_hangs` - número de travas únicas encontradas
- `total_tmout` - número total de casos de teste que cronometraram
- `last_find` - segundos desde que a última descoberta foi encontrada
- `last_crash` - segundos desde que o último acidente foi encontrado
- `last_hang` - segundos desde que o último enforcamento foi encontrado
- `execs_since_crash` - executivos desde que o último acidente foi encontrado
- `last_edge_execs` - número de execuções totais realizadas quando a última nova borda foi encontrada
- `last_edge_find` - segundos desde que a última borda foi encontrada
- `exec_timeout` - o valor da linha de comando - t
- `slowest_exec_ms` - tempo de execução do caso de teste mais lento, medido durante a calibração, em ms
- `peak_rss_mb` - uso máximo de rss alcançado durante fuzzing em MB
- `cpu_affinity` - núcleo da CPU para o fuzzer está ligado, ou -1 se não estiver ligado
- `edges_found` - quantas arestas foram encontradas
- `total_edges` - número total de arestas no mapa de cobertura
- `var_byte_count` - quantas arestas não são determinísticas
- `havoc_expansion` - nível atual de expansão de estragos (aumentou enquanto nenhuma nova cobertura é encontrada)
- `auto_dict_entries` - número de entradas de dicionário geradas automaticamente
- `testcache_size` - tamanho do cache do caso de teste em bytes
- `testcache_count` - número de casos de teste atualmente mantidos na cache
- `testcache_evict` - número de despejos de cache de casos de teste até agora
- `testcache_hits` - respostas do cache do caso de teste (o buffer já estava residente)
- `testcache_misses` - falta o cache do caso de teste (o buffer tinha de ser lido)
- `afl_banner` - texto do banner (por exemplo, o nome do alvo)
- `afl_version` - a versão do AFL++ usada
- `target_mode` - padrão, persistente, qemu, unicórnio, não instrumentado
- `command_line` - linha de comando completa usada para a sessão fuzzing

Entradas adicionais aparecem apenas em modos específicos: `extra_binary` e
`total_execs` são emitidos uma vez por binário de higienizador extra (`-b` / `AFL_SAN_*`),
dando o caminho de cada binário e sua própria contagem de execução; `virgin_bytes` e
`var_bytes` são emitidos apenas quando `AFL_DEBUG` é definido (lixos de cobertura brutos).

`last_edge_execs` suporta os interruptores de estratégia baseados na execução-contagem: uma vez que o
o conjunto de sementes favorecido/cobrindo está esgotado (`pending_favs` atinge 0), permanecendo preso
para um número plano de execuções sem nenhuma nova edge drives todos os três --
forçando o estágio de entrada para o estado do CmpLog primeiro, em seguida, modo de fome,
explore -> explore switch (`-P`), aumentando os limiares de execução.
explorar -> explore switch também dispara após o tempo `-P` se um foi dado,
O que vier primeiro.

A maioria destes mapas diretamente para os elementos da IU discutidos anteriormente.

Além disso, você também pode encontrar uma entrada chamada `plot_data`, contendo um
histórico do plotable para a maioria destes campos. Se tiver o gnuplot instalado, você
pode transformar isso em um bom relatório de progresso com a ferramenta `afl-plot` incluído.

A ferramenta `afl-health` lê estes arquivos `fuzzer_stats` e `plot_data` para você
e transforma-os em um veredicto de campanha, uma tendência, e classificação, conselho accionável -
local ou sobre ssh. Veja
[fuzzing_in_profundish.md](aflplusplus-docs-fuzzing-in-depth-md.md#e-the-status-of-the-fuzz-campaign).

<a id="addendum-automatically-sending-metrics-with-statsd"></a>
### Addendum: enviando automaticamente as métricas com StatsD

Em um ambiente CI ou ao executar vários fuzzers, pode ser tedioso registrar
em cada um deles ou implementar scripts para ler as estatísticas fuzzer.
`AFL_STATSD` (e as outras variáveis de ambiente relacionadas `AFL_STATSD_HOST`,
`AFL_STATSD_PORT`, `AFL_STATSD_TAGS_FLAVOR`) você pode enviar automaticamente métricas
para o seu servidor StatsD favorito. Dependendo do seu servidor StatsD, você será
capaz de monitorar, acionar alertas ou executar ações com base nessas métricas
(p. ex.: alerta para os executivos lentos para uma nova construção, limiar de quebras, tempo desde
última falha > X, etc.).

As métricas selecionadas são um subconjunto de todas as métricas encontradas no status e em
o arquivo de gráfico. A lista é a seguinte: `cycle_done`, `cycles_wo_finds`,
`execs_done`,`execs_per_sec`,`corpus_count`,`corpus_favored`,`corpus_found`,
`corpus_imported`, `max_depth`, `cur_item`, `pending_favs`, `pending_total`,
`corpus_variable`, `saved_crashes`, `saved_hangs`, `total_crashes`,
`slowest_exec_ms`, `edges_found`, `var_byte_count`, `havoc_expansion`.
definições podem ser encontradas na adenda acima.

Ao usar várias instâncias fuzzer com StatsD, é recomendado *strongly*
para configurar o sabor (`AFL_STATSD_TAGS_FLAVOR`) para corresponder ao seu servidor StatsD. Isto
permitirá que você veja o desempenho individual fuzzer, detectar os ruins, ver o
progresso de cada estratégia...

---

## Procedência desta tradução

Fonte: [https://github.com/AFLplusplus/AFLplusplus](https://github.com/AFLplusplus/AFLplusplus/blob/d0070729206a80a9af297b2341edd63f68fdac35/docs/afl-fuzz_approach.md). Licença: [AGPL-3.0-or-later](../../99-Assets/upstream/aflplusplus/LICENSE.txt). Commit: d0070729206a80a9af297b2341edd63f68fdac35.

O original preservado, a lista de mudanças de apresentação e os hashes constam no manifesto do projeto. Nenhum exemplo desta documentação foi executado automaticamente.
