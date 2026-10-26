---
title: "aflplusplus — documentação oficial"
type: "official-documentation"
tool: "aflplusplus"
status: "translated-machine"
reviewed: "2026-10-26"
language: "pt-BR"
tags: ["documentation", "tool/aflplusplus"]
cssclasses: ["fieldbook"]
source_url: "https://github.com/AFLplusplus/AFLplusplus/blob/d0070729206a80a9af297b2341edd63f68fdac35/docs/best_practices.md"
source_commit: "d0070729206a80a9af297b2341edd63f68fdac35"
source_sha256: "0697a453310aeb9b7c47179a437d3dd333bc035453486cb79165c10a8db9f8b5"
license_spdx: "AGPL-3.0-or-later"
human_review: "pending"
source_scope: "Repository root README and owned doc/docs/documentation Markdown or RST files; not a claim of full wiki/site coverage"
---

> Tradução automática local para português, ainda sem revisão humana integral. Estrutura e blocos de código preservados; referências externas não significam conteúdo espelhado.

# Best practices

## Sumário

### Alvos

* [Fuzzing de um alvo com código fonte disponível](#fuzzing-de-um-alvo-com-código-fonte-disponível)
* [Fuzzing de um alvo com bibliotecas instrumentadas do dlopen ()](#fuzzing-de-um-alvo-com-bibliotecas-instrumentadas-do-dlopen)
* [Fuzzing de um alvo somente binário](#fuzzing-de-um-alvo-somente-binário)
* [Fuzzing um programa GUI](#fuzzing-um-programa-gui)
* [Fuzzing de um serviço de rede](#fuzzing-de-um-serviço-de-rede)

### Melhorias

* [Melhorar a velocidade](#melhorar-a-velocidade)
* [Melhorar a estabilidade](#melhorar-a-estabilidade)

## Alvos

### Fuzzing de um alvo com código fonte disponível

Para saber como furar um alvo se o código fonte estiver disponível, consulte
[fuzzing_in_profundish.md](aflplusplus-docs-fuzzing-in-depth-md.md).

### Fuzzing de um alvo com bibliotecas instrumentadas do dlopen

Se um alvo fuzzing baseado em código fonte carrega bibliotecas instrumentadas com
dolopen () após o servidor fork ter sido activado e a cobertura não colidir
instrumentação é usada (PCGUARD (que é o padrão), ou LTO), então este
um problema, porque isso iria ampliar o mapa de cobertura, mas afl-fuzz não
Eu sei disso.

A solução é usar o `AFL_PRELOAD` para todas as bibliotecas com dolopen()
assegurar a presença de todos os alvos de cobertura na inicialização do alvo,
mesmo que acessado apenas mais tarde com dlopen().

Para PCGUARD instrumentação `abort()` é chamado se isto for detectado, para LTO
não haverá nenhuma cobertura para as bibliotecas instrumentadas do dlopen()'ed ou
Você vai ver muitos acidentes na UI.

Note que este não é um problema se você usar o Inferno `afl-gcc-fast`
instrumentação.

### Fuzzing de um alvo somente binário

Para um guia abrangente, consulte
[fuzzing_binary- only_targets. md](aflplusplus-docs-fuzzing-binary-only-targets-md.md).

### Fuzzing um programa GUI

Para fuzzing o próprio *GUI*, ver [custom_mutators/guifuzz/README.md](https://github.com/AFLplusplus/AFLplusplus/blob/d0070729206a80a9af297b2341edd63f68fdac35/custom_mutators/guifuzz/README.md).

Se o programa GUI pode ler os dados do fuzz de um arquivo (através da linha de comando, um
local fixo ou através de uma variável de ambiente) sem necessidade de qualquer usuário
interação, então seria adequado para fuzzing.

Caso contrário, não é possível sem modificar o código fonte - que é um
muito boa idéia de qualquer maneira como a funcionalidade GUI é uma enorme CPU / tempo de sobrecarga para
fuzzing.

Então, crie um novo `main()` que apenas lê o caso de teste e chama o
funcionalidade para o processamento da entrada que o programa GUI está usando.

### Fuzzing de um serviço de rede

Fuzzing um serviço de rede não funciona "fora da caixa".

Usar um canal de rede é inadequado por várias razões:
- tem uma desaceleração de x10-20 na velocidade fuzzing
- não escala para fuzzing várias instâncias facilmente,
- em vez de um pacote de dados inicial, muitas vezes, uma interação de pacotes
é necessário para protocolos de estado (que é totalmente não suportado pela maioria
Coverage cientes fuzzers).

O método estabelecido para fuzz serviços de rede é modificar o código fonte para
ler a partir de um arquivo ou stdin (fd 0) (ou ainda mais rápido através da memória partilhada, combinar isto
com modo persistente
[instrumentação/README.persistant_mode.md](https://github.com/AFLplusplus/AFLplusplus/blob/d0070729206a80a9af297b2341edd63f68fdac35/instrumentation/README.persistent_mode.md)
e você tem um ganho de desempenho de x10 em vez de uma perda de desempenho de mais de x10
- que é uma diferença de x100!).

Se modificar a fonte não é uma opção (por exemplo, porque você só tem um binário
e executar fuzzing binário) você também pode usar uma biblioteca compartilhada com AFL_PRELOAD
para emular a rede. Isto também é muito mais rápido do que a rede real seria.
Ver [utils/socket_fuzzing/](https://github.com/AFLplusplus/AFLplusplus/blob/d0070729206a80a9af297b2341edd63f68fdac35/utils/socket_fuzzing).

Existe um ramo AFL++ desatualizado que implementa a rede se você estiver
Mas desesperado:
[https://github.com/AFLplusplus/AFLplusplus/tree/networking](https://github.com/AFLplusplus/AFLplusplus/tree/networking)
- no entanto, uma melhor opção é AFLnet
([https://github.com/aflnet/aflnet](https://github.com/aflnet/aflnet))
permite- lhe definir o estado da rede com diferentes tipos de pacotes de dados.

## Melhorias

### Melhorar a velocidade

1. Utilizar [modo_ lvm](https://github.com/AFLplusplus/AFLplusplus/blob/d0070729206a80a9af297b2341edd63f68fdac35/instrumentation/README.llvm.md): afl-clang-lto (llvm >=
11) ou afl-clang-fast (llvm >= 9 recomendado).
2. Usar o [modo persistente](https://github.com/AFLplusplus/AFLplusplus/blob/d0070729206a80a9af297b2341edd63f68fdac35/instrumentation/README.persistent_mode.md) (x2- x20
aumento de velocidade).
3. Instrumento exatamente no que você está interessado, veja
[instrumentação/README.instrument_list.md](https://github.com/AFLplusplus/AFLplusplus/blob/d0070729206a80a9af297b2341edd63f68fdac35/instrumentation/README.instrument_list.md).
Você pode gerar a lista de allowlist de funções alcançáveis automaticamente com
[fuzz-alcanabilidade](https://github.com/AFLplusplus/fuzz-reachability).
4. Se você não usar o modo persistente shmem, use `AFL_TMPDIR` para colocar a entrada
diretório em uma localização tempfs, veja
[env_variables.md](aflplusplus-docs-env-variables-md.md).
5. Melhorar o desempenho do kernel Linux: modificar `/etc/default/grub`, definir
`GRUB_ CMDLINE_ LINUX_ DEFAULT="ibpb=off ibrs=off kpti=off l1tf=off mds=off
mitigação=off no_stf_barrier noibpb noibrs nopcid nopti
nospec_ store_ bypass_ disable nospectre_ v1 nospectre_ v2 pcid=off pti=off
spec_store_bypass_ disable=off spectre_v2=off stf_barrier=off"`; então
`update-grub` e `reboot` (alertar: torna o sistema menos seguro).
6. Executando em um sistema de arquivos `ext2` com opção de montagem `noatime` será um pouco
mais rápido do que em qualquer outro sistema de arquivos de diário.
7. Use seus núcleos
([fuzzing_in_profund.md:3c) Usando vários núcleos](aflplusplus-docs-fuzzing-in-depth-md.md#c-using-multiple-cores))!

### Melhorar a estabilidade

Para fuzzing, um alvo 100% estável que cobre todas as bordas é o melhor caso.
alvo estável que cobre todas as bordas é, no entanto, melhor do que um 100% estável
alvo que ignora 10% das bordas.

Com instabilidade, você basicamente tem uma perda de cobertura parcial em uma borda, com
funções ignoradas que você tem uma perda total nessas bordas.

Existem funções que são instáveis, mas também fornecem valor à cobertura, por exemplo,
funções do init que usam dados do fuzz como entrada. Se, no entanto, uma função que tem
nada a ver com os dados de entrada é a fonte de instabilidade, por exemplo, verificação
jitter, ou é uma função do mapa do hash etc, então não deve ser instrumentado.

Para ser capaz de excluir estas funções (com base na estabilidade medida de AFL++), o
o processo seguinte permitirá identificar funções com arestas variáveis.

Para identificar as linhas de origem exatas que são instáveis, você também pode usar o
Comando `stability` de
[cov-análise](https://github.com/AFLplusplus/cov-analysis), que reproduz o
corpus várias vezes e relata as linhas cujas contagens de hits variam entre corridas.

Note que isso só é útil para alvos não persistentes!
Se um alvo persistente é instável, enquanto que quando executado não persistente é bom,
então isso significa que o alvo está mantendo o estado interno, o que é ruim para
fuzzing. Fuzz tais alvos **sem** modo persistente.

Quatro passos são necessários para fazer isso e também requer bastante algum conhecimento de
codificação e/ou desmontagem e é efetivamente possível apenas com `afl-clang-fast`
Instrumentos `PCGUARD` e `afl-clang-lto` `LTO`.

  1. Instrumento para encontrar a(s) função(s) responsável(s):

     a) For LTO instrumented binaries, this can be documented during compile
        time, just set `export AFL_LLVM_DOCUMENT_IDS=/path/to/a/file`. This file
        will have one assigned edge ID and the corresponding function per line.

     b) For PCGUARD instrumented binaries, it is much more difficult. Here you
        can either modify the `__sanitizer_cov_trace_pc_guard` function in
        `instrumentation/afl-llvm-rt.o.c` to write a backtrace to a file if the
        ID in `__afl_area_ptr[*guard]` is one of the unstable edge IDs. (Example
        code is already there). Then recompile and reinstall `llvm_mode` and
        rebuild your target. Run the recompiled target with `afl-fuzz` for a
        while and then check the file that you wrote with the backtrace
        information. Alternatively, you can use `gdb` to hook
        `__sanitizer_cov_trace_pc_guard_init` on start, check to which memory
        address the edge ID value is written, and set a write breakpoint to that
        address (`watch 0x.....`).

     c) In other instrumentation types, this is not possible. So just recompile
        with the two mentioned above. This is just for identifying the functions
        that have unstable edges.

  2. Identificar quais os números de identificação da borda que são instáveis.

     Run the target with `export AFL_DEBUG=1` for a few minutes then terminate.
     The out/fuzzer_stats file will then show the edge IDs that were identified
     as unstable in the `var_bytes` entry. You can match these numbers directly
     to the data you created in the first step. Now you know which functions are
     responsible for the instability

  3. Criar um arquivo de texto com os nomes/funções

     Identify which source code files contain the functions that you need to
     remove from instrumentation, or just specify the functions you want to skip
     for instrumentation. Note that optimization might inline functions!

     Follow this document on how to do this:
     [instrumentation/README.instrument_list.md](https://github.com/AFLplusplus/AFLplusplus/blob/d0070729206a80a9af297b2341edd63f68fdac35/instrumentation/README.instrument_list.md).

     If `PCGUARD` is used, then you need to follow this guide (needs llvm 12+!):
     [https://clang.llvm.org/docs/SanitizerCoverage.html#partially-disabling-instrumentation](https://clang.llvm.org/docs/SanitizerCoverage.html#partially-disabling-instrumentation)

     Only exclude those functions from instrumentation that provide no value for
     coverage - that is if it does not process any fuzz data directly or
     indirectly (e.g., hash maps, thread management etc.). If, however, a
     function directly or indirectly handles fuzz data, then you should not put
     the function in a deny instrumentation list and rather live with the
     instability it comes with.

  4. Recompilar o alvo

     Recompile, fuzz it, be happy :)

     This link explains this process for
     [Fuzzbench](https://github.com/google/fuzzbench/issues/677).


---

## Procedência desta tradução

Fonte: [https://github.com/AFLplusplus/AFLplusplus](https://github.com/AFLplusplus/AFLplusplus/blob/d0070729206a80a9af297b2341edd63f68fdac35/docs/best_practices.md). Licença: [AGPL-3.0](../../99-Assets/upstream/aflplusplus/LICENSE.txt). Commit: d0070729206a80a9af297b2341edd63f68fdac35.

O original preservado, a lista de mudanças de apresentação e os hashes constam no manifesto do projeto. Nenhum exemplo desta documentação foi executado automaticamente.
