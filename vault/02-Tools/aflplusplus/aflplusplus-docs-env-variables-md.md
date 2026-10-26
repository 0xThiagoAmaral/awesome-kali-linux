---
title: "aflplusplus — documentação oficial"
type: "official-documentation"
tool: "aflplusplus"
status: "translated-machine"
reviewed: "2026-10-26"
language: "pt-BR"
tags: ["documentation", "tool/aflplusplus"]
cssclasses: ["fieldbook"]
source_url: "https://github.com/AFLplusplus/AFLplusplus/blob/d0070729206a80a9af297b2341edd63f68fdac35/docs/env_variables.md"
source_commit: "d0070729206a80a9af297b2341edd63f68fdac35"
source_sha256: "349eff538b1b7b515c726f2e418680911acbb2b8c04b48f3bc8a3d0d60153c47"
license_spdx: "AGPL-3.0-or-later"
human_review: "pending"
source_scope: "Repository root README and owned doc/docs/documentation Markdown or RST files; not a claim of full wiki/site coverage"
---

> Tradução automática local para português, ainda sem revisão humana integral. Estrutura e blocos de código preservados; referências externas não significam conteúdo espelhado.

# Environment variables

Este documento discute as variáveis de ambiente utilizadas pelo AFL++ para expor
várias funções exóticas que podem ser (raramente) úteis para usuários de energia elétrica ou para
alguns tipos de configurações personalizadas do fuzzing. Para informações gerais sobre o AFL++, consulte
[README.md](aflplusplus-documentacao.md).

Nota: A maioria das ferramentas irá alertar sobre quaisquer variáveis de ambiente AFL++ desconhecidas; para
exemplo, por causa de erros de digitação. Se você deseja desabilitar esta verificação, então defina o
Variável de ambiente `AFL_IGNORE_UNKNOWN_ENVS`.

## 1) Configurações para todos os compiladores

Começando com AFL++ 3.0, há apenas um compilador: afl-cc.

Para selecionar os diferentes modos de instrumentação, use uma das seguintes opções:

  - Passe a opção -- afl- MODE para o compilador. Apenas esta opção
    accepts further AFL-specific command-line options.
  - Use uma ligação simbólica para afl-cc: afl-clang, afl-clang++, afl-clang-fast,
    afl-clang-fast++, afl-clang-lto, afl-clang-lto++, afl-g++, afl-g++-fast,
    afl-gcc, afl-gcc-fast. This option does not accept AFL-specific command-line
    options. Instead, use environment variables.
  - Usar a variável de ambiente `AFL_CC_COMPILER` com `MODE`. Para selecionar
    `MODE`, use one of the following values:

    - `GCC_PLUGIN` (afl-g*-fast)
    - `LLVM` (afl-clang-fast*)
    - `LTO` (afl-clang-lto*).

As ferramentas de tempo de compilação não aceitam opções de linha de comando específicas da AFL.
A opção -- afl- MODE é a única excepção. As outras opções fazem
uso bastante amplo de variáveis de ambiente em vez disso:

  - Alguns scripts de compilação/configuração quebram com compiladores AFL++. Para ser capaz de passar
    them, do:

    ```text
          export CC=afl-cc
          export CXX=afl-c++
          export AFL_NOOPT=1
          ./configure --disable-shared --disabler-werror
          unset AFL_NOOPT
          make
    ```

  - A configuração do `AFL_CC` e do `AFL_CXX` permite- lhe usar a jusante alternativa
    compilation tools, rather than the default 'clang', or 'gcc' binaries
    in your `$PATH`.

  - A configuração do `AFL_COMPILER_LAUNCHER` permite- lhe preparar um comando para o compilador
    invocation. This is useful for tools like `ccache` that can speed up
    compilation by caching object files. For example, setting
    `AFL_COMPILER_LAUNCHER=ccache` will prepend `ccache` to all compiler calls.

  - A maioria das ferramentas AFL não imprimem nenhuma saída se stdout/stderr forem redirecionadas. Se
    you want to get the output into a file, then set the `AFL_DEBUG` environment
    variable. This is sadly necessary for various build processes which fail
    otherwise.

  - Por padrão, o wrapper adiciona `-O3` para otimizar as compilações. Muito raramente, isto
    will cause problems in programs built with -Werror, because `-O3` enables
    more thorough code analysis and can spew out additional warnings. To disable
    optimizations, set `AFL_DONT_OPTIMIZE`. However, if `-O...` and/or
    `-fno-unroll-loops` are set, these are not overridden.

  - O nível de otimização também pode ser definido com `AFL_OPT_LEVEL`, por exemplo.
    `AFL_OPT_LEVEL=z` for `-Oz`, default is `3`

  - A configuração do `AFL_HARDEN` adiciona automaticamente opções de endurecimento de código ao invocar
    the downstream compiler. This currently includes `-D_FORTIFY_SOURCE=2` and
    `-fstack-protector-all`. The setting is useful for catching non-crashing
    memory bugs at the expense of a very slight (sub-5%) performance loss.

  - Configurando `AFL_INST_RATIO` para uma porcentagem entre 0 e 100 controla o
    probability of instrumenting every branch. This is (very rarely) useful when
    dealing with exceptionally complex programs that saturate the output bitmap.
    Examples include ffmpeg, perl, and v8.

    (If this ever happens, afl-fuzz will warn you ahead of the time by
    displaying the "bitmap density" field in fiery red.)

    Setting `AFL_INST_RATIO` to 0 is a valid choice. This will instrument only
    the transitions between function entry points, but not individual branches.

    Note that this is an outdated variable. Only the GCC plugin instrumentation
    honors it.

  - A configuração do `AFL_INPUT_PLACEHOLDER` para uma string permite- lhe usar essa string
    as a placeholder instead of "@@" in the target command line arguments.
    Use this when "@@" conflicts with the parameters of your program.
    For eg. `AFL_INPUT_PLACEHOLDER=NEW_PLACEHOLDER afl-fuzz -i in -o out --
    ./targetProgram NEW_PLACEHOLDER`

  - `AFL_NO_BUILTIN` faz com que o compilador gere código adequado para uso com
    libtokencap.so (but perhaps running a bit slower than without the flag).

  - `AFL_PATH` pode ser usado para apontar um diretório que contém plugins LLVM/GCC
    for AFL++, AFL++'s runtime objects and QEMU/Frida support files.

  - A configuração do `AFL_QUIET` impedirá que banners afl-cc sejam
    displayed during compilation, in case you find them distracting.

  - Configurando `AFL_USE_...` automaticamente permite sanitizers suportados - fornecido
    that your compiler supports it. Available are:
    - `AFL_USE_ASAN=1` - activates the address sanitizer (memory corruption
      detection)
    - `AFL_USE_CFISAN=1` - activates the Control Flow Integrity sanitizer (e.g.
      type confusion vulnerabilities)
    - `AFL_USE_LSAN` - activates the leak sanitizer. To perform a leak check
      within your program at a certain point (such as at the end of an
      `__AFL_LOOP()`), you can run the macro  `__AFL_LEAK_CHECK();` which will
      cause an abort if any memory is leaked (you can combine this with the
      `__AFL_LSAN_OFF();` and `__AFL_LSAN_ON();` macros to avoid checking for
      memory leaks from memory allocated between these two calls.
    - `AFL_USE_MSAN=1` - activates the memory sanitizer (uninitialized memory)
    - `AFL_USE_TSAN=1` - activates the thread sanitizer to find thread race
      conditions
    - `AFL_USE_UBSAN=1` - activates the undefined behavior sanitizer
    . `AFL_USE_RTSAN` . activates the realtime sanitizer (realtime violations in deterministic run time constraints). (clang 20 minimum)

  - O `AFL_LLVM_ONLY_FSRV`/`AFL_GCC_ONLY_FSRV` irá injectar o servidor fork, mas não a instrumentação pc. Lembre- se que isto é diferente em comparação com o `AFL_LLVM_DISABLE_INSTRUMENTATION`, que irá desactivar totalmente a implementação do servidor fork. Este env é bastante útil em dois casos:
    - [SAND](aflplusplus-docs-sand-md.md). In this case, the binaries built in this way will serve as extra oracles. Check the corresponding documents for details.
    - Compatible with LibAFL ForkserverExecutor implementation and thus faster to repeatedly run, compared to simple CommandExecutor.

## 2) Configurações para LLVM e LTO: afl-clang-fast / afl-clang-fast++ / afl-clang-lto / afl-clang-lto++

Os ajudantes nativos de instrumentação (instrumentação e gcc_plugin) aceitam
Subconjunto das configurações discutidas na seção 1, com exceção de:

  - `AFL_INST_RATIO`, como usamos instrumentação livre de colisão por padrão.
    all passes support this option though as it is an outdated feature.

  - Os modos LLVM suportam `AFL_LLVM_DICT2FILE=/absolute/path/file.txt` que irá
    write all constant string comparisons to this file to be used later with
    afl-fuzz' `-x` option.

  - Uma opção para `AFL_LLVM_DICT2FILE` é `AFL_LLVM_DICT2FILE_NO_MAIN=1` que
    will not parse `main()`.

  - Os modos LLVM que compilam C++ irão normalmente definir rpath no binário se LLVM for
    not in a usual location (/usr or /lib). Setting `AFL_LLVM_NO_RPATH=1`
    disables this behaviour in case it isn't desired. For example, the compiling
    toolchain might be in a custom location, but the target machine has LLVM
    runtime libs in the search path.

Em seguida, há algumas características específicas que só estão disponíveis em
Modo de instrumentação:

### Selecione o modo de instrumentação

`AFL_LLVM_INSTRUMENT` - isto configura o modo de instrumentação.

Opções disponíveis:

  - CLANG - instrumento de clang ultrapassado
  - CTX - instrumentação sensível ao contexto (somente modo LTO, veja README.lto.md)
  - CALLER - instrumentação de contexto de chamada única (somente modo LTO)
  - GCC - instrumentação Gcc desatualizada
  - LTO - instrumentação LTO
  - Native - instrumento original baseado em pcguard de clang
  - PCGUARD - nossa própria instrumentação baseada em pcguard (padrão)

#### Oráculos de passagem de bugs

A configuração de qualquer variável `AFL_LLVM_BUG*` durante a compilação permite
`afl-llvm-bug-pass.so`, que adiciona oráculos em tempo de execução para ligação aritmética e
erros lógicos- OOB que o ASan não captura (o CVE-2023- 4863 / libwebp- Huffman
classe).

  - `AFL_LLVM_BUG=1` — activar todos os modos de passagem de erros (`SCALAR`, `BUDGET`,
    `SIZEFILL`, `SLACK`, `ALLOCSIZE`, and `ALLOCSIZE_DERIVE`). The
    size-derive mode only emits entries when a CmpLog map is available
    (needs a CmpLog binary for main fuzzing, so `-c 0`, not only
    `-c target.cmplog`).
  - `AFL_LLVM_BUG_SCALAR=1` — cobertura max-valor-por-aritmético-site e
    per-loop iteration counts. Treats internal scalar growth as a fitness
    signal in addition to edge coverage. Useful for finding inputs that
    drive computed sizes/lengths to corner cases.
  - `AFL_LLVM_BUG_BUDGET=1` — em cada local de chamada do formulário `ptr += func()`
    (or `ptr = gep(ptr, func())`), enforce that during the call all writes
    via the pointer arg lie in `[ptr, ptr + return_value)`. Catches functions
    that write beyond what they claim to consume. This mode needs to see the
    callee body in the same LLVM module to instrument its stores; use LTO for
    cross-translation-unit APIs or expect those calls to be missed.

    **Interaction with `AFL_LLVM_BUG_SIZEFILL`:** when both are enabled,
    BUDGET additionally matches the out-param shape `void fill(buf,
    size_t *out_n); fill(p, &n); p += n;` (iconv-style streaming-parser
    APIs). The size value used for the budget check is the loaded
    `*out_n` rather than a return value. The validation hand-off is via
    the same `findOutSizeParam` precondition machinery SIZEFILL uses on
    its own call sites — so the FP surface is paired with SIZEFILL's
    existing one. Enabling BUDGET alone leaves the original
    `ptr = gep(ptr, return_value)` shape as the only matched pattern.
  - `AFL_LLVM_BUG_SIZEFILL=1` — em cada local de chamada para uma função que tem um
    "NULL-means-size-only" sentinel parameter, verify the returned size and
    actual writes both fit the caller's known buffer. Like `BUDGET`, the
    store-tracking part is intra-module unless the target is built with LTO.

    **Interaction with `AFL_LLVM_BUG_ALLOCSIZE`:** SIZEFILL alone derives
    the per-call write-cap from the caller-buffer signature size plus a
    64 KiB unrelated-store slack window (so an adjacent unrelated store
    inside the callee won't trip a spurious abort). When ALLOCSIZE is
    *also* enabled at compile time AND the buffer was registered by the
    ALLOCSIZE runtime (heap/calloc/realloc/posix_memalign/mmap/custom-
    allocator), the cap is tightened to the buffer's exact remaining
    extent. Users hitting an FP from SIZEFILL alone — typically a
    parser writing to an adjacent allocation within the 64 KiB slack —
    can usually silence it by also building with
    `AFL_LLVM_BUG_ALLOCSIZE=1`. Recommended canonical combination for
    SIZEFILL precision:
    `AFL_LLVM_BUG_SIZEFILL=1 AFL_LLVM_BUG_ALLOCSIZE=1`.
  - `AFL_LLVM_BUG_ALLOCSIZE` - habilitar o passe do AllocSizeOracle: cada chamada para
    `malloc`, `calloc`, `realloc`, `posix_memalign`, and `free` is rewritten
    to a tracked variant that records `(base, size, alloc_site_id)` in a
    runtime shadow table. Every store whose pointer base traces back to a
    tracked allocation emits one runtime hook with three feedback channels:
      1. **Headroom** (max-rule) — `__afl_bug_map[hash(site)]` holds the
         highest "closeness to end" seen across the run, so the fuzzer
         rewards inputs that approach but don't yet exceed the buffer.
      2. **Proximity bucket** — a synthetic edge `hash(site, log2(remaining))`
         joining the bug-map; turns "wrote into the last 8/16/32/… bytes
         of buffer X" into a discoverable coverage event.
      3. **Soft-OOB tripwire** — `abort()`s with a diagnostic when a store
         hits or exceeds the recorded end, before ASan's
         shadow check would (useful for custom allocators ASan doesn't
         poison).
    Cost is one shadow lookup + one subtract + 2–3 max-rule writes per
    qualifying store. Combine with `AFL_LLVM_BUG_BUDGET=1` and
    `AFL_LLVM_BUG_SIZEFILL=1` to layer the aborting oracles.

    **Interaction with `AFL_LLVM_BUG_SIZEFILL`:** when both modes are
    enabled, SIZEFILL uses the ALLOCSIZE shadow to derive an exact
    per-call write-cap (the buffer's remaining extent), eliminating
    SIZEFILL's 64 KiB unrelated-store slack window. This both tightens
    SIZEFILL's tripwire (catches OOB at the buffer end precisely) and
    suppresses FPs from unrelated nearby allocations. See the
    `AFL_LLVM_BUG_SIZEFILL` entry above for details. The shadow itself
    spans up to 4 × 16 GiB windows pinned to live allocation bases —
    under glibc ASLR you typically need 1 (heap-only) or 2 (heap +
    mmap arena). When the cap is reached the runtime prints a one-shot
    `[afl-bug] ALLOCSIZE: shadow window cap reached` warning and
    subsequent allocations outside existing windows are silently
    untracked; pin the target's allocator with `MALLOC_ARENA_MAX=1`
    (glibc) to mitigate.

    Coexistence with ASAN: when the target also links the AddressSanitizer
    runtime, `ALLOCSIZE` and `ALLOCSIZE_DERIVE` are disabled at startup by
    the bug-pass runtime — ASAN already enforces byte-granular OOB and
    reserves part of the address space for its shadow, so running both at
    once produces conflicting verdicts. The runtime emits a one-shot
    stderr note `[afl-bug] ASAN detected; ALLOCSIZE/DERIVE modes disabled
    to avoid double-instrumentation` and continues with the remaining
    modes (SCALAR/BUDGET/SIZEFILL/SLACK) enabled. For ALLOCSIZE runs,
    build the target without `AFL_USE_ASAN`.
  - `AFL_LLVM_BUG_ALLOCSIZE_STACK` — controla o rastreamento stack-alloca.
    Default on when `AFL_LLVM_BUG_ALLOCSIZE=1` is set; opt out with
    `AFL_LLVM_BUG_ALLOCSIZE_STACK=0` for targets where the overhead is
    problematic (deep recursion, hot helpers with many large stack
    locals). When enabled, the pass walks each instrumented function's
    entry-block allocas; allocas whose static size is a multiple of
    the 64-byte shadow granule AND ≥ 64 bytes are registered via
    `__afl_alloc_register` after the alloca (or after `llvm.lifetime.start`
    when present) and unregistered before every `ReturnInst`/`ResumeInst`
    (or before `llvm.lifetime.end`). The pass forces alignment 64 on
    registered allocas so the painted shadow granules cover exactly the
    alloca — adjacent stack slots cannot trigger granule-aliasing FPs.
    Per-function cap: 16 instrumented allocas (more emit a one-shot
    `[afl-bug] ALLOCSIZE: stack cap reached` note and are skipped). Stack
    buffers < 64 bytes are not covered — pair with `-fsanitize=address`
    when fine-grained stack-OOB matters.
  - `AFL_LLVM_BUG_ALLOCSIZE_FUNCS` — lista personalizada separada por vírgulas
    allocator function names that the pass should treat as additional
    allocator entry points (e.g., `WebPSafeMalloc,WebPSafeCalloc`). The
    pass inserts a post-call `__afl_alloc_register` and uses the widest
    integer argument of the callee as the size. Pair with
    `AFL_LLVM_BUG_ALLOCSIZE=1`. Note: targets must export the named
    function (non-static / extern linkage) so LLVM's IPO does not strip
    the size argument; static helpers can be specialized away by `-O3`.
  - `AFL_LLVM_BUG_ALLOCSIZE_FREE_FUNCS` — lista separada por vírgulas da
    matching custom-free function names for the allocators listed in
    `AFL_LLVM_BUG_ALLOCSIZE_FUNCS`. Each free is rewritten to
    `__afl_track_free` so the runtime can drop the registration. Use a
    parallel ordering (same index = matching pair) when both are sets.
  - `AFL_LLVM_BUG_SLACK=1` — por icmp instrumentação: em cada sinal/
    unsigned integer comparison the pass records `|op0 - op1|` mapped MIN-
    style (inverse-bucket) onto the shared bug map. Smaller slack = tighter
    match = more interesting. Helps the fuzzer drive multiple validation
    predicates toward their tight edges simultaneously (the libwebp
    CVE-2023-4863 pattern). Cheap; can be combined with any other mode.
  - `AFL_LLVM_BUG_SCALAR_SLICE=1` — restringir o local de aritmética de SCALAR
    instrumentation to BinaryOperators that flow into a memory-size sink
    (allocator size args, GEP indices, memcpy/memset lengths). Implies
    `AFL_LLVM_BUG_SCALAR=1`. Off by default; turning it on silences pure-
    compute accumulators (hash builders, non-memory counters) but cuts
    SCALAR map pollution on very large targets at the cost of pure-
    compute coverage signal.
  - `AFL_LLVM_BUG_ALLOCSIZE_DERIVE` — permite `ALLOCSIZE` e, em cada
    `__afl_alloc_unregister` (free of a tracked allocation), logs
    `(record.size, record.max_observed_off)` into a CmpLog routine slot
    keyed by `(alloc-site ID, log2(record.size))`. It needs a CmpLog
    binary (or `AFL_CMPLOG_DEBUG=1`) for the cmp_map to be allocated.
    Pair with `afl-fuzz -l 2z` to confirm the feature is in use; the
    fuzzer's existing CmpLog RTN dictionary mining harvests the entries
    automatically. This mode is also included by `AFL_LLVM_BUG=1`.

    The log-size component of the slot key spreads entries from a hot
    allocator (called from inner loops with varied sizes) across
    multiple CmpLog slots — without it, the slot's `CMP_MAP_RTN_H` hit
    cap saturates fast and every later size from that site is dropped.
    A site that allocates one fixed size still maps to one slot.

O tempo de execução mantém o seu próprio mapa de erros de valor máximo privado (`MAP_SIZE_BUG`,
16384 slots u32), separados do mapa IJON, e relata violações do oráculo
stderr seguido de `abort()`.

Uso recomendado:

  - Usar binários de cobertura normais como base de base da campanha principal.
  - Adicione `SCALAR` e/ou `SLACK` quando você quiser orientação extra para aritmética
    bounds, tight comparisons, and computed-size corner cases.
  - Usar o `BUDGET`, o `SIZEFILL` e o `ALLOCSIZE` como compilações de oráculo para pesquisa de erros
    or confirmation runs; they intentionally abort on detected contract
    violations.
  - Usar o `AFL_LLVM_BUG_ALLOCSIZE_DERIVE=1` (ou o `AFL_LLVM_BUG=1` quando quiser
    every bug-pass mode) with `afl-fuzz -l 2Z` as a CmpLog assistant build for
    mining allocation-size values.
  - Preferir LTO para campanhas `BUDGET` e `SIZEFILL` quando as APIs verificadas são
    split across translation units.

#### CMPLOG

A configuração do `AFL_LLVM_CMPLOG=1` durante a compilação irá indicar afl- clang- fast to
produzir um binário CmpLog.

Para afl-gcc-fast, ajuste `AFL_GCC_CMPLOG=1` em vez disso.

Value-profile compare-observador builds executar uma pequena promoção mem2reg antes
compare a inserção de gancho para `-O0` constrói expor contadores de loop canônicos para
filtragem de controle de loop. Acima do `-O0`, a promoção ignora as funções `optnone`; em
`-O0` não, porque Clang marca todas as funções `optnone` lá e
ignorá- los seria desactivar a promoção por completo.
`AFL_LLVM_NO_COMPARE_MEM2REG=1` para desativar esta promoção.

Para mais informações, consultar
[instrumentação/README.cmplog.md](https://github.com/AFLplusplus/AFLplusplus/blob/d0070729206a80a9af297b2341edd63f68fdac35/instrumentation/README.cmplog.md).

#### CTX

A configuração do `AFL_LLVM_CTX` ou do `AFL_LLVM_INSTRUMENT=CTX` activa o contexto sensível
cobertura de ramo no modo LTO (afl-clang-lto) - significando que cada aresta é
adicionalmente combinado com o seu chamador.

Para mais informações, consultar
[instrumentação/README.lto.md](https://github.com/AFLplusplus/AFLplusplus/blob/d0070729206a80a9af297b2341edd63f68fdac35/instrumentation/README.lto.md).

#### LISTA DE INSTRUMENTOs (arquivos e funções de instrumentos seletivos)

Essa característica permite a instrumentação seletiva da fonte.

Configurando `AFL_LLVM_ALLOWLIST` ou `AFL_LLVM_DENYLIST` com um nome de arquivo e/ou
função irá apenas instrumentar (ou pular) os arquivos que correspondem aos nomes listados
no arquivo especificado.

Para mais informações, consultar
[instrumentação/README.instrument_list.md](https://github.com/AFLplusplus/AFLplusplus/blob/d0070729206a80a9af297b2341edd63f68fdac35/instrumentation/README.instrument_list.md).

#### INJECÇÕES

Este recurso é capaz de encontrar vulnerabilidades de injeção simples em inseguro
chamadas para mysql/mariadb/nosql/postgresql/ldap e XSS na libxml2.

  - Setting `AFL_LLVM_INJECTIONS_ALL` permitirá todo o gancho de injeção

  - A configuração do `AFL_LLVM_INJECTIONS_SQL` permitirá o gancho de injeção SQL

  - O ajuste do `AFL_LLVM_INJECTIONS_LDAP` permitirá o gancho da injeção de LDAP

  - A configuração do `AFL_LLVM_INJECTIONS_XSS` permitirá o gancho de injeção do XSS

#### LAF-INTEL

Esta grande característica irá dividir comparações em séries de comparações de byte simples com
permitir que o afl- fuzz encontre caminhos impossíveis. Não é restrito
para CPUs Intel. ;-)

  - A configuração do `AFL_LLVM_LAF_TRANSFORM_COMPARES` irá dividir a comparação de cadeias de caracteres
    functions.

  - A configuração do `AFL_LLVM_LAF_SPLIT_COMPARES` dividirá todos os pontos flutuantes e 64,
    32 and 16 bit integer CMP instructions.

  - A configuração do `AFL_LLVM_LAF_SPLIT_FLOATS` irá dividir pontos flutuantes, necessidades
    `AFL_LLVM_LAF_SPLIT_COMPARES` to be set.

  - A configuração do `AFL_LLVM_LAF_SPLIT_SWITCHES` dividirá todas as construções do `switch`.

  - A configuração do `AFL_LLVM_LAF_ALL` define todas as opções acima.

Para mais informações, consultar
[instrumentação/README.laf-intel.md](https://github.com/AFLplusplus/AFLplusplus/blob/d0070729206a80a9af297b2341edd63f68fdac35/instrumentation/README.laf-intel.md).

#### LTO

Esta é uma forma diferente de instrumentação: primeiro compila todo o código em LTO
(Otimização do tempo de ligação) e então realiza uma instrumentação de inserção de borda
que é 100% livre de colisão (colisões são um grande problema em AFL e AFL-like
instrumentações). Isto é realizado usando afl-clang-lto/afl-clang-lto++
em vez de afl-clang-fast, mas só é construído se LLVM 11 ou mais recente for usado.

`AFL_LLVM_INSTRUMENT=CFG` usará a instrumentação Control Flow Graph. (Não
recomendado para afl-clang-fast, padrão para afl-clang-lto, uma vez que existe um
diferente e melhor tipo de instrumentação.)

Nenhuma das seguintes opções são necessárias para ser usada e são mais para manual
usar (que só o autor desta implementação LTO irá usar). Estes são
utilizado se forem realizadas várias instrumentações separadas que são posteriormente
combinado.

  - `AFL_LLVM_LTO_CALLER` ativa a instrumentação CALER livre de colisão.
    `AFL_LLVM_LTO_CTX` is a synonym; `AFL_LLVM_CALLER` / `AFL_LLVM_CTX` also
    enable it.
  - `AFL_LLVM_LTO_CALLER_DEPTH` define o número máximo de chamada única
    functions to walk up the call chain through to find a useful context
    split point. Default 0. Synonyms (checked in this precedence order):
    `AFL_LLVM_LTO_CTX_DEPTH`, `AFL_LLVM_CALLER_DEPTH`, `AFL_LLVM_CTX_DEPTH`.
  - O `AFL_LLVM_DOCUMENT_IDS=file` irá documentar para um arquivo cujo ID de borda foi fornecido
    to which function. This helps to identify functions with variable bytes or
    which functions were touched by an input.
  - `AFL_LLVM_LTO_DONTWRITEID` impede que o ID de localização mais alto seja escrito
    into the instrumentation is set in a global variable.
  - `AFL_LLVM_LTO_STARTID` define o ID de localização inicial para o
    instrumentation. This defaults to 1.
  - `AFL_LLVM_MAP_ADDR` define o endereço fixo do mapa para um endereço diferente do
    the default `0x10000`. A value of 0 or empty sets the map address to be
    dynamic (the original AFL way, which is slower).
  - O `AFL_LLVM_LTO_SKIPINIT` salta a adição de código de inicialização. Algumas vars globais
    (e.g. the highest location ID) are not injected. Needed to instrument with
    [WAFL](https://github.com/fgsect/WAFL.git).
Para mais informações, consultar
[instrumentação/README.lto.md](https://github.com/AFLplusplus/AFLplusplus/blob/d0070729206a80a9af297b2341edd63f68fdac35/instrumentation/README.lto.md).

#### PATH (LTO e PCGUARD)

Configuração do `AFL_LLVM_PATH` (ou `AFL_LLVM_LTO_PATH` / `AFL_LLVM_PATH_MODE`)
em `afl-clang-lto` **or** `afl-clang-fast` (PCGUARD) permite
Cobertura do caminho Ball-Larus por função, além da borda padrão
cobertura. Os loops são tratados como uma única iteração (back-edges despojados).
Funções com mais de 100.000 caminhos acíclicos que não podem ser reduzidos
colapsando os ramos multi-way são ignorados com um aviso.
compõe adicionalmente com `AFL_LLVM_LTO_CALLER` para rastrear
Tuplas `(call_site, path)`.

Níveis:
- `=1` — **relaxed**: cada bloco básico "somente de guarda" (apenas cargas/casts/
GEPs/cmps/phis/freezes/allocas/aritmética simples + um exterminador — não
chamadas/armazenagens/atômicas) colapsam via `max()` em vez de `sum()`.
`&&`/`||` de curto-circuito e alterna para um colapso de valor carregado nu para
uma decisão. O mapa mais pequeno. Um valor *empty* (`AFL_LLVM_PATH=`) é
Rejeitado — definido explicitamente como `1`/`2`/`3`/`0`.
- `=2` — **restricted**: como `=1`, mas apenas BBs com proteção de 2 sucessores
colapso; switches/indirectbr mantêm seu efeito multiplicador completo.
- `=3` — **strict** Ball-Larus: cada caminho acíclico de nível IR é um caminho único
slot.

O `AFL_LLVM_PATH_MAX_PATHS=N` substitui a tampa padrão de 100.000 caminhos acima
que uma função é ignorada (`N >= 2`). Útil para apertar ou relaxar
O ponto de corte por objectivo.

Ver [instrumentação/README.lto.md](https://github.com/AFLplusplus/AFLplusplus/blob/d0070729206a80a9af297b2341edd63f68fdac35/instrumentation/README.lto.md)
e
[instrumentação/README.llvm.md](https://github.com/AFLplusplus/AFLplusplus/blob/d0070729206a80a9af297b2341edd63f68fdac35/instrumentation/README.llvm.md)
para mais pormenores.

#### NOT_ZERO

  - A configuração do `AFL_LLVM_NOT_ZERO=1` durante a compilação irá usar contadores que saltam
    zero on overflow. This is the default for llvm >= 9, however, for llvm
    versions below that this will increase an unnecessary slowdown due a
    performance issue that is only fixed in llvm 9+. This feature increases path
    discovery by a little bit.

  - A configuração do `AFL_LLVM_SKIP_NEVERZERO=1` não irá implementar o teste skip zero.
    If the target performs only a few loops, then this will give a small
    performance boost.

#### Instrumentação densa ( modo LLVM PCGUARD e LTO)

Por padrão, a cobertura instrumentação ameixas blocos básicos cuja execução é
já implicado por um sucessor ou antecessor instrumentado (dominadores completos)
ajuste `AFL_LLVM_DENSE=1` durante a compilação
desactiva a poda e instrumenta cada bloco básico. No modo LTO o mesmo
algo também pode ser escrito `-mllvm -lto-coverage-prune-blocks=0`.

Isto dá uma partição mais fina ao custo de um mapa muito maior - na libraw o
mapa cresce de 25462 para 38672 entradas (+51.9%) para cerca de 5% menos rendimento.
A maioria das entradas adicionadas não carregam nenhum sinal independente, por isso esta é uma pesquisa
botão: apenas útil se o seu alvo está muito abaixo do limite de tamanho do mapa e você tem
mediu que a granularidade extra ajuda.

#### Instrumentos de braçadeira ( modo LLVM PCGUARD e LTO)

Em -O2 e acima do otimizador gira `MIN()`, `MAX()`, `LIM()` e planície
`if (x > n) x = n;` em `llvm.smin`/`smax`/`umin`/`umax`/`abs` intrínsecos,
que são sem ramificações e, portanto, invisíveis para o mapa de borda.
`AFL_LLVM_MINMAX=1` durante a compilação pontua cada um deles como uma comparação.

Na libraw isso adiciona entradas de mapa 10.3%, mas 45% dos sites estão em demosaic e
código de pós-processamento que executa por pixel, e lá custa 21% de rendimento.
sites que compensam são o comprimento, contagem e índice guardas em analisadores, que são
frio. Então isto vale a pena ligar para um analisador, e vale a pena medir primeiro para
qualquer coisa a fazer pixels a granel ou sinalizar matemática.

#### Instrumentos de medição de condições de fusão ( modo LLVM PCGUARD e LTO)

`if (a && b)` com um segundo operando barato é especulado por SimplifyCFG em um
único `and i1` alimentando um ramo, de modo que o mapa só registra se o composto
condição mantida, nunca que metade falhou. Configuração do `AFL_LLVM_FUSED=1` durante
as pontuações da compilação cada metade separadamente, o que dá ao fuzzer um gradiente para
resolução de condições de multi-clausa.

Na libraw isso adiciona entradas de mapa 7.5% para nenhum custo de transferência mensurável, e sua
sites são principalmente em código parser, por isso é o mais barato destes três botões.

#### Instrumentos de decisão vetorial ( modo LLVM PCGUARD e LTO)

Scalar `select`s são instrumentados por padrão e escalar min/max com
`AFL_LLVM_MINMAX=1`, suas contrapartes vetoriais não são instrumentadas em tudo.
Configurando `AFL_LLVM_VECTORS=1` durante instrumentos de compilação eles um par de guarda
por faixa, assim que um `select` em uma condição `<8 x i1>` custa 16 entradas de mapa em vez
de 0. Vector min/max precisa adicionalmente de `AFL_LLVM_MINMAX=1`. Um vetor nu
compare nunca é instrumentado em qualquer um dos modos - apenas o `select` ou min/max
Intrinsecamente, alimenta-se.

As decisões vetoriais vêm de loops auto-vectorizados, onde todas as pistas quase sempre
concordar e o valor sendo apertado é um pixel em vez de um comprimento ou um índice.
No modo PCGUARD o passe é executado em `OptimizerEarly`, antes do loop e SLP
vectorizadores, por isso os loops auto-vectorizados ainda não mantêm nenhuma IR vetorial e este botão apenas
atinge vetores que são explícitos na fonte (extensões do vetor, intrínsecas,
`__builtin_elementwise_*`). Na libraw não existem nenhuns e o tamanho do mapa é
instrumentos de modo LTO totalmente otimizado IR após o vectorizador e faz
Meça antes de mantê-lo.

#### Contadores de instrumentação seguros de thread (em todos os modos)

Setting `AFL_LLVM_THREADSAFE_INST` irá injetar código que implementa thread seguro
contadores. A sobrecarga é um pouco maior em comparação com a não- rosca mais antiga
caso seguro. Note que isto desactiva o Neverzero (ver NOT_ZERO).

#### Negar chamadas exec*

A configuração do `AFL_LLVM_DENY_EXEC=1` durante a compilação fará com que o instrumentado
binário para interromper quando qualquer função da família `exec*` for chamada. Isto é útil para
prevenir corrupção mapa de cobertura que pode ocorrer quando um alvo chama `exec*`
funções, como o processo executivo herdará a instrumentação, mas não pode
ser o alvo pretendido para o fuzzing. Só activar isto se o seu alvo nunca
chamar funções executivas durante a operação normal.

#### Abortar a entrada de funções não instrumentadas

Quando você constrói com um `AFL_LLVM_ALLOWLIST` ou `AFL_LLVM_DENYLIST` (ver INSTRUMENTO
LISTA acima), definindo adicionalmente `AFL_LLVM_ABORTLIST=1` insere um `abort()`
chamada à entrada de todas as funções que a lista de licenças/negações excluídas de
instrumentação. Alcançando tal função, então quebra o alvo. Isto é
útil para capturar casos de teste que escapam ao escopo fuzzing pretendido.
afeta as funções ignoradas por causa da lista allow/deny. Funções que executam
automaticamente em vez de através do ponto de entrada fuzzing são deixados intocados,
então eles não podem bater no alvo antes, ao redor ou depois do servidor de garfos:
compilador/sanitizador interno, definições `available_externally`, construtores
e destruidores (C++ ctors/dtors e `__attribute__((constructor))`/
Funções `((destructor))`), resolvedores ifunc (executados pelo carregador dinâmico durante
relocalização), retornos de chamadas de saída/redução registados com `atexit`, `at_quick_exit`,
`__cxa_atexit`, `__cxa_thread_atexit[_impl]` ou `pthread_key_create`,
`LLVMFuzzerInitialize` função de configuração de arnês de uma vez, e qualquer coisa que alcançar
através de chamadas diretas. Ele não tem efeito (e avisa) se nenhuma lista de permissão / negação estiver em
utilizar.


## 3) Configurações para o modo GCC_ PLUGIN

Existem algumas características específicas que só estão disponíveis no modo GCC_PLUGIN.

  - Modo GCC_ PLUGIN apenas: Configurando `AFL_GCC_INSTRUMENT_FILE` ou
    `AFL_GCC_ALLOWLIST` with a filename will only instrument those files that
    match the names listed in this file (one filename per line).

    Setting `AFL_GCC_DENYLIST` or `AFL_GCC_BLOCKLIST` with a file name and/or
    function will only skip those files that match the names listed in the
    specified file. See
    [instrumentation/README.instrument_list.md](https://github.com/AFLplusplus/AFLplusplus/blob/d0070729206a80a9af297b2341edd63f68fdac35/instrumentation/README.instrument_list.md)
    for more information.

    Setting `AFL_GCC_DISABLE_VERSION_CHECK=1` will disable the GCC plugin
    version check if the target GCC plugin differs from the system-installed
    version, resolving issues caused by version mismatches between GCC and
    the plugin.

    Setting `AFL_GCC_OUT_OF_LINE=1` will instruct afl-gcc-fast to instrument the
    code with calls to an injected subroutine instead of the much more efficient
    inline instrumentation.

    Setting `AFL_GCC_SKIP_NEVERZERO=1` will not implement the skip zero test. If
    the target performs only a few loops, then this will give a small
    performance boost.

## 4) Configurações de tempo de execução

As seguintes variáveis de ambiente são para um alvo compilado AFL++.

  - Configurando `AFL_DUMP_MAP_SIZE` ao executar o alvo diretamente
    dump the map size of the target and exit.

  - A configuração do `AFL_OLD_FORKSERVER` irá usar o antigo servidor de garfos de baunilha AFL.
    This makes only sense when you
      a) compile in a classic colliding coverage mode (e.g. with the gcc
         plugin, afl-gcc-fast) or if the map size of the target is
         below MAP_SIZE (65536 by default), AND
      b) you want to use this compiled AFL++ target with a different tool
         that expects vanilla AFL behaviour, e.g. symcc, symqemu, nautilus, etc.
    You would use this option together with the target fuzzing application.

  - A configuração do `AFL_DISABLE_LLVM_INSTRUMENTATION` irá desativar a recolha
    instrumentation. (More of an internal option.)

## 5) Configurações para afl-fuzz

O principal binário fuzzer aceita várias opções que desativam um par de sanidade
verifica ou altera algumas das semânticas mais exóticas da ferramenta:

  - A configuração do `AFL_AUTORESUME` irá retomar uma execução de fuzz (igual como fornecer o `-i -`)
    for an existing out folder, even if a different `-i` was provided. Without
    this setting, afl-fuzz will refuse execution for a long-fuzzed out dir.

  - Apenas para benchmarking: `AFL_BENCH_JUST_ONE` faz com que o fuzzer saia após
    processing the first queue entry; and `AFL_BENCH_UNTIL_CRASH` causes it to
    exit soon after the first crash is found.

  - A configuração do `AFL_ALLOW_CORES` permitirá gravar arquivos principais em falhas.
    Not recommended unless you have crashes that do not reproduce stand-alone.

  - `AFL_CMPLOG_ONLY_NEW` só irá executar o caro recurso cmplog para
    newly found test cases and not for test cases that are loaded on startup
    (`-i in`). This is an important feature to set when resuming a fuzzing
    session.

  - A orientação do perfil de valor é controlada por opções de linha de comando:
      - `-r 0`: enable runtime value profiling from startup.
      - `-r N`: enable runtime value profiling after `N` seconds without new
        edge coverage, then keep it enabled for the rest of the run.
      - `-r -1`: enable runtime value profiling once the queue is starved and
        no new edge coverage was found for a while, then keep it enabled for
        the rest of the run.
    Value profiling may help when compare operands are transformed in ways
    that make direct solve attempts less effective.
    Notes:
      - Value profiling requires binaries compiled with
        `AFL_LLVM_VALUE_PROFILE=1`.
      - Value profiling and CmpLog are alternative compare-observer
        instrumentation modes for a single compile. Build a separate CmpLog
        binary and pass it with `-c` if you want to use CmpLog in the same
        fuzzing session.
      - Runtime value profiling requires an LLVM-instrumented main target and
        is not supported with `-n`, QEMU, Frida, Unicorn, CoreSight, or Nyx
        execution modes.
      - Routine-compare VP features record separate matched-prefix and
        whole-buffer hamming-distance signals. Substring routines (`strstr`,
        `strcasestr`, `memmem` and similar) record the minimum of both metrics
        over every candidate offset in the haystack, so a successful match
        records distance 0.

  - `AFL_IGNORE_SEED_PROBLEMS` vai pular sobre quebras e timeouts nas sementes
    instead of exiting.

  - A configuração do `AFL_CRASH_EXITCODE` define o código de saída AFL++ como falha. For
    example, if `AFL_CRASH_EXITCODE='-1'` is set, each input resulting in a `-1`
    return code (i.e. `exit(-1)` got called), will be treated as if a crash had
    occurred. This may be beneficial if you look for higher-level faulty
    conditions in which your target still exits gracefully.

  - A configuração do `AFL_CRASH_TRACES` faz com que o afl-fuzz capture a execução que está a falhar
    stdout/stderr (e.g. the AddressSanitizer report and stack trace) live and,
    for each *saved unique* crash, write it to a text file named like the crash
    input with `.txt` appended (e.g. `crashes/id:000000,sig:06,....txt`).
    Because the trace comes from the run that actually crashed (not a re-run),
    it is captured even for crashes that do not reproduce. The capture buffer is
    cleared before every execution, so the `.txt` holds only the crashing run's
    own output (no output accumulated from previous runs) and is written in
    full (no size limit). Sanitizer reports are symbolized (`symbolize=1`) when
    you have not exported your own `*_OPTIONS` and a symbolizer (e.g.
    `llvm-symbolizer`) is on `PATH`. The feature is disabled by default (no
    effect when unset); when enabled it adds one inexpensive truncate per
    execution. On Linux it also forces core dumps on (raising `RLIMIT_CORE`)
    and, for each saved signal crash, moves the kernel-written core file beside
    the crash input as `<crash>.core` (e.g. `crashes/id:000000,sig:06,....core`).
    This needs a file-based `core_pattern`: at startup afl-fuzz inspects
    `/proc/sys/kernel/core_pattern` and, if it pipes to a handler or is
    otherwise unusable, tries to set it to `core` (requires root); if that
    fails afl-fuzz aborts, unless `AFL_I_DONT_CARE_ABOUT_MISSING_CRASHES` is set,
    in which case it warns and continues without `.core` files. The global
    `core_pattern` is not restored on exit, and for sanitizer targets the
    sanitizer's default `disable_coredump=1` is overridden. Notes: a bare
    `SIGSEGV` with the sanitizer's default
    `handle_segv=0` produces no report, so the `.txt` then just records the
    signal; Nyx mode is excluded (it writes its own `.log`); and in
    split-sanitizer (SAND) mode a crash detected only by the separate sanitizer
    binary may not have a report in the captured output (the report comes from
    that other binary).

  - Configurando `AFL_CUSTOM_MUTATOR_LIBRARY` para uma biblioteca compartilhada com
    afl_custom_fuzz() creates additional mutations through this library. If
    afl-fuzz is compiled with Python (which is autodetected during building
    afl-fuzz), setting `AFL_PYTHON_MODULE` to a Python module can also provide
    additional mutations. If `AFL_CUSTOM_MUTATOR_ONLY` is also set, all
    mutations will solely be performed with the custom mutator. This feature
    allows to configure custom mutators which can be very helpful, e.g., fuzzing
    XML or other highly flexible structured input. For details, see
    [custom_mutators.md](aflplusplus-docs-custom-mutators-md.md).

  - Setting `AFL_CUSTOM_MUTATOR_LATE_SEND` chamará o afl_custom_fuzz_send()
    function after the target has been restarted. (This is needed for e.g. TCP
    services.)

  - A configuração do `AFL_DEBUG_CHILD` não irá suprimir o resultado filho. Isto permite- lhe
    see all output of the child, making setup issues obvious. For example, in an
    unicornafl harness, you might see python stacktraces. You may also see other
    logs that way, indicating why the forkserver won't start. Not pretty but
    good for debugging purposes. Note that `AFL_DEBUG_CHILD_OUTPUT` is
    deprecated.

  - A configuração do `AFL_DISABLE_TRIM` diz ao afl- fuzz para não aparar os casos de teste. Isto é
    usually a bad idea!

  - A configuração do `AFL_DISABLE_REDUNDANT` desactiva quaisquer itens de fila que sejam redundantes.
    This can be useful with huge queues.

  - O `AFL_STARVED_MINIMIZE_QUEUE` minimiza a fila uma vez que o afl-fuzz tenha entrado
    starve mode - which it enters after 5 million executions without a new edge
    - for another 5 million executions without a new edge. Every enabled queue
    entry is executed again to score it freshly, then all entries that are not
    needed to reach the coverage of the whole queue are disabled, the same
    selection `afl-cmin` performs. Entries that were never fuzzed are always
    kept. The coverage that is lost this way is reset in the virgin bitmap, so
    it can be found again - by smaller and faster inputs, hopefully. With `-B`
    the bitmap is left untouched, because it is an explicit baseline of coverage
    that shall not be rediscovered. How often the queue was really minimized -
    which requires that entries were actually disabled - is reported as
    `starve_minimized` in the `fuzzer_stats` file.

  - A configuração do `AFL_KEEP_TIMEOUTS` manterá entradas de execução mais longas se chegarem
    new coverage

  - Pelo contrário, se você não estiver interessado em quaisquer timeouts, você pode definir
    `AFL_IGNORE_TIMEOUTS` to get a bit of speed instead.

  - `AFL_EXIT_ON_SEED_ISSUES` irá restaurar o comportamento de afl-fuzz baunilha que
    does not allow crashes or timeout seeds in the initial -i corpus.

  - `AFL_CRASHING_SEEDS_AS_NEW_CRASH` irá tratar as sementes de colisão como novo crash. estes
    crashes will be written to crashes folder as op:dry_run, and orig:<seed_file_name>.

  - O `AFL_EXIT_ON_TIME` faz com que o afl- fuzz termine se não foram encontrados novos caminhos
    within a specified period of time (in seconds). May be convenient for some
    types of automated jobs.

  - O `AFL_EXIT_WHEN_DONE` faz com que o afl-fuzz termine quando todos os caminhos existentes
    have been fuzzed and there were no new finds for a while. This is basically
    when the fuzzing state says `state: finished`

  - A configuração do `AFL_EXPAND_HAVOC_NOW` iniciar- se- á no modo de destruição extendido que
    includes costly mutations. afl-fuzz automatically enables this mode when
    deemed useful otherwise.

  - `AFL_FAST_CAL` mantém o estágio de calibração cerca de 2,5x mais rápido (embora menos
    precise), which can help when starting a session against a slow target.
    `AFL_CAL_FAST` works too.

  - A configuração do `AFL_FORCE_UI` forçará a pintura da UI na tela, mesmo que não
    valid terminal was detected (for virtual consoles).

  - A configuração do `AFL_FORKSRV_INIT_TMOUT` permite- lhe indicar um tempo- limite diferente
    to wait for the forkserver to spin up. The specified value is the new timeout, in milliseconds.
    The default is the `-t` value times `FORK_WAIT_MULT` from `config.h` (usually 10), so for a `-t 100`, the default would wait for `1000` milliseconds.
    The `AFL_FORKSRV_INIT_TMOUT` value does not get multiplied. It overwrites the initial timeout afl-fuzz waits for the target to come up with a constant time.
    Setting a different time here is useful if the target has a very slow startup time, for example, when doing
    full-system fuzzing or emulation, but you don't want the actual runs to wait
    too long for timeouts.

  - A configuração do `AFL_HANG_TMOUT` permite- lhe indicar um tempo- limite diferente para
    deciding if a particular test case is a "hang". The default is 1 second or
    the value of the `-t` parameter, whichever is larger. Dialing the value down
    can be useful if you are very concerned about slow inputs, or if you don't
    want AFL++ to spend too much time classifying that stuff and just rapidly
    put all timeouts in that bin.

  - Se é Jakub, pode precisar de `AFL_I_DONT_CARE_ABOUT_MISSING_CRASHES`.
    Others need not apply, unless they also want to disable the
    `/proc/sys/kernel/core_pattern` check.

  - Se afl-fuzz encontrar uma configuração incorreta do fuzzing durante uma sessão do fuzzing
    (not at startup), it will terminate. If you do not want this, then you can
    set `AFL_IGNORE_PROBLEMS`. If you additionally want to also ignore coverage
    from late loaded libraries, you can set `AFL_IGNORE_PROBLEMS_COVERAGE`.

  - Ao executar com múltiplos afl-fuzz ou com `-F`, definindo `AFL_IMPORT_FIRST`
    causes the fuzzer to import test cases from other instances before doing
    anything else. This makes the "own finds" counter in the UI more accurate.

  - Ao executar com múltiplos afl-fuzz ou com `-F`, definindo `AFL_FINAL_SYNC`
    will cause the fuzzer to perform a final import of test cases when
    terminating. This is beneficial for `-M` main fuzzers to ensure it has all
    unique test cases and hence you only need to `afl-cmin` this single
    queue.

  - Setting `AFL_INPUT_LEN_MIN` e `AFL_INPUT_LEN_MAX` são uma alternativa para
    the afl-fuzz -g/-G command line option to control the minimum/maximum
    of fuzzing input generated.

  - `AFL_KILL_SIGNAL`: Defina o ID do sinal para ser entregue aos processos infantis
    on timeout. Unless you implement your own targets or instrumentation, you
    likely don't have to set it. By default, on timeout and on exit, `SIGKILL`
    (`AFL_KILL_SIGNAL=9`) will be delivered to the child.

  - `AFL_FORK_SERVER_KILL_SIGNAL`: Defina o ID do sinal a ser entregue ao
    fork server when AFL++ is terminated. Unless you implement your
    fork server, you likely do not have to set it. By default, `SIGTERM`
    (`AFL_FORK_SERVER_KILL_SIGNAL=15`) will be delivered to the fork server.
    If only `AFL_KILL_SIGNAL` is provided, `AFL_FORK_SERVER_KILL_SIGNAL` will
    be set to same value as `AFL_KILL_SIGNAL` to provide backward compatibility.
    If `AFL_FORK_SERVER_KILL_SIGNAL` is also set, it takes precedence.

    NOTE: Uncatchable signals, such as `SIGKILL`, cause child processes of
    the fork server to be orphaned and leaves them in a zombie state.

  - `AFL_MAP_SIZE` define o tamanho do mapa compartilhado que afl-analyze, afl-fuzz,
    afl-showmap, and afl-tmin create to gather instrumentation data from the
    target. This must be equal or larger than the size the target was compiled
    with.

  - A configuração do `AFL_MAX_DET_EXTRAS` irá alterar o limiar em que número de
    elements in the `-x` dictionary and LTO autodict (combined) the
    probabilistic mode will kick off. In probabilistic mode, not all dictionary
    entries will be used all of the time for fuzzing mutations to not slow down
    fuzzing. The default count is `200` elements. So for the 200 + 1st element,
    there is a 1 in 201 chance, that one of the dictionary entries will not be
    used directly.

  - A configuração do `AFL_NO_AFFINITY` desactiva as tentativas de ligação a um núcleo específico da CPU
    on Linux systems (and disables the performance-core scheduling preference on
    macOS). This slows things down, but lets you run more instances of afl-fuzz
    than would be prudent (if you really want to).

  - `AFL_NO_ARITH` faz com que AFL++ pule a maioria das aritméticas determinísticas.
    This can be useful to speed up the fuzzing of text-based file formats.

  - A configuração do `AFL_NO_AUTODICT` não irá carregar um dicionário automático gerado pelo LTO
    that is compiled into the target.

  - A configuração de `AFL_NO_COLOR` ou `AFL_NO_COLOUR` omitirá sequências de controle para
    coloring console output when configured with USE_COLOR and not
    ALWAYS_COLORED.

  - O elemento CPU mostrado na parte inferior da tela é bastante simplista e
    may complain of high load prematurely, especially on systems with low core
    counts. To avoid the alarming red color for very high CPU usages, you can
    set `AFL_NO_CPU_RED`.

  - A configuração do `AFL_NO_FORKSRV` desativa a otimização do servidor de garfos, revertendo para
    fork + execve() call for every tested input. This is useful mostly when
    working with unruly libraries that create threads or do other crazy things
    when initializing (before the instrumentation has a chance to run).

    Note that this setting inhibits some of the user-friendly diagnostics
    normally done when starting up the forkserver and causes a pretty
    significant performance drop.

  - `AFL_NO_SNAPSHOT` irá aconselhar afl-fuzz a não usar o recurso de instantâneo se
    the snapshot lkm is loaded.

  - `AFL_NO_FASTRESUME` não tentará ler ou escrever um arquivo de currículo rápido.

  - `AFL_FORCE_FASTRESUME` por outro lado irá carregar o arquivo de currículo rápido
    (if it exists) even if the target binary was changed. Note that the
    coverage map size must be exactly the same for this to work.

  - O ajuste do `AFL_NO_UI` inibe completamente a UI e apenas periodicamente imprime
    some basic stats. This behavior is also automatically triggered when the
    output from afl-fuzz is redirected to a file or to a pipe.

  - A configuração do `AFL_NO_STARTUP_CALIBRATION` irá saltar a calibração inicial
    of all starting seeds, and start fuzzing at once. Use with care, this
    degrades the fuzzing performance!

  - A configuração do `AFL_NO_WARN_INSTABILITY` irá suprimir avisos de instabilidade.

  - No modo QEMU (- Q) e no modo FRIDA (- O), o `AFL_PATH` será procurado
    afl-qemu-trace and afl-frida-trace.so.

  - Se você estiver usando o modo persistente (você deve, veja
    [instrumentation/README.persistent_mode.md](https://github.com/AFLplusplus/AFLplusplus/blob/d0070729206a80a9af297b2341edd63f68fdac35/instrumentation/README.persistent_mode.md)),
    some targets keep inherent state due which a detected crash test case does
    not crash the target again when the test case is given. To be able to still
    re-trigger these crashes, you can use the `AFL_PERSISTENT_RECORD` variable
    with a value of how many previous fuzz cases to keep prior a crash. If set to
    e.g., 10, then the 9 previous inputs are written to out/default/crashes as
    RECORD:000000,cnt:000000 to RECORD:000000,cnt:000008 and
    RECORD:000000,cnt:000009 being the crash case. NOTE: This option needs to be
    enabled in config.h first!

  - Note que `AFL_POST_LIBRARY` está desactualizado, use `AFL_CUSTOM_MUTATOR_LIBRARY`
    instead.

  - A configuração do `AFL_PRELOAD` faz com que o AFL++ defina o `LD_PRELOAD` para o binário alvo
    without disrupting the afl-fuzz process itself. This is useful, among other
    things, for bootstrapping libdislocator.so.

  - `AFL_SHA1_FILENAMES` faz com que AFL++ gere arquivos nomeados pelo hash SHA1
    of their contents, rather than use the standard `id:000000,...` names.
    Warning: this disables any syncing to any AFL instances!

  - `AFL_SHM_KEEP_NAME` mantém os objetos de memória compartilhados POSIX (a cobertura,
    CmpLog, value profile, state and shared memory test case maps) reachable
    under their name for the whole session. Only relevant where those maps are
    POSIX shared memory - macOS and any build with `USEMMAP`, i.e. not the
    default Linux build, which uses SysV segments. Normally each map is
    `shm_unlink()`ed the moment it is created and only handed to the target as
    an inherited file descriptor, so a SIGKILLed fuzzer cannot leave anything
    behind in `/dev/shm`. Set this if the target was built by an afl-cc that
    predates the descriptor handover and can therefore only `shm_open()` the
    name - the trade-off is that the maps leak if the fuzzer is SIGKILLed.
    Rebuilding the target is the better fix. It also applies to afl-showmap,
    afl-tmin, afl-analyze, afl-cmin and afl-merge.

  - O `AFL_SHUFFLE_QUEUE` reordena aleatoriamente a fila de entrada na inicialização. Solicitado
    by some users for unorthodox parallelized fuzzing setups, but not advisable
    otherwise.

  - Ao desenvolver instrumentação personalizada em cima de afl-fuzz, você pode usar
    `AFL_SKIP_BIN_CHECK` to inhibit the checks for non-instrumented binaries and
    shell scripts; and `AFL_DUMB_FORKSRV` in conjunction with the `-n` setting
    to instruct afl-fuzz to still follow the fork server protocol without
    expecting any instrumentation data in return. Note that this also turns off
    auto map size detection.

  - A configuração do `AFL_SKIP_CPUFREQ` ignora a verificação da política de escalonamento da CPU. Isto é
    useful if you can't change the defaults (e.g., no root access to the system)
    and are OK with some performance loss.

  - A configuração do `AFL_STATSD` permite a recolha de métricas StatsD. Por omissão, o AFL++
    will send these metrics over UDP to 127.0.0.1:8125. The host and port are
    configurable with `AFL_STATSD_HOST` and `AFL_STATSD_PORT` respectively. To
    enable tags (banner and afl_version), you should provide
    `AFL_STATSD_TAGS_FLAVOR` that matches your StatsD server (see
    `AFL_STATSD_TAGS_FLAVOR`).

  - Configurando `AFL_STATSD_TAGS_FLAVOR` para um dos `dogstatsd`, `influxdb`,
    `librato`, or `signalfx` allows you to add tags to your fuzzing instances.
    This is especially useful when running multiple instances (`-M/-S` for
    example). Applied tags are `banner` and `afl_version`. `banner` corresponds
    to the name of the fuzzer provided through `-M/-S`. `afl_version`
    corresponds to the currently running AFL++ version (e.g., `++3.0c`). Default
    (empty/non present) will add no tags to the metrics. For more information,
    see [rpc_statsd.md](aflplusplus-docs-rpc-statsd-md.md).

  - `AFL_SYNC_TIME` permite que você especifique um tempo mínimo diferente (em minutos)
    between fuzzing instances synchronization. Default sync time is 20 minutes,
    note that time is halved for -M main nodes.

  - `AFL_NO_SYNC` desativa qualquer sincronização e tem prioridade em todos
    other syncing parameters, including a sync forced with `SIGUSR2`.

  - A configuração do `AFL_TARGET_ENV` faz com que o AFL++ defina variáveis de ambiente extra para
    the target binary. Example: `AFL_TARGET_ENV="VAR1=1 VAR2='a b c'" afl-fuzz
    ... `. This exists mostly for things like `LD_LIBRARY_PATH` but it would
    theoretically allow fuzzing of AFL++ itself (with 'target' AFL++ using some
    AFL_ vars that would disrupt work of 'fuzzer' AFL++). Note that when using
    QEMU mode, the `AFL_TARGET_ENV` environment variables will apply to QEMU, as
    well as the target binary. Therefore, in this case, you might want to use
    QEMU's `QEMU_SET_ENV` environment variable (see QEMU's documentation because
    the format is different from `AFL_TARGET_ENV`) to apply the environment
    variables to the target and not QEMU.

  - O `AFL_TESTCACHE_ENTRIES` é obsoleto e ignorado.
    bounded by `AFL_TESTCACHE_SIZE` alone.

  - `AFL_TESTCACHE_SIZE` permite que você sobreponha o tamanho de `#defina
    TESTCASE_CACHE` in config.h. Recommended values are 50-250MB - or more if
    your fuzzing finds a huge amount of paths for large inputs. The cache
    holds the queue entries with the highest selection probability per byte,
    so a larger value keeps paying off.

  - `AFL_TMPDIR` é usado para escrever o arquivo `.cur_input` para se ele existe, e em
    the normal output directory otherwise. You would use this to point to a
    ramdisk/tmpfs. This increases the speed by a small value but also reduces
    the stress on SSDs.

  - A configuração do `AFL_TRY_AFFINITY` tenta tentar ligar a um núcleo específico da CPU
    on Linux systems, but will not terminate if that fails.

  - Por padrão no Linux, o modo persistente usa memória compartilhada e futexes para
    child synchronization. This reduces the overhead of communication between
    afl-fuzz and the persistent target child. Setting `AFL_OLD_CHILD_SYNC`
    restores the old file descriptor based persistent synchronization behavior.

  - As seguintes variáveis de ambiente só são necessárias se você implementar
    your own forkserver or persistent mode, or if __AFL_LOOP or __AFL_INIT
    are in a shared library and not the main binary:
    - `AFL_DEFER_FORKSRV` enforces a deferred forkserver even if none was
      detected in the target binary
    - `AFL_PERSISTENT` enforces persistent mode even if none was detected
      in the target binary

  - Se você precisar de um servidor de garfos no seu alvo por causa do início
    constructors in your target, you can set `AFL_EARLY_FORKSERVER`.
    Note that this is not a compile time option but a runtime option :-)

  - Defina `AFL_PIZZA_MODE` para 1 para habilitar o primeiro menu de estatísticas de 1o de abril, definido para -1
    to disable although it is 1st of April. 0 is the default and means enable
    on the 1st of April automatically.

  - Se você precisar de um intervalo específico para atualizar o arquivo fuzzer_stats, você pode
    set `AFL_FUZZER_STATS_UPDATE_INTERVAL` to the interval in seconds you'd
    the file to be updated.
    Note that will not be exact and with slow targets it can take seconds
    until there is a slice for the time test.

  - Ao usar `AFL_PRELOAD` com uma pré-carga que desativa o `fork()`
    the target, the forkserver becomes unable to fork.
    To overcome this issue, the `AFL_PRELOAD_DISCRIMINATE_FORKSERVER_PARENT`
    permits to be able to check in the preloaded library if the environment
    variable `AFL_FORKSERVER_PARENT` is set, to be able to use vanilla
    `fork()` in the forkserver, and the placeholder in the target.
    Here is a POC :
    ```C
    // AFL_PRELOAD_DISCRIMINATE_FORKSERVER_PARENT=1 afl-fuzz ...
    pid_t fork(void)
    {
        if (getenv("AFL_FORKSERVER_PARENT") == NULL)
            return 0; // We are in the target
        else
            return real_fork(); // We are in the forkserver
    }
    ```

  - O `AFL_FORKSRV_UID` permite- lhe indicar o UID que deverá ser usado quando
    running the fork server. When setting this variable, user should ensure
    afl-fuzz binary has enough privileges to modify the UID (e.g. CAP\_SETUID
    capability in Linux system).

  - O `AFL_FORKSRV_GID` permite- lhe indicar o GID e o grupo suplementar
    IDs that should be used when running the fork server. When setting this
    variable, user should ensure afl-fuzz binary has enough privileges to
    modify the GIDs (e.g. CAP\_SETGID capability in Linux system).

  - Quando ambos `AFL_FORKSRV_UID` e `AFL_FORKSRV_GID` são definidos, binário afl-fuzz
    and the fork server no longer share any IDs. Thus, afl-fuzz binary changes
    the group owner of the created files to ensure that the fork server can
    still access them. In such case, user should ensure afl-fuzz binary has
    enough privileges to modify the ownership of entities (e.g. CAP\_CHOWN
    capability in Linux system).

  - A configuração do `AFL_FRAMESHIFT_DISABLE` irá desativar o estágio de análise do frameshift.
    Frameshift automatically discovers size/offset fields in structured inputs
    and keeps them consistent as mutations insert or delete bytes. Disabling it
    may be useful for targets that do not consume structured binary formats, or
    when you want to avoid the overhead of the analysis entirely.

  - `AFL_FRAMESHIFT_MAX_OVERHEAD` controla a fração máxima do total fuzzing
    time that frameshift analysis is allowed to consume. The value is a float
    between `0.0` and `1.0` (default `0.10`, i.e. 10%). It is enforced as a token
    bucket: credit accrues as this fraction of the total run time and each
    analysis slice spends from it. A new slice is admitted only when enough
    credit remains for a minimally useful slice, and its deadline is capped to
    the remaining credit, so a single slice cannot overshoot the configured
    overhead by a full analysis budget.

  - Normalmente um `README.txt` é escrito para o diretório `crashes/` quando um primeiro
    crash is found. Setting `AFL_NO_CRASH_README` will prevent this. Useful when
    counting crashes based on a file count in that directory.

## 6) Configurações para afl-qemu-trace

O wrapper QEMU usado para instrumentar código somente binário suporta várias configurações:

  - A configuração do `AFL_QEMU_CUSTOM_BIN` fará com que o afl- fuzz salte a pré- pendente
    `afl-qemu-trace` to your command line. Use this if you wish to use a
    custom afl-qemu-trace or if you need to modify the afl-qemu-trace
    arguments.

  - Configurando o `AFL_COMPCOV_LEVEL` permite o rastreamento CompareCoverage de todos os cmp
    and sub in x86 and x86_64 and memory comparison functions (e.g., strcmp,
    memcmp, ...) when libcompcov is preloaded using `AFL_PRELOAD`. More info at
    [qemu_mode/libcompcov/README.md](https://github.com/AFLplusplus/AFLplusplus/blob/d0070729206a80a9af297b2341edd63f68fdac35/qemu_mode/libcompcov/README.md).

    There are two levels at the moment, `AFL_COMPCOV_LEVEL=1` that instruments
    only comparisons with immediate values / read-only memory and
    `AFL_COMPCOV_LEVEL=2` that instruments all the comparisons. Level 2 is more
    accurate but may need a larger shared memory.

  - O `AFL_DEBUG` irá imprimir o ponto de entrada encontrado para o binário para o stderr. Use
    this if you are unsure if the entry point might be wrong - but use it
    directly, e.g., `afl-qemu-trace ./program`.

  - `AFL_ENTRYPOINT` permite que você especifique um ponto de entrada específico no
    binary (this can be very good for the performance!). The entry point is
    specified as hex address, e.g., `0x4004110`. Note that the address must be
    the address of a basic block.

  - Configurando `AFL_INST_LIBS` faz com que o tradutor também instrumente o código
    inside any dynamically linked libraries (notably including glibc).

  - Você pode usar `AFL_QEMU_INST_RANGES=0xaaaa-0xbbbb,0xcccc-0xdddd` para apenas
    instrument specific memory locations, e.g. a specific library. You may
    also provide the filename of the library. Excluding ranges takes priority
    over any included ranges or `AFL_INST_LIBS`. See
    [qemu_mode/README.md#partial-instrumenation](https://github.com/AFLplusplus/AFLplusplus/blob/d0070729206a80a9af297b2341edd63f68fdac35/qemu_mode/README.md#6-partial-instrumentation)).

  - Você pode usar `AFL_QEMU_EXCLUDE_RANGES=0xaaaa-0xbbbb,0xcccc-0xdddd` para **NOT**
    instrument specific memory locations, e.g. a specific library.
    Excluding ranges takes priority over any included ranges or `AFL_INST_LIBS`.

  - É possível definir `AFL_INST_RATIO` para pular a instrumentação em alguns
    of the basic blocks, which can be useful when dealing with very complex
    binaries.

  - Configurando o `AFL_QEMU_COMPCOV` permite o rastreamento CompareCoverage de todos os cmp
    and sub in x86 and x86_64. This is an alias of `AFL_COMPCOV_LEVEL=1` when
    `AFL_COMPCOV_LEVEL` is not specified.

  - Com `AFL_QEMU_FORCE_DFL`, você força o QEMU a ignorar o sinal registrado
    handlers of the target.

  - Quando o alvo é i386/x86_64, você pode especificar o endereço da função
    that has to be the body of the persistent loop using
    `AFL_QEMU_PERSISTENT_ADDR=start addr`.

  - Com o `AFL_QEMU_PERSISTENT_GPR=1`, o QEMU salvará o valor original de
    general purpose registers and restore them in each persistent cycle.

  - Outra modalidade para executar o loop persistente é especificar também o
    `AFL_QEMU_PERSISTENT_RET=end addr` environment variable. With this variable
    assigned, instead of patching the return address, the specified instruction
    is transformed to a jump towards `start addr`.

  - Com o `AFL_QEMU_PERSISTENT_RETADDR_OFFSET`, você pode especificar o deslocamento de
    the stack pointer in which QEMU can find the return address when `start
    addr` is hit.

  - Com `AFL_USE_QASAN`, você pode ativar QEMU AddressSanitizer para dinamicamente
    linked binaries.

  - Usando AFL_QEMU_IJON=test.conf permite qemu chamar a função ijon,
    which allows aflpp to additionally gain awareness of 
    changes in key variables of the target program, 
    which is an excellent supplement to coverage-only feedback.(see
    [qemu_mode/README.md](https://github.com/AFLplusplus/AFLplusplus/blob/d0070729206a80a9af297b2341edd63f68fdac35/qemu_mode/README.md) for more details).

  - O binário QEMU subjacente reconhecerá qualquer "espaço de usuário padrão"
    emulation" variables (e.g., `QEMU_STACK_SIZE`), but there should be no
    reason to touch them.

## 7) Configurações para afl-frida-trace

A embalagem FRIDA usada para instrumentar o código somente binário suporta muitos dos mesmos
opções como `afl-qemu-trace`, mas também tem um número de avançado adicional
opções. Estes estão listados em breve abaixo (ver
[frida_mode/README.md](https://github.com/AFLplusplus/AFLplusplus/blob/d0070729206a80a9af297b2341edd63f68fdac35/frida_mode/README.md) para mais detalhes).
as configurações são fornecidas para compatibilidade com o modo QEMU, a maneira preferida de
configure o modo FRIDA através do seu [scripting](https://github.com/AFLplusplus/AFLplusplus/blob/d0070729206a80a9af297b2341edd63f68fdac35/frida_mode/Scripting.md)
apoio.

* `AFL_FRIDA_DEBUG_MAPS` - Ver `AFL_QEMU_DEBUG_MAPS`
* `AFL_FRIDA_DRIVER_NO_HOOK` - Veja `AFL_QEMU_DRIVER_NO_HOOK`. Ao usar o
Controlador QEMU para fornecer um loop `main` para um usuário fornecido
`LLVMFuzzerTestOneInput`, esta opção configura o driver para ler a entrada de
`stdin` em vez de usar casos de teste em memória.
* `AFL_FRIDA_EXCLUDE_RANGES` - Ver `AFL_QEMU_EXCLUDE_RANGES`
* `AFL_FRIDA_INST_COVERAGE_FILE` - Arquivo para escrever cobertura de formato DynamoRio
informações (por exemplo, a serem carregadas no farol IDA).
* `AFL_FRIDA_INST_DEBUG_FILE` - Arquivo para escrever montagem bruta de blocos originais
e seus homólogos instrumentados durante a compilação em bloco.
* `AFL_FRIDA_INST_JIT` - Activar a instrumentação do Just-In-Time compilado
código. O código é considerado JIT se o segmento executável não for suportado por
Um arquivo.
* `AFL_FRIDA_INST_NO_DYNAMIC_LOAD` - Não instrumente o código carregado até tarde
tempo de execução. Estritamente limita a instrumentação ao que foi incluído.
* `AFL_FRIDA_INST_NO_OPTIMIZE` - Não use cobertura de montagem em linha otimizada
instrumentação (o padrão quando disponível).
`AFL_FRIDA_INST_TRACE`.
* `AFL_FRIDA_INST_NO_BACKPATCH` - Desabilitar o backpatching. No final da execução
cada bloco, o controle retornará à FRIDA para identificar o próximo bloco para
executar.
* `AFL_FRIDA_INST_NO_PREFETCH` - Desactivar o prefetching. Por omissão, o filho irá
reportar os blocos instrumentados de volta para o pai para que ele também possa instrumentar
eles e eles são herdados pela próxima criança no garfo, implica
`AFL_FRIDA_INST_NO_PREFETCH_BACKPATCH`.
* `AFL_FRIDA_INST_NO_PREFETCH_BACKPATCH` - Desactivar a prefetching do perseguidor
informações de backpatching. Por padrão, o filho irá relatar
backpatches para o pai para que eles possam ser aplicados e, em seguida, ser herdados por
A próxima criança no garfo.
* `AFL_FRIDA_INST_RANGES` - Ver `AFL_QEMU_INST_RANGES`
* `AFL_FRIDA_INST_SEED` - Define a semente inicial para a função de hash usada para
gerar IDs de bloco (e, portanto, borda). Definir isto para um valor constante pode ser
útil para fins de depuração, por exemplo, para investigar bordas instáveis.
* `AFL_FRIDA_INST_TRACE` - Log to stdout o endereço dos blocos executados, implica
`AFL_FRIDA_INST_NO_OPTIMIZE`.
* `AFL_FRIDA_INST_TRACE_UNIQUE` - De acordo com `AFL_FRIDA_INST_TRACE`, mas cada borda
é registrado apenas uma vez, requer `AFL_FRIDA_INST_NO_OPTIMIZE`.
* `AFL_FRIDA_INST_UNSTABLE_COVERAGE_FILE` - Arquivo para escrever o formato DynamoRio
informações de cobertura para as bordas instáveis (por exemplo, a serem carregadas no IDA)
farol).
* `AFL_FRIDA_JS_SCRIPT` - Defina o script a ser carregado pelo script FRIDA
motor. Veja [frida_mode/Scripting.md](https://github.com/AFLplusplus/AFLplusplus/blob/d0070729206a80a9af297b2341edd63f68fdac35/frida_mode/Scripting.md) para detalhes.
* `AFL_FRIDA_OUTPUT_STDOUT` - Redirecionar a saída padrão do alvo
aplicativo para o arquivo nomeado (supervisiona a configuração do `AFL_DEBUG_CHILD`)
* `AFL_FRIDA_OUTPUT_STDERR` - Redireccionar o erro padrão do alvo
aplicativo para o arquivo nomeado (supervisiona a configuração do `AFL_DEBUG_CHILD`)
* `AFL_FRIDA_PERSISTENT_ADDR` - Ver `AFL_QEMU_PERSISTENT_ADDR`
* `AFL_FRIDA_PERSISTENT_CNT` - Ver `AFL_QEMU_PERSISTENT_CNT`
* `AFL_FRIDA_PERSISTENT_DEBUG` - Inserir um ponto de interrupção no código instrumentado
em `AFL_FRIDA_PERSISTENT_HOOK` e `AFL_FRIDA_PERSISTENT_RET` para permitir que
usuário para detectar problemas no loop persistente usando um depurador.
* `AFL_FRIDA_PERSISTENT_HOOK` - Ver `AFL_QEMU_PERSISTENT_HOOK`
* `AFL_FRIDA_PERSISTENT_RET` - Ver `AFL_QEMU_PERSISTENT_RET`
* `AFL_FRIDA_SECCOMP_FILE` - Escreva um log de quaisquer syscalls feitos pelo alvo para
o arquivo especificado.
* `AFL_FRIDA_STALKER_ADJACENT_BLOCKS` - Configurar o número de blocos adjacentes
para obter ao gerar código instrumentado. Obtendo blocos no mesmo
ordem que aparecem no programa original, em vez da ordem de execução
deve ajudar a reduzir a localidade e adjacência. Isso inclui permitir-nos
vetor entre blocos adjacentes usando um slide NOP em vez de um imediato
Branch.
* `AFL_FRIDA_STALKER_IC_ENTRIES` - Configurar o número de entradas de cache em linha
instruções de ramo ao longo do lado que fornecem um cache para evitar ter que
Ligue de volta para o FRIDA para encontrar o próximo bloco. O padrão é 32.
* `AFL_FRIDA_STATS_FILE` - Escreva informações estatísticas sobre o código
instrumentado para o nome do arquivo indicado. As estatísticas são escritas apenas para o
processo infantil quando novo bloco é instrumentado (quando o
O `AFL_FRIDA_STATS_INTERVAL` expirou. Repare que só porque um novo caminho é
encontrado não significa que um novo bloco precisa ser compilado. Pode ser que o
os blocos existentes instrumentados foram executados em uma ordem diferente.
* `AFL_FRIDA_STATS_INTERVAL` - A frequência máxima para estatísticas de saída
informações. As estatísticas serão escritas sempre que forem atualizadas se o dado
O intervalo foi decorrido desde a última vez que foram escritos.
* `AFL_FRIDA_TRACEABLE` - Defina o processo filho para ser rastreável por qualquer processo
ajudar a depurar e superar as restrições impostas pelo YAMA. Apoiado
Somente Linux. Permite que um usuário não- root use `gcore` ou similar para coletar um
descarte do núcleo do alvo instrumentado. Observe que para capturar o núcleo
descarte você deve definir um tempo limite suficiente (usando `-t`) para evitar `afl-fuzz`
matar o processo enquanto está a ser despejado.

## 8) Configurações para afl-cmin e afl-merge

`afl-cmin` (e sua ligação simbólica `afl-merge`) oferece muito pouca personalização:

  - `AFL_MAP_SIZE` (também conhecido por `AFL_MAPSIZE`) define o tamanho do mapa de cobertura em vez de
    detecting it from the target. The value is validated and rounded up to a
    multiple of 64, exactly as for the other tools.

  - `AFL_SHA1_FILENAMES` nomeia os arquivos de saída após o SHA-1 de seus
    contents instead of keeping the original file name.

  - `AFL_INPUT_PLACEHOLDER` substitui `@@` como placeholder do arquivo de entrada no
    target command line.

  - A configuração do `AFL_PATH` oferece uma forma de especificar a localização do afl-qemu-trace
    (`-Q` mode) and libnyx.so (`-X` mode).

  - `AFL_SKIP_BIN_CHECK` ignora a verificação de instrumentação do binário alvo.

Arquivos temporários (o caso de teste entregue ao alvo e o rastro por trabalhador)
logs) são mantidos em um diretório privado abaixo do diretório de saída que é
removido novamente quando a execução terminar, também quando falhar.

As variantes do script (`afl-cmin.py`, `afl-cmin.bash`) coletam cobertura com
`afl-showmap` e também honrar `AFL_ALLOW_TMP`, `AFL_KEEP_TRACES`
(deixando `<out_dir>/.traces/` no lugar) e `AFL_CMIN_ALLOW_ANY`, mais cada
Variável `afl-showmap`, como `AFL_PRINT_FILENAMES`.

## 9) Configurações para afl-tmin

Praticamente nada para jogar. Bem, no modo QEMU (`-Q`), `AFL_PATH` será
pesquisado por afl- qemu- trace. Além disso, o `TMPDIR` pode ser usado se
arquivo temporário não pode ser criado no diretório de trabalho atual.

Você pode especificar `AFL_TMIN_EXACT` se quiser que o afl-tmin exija caminhos de execução
para corresponder ao minimizar falhas. Isto tornará a minimização menos útil, mas
pode impedir que a ferramenta de "jumping" de uma condição de colisão para outra em
software muito buggy. Você provavelmente quer combiná-lo com a bandeira `-e`.

## 10) Configurações para afl-analyze

Você pode definir `AFL_ANALYZE_HEX` para obter deslocamentos de arquivos impressos como hexadecimal em vez
decimal.

## 11) Configuração do libdislocator

A biblioteca honra estas variáveis de ambiente:

  - `AFL_ALIGNED_ALLOC=1` irá forçar o alinhamento do tamanho da alocação para
    `max_align_t` to be compliant with the C standard.

  - `AFL_LD_HARD_FAIL` altera o comportamento chamando `abort()` em excesso
    allocations, thus causing what AFL++ would perceive as a crash. Useful for
    programs that are supposed to maintain a specific memory footprint.

  - `AFL_LD_LIMIT_MB` cobre o tamanho do uso máximo de heap permitido pelo
    library, in megabytes. The default value is 1 GB. Once this is exceeded,
    allocations will return NULL.

  - `AFL_LD_NO_CALLOC_OVER` inibe `abort()` no `calloc()` transborda.
    the common allocators check for that internally and return NULL, so it's a
    security risk only in more exotic setups.

  - `AFL_LD_VERBOSE` faz com que a biblioteca para produzir algumas mensagens de diagnóstico que
    may be useful for pinpointing the cause of any observed issues.

## 12) Configuração da libtokencap

Esta biblioteca aceita `AFL_TOKEN_FILE` para indicar a localização para a qual o
Os símbolos descobertos devem ser escritos.

## 13) Variáveis de terceiros definidas por afl-fuzz & outras ferramentas

Várias variáveis não são interpretadas diretamente pelo afl-fuzz, mas são definidas para
valores óptimos, se já não estiverem presentes no ambiente:

  - Por padrão, `ASAN_OPTIONS` são definidos como (entre outros):

    ```text
    abort_on_error=1
    detect_leaks=0
    malloc_context_size=0
    symbolize=0
    allocator_may_return_null=1
    ```

    If you want to set your own options, be sure to include `abort_on_error=1` -
    otherwise, the fuzzer will not be able to detect crashes in the tested app.
    Similarly, include `symbolize=0`, since without it, AFL++ may have
    difficulty telling crashes and hangs apart.

  - Da mesma forma, o `LSAN_OPTIONS` padrão está definido como:

    ```text
    exit_code=23
    fast_unwind_on_malloc=0
    symbolize=0
    print_suppressions=0
    ```

    Be sure to include the first ones for LSAN and MSAN when customizing
    anything, since some MSAN and LSAN versions don't call `abort()` on error,
    and we need a way to detect faults.

  - Na mesma veia, por padrão, `MSAN_OPTIONS` são definidos como:

    ```text
    exit_code=86 (required for legacy reasons)
    abort_on_error=1
    symbolize=0
    msan_track_origins=0
    allocator_may_return_null=1
    ```

  - Por padrão, `LD_BIND_NOW` é definido para acelerar fuzzing, forçando o linker
    to do all the work before the fork server kicks in. You can override this by
    setting `LD_BIND_LAZY` beforehand, but it is almost certainly pointless.


---

## Procedência desta tradução

Fonte: [https://github.com/AFLplusplus/AFLplusplus](https://github.com/AFLplusplus/AFLplusplus/blob/d0070729206a80a9af297b2341edd63f68fdac35/docs/env_variables.md). Licença: [AGPL-3.0](../../99-Assets/upstream/aflplusplus/LICENSE.txt). Commit: d0070729206a80a9af297b2341edd63f68fdac35.

O original preservado, a lista de mudanças de apresentação e os hashes constam no manifesto do projeto. Nenhum exemplo desta documentação foi executado automaticamente.
