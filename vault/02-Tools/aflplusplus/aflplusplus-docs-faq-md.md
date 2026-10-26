---
title: "aflplusplus — documentação oficial"
type: "official-documentation"
tool: "aflplusplus"
status: "translated-machine"
reviewed: "2026-10-26"
language: "pt-BR"
tags: ["documentation", "tool/aflplusplus"]
cssclasses: ["fieldbook"]
source_url: "https://github.com/AFLplusplus/AFLplusplus/blob/d0070729206a80a9af297b2341edd63f68fdac35/docs/FAQ.md"
source_commit: "d0070729206a80a9af297b2341edd63f68fdac35"
source_sha256: "18c61dafbfe58555c0e28cd022865534a6217805dc8fbcc1b35f71c4f8ac0c96"
license_spdx: "AGPL-3.0-or-later"
human_review: "pending"
source_scope: "Repository root README and owned doc/docs/documentation Markdown or RST files; not a claim of full wiki/site coverage"
---

> Tradução automática local para português, ainda sem revisão humana integral. Estrutura e blocos de código preservados; referências externas não significam conteúdo espelhado.

# Frequently asked questions (FAQ)

Se você encontrar uma pergunta interessante ou importante faltando, submeta-a via
[https://github.com/AFLplusplus/AFLplusplus/discussions](https://github.com/AFLplusplus/AFLplusplus/discussions).

<a id="general"></a>
## Geral

<details>
<summary id="what-is-the-difference-between-afl-and-aflplusplus">Qual é a diferença entre AFL e AFL++?</summary><p>

AFL++ é um garfo superior à AFL do Google - mais velocidade, mais e melhor
mutações, mais e melhor instrumentação, suporte de módulo personalizado, etc.

O American Fuzzy Lop (AFL) foi desenvolvido por Michal "lcamtuf" Zalewski começando
em 2013/2014, e quando deixou o Google no final de 2017 ele parou de desenvolvê-lo.

No final de 2019, a equipe do Google fuzzing assumiu a manutenção da AFL,
no entanto, é apenas aceitar RPs da comunidade e não está se desenvolvendo
As melhorias já não são mais.

No segundo trimestre de 2019, 1 1/2 anos mais tarde, quando não há mais desenvolvimento
da AFL tinha acontecido e tornou-se claro que não haveria nenhum vindo, AFL++ foi
nascido, onde inicialmente patches da comunidade foram coletados e aplicados para bug
correções e melhorias. Em seguida, a partir de vários spin-offs AFL - principalmente acadêmico
pesquisa - características foram integradas, o que já resultou em uma
AFL.

Até o final de 2019, a equipe AFL++ tinha crescido para quatro desenvolvedores ativos
que, em seguida, implementaram suas próprias pesquisas e características, tornando-se agora de longe
o fuzzer guiado mais flexível e recurso rico disponível como código aberto. E
em benchmarks independentes fuzzing é um dos melhores fuzzers disponíveis,
  e.g.,
[Relatório Fuzzbench](https://www.fuzzbench.com/reports/2020-08-03/index.html).
</p></details>

<details>
<summary id="is-afl-a-whitebox-graybox-or-blackbox-fuzzer">Is AFL++ uma caixa branca, caixa cinza ou caixa preta fuzzer?</summary><p>

A definição dos termos caixa branca, caixa cinza e caixa preta fuzzing varia
de uma fonte para outra. Por exemplo, "graybox fuzzing" pode significar
somente binário ou código fonte fuzzing, ou algo completamente diferente.
Portanto, tentamos evitá-los.

[O Livro Fuzzing](https://www.fuzzingbook.org/html/GreyboxFuzzer.html#AFL:-An-Effective-Greybox-Fuzzer)
descreve a AFL original para ser uma caixa cinza fuzzer. Nesse sentido, AFL++ é
também uma caixa cinza fuzzer.
</p></details>

<details>
<summary id="where-can-i-find-tutorials">Onde posso encontrar tutoriais?</summary><p>

Compilamos uma lista de tutoriais e exercícios, ver
[tutoriais. md](aflplusplus-docs-tutorials-md.md).
</p></details>

<details>
<summary id="what-is-an-edge">O que é um "bordo"?</summary><p>

Um programa contém `functions`, `functions` contém o código da máquina compilado.
O código da máquina compilado em um `function` pode ser em um único ou muitos `básicos
bloco`. A `basic block` é o ** maior número possível de máquina subsequente
instruções de código** que tem **Exatamente um ponto de entrada** (que pode ser introduzido por
vários outros blocos básicos) e roda linearmente **sem ramificação ou salto para
outros endereços** (exceto no final).

  ```text
  function() {
    A:
      some
      code
    B:
      if (x) goto C; else goto D;
    C:
      some code
      goto E
    D:
      some code
      goto B
    E:
      return
  }
  ```

Cada bloco de código entre dois locais de salto é um `basic block`.

Um `edge` é então a relação única entre dois conectados diretamente
`basic blocks` (a partir do exemplo de código acima):

  ```text
                Block A
                  |
                  v
                Block B  <------+
              /        \       |
              v          v      |
          Block C    Block D --+
              \
                v
                Block E
  ```

Cada linha entre dois blocos é um `edge`. Observe que alguns loops básicos de bloco
Para si mesmo, isto também seria uma vantagem.
</p></details>

<details>
<summary id="should-you-ever-stop-afl-fuzz-minimize-the-corpus-and-restart">Você deveria parar o afl-fuzz, minimizar o corpus e reiniciar?</summary><p>

Para parar o afl-fuzz, minimize seu corpus e reinicie você normalmente faria:

  ```text
  Control-C  # to terminate afl-fuzz
  $ afl-cmin -T all -i out/default/queue -o minimized_queue -- ./target
  $ AFL_FAST_CAL=1 AFL_CMPLOG_ONLY_NEW=1 afl-fuzz -i minimized_queue -o out2 [other options] -- ./target
  ```

Se isto melhorar o fuzzing ou não for debatido e não tiver sido alcançado consenso
Foi efectuada uma análise aprofundada.

No lado profissional:
    * The queue/corpus is reduced (up to 20%) by removing intermediate paths
      that are maybe not needed anymore.

No lado do contra:
    * Fuzzing time is lost for the time the fuzzing is stopped, minimized and
      restarted.

A grande questão:
    * Does a minimized queue/corpus improve finding new coverage or does it
      hinder it?

A própria análise limitada da equipe AFL++ parece mostrar que manter
caminhos intermediários ajudam a encontrar mais cobertura, pelo menos para afl-fuzz.

Para hongggfuzz em comparação é uma boa idéia reiniciá-lo de tempo para
tempo se você tiver outros fuzzers (por exemplo: AFL++) em execução paralela à sincronização
as descobertas de outros fuzzers para hongggfuzz como ele não tem nenhum recurso de sincronização como
AFL++ ou libfuzzer.

</p></details>

<a id="targets"></a>
## Alvos

<details>
<summary id="how-can-i-fuzz-a-binary-only-target">Como posso fazer um alvo somente binário?</summary><p>

AFL++ é um grande fuzzer se você tiver o código fonte disponível.

No entanto, se houver apenas o programa binário e nenhum código fonte disponível,
então o modo padrão não instrumentado não é eficaz.

Para saber como estes binários podem ser fuzzed, leia
[fuzzing_binary- only_targets. md](aflplusplus-docs-fuzzing-binary-only-targets-md.md).
</p></details>

<details>
<summary id="how-can-i-fuzz-a-network-service">Como posso fazer um serviço de rede?</summary><p>

A resposta curta é - você não pode, pelo menos não "fora da caixa".

Para mais informações sobre os serviços de rede fuzzing, consulte
[best_ practices.md#fuzzing-a-network-service](aflplusplus-docs-best-practices-md.md#fuzzing-a-network-service).
</p></details>

<details>
<summary id="how-can-i-fuzz-a-gui-program">Como posso fazer um programa GUI?</summary><p>

Nem todos os programas GUI são adequados para fuzzing. Se o programa GUI pode ler o
dados fuzz de um arquivo sem precisar de qualquer interação com o usuário, então ele seria
adequado para fuzzing.

Para mais informações sobre os programas GUI fuzzing, consulte
[best_ practices.md#fuzzing-a-gui-program](aflplusplus-docs-best-practices-md.md#fuzzing-a-gui-program).
</p></details>

<a id="performance"></a>
## Desempenho

<details>
<summary id="what-makes-a-good-performance">O que faz um bom desempenho?</summary><p>

Bom desempenho geralmente significa "fazer com que os resultados do fuzzing melhorem".
ser influenciado por vários fatores, por exemplo, velocidade (encontrando lotes de caminhos
rápido) ou minucioso (trabalhando com velocidade diminuída, mas encontrando melhor
Mutações).
</p></details>

<details>
<summary id="how-can-i-improve-the-fuzzing-speed">Como posso melhorar a velocidade fuzzing?</summary><p>

Há algumas coisas que você pode fazer para melhorar a velocidade fuzzing, veja
[best_práticas.md#melhorar a velocidade](aflplusplus-docs-best-practices-md.md#improving-speed).
</p></details>

<details>
<summary id="why-is-my-stability-below-100percent">Por que minha estabilidade está abaixo de 100%?</summary><p>

Estabilidade é medida por quantos por cento das bordas no alvo são
"estável". Enviando a mesma entrada de novo e de novo deve tomar exatamente o mesmo
caminho através do alvo cada vez. Se for esse o caso, a estabilidade é
  100%.

Se, no entanto, ocorrer aleatoriedade, por exemplo, um thread que leia outros dados externos,
reação ao timing, etc., então em algumas das re-execuções com os mesmos dados
o resultado da cobertura da borda será diferente entre as corridas.
a mudança é então marcada como "instável".

Quanto mais "instáveis" bordas existem, mais difícil é para AFL++ para identificar
novos caminhos válidos.

Se estiver em modo persistente (`AFL_LOOP` ou `LLVMFuzzerTestOneInput()`
arneses, um grande número de bordas instáveis pode significar que o alvo mantém
estado interno e, portanto, é possível que falhas não possam ser reproduzidas.
Neste caso, faça **not** fuzz em modo persistente (remover `AFL_LOOP()`
a partir do seu arnês ou chamar `LLVMFuzzerTestOneInput()` arneses com `@@`),
ou defina um valor `AFL_LOOP` baixo, por exemplo 100, e habilite `AFL_PERSISTENT_RECORD`
em `config.h` com o mesmo valor.

Um valor acima de 90% é normalmente bom e um valor acima de 80% também é ok, e
mesmo um valor acima de 20% pode ainda resultar em resultados bem sucedidos de bugs. No entanto,
Recomenda- se que, para valores inferiores a 90% ou 80%, tome
Contramedidas para melhorar a estabilidade.

Para mais informações sobre estabilidade e como melhorar o valor de estabilidade, consulte
[best_práticas.md#melhoramento-estabilidade](aflplusplus-docs-best-practices-md.md#improving-stability).
</p></details>

<details>
<summary id="what-are-power-schedules">O que são agendamentos de energia?</summary><p>

Nem todos os itens da nossa fila/corpo são os mesmos, alguns são mais interessantes,
outros fornecem pouco valor.
Um programa de energia mede como "interessante" um valor é, e dependendo de
O valor calculado passa mais ou menos tempo a mutá-lo.

O AFL++ vem com vários escalonamentos de energia, inicialmente portados de
[AFLFast](https://github.com/mboehme/aflfast), no entanto, modificado para ser mais
eficaz e vários mais modos adicionados.

Os modos mais eficazes são `-p explore` (padrão) e `-p fast`.

Se você fuzz com várias instâncias paralelas afl-fuzz, então é benéfico
para atribuir um calendário diferente a cada instância, no entanto, a maioria deve
ser `fast` e `explore`.

Não faz sentido explicar os pormenores do cálculo e
raciocinando por trás de todas as agendas. Se você estiver interessado, leia a fonte
código e o papel AFLFast.
</p></details>

<a id="troubleshooting"></a>
## Resolução de Problemas

<details>
<summary id="fatal-forkserver-is-already-up-but-an-instrumented-dlopen-library-loaded-afterwards">FATAL: o servidor fork já está ligado, mas uma biblioteca dlopen instrumentada carregada depois</summary><p>

Pode acontecer que você veja este erro na inicialização quando fuzzing um alvo:

  ```text
  [-] FATAL: forkserver is already up, but an instrumented dlopen() library
             loaded afterwards. You must AFL_PRELOAD such libraries to be able
             to fuzz them or LD_PRELOAD to run outside of afl-fuzz.
             To ignore this set AFL_IGNORE_PROBLEMS=1.
  ```

Como o erro descreve, uma chamada dolopen () está acontecendo no alvo que é
carregando uma biblioteca instrumentada após o servidor de fork já estar no lugar. This
é um problema para o afl-fuzz porque quando o servidor for iniciado, temos de saber
o tamanho do mapa já e não pode ser alterado mais tarde.

A melhor solução é simplesmente definir `AFL_PRELOAD=foo.so` para as bibliotecas que
são dlopen'ed (por exemplo, use `strace` para ver qual), ou para definir um servidor de garfos manual
após o último dlopen().

Se esta não é uma opção viável, você pode definir `AFL_IGNORE_PROBLEMS=1`, mas então
o mapa existente será usado também para as bibliotecas recém-carregadas, que
permite que ele funcione, no entanto, a eficiência do fuzzing será parcialmente
degradado. Note que há adicionalmente `AFL_IGNORE_PROBLEMS_COVERAGE` para
adicionalmente diga ao AFL++ para ignorar qualquer cobertura das bibliotecas carregadas tardiamente.
</p></details>

<details>
<summary id="i-got-a-weird-compile-error-from-clang">I obteve um erro de compilação estranho de clang.</summary><p>

Se você vir este tipo de erro ao tentar instrumentar um alvo com
afl-cc/afl-clang-fast/afl-clang-lto:

  ```text
  /prg/tmp/llvm-project/build/bin/clang-18: symbol lookup error: /usr/local/bin/../lib/afl//cmplog-instructions-pass.so: undefined symbol: _ZNK4llvm8TypeSizecvmEv
  clang-18: error: unable to execute command: No such file or directory
  clang-18: error: clang frontend command failed due to signal (use -v to see invocation)
  clang version 18.0.0 (https://github.com/llvm/llvm-project 1d7cf550721c51030144f3cd295c5789d51c4aad)
  Target: x86_64-unknown-linux-gnu
  Thread model: posix
  InstalledDir: /prg/tmp/llvm-project/build/bin
  clang-18: note: diagnostic msg:
  ********************
  ```

Então isso significa que seu sistema operacional atualizou a instalação do clang a partir de uma atualização
pacote e por causa disso os plugins AFL++ lvm não coincidem mais.

Solução: `git pull ; make clean install` de AFL++.
</p></details>

<details>
Alerta de tamanho de mapa <summary id="afl-map-size-warning">AFL++.</summary><p>

Quando você executa um grande programa instrumentado stand-alone ou via afl-showmap
você pode ver um aviso como o seguinte:

  ```text
  Warning: AFL++ tools might need to set AFL_MAP_SIZE to 223723 to be able to run this instrumented program if this crashes!
  ```

Dependendo de como o alvo funciona, ele também pode cair depois.

Solução: basta fazer um `export AFL_MAP_SIZE=(the value in the warning)`.
</p></details>

<details>
Erros do <summary id="linker-errors">Linker.</summary><p>

Se você compilar arneses C++ e ver os erros do `undefined reference` para
variáveis denominadas `__afl_...`, por exemplo:

  ```text
  /usr/bin/ld: /tmp/test-d3085f.o: in function `foo::test()':
  test.cpp:(.text._ZN3fooL4testEv[_ZN3fooL4testEv]+0x35): undefined reference to `foo::__afl_connected'
  clang: error: linker command failed with exit code 1 (use -v to see invocation)
  ```

Então você usa macros AFL++ como `__AFL_LOOP` dentro de um espaço de nomes e isso
Não vai funcionar.

Solução: Mova essa porção de arnês para o espaço de nomes global, por exemplo, antes de:
  ```text
  #include <cstdio>
  namespace foo {
    static void test() {
      while(__AFL_LOOP(1000)) {
        foo::function();
      }
    }
  }

  int main(int argc, char** argv) {
    foo::test();
    return 0;
  }
  ```
após:
  ```text
  #include <cstdio>
  static void mytest() {
    while(__AFL_LOOP(1000)) {
      foo::function();
    }
  }
  namespace foo {
    static void test() {
      mytest();
    }
  }
  int main(int argc, char** argv) {
    foo::test();
    return 0;
  }
  ```
</p></details>


---

## Procedência desta tradução

Fonte: [https://github.com/AFLplusplus/AFLplusplus](https://github.com/AFLplusplus/AFLplusplus/blob/d0070729206a80a9af297b2341edd63f68fdac35/docs/FAQ.md). Licença: [AGPL-3.0-or-later](../../99-Assets/upstream/aflplusplus/LICENSE.txt). Commit: d0070729206a80a9af297b2341edd63f68fdac35.

O original preservado, a lista de mudanças de apresentação e os hashes constam no manifesto do projeto. Nenhum exemplo desta documentação foi executado automaticamente.
