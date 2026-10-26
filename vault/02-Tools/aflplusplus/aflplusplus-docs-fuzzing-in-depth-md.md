---
title: "aflplusplus — documentação oficial"
type: "official-documentation"
tool: "aflplusplus"
status: "translated-machine"
reviewed: "2026-10-26"
language: "pt-BR"
tags: ["documentation", "tool/aflplusplus"]
cssclasses: ["fieldbook"]
source_url: "https://github.com/AFLplusplus/AFLplusplus/blob/d0070729206a80a9af297b2341edd63f68fdac35/docs/fuzzing_in_depth.md"
source_commit: "d0070729206a80a9af297b2341edd63f68fdac35"
source_sha256: "52dc5a3ae5119d7b8584c2bf0bfb0504e2a41129d6b30b0020e42bb54a1459c1"
license_spdx: "AGPL-3.0-or-later"
human_review: "pending"
source_scope: "Repository root README and owned doc/docs/documentation Markdown or RST files; not a claim of full wiki/site coverage"
---

> Tradução automática local para português, ainda sem revisão humana integral. Estrutura e blocos de código preservados; referências externas não significam conteúdo espelhado.

# Fuzzing with AFL++

O seguinte descreve como se faz o fuzz com um alvo se o código fonte estiver disponível.
Se você tem um alvo somente binário, vá para
[fuzzing_binary- only_targets. md](aflplusplus-docs-fuzzing-binary-only-targets-md.md).

O código fonte fuzzing é um processo em três etapas:

1. Compilar o alvo com um compilador especial que prepara o alvo para ser
Este passo é chamado de "instrumentar um alvo".
2. Prepare o fuzzing selecionando e otimizando o corpus de entrada para o
Alvo.
3. Execute o fuzzing do alvo alterando aleatoriamente a entrada e avaliando se
essa entrada foi processada em um novo caminho no binário alvo.

## 0. Riscos de bom senso

Por favor, tenha em mente que, semelhante a muitos outros computacionalmente-intensivos
tarefas, fuzzing pode colocar uma tensão em seu hardware e no sistema operacional. Em particular:

- Sua CPU irá funcionar quente e precisará de resfriamento adequado. Na maioria dos casos, se
refrigeração é insuficiente ou pára de funcionar corretamente, CPU velocidades serão
automaticamente estrangulado. Dito isto, especialmente quando fuzzing em menos adequado
hardware (laptops, smartphones, etc.), não é totalmente impossível para
Algo para explodir.

- Programas direcionados podem acabar erraticamente agarrando gigabytes de memória ou
enchendo o espaço em disco com arquivos de lixo. AFL++ tenta forçar a memória básica
limites, mas não pode evitar cada e cada acidente possível.
que você não deve ser fuzzing em sistemas onde a perspectiva de perda de dados é
não é um risco aceitável.

- Fuzzing envolve bilhões de leituras e escreve para o sistema de arquivos.
sistemas, este será geralmente fortemente cached, resultando em bastante modesto
E/S "físico" - mas existem muitos fatores que podem alterar esta equação.
é a sua responsabilidade de monitorizar potenciais problemas; com E/S muito pesado,
a vida útil de muitos HDDs e SSDs pode ser reduzida.

Uma boa maneira de monitorar o I/O do disco no Linux é o comando `iostat`:

  ```shell
  $ iostat -d 3 -x -k [...optional disk ID...]
  ```

Usando a variável de ambiente `AFL_TMPDIR` e um disco RAM, você pode ter o
escrita pesada feita em RAM para evitar o desgaste acima mencionado.
exemplo, a seguinte linha executará um recipiente Docker com toda esta predefinição:

  ```shell
  # docker run -ti --mount type=tmpfs,destination=/ramdisk -e AFL_TMPDIR=/ramdisk aflplusplus/aflplusplus
  ```

## 1. Instrumentação do alvo

### a) Selecionando o melhor compilador AFL++ para instrumentar o alvo

AFL++ vem com um compilador central `afl-cc` que incorpora vários diferentes
tipos de metas de compilador e opções de instrumentação.
O fluxo de avaliação o ajudará a selecionar o melhor possível.

É altamente recomendado ter a versão mais nova lvm possível instalado,
não se recomenda qualquer coisa inferior a 9 anos.

NOTIFICAÇÃO IMPORTANTE: o afl-gcc/afl-clang foi removido do AFL++ uma vez que estão obsoletos.

```text
+--------------------------------+
| clang/clang++ 11+ is available | --> use LTO mode (afl-clang-lto/afl-clang-lto++)
+--------------------------------+     see [instrumentation/README.lto.md](instrumentation/README.lto.md)
    |
    | if not, or if the target fails with LTO afl-clang-lto/++
    |
    v
+---------------------------------+
| clang/clang++ 3.8+ is available | --> use LLVM mode (afl-clang-fast/afl-clang-fast++)
+---------------------------------+     see [instrumentation/README.llvm.md](instrumentation/README.llvm.md)
    |
    | if not, or if the target fails with LLVM afl-clang-fast/++
    |
    v
 +--------------------------------+
 | gcc 5+ is available            | -> use GCC_PLUGIN mode (afl-gcc-fast/afl-g++-fast)
 +--------------------------------+    see [instrumentation/README.gcc_plugin.md](instrumentation/README.gcc_plugin.md) and
                                       [instrumentation/README.instrument_list.md](instrumentation/README.instrument_list.md)
    |
    | if not, or if you do not have a gcc with plugin support
    |
    v
   GAME OVER! Install gcc-VERSION-plugin-dev or llvm-VERSION-dev
```

Ligações README clicáveis para o compilador escolhido:

* [Modo LTO - afl-clang- lto](https://github.com/AFLplusplus/AFLplusplus/blob/d0070729206a80a9af297b2341edd63f68fdac35/instrumentation/README.lto.md)
* [Modo LLVM - afl-clang-fast](https://github.com/AFLplusplus/AFLplusplus/blob/d0070729206a80a9af297b2341edd63f68fdac35/instrumentation/README.llvm.md)
* [Modo GCC_ PLUGIN - afl- gcc- fast](https://github.com/AFLplusplus/AFLplusplus/blob/d0070729206a80a9af297b2341edd63f68fdac35/instrumentation/README.gcc_plugin.md)

Você pode selecionar o modo para o compilador afl-cc por um dos seguintes métodos:

* Usando um link simbólico para o afl-cc:
afl-clang-fast, afl-clang-fast++, afl-clang-lto, afl-clang-lto++,
Afl-gcc-fast, afl-g++-fast.
* Usando a variável de ambiente `AFL_CC_COMPILER` com `MODE`.
* Passando as opções de linha de comando --afl-`MODE` para o compilador via
      `CFLAGS`/`CXXFLAGS`/`CPPFLAGS`.

`MODE` pode ser um dos seguintes:

* LTO (afl-clang-lto*)
* LLVM (afl-clang-fast*)
* GCC_ PLUGIN (afl- g*- fast)

Porque não são aceites opções de linha de comandos específicas do AFL++ (ao lado do
--afl-MODE comando), as ferramentas de tempo de compilação fazer bastante amplo uso do ambiente
variáveis, que podem ser listadas com `afl-cc -hh` ou pesquisadas em
[env_variables.md](aflplusplus-docs-env-variables-md.md).

### b) Selecionando opções de instrumentação

Se você instrumentar com o modo LTO (afl-clang-fast/afl-clang-lto), o seguinte
opções estão disponíveis:

* Dividir inteiro, string, float e alternar comparações para que o AFL++ possa ser mais fácil
resolver estes. Esta é uma opção importante se você não tem um muito bom e
grande corpus de entrada. Esta técnica é chamada de laf-intel ou COMPCOV.
isto, defina a seguinte variável de ambiente antes de compilar o alvo:
`export AFL_LLVM_LAF_ALL=1`. Você pode ler mais sobre isso em
[instrumentação/README.laf-intel.md](https://github.com/AFLplusplus/AFLplusplus/blob/d0070729206a80a9af297b2341edd63f68fdac35/instrumentation/README.laf-intel.md).
* Uma técnica diferente (e geralmente uma melhor do que laf-intel) é
instrumento o alvo para que quaisquer valores de comparação no alvo sejam enviados para
AFL++ que então tenta colocar esses valores nos dados fuzzing em diferentes
Esta técnica é muito rápida e boa - se o alvo não
transformar dados de entrada antes da comparação. Portanto, esta técnica é chamada
`input to state` ou `redqueen`. Se você quiser usar esta técnica, então você
tem que compilar o alvo com `AFL_LLVM_CMPLOG=1`.
Você poderia usar o binário resultante tanto para fuzzing normal quanto para `-c` CMPLOG
modo (com `-c 0`), no entanto, isso resultará em uma perda de desempenho de cerca de
  20%.
Assim, é melhor compilar um alvo específico do CMPLOG com
`AFL_LLVM_CMPLOG=1` e passe este nome binário via
`-c cmplog-fuzzing-target` e compilar o alvo novamente normalmente com `afl-cc`
e usar este é o alvo fuzzing como de costume.
Você pode ler mais sobre isso em
[instrumentação/README.cmplog.md](https://github.com/AFLplusplus/AFLplusplus/blob/d0070729206a80a9af297b2341edd63f68fdac35/instrumentation/README.cmplog.md).

Se você usar o modo LTO, LLVM ou GCC_ PLUGIN
(afl-clang-fast/afl-clang-lto/afl-gcc-fast), você tem a opção de seletivamente
instrumento _parts_ do alvo em que você está interessado. Para afl-clang-fast,
você tem que usar uma versão lvm mais recente do que 10.0.0 ou um modo diferente
DEFAULT/PCGUARD.

Este passo pode ser feito quer explicitamente incluindo partes a serem instrumentadas ou
excluindo explicitamente as partes da instrumentação.

* Para instrumentar _somente partes especificadas_, crie um arquivo (por exemplo, `allowlist.txt`)
com todos os nomes de arquivos e/ou funções do código fonte que devem ser
instrumentados e depois:

  1. Basta colocar um nome de arquivo ou função (prefixo com `fun: `) por linha (não
     directory information necessary for filenames) in the file `allowlist.txt`.

     Example:

     ```text
     foo.cpp        # will match foo/foo.cpp, bar/foo.cpp, barfoo.cpp etc.
     fun: foo_func  # will match the function foo_func
     ```

  2. Definir o `export AFL_LLVM_ALLOWLIST=allowlist.txt` para permitir o positivo seletivo
     instrumentation.

* Da mesma forma que _exclude_ especifica partes da instrumentação, crie um arquivo
(por exemplo, `denylist.txt`) com todos os nomes de arquivo do código fonte que devem
ser ignorada durante a instrumentação e depois:

  1. O mesmo que acima. Basta colocar um nome de arquivo ou função por linha no arquivo
     `denylist.txt`.

  2. Definir o `export AFL_LLVM_DENYLIST=denylist.txt` para permitir o negativo seletivo
     instrumentation.

**NOTE:** Durante as funções de otimização pode ser
inlined e então não corresponde à lista! Veja
[instrumentação/README.instrument_list.md](https://github.com/AFLplusplus/AFLplusplus/blob/d0070729206a80a9af297b2341edd63f68fdac35/instrumentation/README.instrument_list.md).

Existem muitas mais opções e modos disponíveis, no entanto, estes são a maioria dos
tempo menos eficaz.

* [instrumentação/README.llvm.md#6) Cobertura de Ramo Sensível ao Contexto AFL++](https://github.com/AFLplusplus/AFLplusplus/blob/d0070729206a80a9af297b2341edd63f68fdac35/instrumentation/README.llvm.md#6-afl-context-sensitive-branch-coverage)
* [instrumentação/README.llvm.md#7) AFL++ N-Gram Branch Coverage](https://github.com/AFLplusplus/AFLplusplus/blob/d0070729206a80a9af297b2341edd63f68fdac35/instrumentation/README.llvm.md#7-afl-n-gram-branch-coverage)

O AFL++ executa a contagem "nunca zero" no seu mapa de bits. Você pode ler mais sobre isso
Aqui:
* [instrumentação/README.llvm.md#8-nunca zero-contadores](https://github.com/AFLplusplus/AFLplusplus/blob/d0070729206a80a9af297b2341edd63f68fdac35/instrumentation/README.llvm.md#8-neverzero-counters)

### c) Selecionando higiénicos

É possível usar higienizadores ao instrumentar alvos para fuzzing, que
permite- lhe encontrar bugs que não resultariam necessariamente em uma falha.

Note que os higienizadores têm um enorme impacto na CPU (= menos execuções por segundo)
e uso de RAM. Além disso, você só deve executar uma instância afl-fuzz por higienizador
tipo. Isto é suficiente porque, por exemplo, um erro depois de livre de uso será apanhado pelo ASAN
De qualquer forma, depois de sincronizar os casos de teste de outros fuzzing
Casos, então executar mais de um endereço alvo higienizado seria um desperdício.

*IF* você está executando um corpus saturado, então você pode correr até metade do
casos com higiénicos.

Uma abordagem alternativa mas mais eficaz é usar [SANDA](aflplusplus-docs-sand-md.md) que poderia
combinar diferentes sanitizers em um rendimento muito mais elevado.

Os seguintes sanitizadores têm suporte incorporado em AFL++:

* ASAN = Endereço SANitizer, encontra vulnerabilidades de corrupção de memória como
use-after-free, NULL ponteiro desreference, buffer overruns, etc Habilitado com
`export AFL_USE_ASAN=1` antes de compilar.
* MSAN = Memory SANitizer, encontra acessos de leitura à memória não inicializada, por exemplo, a
variável local que é definida e lida antes mesmo de estar definida. Activada com
`export AFL_USE_MSAN=1` antes de compilar.
* UBSAN = Sanitizer Comportamento Indefinido, encontra instâncias onde - pelos C e C++
padrões - comportamento indefinido acontece, por exemplo, adicionando dois inteiros assinados onde
o resultado é maior do que o que um inteiro assinado pode conter. Habilitado com `export
AFL_USE_UBSAN=1` antes de compilar.
* CFISAN = Control Flow Integrity SANitizer, encontra instâncias onde o controle
o fluxo é encontrado para ser ilegal. Originalmente isto foi para evitar o retorno
programação orientada (ROP) explorar cadeias de funcionamento. Em fuzzing, este
reduz-se, na sua maioria, à detecção de vulnerabilidades de confusão de tipo - ou seja,
no entanto, uma das mais importantes e perigosas corrupção de memória C++
classes! Activado com o `export AFL_USE_CFISAN=1` antes de compilar.
* TSAN = Thread SANitizer, encontra as condições de corrida de thread. Activado com `export
AFL_USE_TSAN=1` antes de compilar.
* LSAN = Leak SANitizer, encontra vazamentos de memória em um programa.
problema de segurança, mas para os desenvolvedores isso pode ser muito valioso.
os outros higienizadores acima deste precisa `__AFL_LEAK_CHECK();` adicionado a todas as áreas
do código fonte alvo onde você encontra uma verificação de vazamento necessária! Activado com
`export AFL_USE_LSAN=1` antes de compilar. Para ignorar a verificação de perda de memória
para certas alocações, `__AFL_LSAN_OFF();` pode ser usado antes da memória é
alocado, e `__AFL_LSAN_ON();` depois. Memória alocada entre estes
duas macros não serão verificadas por vazamentos de memória.

É possível modificar ainda mais o comportamento dos higienizadores em tempo de execução por
definindo `ASAN_OPTIONS=...`, `LSAN_OPTIONS` etc. - os parâmetros disponíveis podem
ser pesquisado na documentação de higienizador de llvm/clang. afl-fuzz, no entanto,
necessita de alguns parâmetros específicos importantes para o fuzzing. Se quiser
Para definir o seu próprio, ele pode sair e relatar o que está faltando.

Note que alguns higiénicos não podem ser utilizados em conjunto, por exemplo, ASAN e MSAN, e
outros frequentemente não podem trabalhar em conjunto por causa da estranheza do alvo, por exemplo, ASAN e
CFISAN. Você pode precisar experimentar quais higienizadores você pode combinar em um
alvo (o que significa que mais instâncias podem ser executadas sem um alvo higienizado, que
é mais eficaz).

Note que alguns higiénicos (MSAN e LSAN) saem com um código de saída específico
em vez de abortar. Afl-fuzz trata estes códigos de saída como um acidente quando estes
os sanitizers estão habilitados. Se o alvo usar estes códigos de saída, poderá haver false
positivos entre as falhas salvas. LSAN usa código de saída 23 e MSAN usa saída
Código 86.

### d) Modificação do alvo

Se o alvo tiver funcionalidades que tornem o fuzzing mais difícil, por exemplo, somas de verificação,
HMAC, etc., em seguida, modificar o código fonte para que as verificações para estes valores são
removido. Isto pode até ser feito com segurança para o código- fonte usado no funcionamento
produtos, eliminando estes controlos dentro destes blocos específicos AFL++:

```text
#ifdef FUZZING_BUILD_MODE_UNSAFE_FOR_PRODUCTION
  // say that the checksum or HMAC was fine - or whatever is required
  // to eliminate the need for the fuzzer to guess the right checksum
  return 0;
#endif
```

Todos os compiladores AFL++ definirão esta definição de pré-processador automaticamente.

### e) Instrumentação do objectivo

Nesta etapa, o código fonte alvo é compilado para que ele possa ser fuzzed.

Basicamente, você tem que dizer ao sistema de compilação de destino que o AFL++ selecionado
é usado o compilador. Também - se possível - você deve configurar sempre a compilação
sistema de tal forma que o alvo é compilado estática e não dinamicamente.
Como fazer isso é descrito abaixo.

A regra #1 ao instrumentar um alvo é: evitar instrumentar bibliotecas compartilhadas
a todo o custo. Você precisaria definir `LD_LIBRARY_PATH` para apontar para estes, você
poderia acidentalmente digitar "make install" e instalá-los sistema amplo - por isso não.
Realmente não. **Sempre compile bibliotecas que você deseja ter instrumentado como estática
e ligue estes ao programa alvo!**

Em seguida, construa o alvo. (Geralmente com `make`.)

**NOTES**

1. Às vezes configurar e construir sistemas são inconstantes e não gostam stderr
saída (e pensar que isto significa uma falha de teste) - que é algo que AFL++ gosta
para mostrar estatísticas. Recomenda- se desactivar a instrumentação AFL++
reportar através do `export AFL_QUIET=1`.

2. Às vezes configurar e construir erros de sistemas em avisos - estes devem ser
desabilitado (por exemplo, `--disable-werror` para alguns scripts de configuração).

3. Caso o sistema configure/build reclame sobre o compilador de AFL++ e
aborta, então defina o `export AFL_NOOPT=1` que então se comportará como o
compilador real e execute o passo de configuração separadamente. Para construir o alvo
depois esta opção tem que ser desactivada novamente!

#### configurar

Para sistemas de compilação `configure`, isso geralmente é feito por:

```text
CC=afl-clang-fast CXX=afl-clang-fast++ ./configure --disable-shared
```

Note que se você estiver usando o compilador (melhor) afl-clang-lto, você também tem que
definir `AR` para lvm-ar[-VERSION] e `RANLIB` para lvm-ranlib[-VERSION] - tal como está
descrito em [instrumentação/README.lto.md](https://github.com/AFLplusplus/AFLplusplus/blob/d0070729206a80a9af297b2341edd63f68fdac35/instrumentation/README.lto.md).

#### CMake

Para os sistemas de compilação CMake, isso geralmente é feito por:

```text
mkdir build; cd build; cmake -DCMAKE_C_COMPILER=afl-cc -DCMAKE_CXX_COMPILER=afl-c++ ..
```

Note que se você estiver usando o compilador afl-clang-lto (melhor) você também tem que
definir AR para lvm-ar[-VERSION] e RANLIB para llvm-ranlib[-VERSION] - tal como é
descrito em [instrumentação/README.lto.md](https://github.com/AFLplusplus/AFLplusplus/blob/d0070729206a80a9af297b2341edd63f68fdac35/instrumentation/README.lto.md).

#### Sistema de Compilação de Mesão

Para o Meson Build System, você tem que definir o compilador AFL++ com
Primeiro comando!

```text
CC=afl-cc CXX=afl-c++ meson
```

#### Outros sistemas de compilação ou se configurar/cmake não funcionou

Às vezes `cmake` e `configure` não captam o compilador AFL++ ou o
`RANLIB`/`AR` que é necessário - porque isso simplesmente não foi previsto pelo
desenvolvedor do alvo. Ou eles têm opções não- padrão. Descubra se existe
é uma forma não- padrão de configurar isto, caso contrário configurar a compilação normalmente e editar
o ambiente de compilação gerado posteriormente manualmente para apontá-lo para a direita
compilador (e/ou `RANLIB` e `AR`).

Em complexos, estranhos, sistemas de construção alienígena você pode tentar este projeto puro:
[https://github.com/fuzzah/exeptor](https://github.com/fuzzah/exeptor)

#### Scripts do linker

Se o projeto usar scripts do linker para ocultar os símbolos exportados pelo
binário, então você pode ver erros como:

```text
undefined symbol: __afl_area_ptr
```

A solução é modificar o script linker para adicionar:

```text
{
  global:
    __afl_*;
}
```

### f) Melhor instrumentação

Se você apenas fuzz um programa alvo como-is, você está desperdiçando uma grande oportunidade para
muito mais velocidade fuzzing.

Esta variante requer a utilização de afl-clang-lto, afl-clang-fast ou
Afl-gcc-fast.

É o chamado `persistent mode`, que é muito, muito mais rápido, mas requer
que você codifica um arquivo fonte que está especificamente chamando as funções de destino
que você quer fuzz, mais algumas funções específicas AFL++ em torno dele. Veja
[instrumentação/README.persistant_mode.md](https://github.com/AFLplusplus/AFLplusplus/blob/d0070729206a80a9af297b2341edd63f68fdac35/instrumentation/README.persistent_mode.md)
para mais pormenores.

Basicamente, se você não fuzz um alvo em modo persistente, então você é apenas
fazendo-o por um hobby e não profissionalmente :-).

### g) Arreios libfuzzer fuzzer com LLVMFuzzerTestOneInput()

libfuzzer `LLVMFuzzerTestOneInput()` arneses são o padrão defacto para
fuzzing, e eles podem ser usados com AFL++ (e honggfuzz) também!

Compilar é tão simples como:

```text
afl-clang-fast++ -fsanitize=fuzzer -o harness harness.cpp targetlib.a
```

Você pode até usar recursos avançados de libfuzzer como `FuzzedDataProvider`,
`LLVMFuzzerInitialize()` etc. e eles vão funcionar!

O binário gerado é fuzzed com afl-fuzz como qualquer outro alvo fuzz.

Bônus: o alvo já está otimizado para fuzzing devido ao modo persistente e
casos de teste de memória compartilhada e, portanto, dá-lhe a velocidade mais rápida possível.

Para mais informações, consultar
[utils/aflpp_driver/README.md](https://github.com/AFLplusplus/AFLplusplus/blob/d0070729206a80a9af297b2341edd63f68fdac35/utils/aflpp_driver/README.md).

Escrever um arnês que realmente exerce as partes interessantes do alvo é
uma habilidade própria. Para uma caminhada prática do que faz um arnês
eficaz - e os erros comuns que aleijam um - ver
[https://srlabs.de/blog/unlocking-secrets-effective-fuzzing-harness](https://srlabs.de/blog/unlocking-secrets-effective-fuzzing-harness).

## 2. Preparando a campanha fuzzing

Como você fuzz o alvo com entrada mutada, tendo como entradas diversas para o
O alvo, tanto quanto possível, melhora muito a eficiência.

### a) Recolha de entradas

Para funcionar corretamente, o fuzzer requer um ou mais arquivos iniciais que
conter um bom exemplo dos dados de entrada normalmente esperados pelo alvo
aplicação.

Tente reunir entradas válidas para o alvo de onde quer que você possa. Por exemplo, se for
o formato de imagem PNG, tente encontrar o maior número possível de arquivos PNG, por exemplo, de
bugs reportados, suítes de teste, downloads aleatórios da internet, caso de teste unitário
dados - de todo o tipo de software PNG.

Se o formato de entrada não for conhecido, você também pode modificar um programa de destino para escrever
dados normais que recebe e processa para um arquivo e usa estes.

Você pode encontrar muitos bons exemplos de iniciar arquivos no
Subdiretório [casos de ensaio/](https://github.com/AFLplusplus/AFLplusplus/blob/d0070729206a80a9af297b2341edd63f68fdac35/testcases) que vem com esta ferramenta.

### b) Tornar o corpus de entrada único

Use a ferramenta AFL++ `afl-cmin` para remover entradas do corpus que não
Produzir um novo caminho/cobertura no alvo:

1. Coloque todos os arquivos do [passo a](#a-recolha-de-entradas) em uma pasta, por exemplo,
`INPUTS`.
2. Executar afl-cmin:
   * Se o programa alvo for chamado por fuzzing como `bin/target INPUTFILE`,
     replace the INPUTFILE argument that the target program would read from with
     `@@`:

     ```text
     afl-cmin -i INPUTS -o INPUTS_UNIQUE -- bin/target -someopt @@
     ```

   * Se o alvo for lido do stdin (input padrão), basta omitir o `@@`
     as this is the default:

     ```text
     afl-cmin -i INPUTS -o INPUTS_UNIQUE -- bin/target -someopt
     ```

Este passo é altamente recomendado, porque depois o corpo de teste não é
inchada com duplicatas ainda, o que atrasaria o progresso do fuzzing!

Para em vez *add* apenas as entradas que dão nova cobertura para um já existente
corpus (como `-merge=1` da libFuzzer), use `afl-merge`. Ao contrário do `afl-cmin`, ele faz
não minimiza o diretório de saída em si, ele só adiciona entradas que cobrem
algo que o corpus de saída já não cobre:

```text
afl-merge -o CORPUS -i NEW_INPUTS -- bin/target -someopt @@
```

O corpus de saída também pode ser dado como o primeiro diretório (então `-i` não deve
ser usado), e `-o` pode aparecer no início ou no fim:

```text
afl-merge CORPUS NEW_INPUTS1 NEW_INPUTS2 -- bin/target -someopt @@
```

### c) Minimizar todos os arquivos de corpus

Quanto mais curtos os arquivos de entrada que ainda atravessam o mesmo caminho dentro do alvo,
quanto melhor o fuzzing será. Esta minimização é feita com `afl-tmin`,
no entanto, é um processo longo como este tem que ser feito para cada arquivo:

```text
mkdir input
cd INPUTS_UNIQUE
for i in *; do
  afl-tmin -i "$i" -o "../input/$i" -- bin/target -someopt @@
done
```

Este passo também pode ser paralelizado, por exemplo, com `parallel`.

Note que este passo é bastante opcional embora.

### Feito!

A pasta INPUTS_ UNIQUE/ do [passo b](#b-tornar-o-corpus-de-entrada-único) -
ou até melhor a entrada do diretório/ se você minimizou o corpus em
[passo c](#c-minimizar-todos-os-arquivos-de-corpus) - é o corpus de entrada resultante
diretório a ser usado em fuzzing! :-)

## 3. Fuzzing o alvo

Nesta etapa final, fuzz o alvo. Não há muitas opções importantes
para executar o alvo - a menos que você queira usar muitos núcleos/threads de CPU para o
fuzzing, que tornará o fuzzing muito mais útil.

Se você apenas usar uma instância para fuzzing, então você é fuzzing apenas por diversão e
não é grave :-)

### a) Correndo afl-fuzz

Antes mesmo de fazer uma execução de teste de afl-fuzz, execute o `sudo afl-system-config` (on
a máquina se você executar o afl- fuzz em um recipiente Docker). Isto reconfigura o
sistema para a velocidade ideal - que afl-fuzz verifica e fianças de outra forma.
`export AFL_SKIP_CPUFREQ=1` para o afl-fuzz saltar esta verificação se não conseguir correr
afl-system-config com privilégios de root no host por qualquer razão.

Nota:

* Há também `sudo afl-persistent-config` que define permanente adicional
opções de inicialização para um desempenho muito melhor fuzzing.
* Ambos os scripts melhorar o seu desempenho fuzzing, mas também diminuir o seu sistema
proteção contra ataques! Assim, definir regras de firewall fortes e apenas expor SSH
como um serviço de rede se você usar estes (o que é altamente recomendado).

Se executar o afl- fuzz num contentor Docker, recomenda- se passar a opção [`--cpuset-cpus`](https://docs.docker.com/engine/containers/resource_constraints/#configure-the-default-cfs-scheduler) com núcleos de CPU gratuitos para docker daemon ao iniciar o contentor, ou passar o `AFL_NO_AFFINITY` para afl- fuzz. Isto deve- se ao facto de o AFL++ se ligar a um núcleo de CPU livre por omissão, enquanto o contentor Docker irá impedir que a instância AFL++ veja os processos noutros contentores ou máquina, o que leva a todas as instâncias AFL++ que tentam ligar o mesmo núcleo de CPU.

Se você tiver um corpus de entrada do [passo 2](#2-preparando-a-campanha-fuzzing),
em seguida, especifique este diretório com a opção `-i`. Caso contrário, crie um novo
diretório e criar um arquivo com qualquer conteúdo como dados de teste lá.

Se você não quer nada de especial, os padrões já são geralmente melhores,
por isso tudo que você precisa é especificar o diretório de entrada de sementes com o resultado de
passo [2a) Recolha de entradas](#a-recolha-de-entradas):

```text
afl-fuzz -i input -o output -- bin/target -someopt @@
```

Note que o diretório especificado com `-o` será criado se não for
Existir.

Ele pode ser valioso para executar afl-fuzz em um `screen` ou `tmux` shell para que você possa registrar
off, ou o afl-fuzz não é abortado se estiver a executá- lo numa sessão ssh remota
onde a conexão falha no meio. Só faça isso uma vez que você tiver
verificou se a sua configuração fuzzing funciona! Execute-a como `screen -dmS afl-main --
afl-fuzz -M main-$HOSTNAME -i ...` e ele vai começar em uma sessão de tela.
Para entrar nesta sessão, digite `screen -r afl-main`. Veja - faz sentido
nomeia a sessão de tela como o nome do afl-fuzz `-M`/`-S` :-) Para mais
informações no tela ou tmux, verificar a sua documentação.

Se você precisar parar e reiniciar o fuzzing, use as mesmas opções de linha de comando
(ou até mesmo alterá-los selecionando um calendário de potência diferente ou outra mutação
modo!) e alternar o diretório de entrada com um traço (`-`):

```text
afl-fuzz -i - -o output -- bin/target -someopt @@
```

Adicionar um dicionário é útil. Você tem as seguintes opções:

* Veja o diretório
[dicionários/](https://github.com/AFLplusplus/AFLplusplus/blob/d0070729206a80a9af297b2341edd63f68fdac35/dictionaries), se algo já está incluído para o seu
formato de dados, e diga afl-fuzz para carregar esse dicionário adicionando `-x
dicionários/format.dict».
* Com `afl-clang-lto`, você tem uma geração de autodictionary para a qual você precisa
para não fazer nada além de usar o afl-clang-lto como compilador.
* Com `afl-clang-fast`, você pode definir
`AFL_LLVM_DICT2FILE=/full/path/to/new/file.dic` para gerar automaticamente um
dicionário durante a compilação alvo.
Adicionando `AFL_LLVM_DICT2FILE_NO_MAIN=1` para não processar o main (normalmente linha de comando
parâmetro de análise) é muitas vezes uma boa idéia também.
* Você também tem a opção de gerar um dicionário você mesmo durante um
corrida independente do alvo, ver
[utils/libtokencap/README.md](https://github.com/AFLplusplus/AFLplusplus/blob/d0070729206a80a9af297b2341edd63f68fdac35/utils/libtokencap/README.md).
* Finalmente, você também pode escrever um arquivo de dicionário manualmente, é claro.

afl-fuzz tem uma variedade de opções que ajudam a contornar as peculiaridades do alvo, como
locais muito específicos para o arquivo de entrada (`-f`), realizando determinístico
fuzzing (`-D`) e muitos mais. Confira `afl-fuzz -h`.

Recomendamos que você defina um limite de memória para executar o alvo com `-m`
que define a memória máxima em MB. Isto previne uma potencial extra- memória
problema para o seu sistema mais ajuda você a detectar falha `malloc()` faltando
lidar com o alvo. Jogue com vários valores `-m` até encontrar um
que funciona com segurança para todas as suas sementes de entrada (se você tem boas e, em seguida,
duplo ou quádruplo isso).

Por padrão, o afl-fuzz nunca pára o fuzzing. Para terminar o AFL++, pressione Control-C ou
enviar um sinal SIGINT. Você pode limitar o número de execuções ou aproximar
tempo de execução em segundos com opções também.

Quando você iniciar afl-fuzz, você verá uma interface de usuário que mostra o que o
status é:

[Imagem/recurso externo: resources/screenshot.png](https://github.com/AFLplusplus/AFLplusplus/blob/d0070729206a80a9af297b2341edd63f68fdac35/docs/resources/screenshot.png)

Todos os rótulos são explicados em
[afl-fuzz_approach.md#compreendendo-o-estado-tela](aflplusplus-docs-afl-fuzz-approach-md.md#understanding-the-status-screen).

### b) Manter o uso da memória e os intervalos de tempo em cheque

Os limites de memória não são aplicados pelo afl-fuzz por padrão e o sistema pode acabar
Você pode diminuir a memória com a opção `-m`, o valor está em MB.
Se isto é muito pequeno para o alvo, normalmente você pode ver isso por afl-fuzz
fiança com a mensagem de que ele não pôde se conectar ao servidor de garfos.

Considere definir valores baixos para `-m` e `-t`.

Para programas que são nominalmente muito rápido, mas ficar lento para algumas entradas, você
também pode tentar definir valores `-t` que são mais puníveis do que o que `afl-fuzz`
se atreve a usar por conta própria. Em máquinas rápidas e ociosas, descer para `-t 5` pode ser
Um plano viável.

O parâmetro `-m` também vale a pena olhar. Alguns programas podem acabar gastando
justo tempo alocando e inicializando megabytes de memória quando
Os valores baixos de `-m` podem fazê-los desistir mais cedo
e não perder tempo com a CPU.

### c) Usando múltiplos núcleos

Se você quer seriamente fuzz, em seguida, use tantos núcleos / threads como possível para
Foca o teu alvo.

Na mesma máquina - devido ao design de como funciona AFL++ - há um máximo
número de núcleos/threads de CPU que são úteis, use mais e o global
o desempenho degrada- se em vez disso. Este valor depende do alvo, e o limite é
entre 32 e 64 núcleos por máquina.

Se você tem a RAM, é altamente recomendado executar as instâncias com um cache
dos casos de teste. Dependendo do tamanho médio do caso de teste (e aqueles encontrados
durante o fuzzing) e seu número, um valor entre 50-500MB é recomendado.
pode definir o tamanho do cache (em MB) definindo a variável de ambiente
`AFL_TESTCACHE_SIZE`.

O cache mantém os casos de teste com a maior probabilidade de seleção por byte,
recomputado sempre que a fila muda, então aumentar o tamanho continua melhorando o
taxa de hit em vez de preencher com entradas arbitrárias.

Deve haver um fuzzer principal (`-M main-$HOSTNAME` opção - definir também
`AFL_FINAL_SYNC=1`) e tantos fuzzers secundários (por exemplo, `-S variant1`) como você
tem núcleos que você usa. Cada entrada `-M`/`-S` precisa de um nome único (que pode ser
seja o que for), no entanto, o mesmo `-o` localização de saída diretório tem que ser usado para
todos os casos.

Para cada fuzzer secundário deve haver uma variação, por exemplo:
* deve-se fuzz o alvo que foi compilado com higienizadores ativados
(`export AFL_USE_ASAN=1 ; export AFL_USE_UBSAN=1 ; export AFL_USE_CFISAN=1`)
* um ou dois devem fuzz o alvo com CMPLOG/redqueen (ver acima), pelo menos
uma instância cmplog deve seguir transformações (`-l 2AT`)
* um a três fuzzers devem fuzz um alvo compilado com laf-intel/COMPCOV (ver
Nota importante: se executar mais de um laf-intel/COMPCOV fuzzer e
você quer que eles compartilhem seus resultados intermediários, o fuzzer principal (`-M`) deve
seja um deles (embora isso não seja realmente recomendado).

Os outros secundários devem ser executados assim:
* 10% deve usar a fila antiga de ciclismo com `-Z`
* 50- 70% devem ser executados com `AFL_DISABLE_TRIM`
* 40% deve ser executado com `-P explore` e 20% com `-P exploit`
* Se você usar o `-a`, então defina 30% das instâncias para não usar o `-a`; se você fez
não definir `-a` (por quê??), então definir 30% para `-a ascii` e 30% para `-a binary`.
* executar cada um com um calendário de potência diferente, recomendado são: `explore` (padrão),
`fast`, `coe`, `lin`, `quad`, `exploit` e `rare` que você pode definir com
a opção `-p`, por exemplo, `-p explore`.
[Perguntas Frequentes](aflplusplus-docs-faq-md.md#what-are-power-schedules) para detalhes.

Pode ser útil para definir `AFL_IGNORE_SEED_PROBLEMS=1` para saltar sobre sementes que
falha ou tempo- limite durante a inicialização.

Além disso, recomenda-se definir `export AFL_IMPORT_FIRST=1` para carregar casos de teste
de outros fuzzers na campanha primeiro. Mas note que pode retardar o início
do primeiro fuzz por bastante se você tiver muitos fuzzers e/ou muitas sementes.

Se você tem um corpus grande, um corpus de uma execução anterior ou são fuzzing em um CI,
então também definir `export AFL_CMPLOG_ONLY_NEW=1` e `export AFL_FAST_CAL=1`.
Se a fila no CI é enorme e/ou o tempo de execução é lento, então você pode
também adicione `AFL_NO_STARTUP_CALIBRATION=1` para pular a calibração inicial da fila
fase e iniciar fuzzing de uma só vez - mas só fazer isso se a fase de calibração
Seria muito tempo para o teu tempo de fuga.

Você também pode usar diferentes fuzzers. Se você estiver usando spinoffs AFL ou AFL
conformando fuzzers, em seguida, basta usar o mesmo diretório -o e dar-lhe um único
Nome `-S`. Exemplos são:
* [Fuzzolic](https://github.com/season-lab/fuzzolic)
* [symcc](https://github.com/eurecom-s3/symcc/)
* [Eclipser](https://github.com/SoftSec-KAIST/Eclipser/)
* [AFLsmart](https://github.com/aflsmart/aflsmart)
* [FairFuzz](https://github.com/carolemieux/afl-rb)
* [Neuzz](https://github.com/Dongdongshe/neuzz)
* [Angora](https://github.com/AngoraFuzzer/Angora)

Uma lista longa pode ser encontrada em
[https://github.com/Microsvuln/Awesome-AFL](https://github.com/Microsvuln/Awesome-AFL).

No entanto, você também pode sincronizar AFL++ com hongggfuzz, libfuzzer com `-entropic=1`,
Basta mostrar o fuzzer principal (`-M`) com a opção `-F` onde a fila / trabalho
diretório de um fuzzer diferente é, por exemplo, `-F /src/target/honggfuzz`. Usando
honggfuzz (com `-n 1` ou `-n 2`) e libfuzzer em paralelo é altamente
Recomendado!

### d) Usando várias máquinas para fuzzing

Talvez você tenha mais de uma máquina que você quer fuzz o mesmo alvo em. Iniciar
a orquestra `afl-fuzz` (e talvez libfuzzer, honggfuzz, ...) como quiser,
basta garantir que você tenha uma única instância `-M` por servidor, e que
seu nome é único, daí a recomendação para `-M main-$HOSTNAME`.

Agora existem três estratégias sobre como você pode sincronizar entre os servidores:
* nunca: soa estranho, mas isso faz de cada servidor uma ilha e tem a chance
que cada um segue caminhos diferentes para o alvo. Você pode fazer isso ainda mais
interessante, mesmo dando sementes diferentes para cada servidor.
* regularmente (~4h): isso garante que todas as campanhas fuzzing nos servidores "ver"
A mesma coisa. É como fuzzing em um servidor enorme.
* em intervalos de 1/10 do tempo de execução esperado total do fuzzing
sincronizar. Isto tenta um pouco combinar ambos. Tenha alguma individualidade dos caminhos
cada campanha em um servidor explora, por outro lado, se um fica preso onde
outro progresso encontrado que é entregue fazendo com que ele desencaixe.

O processo de sincronização em si é muito simples. Como instância `-M main-$HOSTNAME`
sincroniza com todos os segundos do `-S`, bem como com outros fuzzers, você tem que copiar apenas
este diretório para as outras máquinas.

Digamos que todos os servidores têm o diretório `-o out` em /target/foo/out, e você
criou um arquivo `servers.txt` que contém os nomes das máquinas de todos os participantes
servidores, além de ter uma chave ssh implantada em todos eles, então execute:

```bash
for FROM in `cat servers.txt`; do
  for TO in `cat servers.txt`; do
    rsync -rlpogtz --rsh=ssh $FROM:/target/foo/out/main-$FROM $TO:target/foo/out/
  done
done
```

Você pode executar isso manualmente, por trabalho do cron - como você precisa dele. Há um mais
script complexo e configurável em
[utils/distributed_fuzzing](https://github.com/AFLplusplus/AFLplusplus/blob/d0070729206a80a9af297b2341edd63f68fdac35/utils/distributed_fuzzing).

Uma instância capta apenas tais casos de teste recém- copiados com o seu próximo
sincronização programada, que pode ser até `AFL_SYNC_TIME` (20 minutos por padrão)
Para fazer a sincronização imediatamente, envie-lhe um `SIGUSR2`, por exemplo.
`killall -USR2 afl-fuzz`. A sincronização - do diretório de sincronização `-M`/`-S`, bem como
de todos os diretórios estrangeiros `-F` - é executado assim que a entrada da fila que
está atualmente sendo fuzzed está feito, por isso ele não joga fora nenhum trabalho.

### e) O status da campanha de fuzz

AFL++ vem com o script `afl-whatsup` para mostrar o status do fuzzing
campanha.

Basta fornecer o diretório que o afl-fuzz é dado com a opção `-o` e você
verá um status detalhado de cada fuzzer nessa campanha mais um resumo.

Para ter apenas o resumo, use o interruptor `-s`, por exemplo, `afl-whatsup -s out/`.

Se você tem vários servidores, então use o comando após uma sincronização ou você tem que
execute este script por servidor.

Para uma análise mais profunda do que o resumo `afl-whatsup`, use `afl-health`.
de apenas listar os números que diagnostica a campanha e emite um veredito
(`healthy`, `degraded`, `stalled`, `misconfigured`, `dead`, ou - se não
O `fuzzer_stats` foi encontrado em tudo - `no_instances`), um
tendência cross-run, e uma lista classificada de recomendações concretas e acionáveis (por exemplo,
triagem quebra, injetar sementes, adicionar uma instância CMPLOG, investigar baixa estabilidade).
É somente leitura - nunca modifica a campanha que inspeciona - e compreende
Directórios de saída AFL++, carga- afl e ziggie. Como o `afl-whatsup`, você aponta- o
no diretório `-o`:

```bash
afl-health out/
```

Ao contrário do `afl-whatsup` ele pode alcançar campanhas em outras máquinas diretamente sobre ssh,
para que uma frota inteira possa ser verificada numa invocação sem sincronizar primeiro:

```bash
afl-health out/ user@host1:/target/foo/out user@host2:/target/foo/out
```

Ele também oferece `--json` (relatório legível por máquina, incluindo a ação
Directivas), `--summary` (uma linha por campanha / roll-up da frota), `--watch N`
(vivo atualizar a cada N segundos), `--on-change CMD` (executar um gancho quando uma campanha
inverte o estado ou ganha novas falhas) e processa códigos de saída adequados para cron/CI.

Um veredito `DEGRADED` menciona sempre a sua razão - `dead-instances`,
`low-stability`, `exec-slowdown`, ou uma combinação de `+`.
não estão mais correndo são ditos separados em vez de grudados juntos: `killed` (morreu
inesperadamente - OOM, SIGKILL, uma falha), `stopped` (desligar de forma limpa pelo usuário
ou por um limite `-V`/`-E`) e `leftover` (ran antes da execução atual
instâncias iniciadas, ou seja, uma geração de campanha anterior que não foi reiniciada).
Só a primeira conta contra o veredicto, tão deliberadamente parou ou se aposentou
as instâncias já não fazem uma campanha saudável parecer degradada.
do arquivo `fastresume.bin`, que afl-fuzz escreve apenas em um desligamento limpo
(por isso necessita de AFL++ >= 4,22a e sem `AFL_NO_FASTRESUME`; caso contrário a causa é
reportado como `unknown` e conta).

Outra ferramenta para inspecionar o estado atual e o histórico de uma instância específica é
afl-plot, que gera um arquivo index.html e gráficos que mostram como o
A instância fuzzing está a executar. A sintaxe é `afl-plot instance_dir web_dir`,
Por exemplo, `afl-plot out/default /srv/www/htdocs/plot`.

### f) Parar o fuzzing, reiniciar o fuzzing, adicionar novas sementes

Para parar uma corrida afl-fuzz, pressione Control-C.

Para reiniciar uma execução afl-fuzz, basta reutilizar a mesma linha de comando mas substituir o `-i
directório` with `-i -` or set `AFL_AUTORESUME=1`.

Se você quiser adicionar novas sementes a uma campanha fuzzing, você pode usar `afl-addseeds`:

```text
afl-addseeds -i newseeds-an-be-file-or-directory -o out-of-the-fuzzing-campaign
```

### g) Verificando a cobertura do fuzzing

O valor `corpus count` é um indicador ruim para verificar quão boa a cobertura
Sim.

Um indicador melhor - se você usar a instrumentação padrão do llvm com pelo menos
versão 9 - é usar `afl-showmap` com a opção de coleta de cobertura `-C` no
pasta de saída:

```text
$ afl-showmap -C -i out -o /dev/null -- ./target -params @@
...
[*] Using SHARED MEMORY FUZZING feature.
[*] Target map size: 9960
[+] Processed 7849 input files.
[+] Captured 4331 tuples (highest value 255, total values 67130596) in '/dev/nul
l'.
[+] A coverage of 4331 edges were achieved out of 9960 existing (43.48%) with 7849 input files.
```

É ainda melhor verificar as linhas exatas de código que foram alcançadas -
e que não foram encontrados até agora.

Um script de ajuda "fácil" para isso é
[https://github.com/AFLplusplus/cov-analysis](https://github.com/AFLplusplus/cov-analysis),
basta seguir o README.md do nosso projeto separado. Reproduz o corpus através
uma cobertura baseada em fontes LLVM constrói e produz relatórios de HTML/texto anotados.

Uma lacuna de cobertura só vale a pena ser perseguida se o arnês pode realmente alcançá-lo.
ferramenta de acompanhamento
[https://github.com/AFLplusplus/fuzz-reachability](https://github.com/AFLplusplus/fuzz-reachability)
calcula estaticamente o conjunto de funções que um ponto de entrada de fuzz pode alcançar (C, C++
Dê o seu relatório ao `cov-analysis` com o `--reachability` para ter a
relatório de cobertura dill apart code that is *achable but not atinged yet* (o
gap acionável) do código que é *uneachable* pelo arnês (esperado para ficar
descoberto, tão seguro para ignorar).

Para uma análise de como ler tais relatórios de cobertura e transformá-los em
passos próximos concretos para uma campanha, ver
[https://srlabs.de/blog/coverage-analysis](https://srlabs.de/blog/coverage-analysis).

Se você vê que uma área importante ou uma característica não foi coberta até agora, então
tentar encontrar uma entrada que seja capaz de chegar a isso e iniciar um novo secundário em
que fuzzing campanha com essa semente como entrada, deixá-lo correr por alguns minutos,
em seguida, terminá- lo. O nó principal irá pegá- lo e torná-lo disponível para o
outros nós secundários ao longo do tempo. Defina `export AFL_NO_AFFINITY=1` ou `export
AFL_TRY_AFINITY=1` se você não tem núcleo livre.

Note que em quase todos os casos você nunca pode alcançar a cobertura completa.
a funcionalidade é geralmente dependente de opções exclusivas que necessitam
campanhas individuais fuzzing cada com uma destas opções definidas. Por exemplo, se você
fuzz uma biblioteca para converter formatos de imagem e seu alvo é o png para tiff API,
então você não tocará em nenhuma das outras APIs e recursos da biblioteca.

### h) Quanto tempo demora a furar um alvo?

Esta é uma pergunta difícil. Basicamente, se nenhum caminho novo é encontrado por um longo tempo
(por exemplo, durante um dia ou uma semana), então você pode esperar que o seu fuzzing não será
frutífero ainda mais. No entanto, muitas vezes isso só significa que você deve mudar para fora
secundaries for others, por exemplo, módulos de mutadores personalizados, sincronizar com muito diferentes
Fuzzers, etc.

Manter a fila/ directório (para fuzzings futuros dos mesmos ou alvos semelhantes)
e usá-los para semear outros bons fuzzers como libfuzzer com o interruptor -entrópico
Ou Honggfuzz.

### i) Melhorar a velocidade!

* Usar o [modo persistente](https://github.com/AFLplusplus/AFLplusplus/blob/d0070729206a80a9af297b2341edd63f68fdac35/instrumentation/README.persistent_mode.md) (x2- x20
aumento de velocidade).
* Se você não usar o modo persistente shmem, use `AFL_TMPDIR` para apontar a entrada
arquivo em uma localização tempfs, veja [env_variables.md](aflplusplus-docs-env-variables-md.md).
* Linux: Melhorar o desempenho do kernel: modificar `/etc/default/grub`, definir
`GRUB_ CMDLINE_ LINUX_ DEFAULT="ibpb=off ibrs=off kpti=off l1tf=off mds=off
mitigação=off no_stf_barrier noibpb noibrs nopcid nopti
nospec_ store_ bypass_ disable nospectre_ v1 nospectre_ v2 pcid=off pti=off
spec_store_bypass_ disable=off spectre_v2=off stf_barrier=off"`; então
`update-grub` e `reboot` (alertar: torna o sistema mais inseguro) - você pode
também basta executar `sudo afl-persistent-config`.
* Linux: Executando em um sistema de arquivos `ext2` com opção de montagem `noatime` será uma
bit mais rápido do que em qualquer outro sistema de arquivos de diário.
* Veja [3c) Usando múltiplos núcleos](#c-usando-múltiplos-núcleos).
* Executar o `sudo afl-system-config` antes de iniciar a primeira instância afl-fuzz após
uma reinicialização.

### j) Indo além dos acidentes

Fuzzing é uma técnica maravilhosa e subutilizada para descobrir não-crashing
erros de design e implementação, também. Alguns erros interessantes foram
encontrado modificando os programas de destino para chamar `abort()` quando dizer:

- Duas bibliotecas bignum produzem saídas diferentes quando dadas as mesmas
Entrada gerada pelo fuzzer.

- Uma biblioteca de imagens produz diferentes saídas quando solicitado para decodificar o mesmo
input image várias vezes consecutivas.

- Uma biblioteca de serialização/desserialização não consegue produzir saídas estáveis quando
serialização iterativa e desserialização de dados fornecidos pelo fuzzer.

- Uma biblioteca de compressão produz uma saída inconsistente com o arquivo de entrada quando
pediu para comprimir e depois descomprimir uma bolha em particular.

A implementação destes ou similares controlos de sanidade geralmente leva muito pouco tempo; se
você é o mantenedor de um determinado pacote, você pode fazer este código
condicional com `#ifdef FUZZING_BUILD_MODE_UNSAFE_FOR_PRODUCTION` (uma bandeira também
compartilhado com libfuzzer e honggfuzz) ou `#ifdef __AFL_COMPILER` (este é
apenas para AFL++).

### k) Limitações e áreas conhecidas para melhoria

Aqui estão algumas das advertências mais importantes para AFL++:

- AFL++ detecta falhas verificando se o primeiro processo desovado está morrendo devido a
sinal (SIGSEGV, SIGABRT, etc.). Programas que instalam manipuladores personalizados para
estes sinais podem necessitar ter o código relevante comentado para fora.
veia, falhas nos processos infantis gerados pelo alvo fuzzed podem fugir
detecção a menos que você adicione manualmente algum código para pegar isso.

- Como em qualquer outra ferramenta de força bruta, o fuzzer oferece cobertura limitada se
criptografia, somas de verificação, assinaturas criptográficas ou compressão são usados para
Enrole totalmente o formato de dados real a ser testado.

Para trabalhar em torno disso, você pode comentar as verificações relevantes (ver
utils/libpng_no_checksum/ para inspiração); se isto não for possível, você pode
também escreva um pós-processador, um dos ganchos de mutantes personalizados. Veja
[custom_ mutators. md](aflplusplus-docs-custom-mutators-md.md) sobre como utilizar
`AFL_CUSTOM_MUTATOR_LIBRARY`.

- Há alguns desafortunados acordos com a ASAN e os binários de 64 bits.
Não é devido a qualquer falha específica de afl-fuzz.

- Não há suporte direto para serviços de rede fuzzing, daemons de fundo,
ou aplicativos interativos que requerem interação de IU para funcionar.
simples alterações de código para fazê-los se comportar de uma forma mais tradicional. Preeny,
libdesock ou desockmulti também pode oferecer uma opção relativamente simples - veja:
[https://github.com/zardus/preeny](https://github.com/zardus/preeny) ou
[https://github.com/fkie-cad/libdesock](https://github.com/fkie-cad/libdesock)
[https://github.com/zyingp/desockmulti](https://github.com/zyingp/desockmulti)
Se estes falharem, então tente o nosso próprio que pode ser um pouco mais lento, mas é mais
confiável: [utils/libaflppdesoque](https://github.com/AFLplusplus/AFLplusplus/blob/d0070729206a80a9af297b2341edd63f68fdac35/utils/libaflppdesock)

Algumas dicas úteis para modificar serviços baseados em rede também podem ser encontradas em:
[https://www.fastly.com/blog/how-to-fuzz-server-american-fuzzy-lop](https://www.fastly.com/blog/how-to-fuzz-server-american-fuzzy-lop)

- Ocasionalmente, máquinas sencientes levantam-se contra os seus criadores.
para você, por favor consulte
[https://lcamtuf.coredump.cx/prep/](https://lcamtuf.coredump.cx/prep/).

Além disso, consulte [INSTALL. md](aflplusplus-docs-install-md.md) para dicas específicas da plataforma.

## 4. Triaging quebras

O agrupamento de falhas baseado em cobertura geralmente produz um pequeno conjunto de dados que
pode ser rapidamente triado manualmente ou com um script muito simples GDB ou Valgrind.
Cada falha também é rastreável para o seu caso de teste não-crashing pai na fila,
tornando mais fácil diagnosticar falhas.

Dito isso, é importante reconhecer que algumas falhas fuzzing pode ser
difícil de avaliar rapidamente para a exploração sem muita depuração e
trabalho de análise de código. Para ajudar com esta tarefa, afl-fuzz suporta um
Modo "exploração de lixo" ativado com a bandeira `-C`.

Neste modo, o fuzzer leva um ou mais casos de teste de queda como a entrada e
usa suas estratégias fuzzing orientadas por feedback para enumerar muito rapidamente todo o código
caminhos que podem ser alcançados no programa, mantendo-o no estado em queda.

Mutações que não resultam em um crash são rejeitadas; assim são quaisquer alterações que
não afetar o caminho de execução.

A saída é um pequeno corpus de arquivos que podem ser rapidamente examinados para ver
que grau de controlo o atacante tem sobre o endereço defeituoso, ou se
é possível passar por uma leitura inicial fora de limite - e ver o que mentiras
Por baixo.

Mais uma coisa: para minimizar o caso de teste, tente afl-tmin.
pode ser operado de uma forma muito simples:

```shell
./afl-tmin -i test_case -o minimized_result -- /path/to/program [...]
```

A ferramenta funciona com estoirar e casos de teste não- esmagamento iguais. No acidente
modo, aceitará alegremente binários instrumentados e não instrumentados.
não-crashing modo, o minimizer baseia-se na instrumentação padrão AFL++ para
tornar o arquivo mais simples sem alterar o caminho de execução.

O minimizador aceita a sintaxe `-m`, `-t`, `-f` e `@@` de uma forma
compatível com afl-fuzz.

Outra ferramenta em AFL++ é a ferramenta afl- analyze. Ela precisa de um arquivo de entrada, tenta
para inverter bytes sequencialmente e observar o comportamento do programa testado.
em seguida, color-code a entrada com base em quais seções parecem ser críticas e
que não são; embora não à prova de bala, muitas vezes pode oferecer rápidas insights sobre
formatos de arquivo complexos.

`casr-afl` de ferramentas [CASR](https://github.com/ispras/casr) fornece
Triagem confortável para quebras encontradas pelo AFL++. Os relatórios são agrupados e
conter gravidade e outras informações.
```shell
casr-afl -i /path/to/afl/out/dir -o /path/to/casr/out/dir
```

### Se as falhas não se reproduzirem

Às vezes, os resultados do AFL++ não podem ser reproduzidos.

Isso geralmente significa que os limites aplicados no momento do fuzzing que trava o
processo alvo, p. ex. o fim da memória, ou o limite de um ser `-m` definido
Atingido.

Se você fizer fuzzing persistente, então também é possível que o alvo mantenha
estado persistente (este é principalmente para AFL_LOOP/LLVMFuzzerTestOneInput type
Objectivos).
Neste caso, qualquer um dos fuzz com o env var `AFL_ALLOW_CORES` para criar núcleo
arquivos e analisá-los onde o dinheiro ocorre (demora para baixo fuzzing, então só usar
isto para análise), ou você recompila AFL++ com uma configuração config.h que permite
`AFL_PERSISTENT_RECORD` e `AFL_PERSISTENT_REPLAY_ARGPARSE`.
[Leia a documentação](https://github.com/AFLplusplus/AFLplusplus/blob/d0070729206a80a9af297b2341edd63f68fdac35/instrumentation/README.persistent_mode.md) sobre como
para configurar registro persistente em tempo de execução, e como reproduzir estes.


## 5. CI fuzzing

Algumas notas sobre integração contínua (CI) fuzzing - este fuzzing é diferente de
campanhas fuzzing normais como estes são muito mais curtos runs.

Se a fila no CI é enorme e/ou o tempo de execução é lento, então você pode
também adicione `AFL_NO_STARTUP_CALIBRATION=1` para pular a calibração inicial da fila
fase e iniciar fuzzing de uma vez. Mas só fazer isso se o tempo de calibração é
tempo demais para o seu fuzz total disponível tempo de execução.

1. Sempre:
    * LTO has a much longer compile time which is diametrical to short fuzzing -
      hence use afl-clang-fast instead.
    * If you compile with CMPLOG, then you can save compilation time and reuse
      that compiled target with the `-c` option and as the main fuzz target.
      This will impact the speed by ~15% though.
    * `AFL_FAST_CAL` - enables fast calibration, this halves the time the
      saturated corpus needs to be loaded.
    * `AFL_CMPLOG_ONLY_NEW` - only perform cmplog on new finds, not the initial
      corpus as this very likely has been done for them already.
    * If you do not like surprises then set `AFL_PIZZA_MODE=-1`
    * Keep the generated corpus, use afl-cmin and reuse it every time!

2. Além disso, randomize as opções de compilação AFL++, por exemplo:
    * 30% for `AFL_LLVM_CMPLOG`
    * 5% for `AFL_LLVM_LAF_ALL`

3. Também randomize as opções de execução do afl-fuzz, por exemplo:
    * 65% for `AFL_DISABLE_TRIM`
    * 50% for `AFL_KEEP_TIMEOUTS`
    * 50% use a dictionary generated by `AFL_LLVM_DICT2FILE` + `AFL_LLVM_DICT2FILE_NO_MAIN=1`
    * 40% for `AFL_EXPAND_HAVOC_NOW`
    * 20% for old queue processing (`-Z`)
    * for CMPLOG targets, 70% for `-l 2`, 10% for `-l 3`, 20% for `-l 2AT`

4. Fazer *not* executar qualquer modo `-M`, apenas executando modos `-S` é melhor para CI
fuzzing. O `-M` permite o tratamento de filas antigas, etc., o que é bom para um fuzzing
campanha, mas não é bom para curto CI corridas.

Como isso pode parecer pode, por exemplo, ser visto na configuração do AFL++ no Google
[versão anterior doss-fuzz](https://github.com/google/oss-fuzz/blob/3e2c5312417d1a6f9564472f3df1fd27759b289d/infra/base-images/base-builder/compile_afl)
e
[clusterfuzz](https://github.com/google/clusterfuzz/blob/master/src/clusterfuzz/_internal/bot/fuzzers/afl/launcher.py).

## Fim

Confira o [Perguntas Frequentes](aflplusplus-docs-faq-md.md). Talvez ele responda à sua pergunta (que você pode não
mesmo sabendo que você tinha ;-) ).

Isso é basicamente tudo que você precisa saber para executar campanhas fuzzing profissionalmente.
Se você quiser saber mais, as toneladas de textos em [dogs/](https://github.com/AFLplusplus/AFLplusplus/blob/d0070729206a80a9af297b2341edd63f68fdac35/docs) terá você
Coberto.

Note que também existem muitas ferramentas lá fora que ajudam fuzzing com AFL++
(alguns podem ser desactualizados ou não suportados), ver
[terceir_party_tools.md](aflplusplus-docs-third-party-tools-md.md).


---

## Procedência desta tradução

Fonte: [https://github.com/AFLplusplus/AFLplusplus](https://github.com/AFLplusplus/AFLplusplus/blob/d0070729206a80a9af297b2341edd63f68fdac35/docs/fuzzing_in_depth.md). Licença: [AGPL-3.0](../../99-Assets/upstream/aflplusplus/LICENSE.txt). Commit: d0070729206a80a9af297b2341edd63f68fdac35.

O original preservado, a lista de mudanças de apresentação e os hashes constam no manifesto do projeto. Nenhum exemplo desta documentação foi executado automaticamente.
