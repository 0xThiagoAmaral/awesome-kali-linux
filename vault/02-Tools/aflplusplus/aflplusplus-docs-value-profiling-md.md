---
title: "aflplusplus — documentação oficial"
type: "official-documentation"
tool: "aflplusplus"
status: "translated-machine"
reviewed: "2026-10-26"
language: "pt-BR"
tags: ["documentation", "tool/aflplusplus"]
cssclasses: ["fieldbook"]
source_url: "https://github.com/AFLplusplus/AFLplusplus/blob/d0070729206a80a9af297b2341edd63f68fdac35/docs/value_profiling.md"
source_commit: "d0070729206a80a9af297b2341edd63f68fdac35"
source_sha256: "d202c8c5edb2488da7dd8db6b2c97403d8535a04d70f2a0690c09f9ca2f0291b"
license_spdx: "AGPL-3.0-or-later"
human_review: "pending"
source_scope: "Repository root README and owned doc/docs/documentation Markdown or RST files; not a claim of full wiki/site coverage"
---

> Tradução automática local para português, ainda sem revisão humana integral. Estrutura e blocos de código preservados; referências externas não significam conteúdo espelhado.

# Value Profiling

Perfil de valor (VP) adiciona um sinal de distância em cima da cobertura de borda normal.
Em vez de apenas perguntar se uma comparação foi alcançada, AFL++ também rastreia como
fechar os operandos observados são iguais. Isto ajuda em comparações transformadas
onde as tentativas de solução direta são fracas ou impossíveis.

<a id="activation"></a>
## Activação

Perfil de valor atualmente usa instrumentação VP runtime no alvo principal.
Compilar o alvo com `AFL_LLVM_VALUE_PROFILE=1`.

VP e CmpLog são modos alternativos de instrumentação comparado-observador para um
Compilação única. Um alvo compilado com `AFL_LLVM_VALUE_PROFILE=1` emite ganchos VP
para os passes do observador comparado em vez dos ganchos do CmpLog. Use um separado
Binário `-c` compilado pelo CmpLog se quiser o fluxo de trabalho CmpLog do AFL++ no mesmo
Sessão do fuzzing.

- `-r0`: habilitar o perfil de valor da inicialização
- `-rN`: habilitar o perfil de valor após os segundos `N` sem nova cobertura de borda,
em seguida, mantenha- o ativado para o resto da execução
- `-r -1`: habilitar o perfil de valor uma vez que a fila está faminta e nenhuma nova borda tem
foi encontrada para as execuções do `2 * STARVE_EDGE_EXECS` e, em seguida, mantê- la habilitada para
o resto da execução. Com `AFL_STARVED_MINIMIZE_QUEUE` o limiar é
`3 * STARVE_EDGE_EXECS` para que a minimização da fila faminta seja executada primeiro

Sem `-r`, o perfil de valor permanece desactivado.

A VP em tempo de execução requer atualmente um alvo principal compilado com o LLVM
`AFL_LLVM_VALUE_PROFILE=1`. Não é suportado com `-n`, QEMU, Frida,
Modos de execução do Unicórnio, CoreSight, Nyx ou `AFL_NO_FORKSRV`.

O perfil de valor de execução rastreia oito slots de execução por site de comparação atribuído.

Modo de estagnação é baseado na cobertura de borda: `-rN` ativa após o `N` segundos desde
a última nova descoberta de cobertura de bordas. Ela não é baseada no crescimento total da fila.
O modo fome (`-r -1`) usa o mesmo sinal de cobertura de bordas, mas conta execuções
em vez de segundos, e adicionalmente espera até que o fuzzer tenha entrado em fome
modo, o que significa que nenhum item de fila não fuzzed é deixado.
Quando qualquer um dos modos é ativado, o AFL++ reproduz síncronamente a fila existente
uma vez que a fronteira VP também reflete entradas já descobertas.
os processos ativaram somente os itens da fila. Entradas desabilitadas antes da ativação, como
sementes duplicadas de cobertura, não são reconsideradas para VP.

<a id="frontier"></a>
## Fronteira

VP mantém uma fronteira das distâncias mais conhecidas para os pares `(site, slot)`.
Entradas de fila que possuem slots de fronteira são favorecidas para mais fuzzing.

Ser favorecido não é suficiente por si só.
entradas de fila cobrindo todas as bordas conhecidas, e em um alvo pequeno que se define sozinho
já preenche- o, por isso uma entrada que possui o gradiente a campanha está a seguir
termina com a mesma percentagem de tempo de ar que uma entrada que representa apenas um
bordar algumas outras capas de entrada também. Entradas que possuem um slot de fronteira não resolvido
portanto, também obter o seu peso de seleção de fila multiplicado por
`VP_FRONTIER_WEIGHT_MULT` em `config.h` (16), que é aproximadamente o que é preciso para
colocá-los em par com os favoritos de cobertura em vez de atrás deles.

Entradas admitidas apenas através de VP são marcadas com `,+vp` em seu nome de arquivo de fila
e com arquivos de estado sob `.state/vp_only`. Se uma entrada somente VP mais tarde possui não
slots de fronteira, o AFL++ desactiva- o após um período de graça de um ciclo.
A admissão é intencionalmente restrita à distância: custo igual à distância
melhorias não admitem uma nova entrada na fila por si só, embora ainda custe
rompe laços entre os proprietários fronteiriços já admitidos.

Uma distância de zero numa ranhura de fronteira que ainda não possui nenhuma entrada na fila
por si só admite uma nova entrada na fila: a restrição já está satisfeita, então
não há nenhum gradiente a seguir. Um espaço resolvido permanece fechado para o resto
da campanha se um item de fila o detém ou não, então o AFL++ devolve-o
no próximo limite do ciclo de filas. Isso permite a uma entrada apenas de VP cujos slots são todos
resolvido aposentar-se no horário em vez de permanecer vivo - e competindo pelo tempo de ar
- para um gradiente que já não pode produzir.

Os itens apenas para VP também não competem pelos favoritos da cobertura. Eles adicionam não
cobertura de seu próprio, assim que deixar um ganhar um slot `top_rated` deslocaria um
cobertura real encontrar a partir do conjunto favorecido e fixar o VP-somente entrada vivo através
o seu traço de referência muito tempo após o seu gradiente ter sido esgotado.

Os sítios de comparação de rotina estão restritos a funções com comparação reconhecida ou
semântica de pesquisa (o `memcmp`, `strcmp`, `strncmp`, `strstr`, `memmem` e
Famílias `std::string`). O CmpLog é mais amplo "qualquer dois argumentos de ponteiros do mesmo tipo"
heurística não é deliberadamente aplicada sob o perfil de valor: uma não-comparação
chamada como `strcpy` contribuiria com um gradiente sintético que pode
admitir e favorecer permanentemente entradas de fila.

VP rotineiro-compare possui registro separado par-prefixo e buffer inteiro
sinais de distância. rotinas de sub- cordas (`strstr`, `strcasestr`, `memmem`
e similar) registrar o mínimo de ambas as métricas sobre cada offset candidato em
O palheiro, então uma partida bem sucedida registra a distância 0.

Ambos os sinais abrangem toda a janela comparada. Para as famílias terminadas por nul
a comparação termina apenas onde *ambos* operands são nul: um nul em um operand
sozinho é um descompasso como qualquer outro, e cada byte atrás ainda tem que ser
feito igual. Parando a soma do presunto na primeira nul em qualquer um dos operandos seria
comunicar uma distância quase resolvida para uma entrada que não esteja nem perto da correspondência, e
porque essa distância nunca pode atingir zero o mínimo falso iria manter o seu
slot fronteira - e manter sua entrada fila favorecido - para o resto da corrida.
a mesma razão pela qual as famílias `strcmp` e `strcasecmp` dimensionam sua janela de
o operando *longer*, então uma entrada curta é pontuada nos bytes que ainda tem que
crescer, não só naqueles que já tem.

Uma comparação com o resultado ** de uma destas rotinas - o `if (strncmp( a,
b, n))` idioma - não tem perfil de valor. O gancho da própria rotina já carrega
a distância operante, enquanto o inteiro retornado codifica apenas igual ou não e
em que direção: um retorno de `-1` está a um byte de uma partida, mas tem
peso máximo de hamming contra `0`, então marcar seria adicionar um invertido
gradiente que admite e favorece permanentemente entradas de fila.

Todos os ganchos de rotina lidos no máximo 32 bytes por operando, o mesmo ligado CmpLog
usa, que tampa o scan de substring em 32 x 32 byte comparações por chamada. A
jogo que só começa para além dos primeiros 32 bytes palheiros é, portanto, gravado
como uma distância não- zero, mesmo que a própria chamada tenha sucesso; o gradiente sobre
a janela digitalizada permanece válida, a restrição apenas nunca reporta como resolvido.

As comparações de pontos flutuantes são modeladas para `float`, `double`, `_Float16` e
`__bf16` (os dois últimos são alargados para `float`, que é exacto). `long double`,
`__float128` e PowerPC duplo não têm nenhum alvo de alargamento exato, então eles
são marcados na sua codificação de bits através dos ganchos inteiros de 128 bits.
codificação é mapeada para uma chave radix- sort primeiro, de modo que sua ordem não assinada
corresponde à ordem de ponto flutuante em vez de a contradizer. Nas máquinas de 32 bits,
onde os ganchos de 128 bits não existem, estes tipos permanecem uninstrumentados.

Para comparações escalares e de rotina, cada hit dinâmico ordinal seleciona um adjacente
par de fendas, com as duas métricas armazenadas nesse par. Uma vez que uma execução observa
mais hits do que os quatro pares podem representar, mais tarde hits wrap around e update
Os mesmos pares.

O espaço de nomes do site físico tem 65.536 entradas (`VP_MAP_W`), organizadas como
16.384 conjuntos de quatro vias. Um token do site lógico seleciona dois conjuntos de candidatos e um
forma preferida em cada um. Uma etiqueta existente é reutilizada; caso contrário, as reivindicações de execução
uma forma livre no conjunto primário e, em seguida, o conjunto secundário.
estável para a vida útil do mapa em tempo de execução. Se todas as oito formas candidatas forem
ocupado por outras tags, o novo site lógico é omitido em vez de compartilhar ou
despejar o estado de um sítio existente.

<a id="focus-set"></a>
## Foco Definir

O custo de uma batida de tempo de execução é definido por quantos locais distintos são ao vivo, não por
como o mapa é embalado: cerca de 6 ns em poucos milhares de locais ao vivo e cerca de 18 ns
em 60.000, porque cada site ao vivo adiciona outra linha de cache aleatória para tocar.
AFL++, portanto, caps quantos sites podem gravar ao mesmo tempo, em um conjunto de foco reconstruído
em cada fila-ciclo limite.

`VP_FOCUS_TARGET_SITES` em `config.h` (4,096) é o limite máximo em quantos locais
uma reconstrução admite. Possuir um slot de fronteira não é escasso - um site possui o seu próprio
slots, então quase todos os sites gravados possuem um - então o teto, não a propriedade,
é o que limita o conjunto vivo.

Três quartos do orçamento giram sobre os locais que possuem uma fenda de fronteira
cuja distância é ainda acima de zero, que é onde o gradiente a campanha
está a seguir vidas. O trimestre restante gira sobre tudo o resto, então
restrições fora do foco atual ainda são descobertas ao longo do tempo.
as mãos do nível, a sua parte não utilizada para a outra. Cada camada mantém o seu próprio cursor, por isso
Nem o outro morre de fome.

Sites fora do foco definir a fiança fora do gancho antes de tocar no seu slot
estado, que é a segunda linha de cache aleatória que um hit gravado custaria.
é também o que faz a aposentadoria barato, assim que a filtragem permanece em sempre que o
*assinado* espaço de nomes excede o orçamento, mesmo quando a aposentadoria tomou o
número de sites de gravação abaixo dele. Apenas um mapa com poucos sites atribuídos em
total levanta a restrição; lá, cada registro de site e os custos de rotação
Nada.

Sites lógicos que o tempo de execução nunca viu ainda pode reivindicar uma chave física enquanto
o conjunto de focos está em vigor, caso contrário, o código recém-chegado nunca poderia entrar no
rotação. Eles apenas gravam nada até que uma rotação os admite. Isto também é
por que o teto se mantém entre as reconstruções: um local descoberto no meio do ciclo não pode
gravar até que uma rotação o admita.

Enquanto a filtragem está desligada, os sites recém-descobertos gravam imediatamente,
assim, o conjunto ao vivo pode aumentar o orçamento antes do próximo limite do ciclo da fila.
`control_len` relata quantos sites distintos registrados no anterior
execução, e uma reconstrução está agendada para o próximo item da fila assim que isso
a contagem passa o orçamento. A sobreposição é, portanto, limitada por uma fila
entrada, não um ciclo de fila.

<a id="site-retirement"></a>
## Aposentadoria do Site

O mesmo passe aposenta sites que deixaram de pagar por si mesmos:

- Um site cujos slots de fronteira são *all* possuído e resolvido não tem nenhum gradiente sobrando
para oferecer.
- Um site que não possui nenhum slot não resolvido e registrou para
Ciclos de foco `VP_IDLE_RETIRE_CYCLES` sem alterar nada no
fronteira não vale o seu custo gancho.

Um espaço de fronteira vazio é um ordinal dinâmico atingido o local não foi observado
um site é atingido repetidamente dentro de uma execução, e
cada hit ordinal maps para o seu próprio par de slots, resolvendo assim a primeira ocorrência
não diz nada sobre ocorrências que nunca foram alcançadas. Aposentadoria na
apenas as faixas horárias detidas esconderiam essas ocorrências posteriores até à redefinição da fronteira,
que é por isso que a resolução completa requer cada slot e por que a regra ociosa dá um
a aparecerem ciclos de focagem `VP_IDLE_RETIRE_CYCLES` ordinais não observados.

Um site que possui uma fenda não resolvida nunca é aposentado para ficar quieto; ele
gira como qualquer outro site em vez, para que ainda pode ser melhorado em e
lançado, e a entrada de fila segurando-o nunca acaba favorecido para um site
O AFL++ parou de medir.

Aposentadoria é um bit de bandeira por site no mapa de tempo de execução, por isso não custa nada em
memória, e encolhe o conjunto ao vivo exatamente quando o mapa está mais completo, tarde em um
campanha. Um site aposentado não registra nada, mesmo quando o foco não está em
força.

Aposentadoria é desfeita por um reset de fronteira, então um site aposentado cedo pode sempre
voltar. Um site resolvido permanece aposentado quando seu proprietário vai embora, porque o
slot fica fechado sem um.

O relógio ocioso conta apenas ciclos em que o local foi realmente permitido
gravar, e reiniciar sempre que o site reivindica um slot, melhora uma distância,
ou perde um proprietário. Um site nunca é aposentado por não melhorar durante
ciclos que se sentaram fora do conjunto de foco, nem imediatamente após o seu proprietário
desaparece.

Observação caixa de areia, usado pelo guarda de aparar, temporariamente levanta a aposentadoria em
os locais que observa, para que um guarda nunca leia o seu próprio sinal como perdido.

<a id="instrumented-compares"></a>
## Comparações instrumentadas

Além de ignorar o controle de loop canônico compara, as instruções passam gotas
Comparações cujos operandos não derivam transitivamente de uma carga ou de uma função
argumento. Sem dependência de entrada não há restrição solucionável, então o
local seria pura sobrecarga. A análise é conservadora em uma direção
apenas: qualquer coisa que ele não pode ver através - um resultado de chamada, inline asm, um def-use
cadeia mais profunda do que 32 passos - conta como dependente de entrada e mantém seu site.

Isto corta sites no tempo de compilação em vez de em tempo de execução, e porque cada site
também carrega uma guarda, ele melhora o caminho padrão-off também.
instrumentação é intocada: uma construção VP tem o mesmo número de cobertura
pontos como uma construção simples.

Trocas e comparações de rotina não são filtradas desta forma.

<a id="stats"></a>
## Estatísticas

Entradas de fila somente VP são contadas em `value_profile_finds` e em
`corpus_count`, mas eles deliberadamente não atualizar `last_find_time`.
"nenhuma nova descoberta" relógio que conduz `AFL_EXIT_ON_TIME`, o explorar/explorar
switch e o display `time_wo_finds` fica baseado em cobertura, combinando com o
`last_edge_find` relógio que `-rN` modo de estagnação usa.

Note que `cycles_wo_finds`, ea escalada de estrago fechado sobre ele, contar
crescimento da fila em vez do relógio de procura, então as entradas somente de VP ainda repõem
Eles.

<a id="mutation-scope"></a>
## Âmbito da Mutação

O VP orienta actualmente quais os itens da fila que são mantidos e favorecidos. Ainda não existe
posições de mutação de nível de byte guia. As mutações de havoc e determinística ainda usam
a máquina de mutação AFL++ regular sobre o tampão de entrada.

## Overhead

A configuração fixa de oito pontos aloca aproximadamente:

- ~ 8 MiB para a fronteira do lado fuzzer (entradas `65536 * 8`)
- 2.498.576 bytes (cerca de 2.38 MiB) para o mapa de memória partilhada VP em tempo de execução
- 216 KiB para os bitmaps de foco do lado fuzzer e contadores por local

Em uma compilação de 64 bits, o mapa fixo prático é sobre 10.6 MiB.


---

## Procedência desta tradução

Fonte: [https://github.com/AFLplusplus/AFLplusplus](https://github.com/AFLplusplus/AFLplusplus/blob/d0070729206a80a9af297b2341edd63f68fdac35/docs/value_profiling.md). Licença: [AGPL-3.0-or-later](../../99-Assets/upstream/aflplusplus/LICENSE.txt). Commit: d0070729206a80a9af297b2341edd63f68fdac35.

O original preservado, a lista de mudanças de apresentação e os hashes constam no manifesto do projeto. Nenhum exemplo desta documentação foi executado automaticamente.
