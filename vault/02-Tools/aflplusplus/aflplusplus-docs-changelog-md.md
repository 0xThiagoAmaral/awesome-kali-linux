---
title: "aflplusplus — documentação oficial"
type: "official-documentation"
tool: "aflplusplus"
status: "translated-machine"
reviewed: "2026-10-26"
language: "pt-BR"
tags: ["documentation", "tool/aflplusplus"]
cssclasses: ["fieldbook"]
source_url: "https://github.com/AFLplusplus/AFLplusplus/blob/d0070729206a80a9af297b2341edd63f68fdac35/docs/Changelog.md"
source_commit: "d0070729206a80a9af297b2341edd63f68fdac35"
source_sha256: "2b8190c09159c7fefb1ae01c0fa525343fc27e588b104dd08dfe9638058a42fc"
license_spdx: "AGPL-3.0-or-later"
human_review: "pending"
source_scope: "Repository root README and owned doc/docs/documentation Markdown or RST files; not a claim of full wiki/site coverage"
---

> Tradução automática local para português, ainda sem revisão humana integral. Estrutura e blocos de código preservados; referências externas não significam conteúdo espelhado.

# Changelog

Esta é a lista de todas as alterações notáveis feitas em cada público
lançamento da ferramenta. Consulte README.md para o manual geral de instruções.

### Versão ++5.04a (dev)
  - afl-fuzz
    - frameshift timeout fix (fixes spurious timeouts that can occur, especially
      with persistent loop counts of 1
  - afl-cc
    - a plain `-fcf-protection` (part of the default hardened CFLAGS on
      Fedora/RHEL) was mistaken for `AFL_USE_CFISAN` and injected `-flto`,
      which silently disabled PCGUARD instrumentation for the target


### Versão ++5.03c (lançamento)
! Implementação do Perfil de Valor para AFL++ por Khaled Yakdan (@kyakdan) que
    is much more efficient and intelligent than the libfuzzer implementation.
    Enable in the fuzz target with `AFL_LLVM_VALUE_PROFILE=1` and enable for
    afl-fuzz with `-r <seconds>` when to activate (default off)
! macOS agora usa POSIX memória compartilhada em vez de SysV, que levanta o
    `kern.sysv.shmseg` / `kern.sysv.shmmax` ceilings (CmpLog alone needs a
    145 MB segment, far past the 4 MB macOS default). !!! You need to
    recompile your targets on macOS - a target built by an older afl-cc still
    expects a SysV id in `__AFL_SHM_ID` !!!
afl-fuzz
    - big change: limits before switching modes is not time based but exec based now.
    - fix: shmem leakage on target timeouts and crashes - this has been the case
      since vanilla AFL. Now fixed for Linux, MacOS and mmap targets.
    - for more variability, a "starved" mode is implemented now. If for a longer
      time no finds are found, then more seed and mutation variability is
      introduced incl. splicing phase enabled. This is visible in the UI.
    - env `AFL_STARVED_MINIMIZE_QUEUE`: if starve mode does not help either,
      minimize the the queue like afl-cmin does and make the coverage of the
      removed entries rediscoverable. Inspired by `Novelty Not Found: Adaptive
      Fuzzer Restarts to Improve Input Space Coverage`
    - sending `SIGUSR2` forces a sync (AFL internal sync and foreign `-F` ) as
      soon as the current queue entry has been fuzzed
    - the trimming stage no longer throws away what it produces: crashes,
      hangs and new coverage found while shortening a queue entry are now
      saved (visible as `op:trim`/`op:ptrim` in the file names)
    - `-s fixed_seed` now only sets a fixed seed and does not ignore timings
      anymore (required for proper benchmarking in containers without urandom)
    - `-t xxx+` fix so dummy seeds do not kill a start-up. rechecks now over
      time
    - a queue entry that fails its calibration is never fuzzed, so the
      coverage it claimed is now handed back to `virgin_bits` and can be
      rediscovered by an input that does calibrate.
    - the variable behavior flag of a queue entry is cleared now on slow
      resumes, another afl vanilla legacy bug
    - fixed SAND and FrameShift issues
    - symlinked test cases and symlinked subdirectories in the `-i` input
      directory are now followed
    - foreign sync directories (`-F`) now import symlinked test cases too
    - enhancements and fixes for cmplog and ijon
    - due to a bug first introduced in v4.30c the cmplog target was used for
      fuzzing if present - fixed
    - an unreadable foreign sync (`-F`) directory is reported now, once per
      directory, and the directories are listed at startup - a mistyped path
      was silently ignored for the whole run before
    - the queue driver always returns to the main loop now, even when every
      entry it looks at is skipped
    - a custom mutator that fails to load because it was built with an
      instrumenting compiler is named as such instead of just showing the
      missing `__afl_*` symbol
  - afl-cc
    - remove classic AFL instrumentation (colliding coverage), as `AFL_LLVM_PATH`
      and `AFL_LLVM_CALLER` replace these mostly and are overall much better
    - more invisible decisions can be instrumented now, all optional
    - new env var `AFL_LLVM_DENSE=1` to disable PCGUARD basic block pruning
    - new env var `AFL_LLVM_MINMAX=1` scores min/max/abs intrinsics, i.e.
      clamps that the optimizer made branchless. Default off: it adds 10% map
      entries but costs 20% throughput
    - new env var `AFL_LLVM_FUSED=1` scores both halves of a fused condition,
      i.e. `if (a && b)` speculated into a single `and i1`
    - new env var `AFL_LLVM_VECTORS=1` instruments vector selects and vector
      min/max one guard pair per lane (default off, they are rarely worth it)
    - removed the obsolete afl-as assembler wrapper and its remaining references
    - headers shipped in a source checkout are found in `include/` now, an
      in-tree build silently preferred an older installed copy before
    - fix: `CODE_COVERAGE=1` builds
    - IJON: the map expansion is re-applied after a guard-init reset, so a
      target whose coverage is split over several instrumented modules gets
      the full map; the IJON channels also stay live under a tool that
      attached a map without being a forkserver parent (`afl-showmap` on a
      single input, `afl-cmin.bash`); `AFL_DUMP_MAP_SIZE` prints the
      coverage/IJON breakdown to stderr
  - afl-cmin:
    - (all variants: C, python, bash, awk): empty (0 byte) input files are now
      skipped, plus various other fixes and corner case handling
    - afl-merge (symlink) - merge new files into an existing corpus (that is
      not minimized)
    - afl-cmin.c is now the default afl-cmin, but it needed a larger rewrite
    - `-T all` (C and python variants) now counts the CPUs the process is
      actually allowed to run on (like `nproc` does)
    - fix: afl-cmin.c asked afl_shm_init() to chown the shared maps to gid 0,
      which aborted with `fchown() failed` on POSIX shared memory. No tool
      wants a chown here, so it now passes -1 like all the others do.
  - afl- showmap:
    - `-i` now follows symlinked test cases and symlinked subdirectories
    - a child killed by a signal no longer reports a garbage exit code in
      streaming mode (`-S`)
    - the target's instrumentation is checked in `-I` and `-S` mode too, not
      only with `-i`
  - afl-showmap, afl-cmin, afl-tmin, afl-analyze:
    - the IJON max-value slots and a bug-pass map are no longer counted as
      coverage: they hold wide values, not hit counts, and were reported as
      tuples, minimised against and bucket-classified in place
    - fix: releaseshared memory when aborted
  - afl-saúde
    - more speed, more info, a few fixes
  - _mutadores personalizados:
    - removed outdated and pointless radamsa
  - modo_ frida:
    - fix arm64 inline coverage ADRP fixups when instrumentation suppression is
      disabled


### Versão ++5.02c (lançamento)
!!! Você precisa recompilar o modo persistente / LLVMFuzzerTestOneInput alvo !!!!
  - afl-saúde:
    - new tool: AFL++ campaign health tool checker, much more advanced than
      afl-whatsup, with tips, analysis and ssh support
  - Afl-fuzz:
    - Futex implementation missed the clean-up of the shmem
    - Futex shmem now lives in general shared memory map as by default only
      32 such regions are supported in MacOS
    - new runtime value-profiling guidance mode (`-r0`/`-rN`) for LLVM targets
      compiled with `AFL_LLVM_VALUE_PROFILE=1`
  - afl-cc:
    - new C11 mode (`AFL_LLVM_C11` at compile time): afl-cc records each
      function's local variable count and afl-fuzz uses it as an extra queue
      scheduling signal to favor more complex code paths. Noticably improvement,
      based on the paper https://mlsec.org/docs/2026-icse.pdf
    - if `-fsanitize-coverage-allowlist=`/`-fsanitize-coverage-ignorelist=` is
      passed without `AFL_LLVM_ALLOWLIST`/`AFL_LLVM_DENYLIST` being set, the
      supplied list is reused as `AFL_LLVM_ALLOWLIST`/`AFL_LLVM_DENYLIST` (with
      a warning) so the optimized PCGUARD honors it
    - instrument allow/deny lists (`AFL_LLVM_ALLOWLIST`/`AFL_LLVM_DENYLIST` and
      the GCC equivalents): function (`fun:`) entries are now matched verbatim
      with `fnmatch()` instead of having a `*` prepended automatically - add a
      leading `*` yourself for a suffix match. Function entries are matched
      against both the mangled and the demangled (LLVM) / unqualified (GCC)
      name, and an explicit `fun:` prefix now permits `:` so demangled C++/Rust
      names can be listed. File (`src:`) entries are unchanged and still match
      as a suffix (an implicit leading `*`)
    - AFL_LLVM_CRASHLIST - crash on any function that is marked not to be
      instrumented but is entered by fuzzing input
    - bugfix for __AFL_LOOP() that lingered since vanilla afl, first run
      coverage map would look different to following runs, impacting lots of
      functionality (minimizing, stability, etc.)
  - ferramentas de script afl-*:
    - prefer AFL_PATH to find afl-showmap
  - páginas man: fixou as seções SINOPSIS e OPTIONS para várias ferramentas


### Versão ++5.01c (lançamento)
  - O modo persistente do MacOS agora usa o modo futex agora também o que aumenta a velocidade
    and reduces system call overhead (opt out with AFL_FAST_CHILD_SYNC) - this
    requires a MacOS from 2024 onwards (Sonoma 14.4+).
  - afl-fuzz
    - new adaptive MOpt! Much better than the outdated one we still had.
      How good it is still needs to be seen but initially it seems to be
      better than standard havoc
    - enforce halt on UBSAN errors
  - afl-cc:
    - enforce halt on UBSAN errors (AFL_USE_USBAN=1)
    - better cmplog on MacOS
    - removed unsupported LLVM version code paths from afl-cc and llvm passes
    - compcov: fixes for float splittings (thanks to @ngg)
  - nyx_mode:
    - fix nyx_mode issues (thanks to @morehouse)
  - modo_ qemu:
    - non-colliding coverage!
    - faster persistent fuzzing
    - minor bug fixes
  - Qemu_bridge:
    - new mode with current QEMU version, so plugins possible, new processors
    - sightly slower than qemu_mode
    - WIP!


### Versão ++5.00c (lançamento)
! AFL++ agora é um projeto AGPL 3.0!
! Os arquivos onde a licença poderia ser trocada foram movidos para AGPL 3.0+, arquivos
    that were under Apache 2.0 with contributations stay on that license.
! Licença comercial (doar a uma boa causa - nenhum dinheiro para AFL++) está disponível
  - Comutado o https://github.com/AFLplusplus/cov-analysis para o afl-cov desatualizado
  - MacOS suporte versão mais atual para afl-fuzz, afl-cc (incl. LTO) e
    frida mode!
  - Suporte ao FreeBSD atualizado por jsaunders-rr, obrigado!
  - O modo persistente Linux usa o futex agora que aumenta a velocidade e reduz
    system call overhead (opt out with AFL_FAST_CHILD_SYNC), thanks to
    @martinus for most of the implementation!
  - Afl-fuzz:
    - `-I tool` call now receives the new crash as a command line parameter
    - changed to a better map classifier
    - frameshift is disabled now if AFL_CUSTOM_MUTATOR_ONLY is set
    - python module fixes
    - minor speed, leak and zombie enhancements
    - stability info was lost on fast resume - fixed
    - somewhere we removed .state/variable/... now it is back :-)
  - afl-cc:
    - Add LLVM 23 support
    - LTO and PCGUARD: new `AFL_LLVM_PATH` (also `AFL_LLVM_LTO_PATH` /
      `AFL_LLVM_PATH_MODE`) Ball-Larus per-function path coverage on top
      of edge coverage. Three levels: `=1` relaxed (collapse all
      guard-only BBs), `=2` restricted (collapse only 2-successor
      guard-only BBs), `=3` strict Ball-Larus. LTO additionally composes
      with `AFL_LLVM_LTO_CALLER`. See
      instrumentation/README.llvm.md and instrumentation/README.lto.md.
    - Fixes in the PCGUARD and LTO instrumentation that could lead to sanitizer
      triggers in target binaries
    - new instrumentation: `afl-llvm-bug-pass.so` provides five runtime
      oracles (SCALAR, BUDGET, SIZEFILL, ALLOCSIZE, SLACK) plus a slice-
      filter sub-mode for SCALAR, covering arithmetic-bound and logical-
      OOB bugs that ASan misses (CVE-2023-4863 / libwebp-Huffman class).
      Note: ALLOCSIZE/DERIVE are disabled automatically under
      AFL_USE_ASAN to avoid double-instrumentation; see
      docs/env_variables.md.
        * `AFL_LLVM_BUG_SCALAR=1`   - max-value-per-arithmetic-site coverage,
                                      plus per-loop iteration count
        * `AFL_LLVM_BUG_SCALAR_SLICE=1` - restrict SCALAR instrumentation to
                                      arithmetic that flows into a memory-
                                      size sink (allocator size, GEP index,
                                      memcpy/memset length). Implies SCALAR.
        * `AFL_LLVM_BUG_BUDGET=1`   - check `ptr += func()` write-extent
                                      contract
        * `AFL_LLVM_BUG_SIZEFILL=1`  - check NULL-means-size-only idioms
        * `AFL_LLVM_BUG_ALLOCSIZE=1` - track every malloc/calloc/realloc and
                                       feed three signals (headroom IJON-min,
                                       proximity-bucket coverage edge, soft-OOB
                                       tripwire) per in-loop store
        * `AFL_LLVM_BUG_SLACK=1`    - per-icmp |op0-op1| feedback, mapped
                                      MIN-style onto the bug map (inverse-
                                      bucket) for tight-comparison signal
        * `AFL_LLVM_BUG_ALLOCSIZE_FUNCS=Name1,Name2,...` - extend tracking
                                       to user-listed custom allocators
        * `AFL_LLVM_BUG_ALLOCSIZE_FREE_FUNCS=Name1,Name2,...` - matching
                                       custom-free functions for the above
        * `AFL_LLVM_BUG_ALLOCSIZE_DERIVE=1` - log tracked allocation sizes
                                       into CmpLog RTN slots for `-l Z`
        * `AFL_LLVM_BUG=1`           - enable all bug-pass modes
      Per-site bug-map slots are kept in a private MAP_SIZE_BUG region and
      tracked max-rule (compatible with the IJON model)
    - cmplog scheduling extensions (companion to bug-pass):
        * `-l M` (afl-fuzz) - predicate-tightness scheduling. Treat any
          new per-site minimum slack on an inequality CmpLog cmp as a
          coverage event and mark the queue entry favoured. Catches the
          libwebp-1.3.1 / CVE-2023-4863 input pattern (validation
          predicates simultaneously at their tight edges).
        * `AFL_LLVM_BUG_ALLOCSIZE_DERIVE=1` or `AFL_LLVM_BUG=1`
          (compile-time) and
          `-l Z` (afl-fuzz) - size-derive logging. On every freed tracked
          allocation, write `(computed_size, max_observed_offset)` into a
          CmpLog RTN slot keyed by alloc-site. The existing CmpLog
          dictionary mining harvests `computed_size` as a magic constant
          and feeds the producing input bytes back into havoc.
    - afl-cc command line parsing fix for ijon
  - afl- cmin*:
    - nyx_mode is now working for all minimizer variants
  - afl- showmap:
    - no more .afl-showmap-temp-* files lying around
  - IJON dist foi alterado para implementação original IJON: correspondência inicial
    bytes, max length is 1024
  - Ferramentas lib*:
    - MacOS support is back, thanks to @Jay-1409 !


### Versão ++4.40c (lançamento)
  - Afl-fuzz:
    - FrameShift integrated and enabled by default, disable with
      AFL_FRAMESHIFT_DISABLE and configure effort via
      AFL_FRAMESHIFT_MAX_OVERHEAD. In extensive fuzzbench analysis at worst
      (on average) it does nothing, at best it improves time to new coverage
      and total coverage unlocked. https://arxiv.org/pdf/2507.05421
      Thanks to @hgarrereyn for the PR!
    - Fixed several potential crashes when using IJON
    - added `AFL_FORCE_FASTRESUME` which will ignore the saved hash of the
      target - but note it will only work if the coverage map size did not
      change
    - prevent further executed instrumented programs by the fuzz target to
      manipulate the coverage
  - afl-cc:
    - LLVM 22 support (they are again switching around include files ...)
    - g_/curl_/xml_ string support for COMPCOV, thanks to @Prajwal-kp-18
    - optimized hidden CFG instrumentation (don't instrument vector selects)
    - plugin optimization and fixes by @nbars, @kyakdan and @koltiradw
    - marked GCC plugins as unmaintained. We need someone who know gimple and
      is willing to fix the plugin issues, workarounds for gcc bugs and
      overall improve the plugin.
    - env `AFL_LLVM_DENY_EXEC` will abort any common exec calls
  - afl-cmin:
    - new implementation in C by @kcwu - it is currenlty not built though
      because of maturity issues, e.g. does not work with Nyx
    - afl-cmin.py was changing behaviour to hash the original filenames,
      this was reverted.
    - afl-cmin and afl-cmin.py honor `AFL_SHA1_FILENAMES` now
  - afl- showmap:
    - -f support added by Prajwal-kp-18 - thanks!
    - faster stream mode by @nbars
  - modo_ qemu:
    - fix when AFL_EXITPOINT is not set, which could prevent detecting crashes
  - afl-plot:
    - multiple AFL++ out directories now supported, thanks to @Jay-1409 !


### Versão ++4.35c (lançamento)
  - Misturado com o GUIFuzz++: Libertando o Fuzzing de Caixa Cinza no Usuário Gráfico do Desktop
                      Interfacing Applications
    https://futures.cs.utah.edu/papers/25ASE.pdf
  - Afl-fuzz:
    - fix syncing issues with crashes and custom mutators by @AndyH-1
    - another attempt to kill every client, thanks to @leonasdev
  - afl-cc:
    - Huge refactor for default pcguard instrumentation, several minor and
      medium bug fixes, complete hidden decision coverage
    - LTO: also added complete hidden decision coverage
    - Various small fixes by @nbars, thanks!
    - IJON fix to search for the necessary include
    - Allow compiling the gcc plugin with clang++, thanks to @exoosh
    - Fix for unusual bit sizes in cmplog-instructions-pass by @forzafedor
  - modo_ qemu:
    - IJON support, thanks to @nj00001! see qemu_mode/README.md
    - leaner, less warnings, thanks to @McSinyx!
  - afl-tmin
    - fix custom trimmings, thanks to @renatahodovan!
  - mutadores personalizados:
    - Gramatron: fixes + cjson switch by @CarvedCoder, fix by @jubnzv


### Versão ++4.34c (lançamento)
  - IJON integração por @vi3tL0u1s - muito obrigado!!
    - see docs/IJON.md on how to use it
  - Modo_ unicórnio:
    - UnicornAFL v3!! thanks to @wtdcode!
  - modo_ qemu:
    - fix compilation for a few platforms
  - afl-fuzz
    - larger improvements to CMPLOG, thanks to @am009
    - scroll down before clearing the screen to not loose content
    - minor bug fixes
  - afl- showmap
    - fix -C parameter breakage introduced in v4.33c
  - afl-cc:
    - enabled LLVM 22
    - new env: AFL_COMPILER_LAUNCHER to allow ccache usage (thanks to @nbars)
    - fix a offset calculation bug in AFL++ PCGUARD
    - make AFL_DUMP_MAP_SIZE work for CLASSIC modes
    - fix a crash when running with LLVM 20 when compiling PCGUARD with LTO
    - fix deprecation warnings for LLVM 20+
    - fix 128 bit support for cmplog-switches pass
    - fix 32 bit cmplog support
    - skip blocks for instrumentation that are already instrumented
  - Edifício:
    - new NO_UNICORN and NO_QEMU and NO_FRIDA build options
    - build fixes for FreeBSD
  - _mutadores personalizados:
    - added AIXCC Team Atlanta's zero-mq plugin to add testcases from remote


### Versão ++4.33c (lançamento)
  - Afl-fuzz:
    - Use `AFL_PRELOAD_DISCRIMINATE_FORKSERVER_PARENT` if you use AFL_PRELOAD
      to disable fork, see docs (thanks to @alexandredoyen29)
    - Fix for FAST power schedules (introduced in 4.32c) (thanks to @kcwu)
    - Colors for NO_UI output (thanks to @smoelius)
    - Fix potential sync issues when resuming sessions and when instances in a
      campaign are restarted and skip entries that were synced from itself
      (thanks to @kcwu for raising the issues and providing support!)
    - Fix for when fast resuming failed
    - more 64 bit archicture support by @maribu
  - afl-cc:
    - Added instrumenting hidden edges (approx 5% edges were not instrumented,
      LLVM sancov overall misses 8% of edges compared to our implementation)
      Note that is is currently only implemented for our PCGUARD plugin, not
      LTO, CLASSIC, etc.!
    - Fix to make AFL_SAN_NO_INST work with gcc_plugin
    - MacOS aflpp driver compilation fix (-fsanitize=fuzzer implementation)
    - Make AFL_DUMP_MAP_SIZE work even if the target has sanitizer issues
  - qemuafl:
    - Better MIPS persistent mode support
    - `AFL_EXITPOINT` support added
    - `AFL_QEMU_BLOCK_COV` block coverage support added
  - afl-cmin:
    - New afl-cmin.py which is much faster, will be executed by default via
      afl-cmin if it executes successfully (thanks to @kcwu!)
    - Nyx mode now fully works for minimizing (with afl-cmin.py which is
      called by afl-cmin if python is available) - before the map size was
      fixed and so large targets lost coverage.
  - Nova biblioteca de desoquetização: utils/libaflppdesock
    - Likely works when all other desocketing options fail
  - nyx_mode:
    - Properly determine map size


### Versão ++4.32c (lançamento)
  - Corrigido um erro onde após uma reinicialização rápida de um corpo completo fuzzed afl-fuzz
    terminates with "need at least one valid input seed that does not crash"
  - Pequenas melhorias na configuração do afl- *
  - Afl-fuzz:
    - memory leak fixes by @kcwu - thanks!
    - many more nits and small memory saves thanks to @kcwu
    - remove deprecated files from queue/.state
    - fix bitmap update function if no current trace is present 
    - fix for afl_custom_queue_get
    - various small nits
  - afl-cc:
    - fix pass support for LLVM 20 (passes were run too early)
    - dropped plugin support for LLVM 13
    - fix AFL_OLD_FORKSERVER
    - various minor fixes
  - modo_ frida:
    - fixes for new MacOS + M4 hardware

### Versão ++4.31c (lançamento)
  - Modo SAND adicionado (docs/SAND.md) para fuzzing mais eficaz com higienizadores
    (thanks to @wtdcode !)
  - Afl-fuzz:
    - splicing phase is now DISABLED by default because research showed
      it is counterproductive. New command line parameter `-u` to enable
      it.
    - Python 3.13+ support
    - loose file and shared memory permissions on Android and iPhone
  - afl-cc:
    - LLVM 20 support (again - please don't change the API all the time ...)
    - -fsanitize=fuzzer now inserts libAFLDriver.a addtionally early to help
      compiling if LLVMFuzzerTestOneOnput is in an .a archive
    - added __sanitizer_weak_hook_* functions (in case that is helpful in
      weird setups)
    - fix bug with large map sizes when multiple libraries are loaded after
      the shared memory was obtained.

### Versão ++4.30c (lançamento)
! afl-gcc e afl-clang funcionalidade está agora removida!
  - Afl-fuzz:
    - fastresume feature added. if you abort fuzzing and resume fuzzing
      with `-i -` or `AFL_AUTORESUME=1` and the target binary has not changed
      then a dump will be loaded and the calibration phase skipped.
      to disable this feature set `AFL_NO_FASTRESUME=1`
      zlib compression is used if zlib is found at compile time
    - improved seed selection algorithm
    - added `AFL_CUSTOM_MUTATOR_LATE_SEND=1` to call the custom send()
      function after the target has been restarted.
    - because of bad math and undefined behaviour fixes we have to change
      the CMPLOG map. **YOU NEED TO RECOMPILE CMPLOG TARGETS**
    - fixed custom_post_process for calibration
    - fixes for AFL_EXIT_ON_TIME and AFL_EXIT_WHEN_DONE, changed behaviour of
      AFL_EXIT_WHEN_DONE to finish when really done :-)
  - modo_ frida:
    - AFL_FRIDA_PERSISTENT_ADDR can now be be any reachable address not just
      a function entry
    - AFL_DEBUG is now the same as AFL_FRIDA_VERBOSE
    - AFL_FRIDA_DEBUG_MAPS now works as expected
  - modo_ qemu:
    - new hooks supported (optional), see qemu_mode/hooking_bridge - thanks to
      @CowBoy4mH3LL
  - Modo_ unicórnio:
    - fix install and forkserver (thanks aarnav!)
    - pin unicorn version
  - nyx_mode:
    - bugfixes
  - mutadores personalizados:
    - custom_send_tcp custom mutator added, thanks to @dergoegge
  - afl-cc
    - fix to support pointless changes in LLVM 20
    - new runtime (!) variable: `AFL_OLD_FORKSERVER` to use the old vanilla
      AFL type forkserver. Useful for symcc/symqemu/nautilus/etc. with
      AFL_LLVM_INSTRUMENT=CLASSIC
    - new compile time variable: `AFL_OPT_LEVEL` to set a specific optimization
      level, default is `3`
    - correctly explain how to get the correct map size for large targets
    - small fix for weird LLVM defines in redhat
  - formatação de código atualizada para lvm 18
  - melhorado personalizado_ mutantes/aflpp/ standalone/aflpp- standalone
  - adicionado personalizado_ mutantes/autotokens/ standalone/autotokens- standalone
  - Os cabeçalhos AFL++ estão agora instalados em $PREFIX/include/afl

### Versão ++4.21c (lançamento)
  * afl-fuzz
    - fixed a regression in afl-fuzz that resulted in a 5-10% performace loss
      do a switch from gettimeofday() to clock_gettime() which should be rather
      three times faster. The reason for this is unknown.
    - new queue selection algorithm based on 2 core years of queue data
      analysis. gives a noticable improvement on coverage although the results
      seem counterintuitive :-)
    - added AFL_DISABLE_REDUNDANT for huge queues
    - added `AFL_NO_SYNC` environment variable that does what you think it does
    - fix AFL_PERSISTENT_RECORD
    - run custom_post_process after standard trimming
    - prevent filenames in the queue that have spaces
    - minor fix for FAST schedules
    - more frequent stats update when syncing (todo: check performance impact)
    - now timing of calibration, trimming and syncing is measured seperately,
      thanks to @eqv!
    - -V timing is now accurately the fuzz time (without syncing), before
      long calibration times and syncing could result in now fuzzing being
      made when the time was already run out until then, thanks to @eqv!
    - fix -n uninstrumented mode when ending fuzzing
    - enhanced the ASAN configuration
    - make afl-fuzz use less memory with cmplog and fix a memleak
  * afl-cc:
    - re-enable i386 support that was accidently disabled
    - fixes for LTO and outdated afl-gcc mode for i386
    - fix COMPCOV split compare for old LLVMs
    - disable xml/curl/g_ string transform functions because we do not check
      for null pointers ... TODO
    - ensure shared memory variables are visible in weird build setups
    - compatability to new LLVM 19 changes
  * afl-cmin
    - work with input files that have a space
  * afl- showmap
    - fix memory leak on shmem testcase usage (thanks to @ndrewh)
    - minor fix to collect coverage -C (thanks to @bet4it)
  * Corrigido um erro shmem mmap (que raramente surgiu no MacOS)
  * libtokencap: script generate_libtoken_dict.sh adicionado por @a-shvedov

### Versão ++4.20c (lançamento)
! Agora é introduzido um novo modelo de comunicação forkserver. afl-fuzz is
    backward compatible to old compiled targets if they are not built
    for CMPLOG/Redqueen, but new compiled targets will not work with
    old afl-fuzz versions!
Recompile todos os alvos que são instrumentados para CMPLOG/Redqueen!
  - AFL++ agora suporta até 4 bilhões de bordas de cobertura, acima de 6 milhões.
  - Nova opção de compilação: `make PERFORMANCE=1` - isto irá activar especial
    CPU dependent optimizations that make everything more performant - but
    the binaries will likely won't work on different platforms. Also
    enables a faster hasher if the CPU requirements are met.
  - O recurso de registro persistente (veja config.h) foi expandido para também
    support replay, thanks to @quarta-qti !
  - Afl-fuzz:
    - the new deterministic fuzzing feature is now activated by default,
      deactivate with -z. Parameters -d and -D are ignored.
    - small improvements to CMPLOG/redqueen
    - workround for a bug with MOpt -L when used with -M - in the future
      we will either remove or rewrite MOpt.
    - fix for `-t xxx+` feature
    - -e extension option now saves the queue items, crashes, etc. with the
      extension too
    - fixes for trimmming, correct -V time and reading stats on resume by eqv
      thanks a lot!
  - afl-cc:
    - added collision free caller instrumentation to LTO mode. activate with
      `AFL_LLVM_LTO_CALLER=1`. You can set a max depth to go through single
      block functions with `AFL_LLVM_LTO_CALLER_DEPTH` (default 0)
    - fixes for COMPCOV/LAF and most other modules
    - fix for GCC_PLUGIN cmplog that broke on std::strings
  - Afl-whatsup:
    - now also displays current average speed
    - small bugfixes
  - mutadores personalizados:
    - fixes for aflpp custom mutator and standalone tool
    - important fix to the symcc custom mutator
  - Edições menores para afl-persisent-config
  - Impedir que os arquivos temporários sejam deixados para trás ao interromper o afl-whatsup
  - Mais benchmarks de CPU adicionados ao benchmark/

### Versão ++4.10c (lançamento)
  - Afl-fuzz:
    - default power schedule is now EXPLORE, due a fix in fast schedules
      explore is slightly better now.
    - fixed minor issues in the mutation engine, thanks to @futhewo for
      reporting!
    - better deterministic fuzzing is now available, benchmarks have shown
      to improve fuzzing. Enable with -D. Thanks to @kdsjZh for the PR!
  - afl-cc:
    - large rewrite by @SonicStark which fixes a few corner cases, thanks!
    - LTO mode now requires llvm 12+
    - workaround for ASAN with gcc_plugin mode
  - instrumentação:
    - LLVM 18 support, thanks to @devnexen!
    - Injection (SQL, LDAP, XSS) fuzzing feature now available, see
      `instrumentation/README.injections.md` how to activate/use/expand.
    - compcov/LAF-intel:
      - floating point splitting bug fix by @hexcoder
      - due a bug in LLVM 17 integer splitting is disabled there!
      - when splitting floats was selected, integers were always split as well,
        fixed to require AFL_LLVM_LAF_SPLIT_COMPARES or _ALL as it should
    - dynamic instrumentation filtering for LLVM NATIVE, thanks @Mozilla!
      see utils/dynamic_covfilter/README.md
  - modo_ qemu:
    - plugins are now activated by default and a new module is included that
      produces drcov compatible traces for lighthouse/lightkeeper/...
      thanks to @JRomainG to submitting!
  - checkout de Nyx atualizado (corrige um erro) e alguma QV
  - atualizou o mutador de gramática personalizado
  - o documento afl-cmin não funciona no macOS (mas o afl-cmin.bash funciona)

### Versão ++4.09c (lançamento)
  - Afl-fuzz:
    - fixed the new mutation implementation for two bugs
    - added `AFL_FINAL_SYNC` which forces a final fuzzer sync (also for `-F`)
      before terminating.
    - added AFL_IGNORE_SEED_PROBLEMS to skip over seeds that time out instead
      of exiting with an error message
    - allow -S/-M naming up to 50 characters (from 24)
    - CMPLOG:
      - added scale support (-l S)
      - skip unhelpful insertions (u8)
    - added --version and --help command line parameters
    - fixed endless loop when reading malformed dictionaries
    - new custom mutator function: post_run - thanks to yangzao!
  - Afl-whatsup:
    - detect instanced that are starting up and show them as such as not dead
    - now also shows coverage reached
    - option -m shows only very relevant stats
    - option -n will not use color in the output
  - instrumentação:
    - fix for a few string compare transform functions for LAF
    - we are instrumenting __cxx internal functions again. this might break
      a few targets, please report if so.
  - modo_ frida:
    - fixes support for large map offsets
  - suporte para AFL_FUZZER_LOOPCOUNT para afl.rs e LLVMFuzzerTestOneInput
  - afl-cmin/afl-cmin.bash: evitar erros de arquivo desnecessários
  - adicionou nova ferramenta afl-adddseeds que adiciona novas sementes a uma campanha em execução
  - adicionado benchmark/benchmark.py se você quiser ver quão bom é o seu fuzzing
    speed is in comparison to other setups.

### Versão ++4.08c (lançamento)
  - Afl-fuzz:
    - new mutation engine: mutations that favor discovery more paths are
      prefered until no new finds for 10 minutes then switching to mutations
      that favor triggering crashes. Modes and switch time can be configured
      with `-P`. Also input mode for the target can be defined with `-a` to
      be `text` or `binary` (defaults to `generic`)
    - new custom mutator that has the new afl++ engine (so it can easily
      incorporated into new custom mutators), and also comes with a standalone
      command line tool! See custom_mutators/aflpp/standalone/
    - display the state of the fuzzing run in the UI :-)
    - fix timeout setting if '+' is used or a session is restarted
    - -l X option to enable base64 transformation solving
    - allow to disable CMPLOG with '-c -' (e.g. afl.rs enforces '-c 0' on
      every instance which is counterproductive).
  - afl-cmin/afl-cmin.bash:
    - fixed a bug inherited from vanilla AFL where a coverage of
      map[123] = 11 would be the same as map[1123] = 1
    - warn on crashing inputs
    - adjust threads if less inputs than threads specified
  - afl-cc:
    - fixed an off-by-one instrumentation of iselect, hurting coverage a bit.
      Thanks to @amykweon for spotting and fixing!
    - @toka fixed a bug in laf-intel signed integer comparison splitting,
      thanks a lot!!
    - more LLVM compatability
  - modo_ frida:
    - support for long form instrumentation on x86_x64 and arm64
    - renamed utils/get_symbol_addr.sh to utils/frida_get_symbol_addr.sh
  - modo_ qemu:
    - added qemu_mode/utils/qemu_get_symbol_addr.sh

### Versão ++4.07c (lançamento)
  - Afl-fuzz:
    - reverse reading the seeds only on restarts (increases performance)
    - new env `AFL_POST_PROCESS_KEEP_ORIGINAL` to keep the orignal
      data before post process on finds (for atnwalk custom mutator)
    - new env `AFL_IGNORE_PROBLEMS_COVERAGE` to ignore coverage from
      loaded libs after forkserver initialization (required by Mozilla)
  - afl-cc:
    - added @responsefile support
    - new env `AFL_LLVM_LTO_SKIPINIT` to support the AFL++ based WASM
      (https://github.com/fgsect/WAFL) project
    - error and print help if afl-clan-lto is used with lto=thin
    - rewrote our PCGUARD pass to be compatible with LLVM 15+ shenanigans,
      requires LLVM 13+ now instead of 10.0.1+
    - fallback to native LLVM PCGUARD if our PCGUARD is unavailable
    - fixed a crash in GCC CMPLOG
  - afl- showmap:
    - added custom mutator post_process and send support
    - add `-I filelist` option, an alternative to `-i in_dir`
  - afl-cmin + afl-cmin.bash:
    - `-T threads` parallel task support, can be a huge speedup!
  - modo_ qemu:
    - Persistent mode + QASAN support for ppc32 targets by @worksbutnottested
  - uma nova gramática personalizada mutator atnwalk foi submetido por @voidptr127 !
  - dois novos mutadores personalizados estão agora disponíveis:
    - TritonDSE in custom_mutators/aflpp_tritondse
    - SymQEMU in custom_mutators/symqemu

### Versão ++4.06c (lançamento)
  - Afl-fuzz:
    - ensure temporary file descriptor is closed when not used
    - added `AFL_NO_WARN_INSTABILITY`
    - added time_wo_finds to fuzzer_stats
    - fixed a crash in pizza (1st april easter egg) mode. Sorry for
      everyone who was affected!
    - allow pizza mode to be disabled when AFL_PIZZA_MODE is set to -1
    - option `-p mmopt` now also selects new queue items more often
    - fix bug in post_process custom mutator implementation
    - print name of custom mutator in UI
    - slight changes that improve fuzzer performance
  - afl-cc:
    - add CFI sanitizer variant to gcc targets
    - llvm 16 + 17 support (thanks to @devnexen!)
    - support llvm 15 native pcguard changes
    - support for LLVMFuzzerTestOneInput -1 return
    - LTO autoken and llvm_mode: added AFL_LLVM_DICT2FILE_NO_MAIN support
  - modo_ qemu:
    - fix _RANGES envs to allow hyphens in the filenames
    - basic riscv support
  - modo_ frida:
    - added `AFL_FRIDA_STATS_INTERVAL`
    - fix issue on MacOS
  - Modo_ unicórnio:
    - updated and minor issues fixed
  - suporte nyx_mode para todas as ferramentas
  - melhor suporte de opções padrão de higienização para todas as ferramentas
  - novo módulo personalizado: autotoken, um fuzzer livre de gramática para entradas de texto
  - exemplos C de mutantes personalizados corrigidos
  - mais pequenas correções e suporte multi-plataforma

### Versão ++4.05c (lançamento)
  - MacOS: libdislocator, libtokencap etc. não funcionam com o moderno
    MacOS anymore, but could be patched to work, see this issue if you
    want to make the effort and send a PR:
    https://github.com/AFLplusplus/AFLplusplus/issues/1594
  - Afl-fuzz:
    - added afl_custom_fuzz_send custom mutator feature. Now your can
      send fuzz data to the target as you need, e.g. via IPC.
    - cmplog mode now has a -l R option for random colorization, thanks
      to guyf2010 for the PR!
    - queue statistics are written every 30 minutes to
      out/NAME/queue_data if compiled with INTROSPECTION
    - new env: AFL_FORK_SERVER_KILL_SIGNAL
  - afl-showmap/afl-cmin
    - `-t none` now translates to `-t 120000` (120 seconds)
  - unicórnio_modo atualizado
  - atualizados as dependências personalizadas do mutator da ferrugem e o mutator personalizado LibAFL
  - geral melhor higienizador default ajuste manipulação
  - várias correções de erros menores

### Versão ++4.04c (lançamento)
  - corrigir scripts de compilação gramaatron e gramatical_mutator
  - melhorias na configuração do afl-persistente e na configuração do sistema afl-afl
    scripts
  - Afl-fuzz:
    - force writing all stats on exit
    - ensure targets are killed on exit
    - `AFL_FORK_SERVER_KILL_SIGNAL` added
  - afl-cc:
    - make gcc_mode (afl-gcc-fast) work with gcc down to version 3.6
  - modo_ qemu:
    - fixed 10x speed degredation in v4.03c, thanks to @ele7enxxh for
      reporting!
    - added qemu_mode/fastexit helper library
  - Modo_ unicórnio:
    - Enabled tricore arch (by @jma-qb)
    - Updated Capstone version in Rust bindings
  - Modo lvm:
    - AFL runtime will always pass inputs via shared memory, when possible,
      ignoring the command line.


### Versão ++4.03c (lançamento)
  - Construindo agora dá um resumo de construção o que conseguiu e o que não
  - Afl-fuzz:
    - added AFL_NO_STARTUP_CALIBRATION to start fuzzing at once instead
      of calibrating all initial seeds first. Good for large queues
      and long execution times, especially in CIs.
    - default calibration cycles set to 7 from 8, and only add 5 cycles
      to variables queue items instead of 12.
  - afl-cc:
    - fixed off-by-one bug in our pcguard implemenation, thanks for
      @tokatoka for reporting
    - fix for llvm 15 and reenabling LTO, thanks to nikic for the PR!
    - better handling of -fsanitize=..,...,.. lists
    - support added for LLVMFuzzerRunDriver()
    - fix gcc_mode cmplog
    - obtain the map size of a target with setting AFL_DUMP_MAP_SIZE=1
      note that this will exit the target before main()
  - modo_ qemu:
    - added AFL_QEMU_TRACK_UNSTABLE to log the addresses of unstable
      edges (together with AFL_DEBUG=1 afl-fuzz). thanks to
      worksbutnottested!
  - Afl-analyze quebrou em algum momento, corrigir por CodeLogicError, obrigado!
  - afl-cmin/afl-cmin.bash agora tem uma opção -A para permitir também bater
    and timeout inputs
  - Modo_ unicórnio:
    - updated upstream unicorn version
    - fixed builds for aarch64
    - build now uses all available cores


### Versão ++4.02c (lançamento)
  - afl-cc:
    - important fix for the default pcguard mode when LLVM IR vector
      selects are produced, thanks to @juppytt for reporting!
  - 'plugin' gcc:
    - Adacore submitted CMPLOG support to the gcc_plugin! :-)
  - Modo_ lvm:
    - laf cmp splitting fixed for more comparison types
  - modo_ frida:
    - now works on Android!
  - Afl-fuzz:
    - change post_process hook to allow returning NULL and 0 length to
      tell afl-fuzz to skip this mutated input

### Versão ++4.01c (lançamento)
  - fixou os scripts */build_...sh para trabalhar fora do git
  - novo mutante personalizado: libafl com o símbolo fuzzing :)
  - Afl-fuzz:
    - when you just want to compile once and set CMPLOG, then just
      set -c 0 to tell afl-fuzz that the fuzzing binary is also for
      CMPLOG.
    - new commandline options -g/G to set min/max length of generated
      fuzz inputs
    - you can set the time for syncing to other fuzzer now with
      AFL_SYNC_TIME
    - reintroduced AFL_PERSISTENT and AFL_DEFER_FORKSRV to allow
      persistent mode and manual forkserver support if these are not
      in the target binary (e.g. are in a shared library)
    - add AFL_EARLY_FORKSERVER to install the forkserver as earliest as
      possible in the target (for afl-gcc-fast/afl-clang-fast/
      afl-clang-lto)
    - "saved timeouts" was wrong information, timeouts are still thrown
      away by default even if they have new coverage (hangs are always
      kept), unless AFL_KEEP_TIMEOUTS are set
    - AFL never implemented auto token inserts (but user token inserts,
      user token overwrite and auto token overwrite), added now!
    - fixed a mutation type in havoc mode
    - Mopt fix to always select the correct algorithm
    - fix effector map calculation (deterministic mode)
    - fix custom mutator post_process functionality
    - document and auto-activate pizza mode on condition
  - afl-cc:
    - due a bug in lld of llvm 15 LTO instrumentation wont work atm :-(
    - converted all passed to use the new llvm pass manager for llvm 11+
    - AFL++ PCGUARD mode is not available for 10.0.1 anymore (11+ only)
    - trying to stay on top on all these #$&§!! changes in llvm 15 ...
  - modo_ frida:
    - update to new frida release, handles now c++ throw/catch
  - Modo_ unicórnio:
    - update unicorn engine, fix C example
  - utils:
    - removed optimin because it looses coverage due to a bug and is
      unmaintained :-(


### Versão ++4.00c (lançamento)
  - reestruturação de documentação completa, tornada possível pelo Google Season
    of Docs :) thank you Jana!
  - renomeamos várias entradas UI e fuzzer_stat para ser mais preciso,
    e.g. "unique crashes" -> "saved crashes", "total paths" ->
    "corpus count", "current path" -> "current item".
    This might need changing custom scripting!
  - Modo Nyx (emulação completa do sistema com capacidade de instantâneo) foi
    added - thanks to @schumilo and @eqv!
  - Modo_ unicórnio:
    - Moved to unicorn2! by Ziqiao Kong (@lazymio)
    - Faster, more accurate emulation (newer QEMU base), risc-v support
    - removed indirections in rust callbacks
  - novo modo apenas binário fuzzing: coresight_mode para CPUs aarch64 :)
    thanks to RICSecLab submitting!
  - se as bibliotecas instrumentadas são dlopen()' a seguir ao servidor de garfos você
    will now see a crash. Before you would have colliding coverage.
    We changed this to force fixing a broken setup rather then allowing
    ineffective fuzzing.
    See docs/best_practices.md how to fix such setups.
  - Afl-fuzz:
    - cmplog binaries will need to be recompiled for this version
      (it is better!)
    - fix a regression introduced in 3.10 that resulted in less
      coverage being detected. thanks to Collin May for reporting!
    - ensure all spawned targets are killed on exit
    - added AFL_IGNORE_PROBLEMS, plus checks to identify and abort on
      incorrect LTO usage setups and enhanced the READMEs for better
      information on how to deal with instrumenting libraries
    - fix -n dumb mode (nobody should use this mode though)
    - fix stability issue with LTO and cmplog
    - better banner
    - more effective cmplog mode
    - more often update the UI when in input2stage mode
  - qemu_mode/unicorn_mode: escrita OOB fixa ao usar libcompcov,
      thanks to kotee4ko for reporting!
  - modo_ frida:
    - better performance, bug fixes
    - David Carlier added Android support :)
  - afl-showmap, afl-tmin e afl-analyze:
    - honor persistent mode for more speed. thanks to dloffre-snl
      for reporting!
    - fix bug where targets are not killed on timeouts
    - moved hidden afl-showmap -A option to -H to be used for
      coresight_mode
  - Evitar acidentalmente matar serviços não-afl/fuzz ao abortar
    afl-showmap and other tools.
  - afl-cc:
    - detect overflow reads on initial input buffer for asan
    - new cmplog mode (incompatible with older AFL++ versions)
    - support llvm IR select instrumentation for default PCGUARD and LTO
    - fix for shared linking on MacOS
    - better selective instrumentation AFL_LLVM_{ALLOW|DENY}LIST
      on filename matching (requires llvm 11 or newer)
    - fixed a potential crash in targets for LAF string handling
    - fixed a bad assert in LAF split switches
    - added AFL_USE_TSAN thread sanitizer support
    - llvm and LTO mode modified to work with new llvm 14-dev (again.)
    - fix for AFL_REAL_LD
    - more -z defs filtering
    - make -v without options work
  - adicionado o mutator gramatical muito bom "GramaTron" para o
    custom_mutators
  - adicionar otimin, um minimizador de corpus mais rápido e melhor
    Adrian Herrera. Thank you!
  - adicionado script afl-persistant-config para definir a execução do sistema permanente
    configuration settings for fuzzing, for Linux and Macos.
    thanks to jhertz!
  - funções de texto xml, curl & exóticas adicionadas ao recurso do dicionário llvm
  - corrigir problemas AFL_PRELOAD no MacOS
  - removido utils/afl_frida porque frida_mode/ agora é muito melhor
  - alvo de desinstalação adicionado ao makefile (todo: update new readme!)

### Versão ++3.14c (lançamento)
  - Afl-fuzz:
    - fix -F when a '/' was part of the parameter
    - fixed a crash for cmplog for very slow inputs
    - fix for AFLfast schedule counting
    - removed implied -D determinstic from -M main
    - if the target becomes unavailable check out out/default/error.txt
      for an indicator why
    - AFL_CAL_FAST was a dead env, now does the same as AFL_FAST_CAL
    - reverse read the queue on resumes (more effective)
    - fix custom mutator trimming
  - afl-cc:
    - Update to COMPCOV/laf-intel that speeds up the instrumentation
      process a lot - thanks to Michael Rodler/f0rki for the PR!
    - Fix for failures for some sized string instrumentations
    - Fix to instrument global namespace functions in c++
    - Fix for llvm 13
    - support partial linking
    - do honor AFL_LLVM_{ALLOW/DENY}LIST for LTO autodictionary andDICT2FILE
    - We do support llvm versions from 3.8 to 5.0 again
  - modo_ frida:
    - several fixes for cmplog
    - remove need for AFL_FRIDA_PERSISTENT_RETADDR_OFFSET
    - less coverage collision
    - feature parity of aarch64 with intel now (persistent, cmplog,
      in-memory testcases, asan)
  - afl-cmin e afl-showmap -i agora descem em subdiretórios
    (like afl-fuzz does) - note that afl-cmin.bash does not!
  - Afl_analyze:
    - fix timeout handling
    - add forkserver support for better performance
  - assegurar que o afl-compiler-rt seja construído para gcc_module
  - sempre compilar aflpp_driver para arreios libfuzzer
  - adicionar suporte a variáveis de env `AFL_NO_FORKSRV` para
    afl-cmin, afl-tmin, and afl-showmap, by @jhertz
  - removeu documentos desatualizados, melhorou a documentação existente

### Versão ++3.13c (lançamento)
  - Nota: plot_data mudou para o tempo relativo a partir do tempo unix no 3.10
  - frida_mode - novo modo que usa frida para fuzz alvos apenas binários,
    it currently supports persistent mode and cmplog.
    thanks to @WorksButNotTested!
  - criar um dicionário fuzzing com a ajuda do CodeQL graças a
    @microsvuln! see utils/autodict_ql
  - Afl-fuzz:
    - added patch by @realmadsci to support @@ as part of command line
      options, e.g. `afl-fuzz ... -- ./target --infile=@@`
    - add recording of previous fuzz attempts for persistent mode
      to allow replay of non-reproducable crashes, see
      AFL_PERSISTENT_RECORD in config.h and docs/envs.h
    - fixed a bug when trimming for stdin targets
    - cmplog -l: default cmplog level is now 2, better efficiency.
      level 3 now performs redqueen on everything. use with care.
    - better fuzzing strategy yield display for enabled options
    - ensure one fuzzer sync per cycle
    - fix afl_custom_queue_new_entry original file name when syncing
      from fuzzers
    - fixed a crash when more than one custom mutator was used together
      with afl_custom_post_process
    - on a crashing seed potentially the wrong input was disabled
    - added AFL_EXIT_ON_SEED_ISSUES env that will exit if a seed in
      -i dir crashes the target or results in a timeout. By default
      AFL++ ignores these and uses them for splicing instead.
    - added AFL_EXIT_ON_TIME env that will make afl-fuzz exit fuzzing
      after no new paths have been found for n seconds
    - when AFL_FAST_CAL is set a variable path will now be calibrated
      8 times instead of originally 40. Long calibration is now 20.
    - added AFL_TRY_AFFINITY to try to bind to CPUs but don't error if
      it fails
  - afl-cc:
    - We do not support llvm versions prior 6.0 anymore
    - added thread safe counters to all modes (`AFL_LLVM_THREADSAFE_INST`),
      note that this disables NeverZero counters.
    - Fix for -pie compiled binaries with default afl-clang-fast PCGUARD
    - Leak Sanitizer (AFL_USE_LSAN) added by Joshua Rogers, thanks!
    - Removed InsTrim instrumentation as it is not as good as PCGUARD
    - Removed automatic linking with -lc++ for LTO mode
    - Fixed a crash in llvm dict2file when a strncmp length was -1
    - added --afl-noopt support
  - utils/aflpp_driver:
    - aflpp_qemu_driver_hook fixed to work with qemu_mode
    - aflpp_driver now compiled with -fPIC
  - Unicornafl:
    - fix MIPS delay slot caching, thanks @JackGrence
    - fixed aarch64 exit address
    - execution no longer stops at address 0x0
  - atualizado afl-system-config para suportar esquisitice do Arch Linux e aumentar
    MacOS shared memory
  - atualizou o mutador personalizado gramatical para a versão mais recente
  - add - d (add dead fuzzer stats) to afl- whatsup
  - adicionado AFL_PRINT_FILENAMES ao afl- showmap/cmin para imprimir o
    current filename
  - o afl-showmap/cmin irá agora processar os itens da fila em ordem alfabética

### Versão ++3.12c (lançamento)
  - Afl-fuzz:
    - added AFL_TARGET_ENV variable to pass extra env vars to the target
      (for things like LD_LIBRARY_PATH)
    - fix map detection, AFL_MAP_SIZE not needed anymore for most cases
    - fix counting favorites (just a display thing)
  - afl-cc:
    - fix cmplog rtn (rare crash and not being able to gather ptr data)
    - fix our own PCGUARD implementation to compile with llvm 10.0.1
    - link runtime not to shared libs
    - ensure shared libraries are properly built and instrumented
    - AFL_LLVM_INSTRUMENT_ALLOW/DENY were not implemented for LTO, added
    - show correct LLVM PCGUARD NATIVE mode when auto switching to it
      and keep fsanitize-coverage-*list=...
      Short mnemnonic NATIVE is now also accepted.
  - qemu_ mode (thanks @realmadsci):
    - move AFL_PRELOAD and AFL_USE_QASAN logic inside afl-qemu-trace
    - add AFL_QEMU_CUSTOM_BIN
  - unicórnio_modo
    - accidently removed the subfolder from github, re-added
  - adicionado DEFAULT_PERMISSION para config.h para todos os arquivos criados, padrão
    to 0600

### Versão ++3.11c (lançamento)
  - Afl-fuzz:
    - better auto detection of map size
    - fix sanitizer settings (bug since 3.10c)
    - fix an off-by-one overwrite in cmplog
    - add non-unicode variants from unicode-looking dictionary entries
    - Rust custom mutator API improvements
    - Imported crash stats painted yellow on resume (only new ones are red)
  - afl-cc:
    - added AFL_NOOPT that will just pass everything to the normal
      gcc/clang compiler without any changes - to pass weird configure
      scripts
    - fixed a crash that can occur with ASAN + CMPLOG together plus
      better support for unicode (thanks to @stbergmann for reporting!)
    - fixed a crash in LAF transform for empty strings
    - handle erroneous setups in which multiple afl-compiler-rt are
      compiled into the target. This now also supports dlopen()
      instrumented libs loaded before the forkserver and even after the
      forkserver is started (then with collisions though)
    - the compiler rt was added also in object building (-c) which
      should have been fixed years ago but somewhere got lost :(
    - Renamed CTX to CALLER, added correct/real CTX implementation to
      CLASSIC
  - modo_ qemu:
    - added AFL_QEMU_EXCLUDE_RANGES env by @realmadsci, thanks!
    - if no new/updated checkout is wanted, build with:
      NO_CHECKOUT=1 ./build_qemu_support.sh
    - we no longer perform a "git drop"
  - afl-cmin: suporta nomes de arquivos com espaços

### Versão ++3.10c (lançamento)
  - Suporte para Mac OS ARM64
  - Suporte Android fixo e atualizado por Joey Jiaojg - obrigado!
  - Nova opção de instrumentação selectiva com __AFL_COVERAGE_* comandos
    to be placed in the source code.
    Check out instrumentation/README.instrument_list.md
  - afl-fuzz
    - Making AFL_MAP_SIZE (mostly) obsolete - afl-fuzz now learns on
      start the target map size
    - upgraded cmplog/redqueen: solving for floating point, solving
      transformations (e.g. toupper, tolower, to/from hex, xor,
      arithmetics, etc.). This is costly hence new command line option
      `-l` that sets the intensity (values 1 to 3). Recommended is 2.
    - added `AFL_CMPLOG_ONLY_NEW` to not use cmplog on initial seeds
      from `-i` or resumes (these have most likely already been done)
    - fix crash for very, very fast targets+systems (thanks to mhlakhani
      for reporting)
    - on restarts (`-i`)/autoresume (AFL_AUTORESUME) the stats are now
      reloaded and used, thanks to Vimal Joseph for this patch! 
    - changed the meaning of '+' of the '-t' option, it now means to
      auto-calculate the timeout with the value given being the max
      timeout. The original meaning of skipping timeouts instead of
      abort is now inherent to the -t option.
    - if deterministic mode is active (`-D`, or `-M` without `-d`) then
      we sync after every queue entry as this can take very long time
      otherwise
    - added minimum SYNC_TIME to include/config.h (30 minutes default)
    - better detection if a target needs a large shared map
    - fix for `-Z`
    - fixed a few crashes
    - switched to an even faster RNG
    - added hghwng's patch for faster trace map analysis
    - printing suggestions for mistyped `AFL_` env variables
    - added Rust bindings for custom mutators (thanks @julihoh)
  - afl-cc
    - allow instrumenting LLVMFuzzerTestOneInput
    - fixed endless loop for allow/blocklist lines starting with a
      comment (thanks to Zherya for reporting)
    - cmplog/redqueen now also tracks floating point, _ExtInt() + 128bit
    - cmplog/redqueen can now process basic libc++ and libstdc++
      std::string comparisons (no position or length type variants)
    - added support for __afl_coverage_interesting() for LTO and our
      own PCGUARD (llvm 10.0.1+), read more about this function and
      selective coverage in instrumentation/README.instrument_list.md
    - added AFL_LLVM_INSTRUMENT option NATIVE for native clang pc-guard
      support (less performant than our own), GCC for old afl-gcc and
      CLANG for old afl-clang
    - fixed a potential crash in the LAF feature
    - workaround for llvm bitcast lto bug
    - workaround for llvm 13
  - qemuafl
    - QASan (address sanitizer for Qemu) ported to qemuafl!
      See qemu_mode/libqasan/README.md
    - solved some persistent mode bugs (thanks Dil4rd)
    - solved an issue when dumping the memory maps (thanks wizche)
    - Android support for QASan
  - unicornafl
    - Substantial speed gains in python bindings for certain use cases
    - Improved rust bindings
    - Added a new example harness to compare python, c and rust bindings
  - afl-cmin e afl-showmap agora suportam a opção -f
  - afl_plot agora também gera um gráfico nas bordas descobertas
  - padrão alterado: sem limite de memória para afl-cmin e afl-cmin.bash
  - adverte sobre qualquer _AFL e __AFL env vars.
  - definir AFL_IGNORE_UNKNOWN_ENVS para não avisar sobre AFL_ desconhecido... env vars
  - Adicionado Makefile manequim à instrumentação/
  - utils/afl_frida actualizado para ser 5% mais rápido, 7% em x86_x64
  - Adicionado a variável env `AFL_KILL_SIGNAL` (obrigado @ v- p- b)
  - @Edznux adicionou uma documentação agradável sobre como usar rpc.statsd com
    AFL++ in docs/rpc_statsd.md, thanks!

### Versão ++3.00c (lançamento)
  - lvm_ modo/ e gcc_ plug- in/ movido para instrumentação/
  - exemplos/ renomeados para utils/
  - moveu o libdislocator, libtokencap e qdbi_ mode para utils/
  - todos os compiladores combinados com afl-cc que emula os anteriores
  - afl-llvm/gcc-rt.o fundida em afl-compiler-rt.o
  - afl-fuzz
    - not specifying -M or -S will now auto-set "-S default"
    - deterministic fuzzing is now disabled by default and can be enabled with
      -D. It is still enabled by default for -M.
    - a new seed selection was implemented that uses weighted randoms based on
      a schedule performance score, which is much better that the previous
      walk the whole queue approach. Select the old mode with -Z (auto enabled
      with -M)
    - Marcel Boehme submitted a patch that improves all AFFast schedules :)
    - the default schedule is now FAST
    - memory limits are now disabled by default, set them with -m if required
    - rpc.statsd support, for stats and charts, by Edznux, thanks a lot!
    - reading testcases from -i now descends into subdirectories
    - allow the -x command line option up to 4 times
    - loaded extras now have a duplication protection
    - If test cases are too large we do a partial read on the maximum
      supported size
    - longer seeds with the same trace information will now be ignored
      for fuzzing but still be used for splicing
    - crashing seeds are now not prohibiting a run anymore but are
      skipped - they are used for splicing, though
    - update MOpt for expanded havoc modes
    - setting the env var AFL_NO_AUTODICT will not load an LTO autodictionary
    - added NO_SPLICING compile option and makefile define
    - added INTROSPECTION make target that writes all mutations to
      out/NAME/introspection.txt
    - print special compile time options used in help output
    - when using -c cmplog, one of the childs was not killed, fixed
    - somewhere we broke -n dumb fuzzing, fixed
    - added afl_custom_describe to the custom mutator API to allow for easy
      mutation reproduction on crashing inputs
    - new env. var. AFL_NO_COLOR (or AFL_NO_COLOUR) to suppress colored
      console output (when configured with USE_COLOR and not ALWAYS_COLORED)
  - instrumentação
    - We received an enhanced gcc_plugin module from AdaCore, thank you
      very much!!
    - not overriding -Ox or -fno-unroll-loops anymore
    - we now have our own trace-pc-guard implementation. It is the same as
      -fsanitize-coverage=trace-pc-guard from llvm 12, but: it is a) inline
      and b) works from llvm 10.0.1 + onwards :)
    - new llvm pass: dict2file via AFL_LLVM_DICT2FILE, create afl-fuzz
      -x dictionary of string comparisons found during compilation
    - LTO autodict now also collects interesting cmp comparisons,
      std::string compare + find + ==, bcmp
    - fix crash in dict2file for integers > 64 bit
  - mutadores personalizados
    - added a new custom mutator: symcc -> https://github.com/eurecom-s3/symcc/
    - added a new custom mutator: libfuzzer that integrates libfuzzer mutations
    - Our AFL++ Grammar-Mutator is now better integrated into custom_mutators/
    - added INTROSPECTION support for custom modules
    - python fuzz function was not optional, fixed
    - some python mutator speed improvements
  - afl-cmin/afl-cmin.bash agora pesquise primeiro em PATH e por último em AFL_PATH
  - unicornafl sincronizado com a versão a montante 1.02 (fixos, melhores ligações de ferrugem)
  - renomeado AFL_DEBUG_CHILD_OUTPUT para AFL_DEBUG_CHILD
  - Adicionado AFL_ CRASH_ EXITCODE env variável para tratar um filho de código de saída como crash


### Versão ++2.68c (lançamento)
  - adicionou o excelente mutante gramatical GSoC AFL++ por Shengtuo ao nosso
    custom_mutators/ (see custom_mutators/README.md) - or get it here:
    https://github.com/AFLplusplus/Grammar-Mutator
  - algumas alterações de QV para a Apple e seu gmake desatualizado
  - Afl-fuzz:
    - fix for auto dictionary entries found during fuzzing to not throw out
      a -x dictionary
    - added total execs done to plot file
    - AFL_MAX_DET_EXTRAS env variable added to control the amount of
      deterministic dict entries without recompiling.
    - AFL_FORKSRV_INIT_TMOUT env variable added to control the time to wait
      for the forkserver to come up without the need to increase the overall
      timeout.
    - bugfix for cmplog that results in a heap overflow based on target data
      (thanks to the magma team for reporting!)
    - write fuzzing setup into out/fuzzer_setup (environment variables and
      command line)
  - mutadores personalizados:
    - added afl_custom_fuzz_count/fuzz_count function to allow specifying
      the number of fuzz attempts for custom_fuzz
  - Modo_ lvm:
    - ported SanCov to LTO, and made it the default for LTO. better
      instrumentation locations
    - Further llvm 12 support (fast moving target like AFL++ :-) )
    - deprecated LLVM SKIPSINGLEBLOCK env environment


### Versão ++2.67c (lançamento)
  - Suporte para o módulo de instantâneo AFL++ melhorado:
    https://github.com/AFLplusplus/AFL-Snapshot-LKM
  - Devido à instrumentação que precisa de mais memória, os tamanhos iniciais de memória
    for -m have been increased
  - Afl-fuzz:
     - added -F option to allow -M main fuzzers to sync to foreign fuzzers,
       e.g. honggfuzz or libfuzzer
     - added -b option to bind to a specific CPU
     - eliminated CPU affinity race condition for -S/-M runs
     - expanded havoc mode added, on no cycle finds add extra splicing and
       MOpt into the mix
     - fixed a bug in redqueen for strings and made deterministic with -s
     - Compiletime autodictionary fixes
  - Modo_ lvm:
     - now supports llvm 12
     - support for AFL_LLVM_ALLOWLIST/AFL_LLVM_DENYLIST (previous
       AFL_LLVM_WHITELIST and AFL_LLVM_INSTRUMENT_FILE are deprecated and
       are matched to AFL_LLVM_ALLOWLIST). The format is compatible to llvm
       sancov, and also supports function matching :)
     - added neverzero counting to trace-pc/pcgard
     - fixes for laf-intel float splitting (thanks to mark-griffin for
       reporting)
     - fixes for llvm 4.0
     - skipping ctors and ifuncs for instrumentation
     - LTO: switch default to the dynamic memory map, set AFL_LLVM_MAP_ADDR
            for a fixed map address (eg. 0x10000)
     - LTO: improved stability for persistent mode, no other instrumentation
            has that advantage
     - LTO: fixed autodict for long strings
     - LTO: laf-intel and redqueen/cmplog are now applied at link time
            to prevent llvm optimizing away the splits
     - LTO: autodictionary mode is a fixed default now
     - LTO: instrim instrumentation disabled, only classic support used
            as it is always better
     - LTO: env var AFL_LLVM_DOCUMENT_IDS=file will document which edge ID
            was given to which function during compilation
     - LTO: single block functions were not implemented by default, fixed
     - LTO: AFL_LLVM_SKIP_NEVERZERO behaviour was inversed, fixed
     - setting AFL_LLVM_LAF_SPLIT_FLOATS now activates
       AFL_LLVM_LAF_SPLIT_COMPARES
     - support for -E and -shared compilation runs
  - adicionado honggfuzz mutilar como um mutador personalizado em custom_mutators/honggfuzz
  - adicionada de solução de goma de afl-frida a exemplos/afl_frida (principalmente importada
    from https://github.com/meme/hotwax/)
  - pequenas correções para afl-plot, afl-whatsup e criação de página man
  - novo README, FAQ adicionada


### Versão ++2.66c (lançamento)
  - renomeou o branch principal no Github para "stable"
  - renomeado mestre/escravo para principal/secundário
  - renomeada lista negra/lista branca para ignonlist/instrumentlist ->
    AFL_LLVM_INSTRUMENT_FILE and AFL_GCC_INSTRUMENT_FILE
  - alertar sobre variáveis de ambiente desactualizadas
  - Afl-fuzz:
     - -S secondary nodes now only sync from the main node to increase
       performance, the -M main node still syncs from everyone. Added checks
       that ensure exactly one main node is present and warn otherwise
     - Add -D after -S to force a secondary to perform deterministic fuzzing
     - If no main node is present at a sync one secondary node automatically
       becomes a temporary main node until a real main nodes shows up
     - Fixed a mayor performance issue we inherited from AFLfast
     - switched murmur2 hashing and random() for xxh3 and xoshiro256**,
       resulting in an up to 5.5% speed increase
     - Resizing the window does not crash afl-fuzz anymore
     - Ensure that the targets are killed on exit
     - fix/update to MOpt (thanks to arnow117)
     - added MOpt dictionary support from repo
     - added experimental SEEK power schedule. It is EXPLORE with ignoring
       the runtime and less focus on the length of the test case
  - Modo_ lvm:
    - the default instrumentation is now PCGUARD if the llvm version is >= 7,
      as it is faster and provides better coverage. The original afl
      instrumentation can be set via AFL_LLVM_INSTRUMENT=AFL. This is
      automatically done when the instrument_file list feature is used. 
    - PCGUARD mode is now even better because we made it collision free - plus
      it has a fixed map size, so it is also faster! :)
    - some targets want a ld variant for LD that is not gcc/clang but ld,
      added afl-ld-lto to solve this
    - lowered minimum required llvm version to 3.4 (except LLVMInsTrim, which
      needs 3.8.0)
    - instrument_file list feature now supports wildcards (thanks to sirmc)
    - small change to cmplog to make it work with current llvm 11-dev
    - added AFL_LLVM_LAF_ALL, sets all laf-intel settings
    - LTO instrument_files functionality rewritten, now main, _init etc functions
      need not to be listed anymore
    - fixed crash in compare-transform-pass when strcasecmp/strncasecmp was
      tried to be instrumented with LTO
    - fixed crash in cmplog with LTO
    - enable snapshot lkm also for persistent mode
  - Unicornafl
    - Added powerPC support from unicorn/next
    - rust bindings!
  - CMPLOG/Redqueen agora também funciona para MMAP sharedmem
  - garantir que shmem é liberado em erros
  - movemos o radamsa para ser um mutante personalizado em ./custom_mutators/. Não é
    compiled by default anymore.
  - permitir a execução no /tmp (apenas inseguro com umask 0)
  - modo persistente de memória partilhada (em vez de via
    files/stdin) - 10-100% performance increase
  - Suporte geral para PowerPC 64 bits, RiscV, Sparc etc.
  - fixar afl-cmin.bash
  - opções de compilação de desempenho ligeiramente melhores para AFL++ e metas
  - afl-gcc/afl-as fixas que podem romper em sistemas rápidos de reutilização de pids em
    the same second
  - adicionaram muitos dicionários de oss-fuzz, go-fuzz e Jakub Wilk
  - ex-post_library exemplos para exemplos/custom_mutators/
  - Dockerfile atualizado para Ubuntu 20.04 Focal e instalando lvm 11 e
    gcc 10 so afl-clang-lto can be build


### Versão ++2.65c (lançamento):
  - Afl-fuzz:
     - AFL_MAP_SIZE was not working correctly
     - better python detection
     - an old, old bug in AFL that would show negative stability in rare
       circumstances is now hopefully fixed
     - AFL_POST_LIBRARY was deprecated, use AFL_CUSTOM_MUTATOR_LIBRARY
       instead (see docs/custom_mutators.md)
  - Modo_ lvm:
     - afl-clang-fast/lto now do not skip single block functions. This
       behaviour can be reactivated with AFL_LLVM_SKIPSINGLEBLOCK
     - if LLVM 11 is installed the posix shm_open+mmap is used and a fixed
       address for the shared memory map is used as this increases the
       fuzzing speed
     - InsTrim now has an LTO version! :-) That is the best and fastest mode!
     - fixes to LTO mode if instrumented edges > MAP_SIZE
     - CTX and NGRAM can now be used together
     - CTX and NGRAM are now also supported in CFG/INSTRIM mode
     - AFL_LLVM_LAF_TRANSFORM_COMPARES could crash, fixed
     - added AFL_LLVM_SKIP_NEVERZERO to skip the never zero coverage counter
       implementation. For targets with few or no loops or heavily called
       functions. Gives a small performance boost.
  - modo_ qemu:
    - add information on PIE/PIC load addresses for 32 bit
    - better dependency checks
  - 'plugin' gcc:
    - better dependency checks
  - Modo_ unicórnio:
    - validate_crash_callback can now count non-crashing inputs as crash as well
    - better submodule handling
  - afl- showmap: correção para o modo - Q
  - exemplos adicionados/afl_network_proxy que permite fuzz um alvo sobre o
    network (not fuzzing tcp/ip services but running afl-fuzz on one system
    and the target being on an embedded device)
  - exemplos adicionados/afl_untracer que faz um fuzzing apenas binário com o
    modifications done in memory (intel32/64 and aarch64 support)
  - exemplos adicionados/afl_proxy que podem ser facilmente usados para fuzz e instrumento
    non-standard things
  - Todos:
    - forkserver communication now also used for error reporting
    - fix 32 bit build options
    - make clean now leaves qemu-3.1.1.tar.xz and the unicornafl directory
      intact if in a git/svn checkout - unless "deepclean" is used


### Versão ++2.64c (lançamento):
  - Modo LTO em modo lvm_ mode:
    - now requires llvm11 - but compiles all targets! :)
    - autodictionary feature added, enable with `AFL_LLVM_LTO_AUTODICTIONARY`
    - variable map size usage
  - Afl-fuzz:
    - variable map size support added (only LTO mode can use this)
    - snapshot feature usage now visible in UI
    - Now setting `-L -1` will enable MOpt in parallel to normal mutation.
      Additionally, this allows to run dictionaries, radamsa and cmplog.
    - fix for cmplog/redqueen mode if stdin was used
    - fix for writing a better plot_data file
  - qemu_mode: correção para o modo persistente (que não terminaria ou ficaria preso)
  - compare-transform/AFL_LLVM_LAF_TRANSFORM_COMPARES agora transforma também
    static global and local variable comparisons (cannot find all though)
  - forkserver estendido: map_size e mais informações são comunicadas
    afl-fuzz (and afl-fuzz acts accordingly)
  - nova variável de ambiente: AFL_MAP_SIZE para especificar o tamanho do mapa compartilhado
  - se AFL_CC/AFL_CXX estiver definido, mas os compiladores vazios AFL falharam, corrigidos
    (this bug is in vanilla AFL too)
  - sinal de NO_ PYTHON adicionado para desativar suporte python ao construir afl- fuzz
  - mais refatorização


### Versão ++2.63c (lançamento):

! o repositório foi movido de vanhauser- thc para AFLplusplus. Agora é
    an own organisation :)
! desenvolvimento e aceitação de PRs agora acontecem apenas na filial dev
    and only occasionally when everything is fine we PR to master
  - Todos:
    - big code changes to make afl-fuzz thread-safe so afl-fuzz can spawn
      multiple fuzzing threads in the future or even become a library
    - AFL basic tools now report on the environment variables picked up
    - more tools get environment variable usage info in the help output
    - force all output to stdout (some OK/SAY/WARN messages were sent to
      stdout, some to stderr)
    - uninstrumented mode uses an internal forkserver ("fauxserver")
    - now builds with `-D_FORTIFY_SOURCE=2`
    - drastically reduced number of (de)allocations during fuzzing
  - Afl-fuzz:
    - python mutator modules and custom mutator modules now use the same
      interface and hence the API changed
    - AFL_AUTORESUME will resume execution without the need to specify `-i -`
    - added experimental power schedules (-p):
      - mmopt: ignores runtime of queue entries, gives higher weighting to
               the last 5 queue entries
      - rare: puts focus on queue entries that hits rare branches, also ignores
              runtime
  - Modo_ lvm:
    - added SNAPSHOT feature (using https://github.com/AFLplusplus/AFL-Snapshot-LKM)
    - added Control Flow Integrity sanitizer (AFL_USE_CFISAN)
    - added AFL_LLVM_INSTRUMENT option to control the instrumentation type
      easier: DEFAULT, CFG (INSTRIM), LTO, CTX, NGRAM-x (x=2-16)
    - made USE_TRACE_PC compile obsolete
  - LTO livre de colisão instrumentado adicionado em modo llvm_ com afl-clang-lto -
    this mode is amazing but requires you to build llvm 11 yourself
  - Adicionado llvm_mode NGRAM prev_loc cobertura por Adrean Herrera
    (https://github.com/adrianherrera/afl-ngram-pass/), activate by setting
    AFL_LLVM_INSTRUMENT=NGRAM-<value> or AFL_LLVM_NGRAM_SIZE=<value>
  - Adicionado cobertura de branch sensível ao contexto llvm_mode, ativada pela configuração
    AFL_LLVM_INSTRUMENT=CTX or AFL_LLVM_CTX=1
  - Modo instrim do modo lvm_ mode:
    - removed workaround for bug where paths were not instrumented and
      imported fix by author
    - made skipping 1 block functions an option and is disabled by default,
      set AFL_LLVM_INSTRIM_SKIPSINGLEBLOCK=1 to re-enable this
  - modo_ qemu:
    - qemu_mode now uses solely the internal capstone version to fix builds
      on modern Linux distributions
    - QEMU now logs routine arguments for CmpLog when the target is x86
  - afl-tmin:
    - now supports hang mode `-H` to minimize hangs
    - fixed potential afl-tmin missbehavior for targets with multiple hangs
  - Pressionando Control-c em afl-cmin não o terminou para algum OS
  - o API personalizado foi reescrito e agora é o mesmo para Python e compartilhado
    libraries.


### Versão ++2.62c (lançamento):

  - Correção importante para funções de alocação de memória que resultam em afl-fuzz
    not identifying crashes - UPDATE!
  - Pequena correção para -E/-V para liberar a CPU
  - O CmpLog não precisa mais de sancov


### Versão ++2.61c (lançamento):

  - use -march=native se disponível
  - a maioria das ferramentas agora verifica por variáveis de ambiente erroneamente digitadas
  - O gcc 10 agora é suportado
  - as verificações de segurança da memória estão agora desactivadas para um pouco mais de velocidade durante
    fuzzing (only affects creating queue entries), can be toggled in config.h
  - Afl-fuzz:
     - MOpt out of bounds writing crash fixed
     - now prints the real python version support compiled in
     - set stronger performance compile options and little tweaks
     - Android: prefer bigcores when selecting a CPU
     - CmpLog forkserver
     - Redqueen input-2-state mutator (cmp instructions only ATM)
     - all Python 2+3 versions supported now
     - changed execs_per_sec in fuzzer_stats from "current" execs per second
       (which is pointless) to total execs per second
     - bugfix for dictionary insert stage count (fix via Google repo PR)
     - added warning if -M is used together with custom mutators with _ONLY option
     - AFL_TMPDIR checks are now later and better explained if they fail
  - modo_ lvm
     - InsTrim: three bug fixes:
        1. (minor) no pointless instrumentation of 1 block functions
        2. (medium) path bug that leads a few blocks not instrumented that
           should be
        3. (major) incorrect prev_loc was written, fixed!
  - afl-clang-fast:
     - show in the help output for which llvm version it was compiled for
     - now does not need to be recompiled between trace-pc and pass
       instrumentation. compile normally and set AFL_LLVM_USE_TRACE_PC :)
     - LLVM 11 is supported
     - CmpLog instrumentation using SanCov (see llvm_mode/README.cmplog.md)
  - Afl-gcc, afl-clang-fast, afl-gcc-fast:
     - experimental support for undefined behaviour sanitizer UBSAN
       (set AFL_USE_UBSAN=1)
     - the instrumentation summary output now also lists activated sanitizers
     - afl-as: added isatty(2) check back in
     - added AFL_DEBUG (for upcoming merge)
  - modo_ qemu:
     - persistent mode is now also available for arm and aarch64
     - CmpLog instrumentation for QEMU (-c afl-fuzz command line option)
       for x86, x86_64, arm and aarch64
     - AFL_PERSISTENT_HOOK callback module for persistent QEMU
       (see examples/qemu_persistent_hook)
     - added qemu_mode/README.persistent.md documentation
     - AFL_ENTRYPOINT now has instruction granularity
  - o afl-cmin é agora um script sh (invocando o awk) em vez de bash para portabilidade
    the original script is still present as afl-cmin.bash
  - afl-showmap: -i dir opção agora permite o processamento de múltiplas entradas usando o
     forkserver. This is for enhanced speed in afl-cmin.
  - lista negra adicionada e verificação da função instrument_filesing em todos os módulos do modo lvm_mode
  - correção adicionada do projeto Debian para compilar libdislocator e libtokencap
  - libdislocalator: AFL_ALIGNED_ALLOC para forçar o alinhamento do tamanho a max_align_t


### Versão ++2.60c (lançamento):

  - fixou um erro crítico no afl-tmin que foi introduzido durante ++2.53d
  - Casos de ensaio adicionados para afl-cmin e afl-tmin ao teste/teste.sh
  - adicionado ./exemplos/argv_fuzzing ld_preload library by Kjell Braden
  - added preeny's desock_dup ld_preload library as
    ./examples/socket_fuzzing for network fuzzing
  - Adicionada variável de ambiente AFL_AS_FORCE_INSTRUMENT para afl-as - isto é
    for the retrorewrite project
  - agora definimos QEMU_SET_ENV de AFL_PRELOAD quando qemu_mode é usado


### Versão ++2.59c (lançamento):

  - qbdi_ modo: bibliotecas nativas do fuzz andróide via framework QBDI
  - unicorn_mode: comutado para o novo unicornafl, obrigado domenukk
                  (see https://github.com/vanhauser-thc/unicorn)
  - Afl-fuzz:
     - added radamsa as (an optional) mutator stage (-R[R])
     - added -u command line option to not unlink the fuzz input file
     - Python3 support (autodetect)
     - AFL_DISABLE_TRIM env var to disable the trim stage
     - CPU affinity support for DragonFly
  - Modo_ lvm:
     - float splitting is now configured via AFL_LLVM_LAF_SPLIT_FLOATS
     - support for llvm 10 included now (thanks to devnexen)
  - libtokencap:
     - support for *BSD/OSX/Dragonfly added
     - hook common *cmp functions from widely used libraries
  - Compcov:
     - hook common *cmp functions from widely used libraries
     - floating point splitting support for QEMU on x86 targets
  - qemu_mode: AFL_QEMU_DISABLE_CACHE env para desativar o cache QEMU TranslationBlocks
  - afl- analyze: suporte AFL_SKIP_BIN_CHECK adicionado
  - melhores números aleatórios para gcc_plugin e lvm_mode (graças ao devnexen)
  - Dockerfile por cortesia de devnexen
  - adicional regex.dictionary
  - qemu e scripts de download de unicórnio agora tentar baixar até o total
    download succeeded. f*ckin travis fails downloading 40% of the time!
  - mais suporte para Android (por favor teste!)
  - adicionou as poucas coisas Android que já não temos do repositório Google AFL
  - avisos desnecessários removidos


### Versão ++2.58c (lançamento):

  - revertida patch para não desvincular e recriar o arquivo de entrada, resultou em
    performance loss of ~10%
  - script adicionado test/test-performance.sh
  - (re)adicionado gcc_plugin, a instrumentação em linha rápida ainda não está terminada,
    however it includes the instrument_filesing and persistance feature! by hexcoder-
  - Testes gcc_plugin adicionados à estrutura de testes


### Versão ++2.54d-2.57c (lançamento):

  - saltamos para 2.57 em vez de 2.55 para alcançar a versão do Google
  - modo persistente para o QEMU (ver qemu_mode/README.md)
  - biblioteca mutator personalizada é agora um mutator adicional, para exclusivamente usá-lo
    add AFL_CUSTOM_MUTATOR_ONLY (that will trigger the previous behaviour)
  - nova biblioteca qemu_mode/unsigaction que filtra eventos sigaction
  - afl-fuzz: nova opção de linha de comando - I para executar um comando num novo estoiro
  - não mais desvincular o arquivo de entrada, desta forma o arquivo de entrada também pode ser um
    FIFO or disk partition
  - a configuração do LLVM_ CONFIG para o modo llvm_ irá mudar novamente para o seleccionado
    llvm version. If your setup is correct.
  - fuzzing rendimento de estratégia para mutator personalizado estavam faltando da UI, acrescentou-os :)
  - adicionado "fazer testes" que irá realizar verificações para ver que toda a funcionalidade
    is working as expected. this is currently the starting point, its not complete :)
  - recurso de documentação de mutação adicionado ("make document"), cria afl-fuzz-document
    and saves all mutations of the first run on the first file into out/queue/mutations
  - libtokencap e libdislocator agora compilam para o diretório afl_root e são
    installed to the .../lib/afl directory when present during make install
  - mais suporte BSD, por exemplo, livre código de ligação CPU para FreeBSD (graças ao devnexen)
  - redução do código duplicado em afl-fuzz
  - adicionado "fazer ajuda"
  - removeu os avisos de compilação do material interno python
  - página de manual adicionada para afl-clang-fast[++]
  - documentação atualizada
  - Modo de vinho para executar binários Win32 com a instrumentação QEMU (-W)
  - CompararCobertura para o alvo ARM em QEMU/Unicórnio
  - laf-intel em llvm_mode agora também lida com comparações de pontos flutuantes


### Versão ++2.54c (lançamento):

  - refactoração de código grande:
    * all includes are now in include/
    * all AFL sources are now in src/ - see src/README.md
    * afl-fuzz was split up in various individual files for including
      functionality in other programs (e.g. forkserver, memory map, etc.)
      for better readability.
    * new code indention everywhere
  - Páginas manuais de geração automática para todas as ferramentas (principais)
  - adicionado AFL_FORCE_UI para mostrar a UI mesmo que o terminal não seja detectado
  - O lvm 9 agora é suportado (ainda precisa de testes)
  - Android agora é suportado (Graças a JoeyJiao!) - ainda precisa modificar o Makefile embora
  - corrigir qemu edifício em algum Ubuntus (graças ao floyd!)
  - Mutador personalizado por uma biblioteca carregada agora é suportado (graças ao kyakdan!)
  - PR adicionado que inclui pico_rss_mb e slowest_exec_ms no relatório fuzzer_stats
  - mais suporte para *BSD (graças ao devnexen!)
  - corrigir edifício no *BSD (graças a tobias.kortkamp para o patch)
  - corrigir para alguns recursos para suportar mapa diferente tamanho de 2^16
  - afl-showmap: a nova opção -r agora mostra os valores reais nos baldes (stock
    AFL never did), plus shows tuple content summary information now
  - pequenas actualizações docu
  - Contadores NeverZero para QEMU
  - NeverZero contadores para Unicórnio
  - CompararCoverage Unicórnio
  - instrumentação apenas imediata para CompareCoverage


### Versão ++2.53c (lançamento):

  - README é agora README.md
  - importou as poucas pequenas alterações da versão 2.53b
  - unicorn_mode foi adicionado - graças ao domenukk para o patch!
  - jncp@ netcabo. pt
  - corrigir uma falha no modo qemu_ que também existe em stock afl
  - adicionado libcompcov, uma implementação laf-intel para qemu! :)
    see qemu_mode/libcompcov/README.libcompcov.md
  - afl-fuzz agora exibe o núcleo selecionado na tela de status (azul {#})
  - atualizado afl-fuzz e afl-system-config para nova localização do regulador de escala
    in modern kernels
  - usando o velho afl-gcc ineficaz irá agora mostrar um aviso de depreciação
  - todos os arquivos de fila, espera e falha agora têm seu tempo de descoberta em seu nome
  - se llvm_mode foi compilado, afl-clang/afl-clang++ apontará para estes
    instead of afl-gcc
  - instrim adicionado, uma instrumentação muito mais rápida llvm_mode ao custo de
    path discovery. See llvm_mode/README.instrim.md (https://github.com/csienslab/instrim)
  - Modo MOpt (github.com/puppet-meteor/MOpt-AFL), ver docs/README.MOpt.md
  - código adicionado para torná-lo mais portátil para outras plataformas do que Intel Linux
  - adicionado nunca zero contadores para afl-gcc e opcionalmente (por causa de um
    optimization issue in llvm < 9) for llvm_mode (AFL_LLVM_NEVER_ZERO=1)
  - adicionou um novo documento sobre apenas o binário fuzzing: docs/binaryonly_fuzzing.txt
  - mais potência cpu para afl-system-config
  - o patch forkserver adicionado ao afl- tmin, torna- o muito mais rápido (originalmente de
    github.com/nccgroup/TriforceAFL)
  - suporte adicional de instrument_files para lvm_mode via AFL_LLVM_WHITELIST para permitir
    only to instrument what is actually interesting. Gives more speed and less
    map pollution (originally by choller@mozilla)
  - Adicionado Python Module mutator support, python2.7-dev é autodetectado.
    see docs/python_mutators.txt (originally by choller@mozilla)
  - adicionado AFL_CAL_FAST para aplicações lentas e AFL_DEBUG_CHILD_OUTPUT para
    debugging
  - added -V time and -E executs option to better comparation runs, corre afl-fuzz
    for a specific time/executions.
  - adicionado um interruptor de sementes de a - s para permitir a execução da AFL com uma inicial fixa
    seed that is not updated. This is good for performance and path discovery
    tests as the random numbers are deterministic then
  - lvm_mode LAF_... as variáveis env podem agora ser especificadas como AFL_LLVM_LAF_...
    that is longer but in line with other llvm specific env vars


### Versão ++2.52c (2019-06-05):

  - patches comunitários aplicados. Veja documentos/patches para a lista completa.
    LLVM and Qemu modes are now faster.
    Important changes:
      afl-fuzz: -e EXTENSION commandline option
      llvm_mode: LAF-intel performance (needs activation, see llvm/README.laf-intel.md)
      a few new environment variables for afl-fuzz, llvm and qemu, see docs/env_variables.md
  - Adicionado os escalonamentos de energia de AFLfast por Marcel Boehme, mas definir o padrão
    to the AFL schedule, not to the FAST schedule. So nothing changes unless
    you use the new -p option :-) - see docs/power_schedules.md
  - adicionado script de configuração do sistema afl para definir todas as opções de desempenho do sistema para fuzzing
  - llvm_mode funciona com llvm 3.9 até 8 inclusive!
  - qemu_mode foi atualizado de 2.1 para 3.1 - incorporado de
    https://github.com/andreafioraldi/afl and with community patches added


### Versão 2.52b (2017-11-04):

  - Modificado patches QEMU de 2.3.0 para 2.10.0. Resolução de problemas necessária
    several weird issues. All the legwork done by Andrew Griffiths.

  - Adicionado setsid ao afl- showmap. Veja as notas para 2.51b.

  - Modo alvo adicionado (deferido, persistente, qemu, etc) para fuzzer_stats.
    Requested by Jakub Wilk.

  - o afl- tmin deverá agora gravar um arquivo parcialmente minimizado quando Ctrl- C
    is pressed. Suggested by Jakub Wilk.

  - Adicionado uma opção para afl-analyze para despejar offsets em hex. Sugerido por
    Jakub Wilk.

  - Adicionado suporte para parâmetros em triage_crashes.sh. Patch by Adam of
    DC949.

### Versão 2.51b (2017-08-30):

  - Made afl-tmin call setsid para evitar que o lixo traceback da glibc apareça
    up on the terminal in some distros. Suggested by Jakub Wilk.

### Versão 2.50b (2017-08-19):

  - Arranjei um interessante caso de esquina localizado por Jakub Wilk.

  - Endereçado a um problema de incompatibilidade da libtokencap / pthreads. Da mesma forma, localizado
    by Jakub Wilk.

  - Acrescentou uma menção de afl-kit e Pythia.

  - Adicionado AFL_FAST_CAL.

  - O currículo in-place agora preserva .synced. Sugerido por Jakub Wilk.

### Versão 2.49b (2017-07-18):

  - Adicionado AFL_TMIN_EXACT para permitir restrição de caminho para minimização de falhas.

  - Datas adicionadas para lançamentos (retroativamente para todo 2017).

### Versão 2.48b (2017-07-17):

  - Adicionado AFL_ALLOW_TMP para permitir que alguns scripts sejam executados em /tmp.

  - Manuseamento fixo de cwd em afl-analyze (semelhante à peculiaridade em afl-tmin).

  - Tornou possível apontar -o e -f para o mesmo arquivo em afl-tmin.

### Versão 2.47b (2017-07-14):

  - Manuseamento fixo de cwd em afl-tmin.

### Versão 2.46b (2017-07-10):

  - libdislocator agora suporta AFL_LD_NO_CALLOC_OVER para pessoas que não
    want to abort on calloc() overflows.

  - Fiz uma pequena correção para a libtokencap, reportada por Daniel Stender.

  - Adicionado um pequeno dicionário JSON, inspirado em um dicionário feito por Jakub Wilk.

### Versão 2.45b (2017-07-04):

  - Adicionado suporte ao strstr, strcasestr à libtokencap. Contribuído por
    Daniel Hodson.

  - Consertou uma falha de recolocação vista por Jakub Wilk.

  - Definitivamente não há bugs no afl-showmap -c agora.

### Versão 2.44b (2017-06-28):

  - Adicionado um indicador visual do modo ASAN / MSAN ao compilar.
    by Jakub Wilk.

  - Adicionado suporte para afl-showmap-coredumps (-c). Sugerido por Jakub Wilk.

  - Adicionado LD_ BIND_ NOW=1 para o afl- showmap por padrão. Embora não seja realmente útil,
    it reportedly helps reproduce some crashes. Suggested by Jakub Wilk.

  - Adicionado uma nota sobre alocator_may_return_null=1 nem sempre trabalhando com
    ASAN. Spotted by Jakub Wilk.

### Versão 2.43b (2017-06-16):

  - Adicionado AFL_NO_ARITH para ajudar no fuzzing de formatos baseados em texto.
    Requested by Jakub Wilk.

### Versão 2.42b (2017-06-02):

  - Renomeou a macro R () para evitar um problema com lvm_mode no último
    versions of LLVM. Fix suggested by Christian Holler.

### Versão 2.41b (2017-04-12):

  - Dirigiu-se a uma grande queixa de usuário relacionada à detecção de tempo- limite.
    inputs are now binned as "hangs" only if they exceed a far more generous
    time limit than the one used to reject slow paths.

### Versão 2.40b (2017-04-02):

  - Corrigido um pequeno descuido na estratégia de inserção de palavras de dicionário.
    Spotted by Andrzej Jackowski.

  - Fez uma pequena melhoria na estratégia de inserção do bloco de estragos.

  - Regras de cor ajustadas para "já está feito?" indicadores.

### Versão 2.39b (2017-02-02):

  - Relatório de erro melhorado em afl-cmin. Sugerido pelo floyd.

  - Fez um pequeno ajuste para o suporte de guarda- traços. Sugerido pelo kcc.

  - Adicionado uma menção de afl-monitor.

### Versão 2.38b (2017-01-22):

  - Adicionado -mllvm -sanitizer-coverage-block-threshold=0 para trace-pc-guard
    mode, as suggested by Kostya Serebryany.

### Versão 2.37b (2017-01-22):

  - Marcado por Jakub Wilk.

  - Suporte fixo para a instalação do make ao usar o trace-pc.
    Kurt Roeckx.

  - Alternado trace-pc para trace-pc-guard, que deve ser consideravelmente
    faster and is less quirky. Kudos to Konstantin Serebryany (and sorry
    for dragging my feet).

    Note that for some reason, this mode doesn't perform as well as
    "vanilla" afl-clang-fast / afl-clang.

### Versão 2.36b (2017-01-14):

  - Corrigido um erro cosmético mau free() ao interromper as sessões -S. Spotted
    by Johannes S.

  - Fez uma pequena mudança para afl-whatsup para classificar fuzzers pelo nome.

  - Corrigido um pequeno problema com o malloc( 0) no libdislocator.
    Rene Freingruber.

  - Mudou o padrão de clobber no libdislocator para um pouco mais
    reliable one. Suggested by Rene Freingruber.

  - Adicionei uma nota sobre o desempenho do THP. Sugerido por Sergey Davidoff.

  - Adicionado um suporte um tanto não oficial para executar afl-tmin com um
    baseline "mask" that causes it to minimize only for edges that
    are unique to the input file, but not to the "boring" baseline.
    Suggested by Sami Liedes.

  - "Fixed" um problema getPassName() com versões mais recentes do clang.
    Reported by Craig Young and several other folks.

Sim, eu sei que eu tenho um backlog em vários outros recursos pedidos.
Fiquem ligados!

### Versão 2.35b:

  - Corrigimos uma pequena falha na linha cmdline, detectada por Leo Barnes.

  - Corrigido um erro bobo na libdislocator. manchado por Johannes Schultz.

### Versão 2.34b:

  - Adicionado uma nota sobre afl-tmin para technical_details.txt.

  - Adicionado suporte para AFL_NO_UI, como sugerido por Leo Barnes.

### Versão 2.33b:

  - Adicionado código para strip -Wl,-z,defs e -Wl,--no-undefined para afl-clang-fast,
    since they interfere with -shared. Spotted and diagnosed by Toby Hutton.

  - Adicionado algumas dicas fuzzing para Android.

### Versão 2.32b:

  - Adicionado uma verificação para AFL_HARDEN combinada com AFL_USE_*SAN. Sugerido por
    Hanno Boeck.

  - Fez vários outros ajustes cosméticos para ciclo timing na sequência do
    big tweak made in 2.31b.

### Versão 2.31b:

  - O ciclo de estragos alterado conta para um aumento acentuado do desempenho, especialmente
    with -S / -d. See the discussion of FidgetyAFL in:

    https://groups.google.com/forum/#!topic/afl-users/fOPeb62FZUg

    While this does not implement the approach proposed by the authors of
    the CCS paper, the solution is a result of digging into that research;
    more improvements may follow as I do more experiments and get more
    definitive data.

### Versão 2.30b:

  - Fez pequenas melhorias no modo persistente para evitar o controle remoto
    possibility of "no instrumentation detected" issues with very low
    instrumentation densities.

  - Corrigido uma falha menor com um processo de sobra em modo persistente.
    Reported by Jakub Wilk and Daniel Stender.

  - Made bitmaps de modo persistente um pouco mais consistente e ajustado a maneira
    this is shown in the UI, especially in persistent mode.

### Versão 2.29b:

  - Fez uma correção menor #include para llvm_mode. Sugerido por Jonathan Metzman.

  - Fiz actualizações cosméticas aos médicos.

### Versão 2.28b:

  - Adicionado "Life pro tips" para docs/.

  - Casos de teste movidos/_extras/ para dicionários/ para visibilidade.

  - Fez pequenas melhorias para instalar scripts.

  - Acrescentou uma importante dica de segurança.

### Versão 2.27b:

  - Adicionado libtokencap, um recurso simples para interceptar strcmp / memcmp e
    generate dictionary entries that can help extend coverage.

  - Moveu o libdislocator para sua própria dir, adicionou o README.md.

  - A demonstração em exemplos/instrumentado_cmp não é mais.

### Versão 2.26b:

  - Fiz uma correção para libdislocator.so para compilar no MacOS X.

  - Adicionado suporte para DYLD_INSERT_LIBRARIES.

  - Renomeado AFL_LD_PRELOAD para AFL_PRELOAD.

### Versão 2.25b:

  - Fiz algumas atualizações cosméticas para libdislocator.so, renomeado um env
    variable.

### Versão 2.24b:

  - Adicionado libdislocator.so, um alocador experimental e abusivo.
    it out with AFL_LD_PRELOAD=/path/to/libdislocator.so when running
    afl-fuzz.

### Versão 2.23b:

  - Melhorou a métrica de estabilidade para binários de modo persistente.
    spotted by Kurt Roeckx.

  - Fez uma melhoria relacionada que pode trazer a métrica para 100% para aqueles
    targets.

### Versão 2.22b:

  - Mencionou os potenciais conflitos entre MSAN / ASAN e FORTIFY_OURCE.
    There is no automated check for this, since some distros may implicitly
    set FORTIFY_SOURCE outside of the compiler's argv[].

  - Populado o suporte para AFL_LD_PRELOAD para todas as ferramentas companheiras.

  - Fez uma alteração no manuseamento de ./afl-clang-fast-v.
    Jan Kneschke.

### Versão 2.21b:

  - Adicionado algumas notas de relatório de falha para Solaris em docs/INSTALL, como
    investigated by Martin Carpenter.

  - Corrigimos uma pequena confusão de IU com estatísticas de estratégia de destruição.

### Versão 2.20b:

  - Renovou o manuseio de caminhos variáveis, substituindo a contagem de caminhos por um
    "stability" score to give users a much better signal. Based on the
    feedback from Vegard Nossum.

  - Melhorou a estabilidade do comportamento de sincronização com o reinício
    fuzzers. Based on the feedback from Vegard.

  - Alterou a interface para incluir a densidade atual do mapa de bits juntamente com
    total density. Ditto.

  - Adicionado suporte experimental para paralelização -M.

### Versão 2.19b:

  - Fez uma correção para certificar-se de que a ligação de CPU automática acontece em não- sobreposição
    times.

### Versão 2.18b:

  - Fez várias melhorias de desempenho para has_new_bits() e
    classify_counts(). This should offer a robust performance bump with
    fast targets.

### Versão 2.17b:

  - Matou a opção -Z manual e propensa a erros. No Linux, a AFL irá agora
    automatically bind to the first free core (or complain if there are no
    free cores left).

  - Fiz algumas actualizações de documentos nestas linhas.

### Versão 2.16b:

  - Suporte melhorado para versões mais antigas do clang (esperançosamente sem
    breaking anything).

  - Moveu os dados da versão do Makefile para config.h. Sugerido por
    Jonathan Metzman.

### Versão 2.15b:

  - Adicionado uma seção README na procura de bugs não-crashing.

  - Adicionamos dados de licença a vários arquivos chatos. Contribuído por
    Jonathan Metzman.

### Versão 2.14b:

  - Adicionado FUZZING_BUILD_MODE_UNSAFE_FOR_PRODUCTION como uma macro definida quando
    compiling with afl-gcc and friends. Suggested by Kostya Serebryany.

  - Refrescou alguns dos documentos não-x86.

### Versão 2.13b:

  - Corrigido um erro de teste de compilação espúrio com trace-pc e llvm_mode/Makefile.
    Spotted by Markus Teufelberger.

  - Resolveu um problema de cosmética com o que se passa, visto por Brandon Perry.

### Versão 2.12b:

  - Corrigido um problema menor em afl-tmin que pode tornar o alfabeto minimização menos
    efficient during passes > 1. Spotted by Daniel Binderman.

### Versão 2.11b:

  - Corrigido um erro de digitação menor em instrumentado_cmp, manchado por Hanno Eissfeldt.

  - Adicionado uma verificação de tamanho faltando para etapas de inserção determinística.

  - Fez uma melhoria para afl-gotcpu quando -Z não utilizado.

  - Corrigido um erro de digitação em post_library_png.so.c em exemplos/. Spotted by Kostya
    Serebryany.

### Versão 2.10b:

  - Corrigimos uma falha na contagem do núcleo, reportada por Tyler Nighswander.

### Versão 2.09b:

  - Fiz várias atualizações de documentação.

  - Adicionado alguns indicadores visuais para promover e simplificar o uso de -Z.

### Versão 2.08b:

  - Adicionado suporte explícito para - m32 e - m64 para lvm_ mode. Inspirado por
    a request from Christian Holler.

  - Adicionada uma nova opção de benchmarking, conforme solicitado por Kostya Serebryany.

### Versão 2.07b:

  - Adicionada opção de afinidade de CPU (- Z) no Linux. Com alguma precaução, isto pode
    offer a significant (10%+) performance bump and reduce jitter.
    Proposed by Austin Seipp.

  - Atualizado afl-gotcpu para usar a afinidade da CPU onde suportado.

  - Corrigido confundindo mensagens de erro CPU_TARGET com a compilação QEMU.
    Daniel Komaromy and others.

### Versão 2.06b:

  - Trabalhou em torno de soluços de modo persistente LLVM com código compartilhado.
    Contributed by Christian Holler.

  - Adicionado __AFL_COMPILER como uma maneira conveniente de detectar que algo é
    built under afl-gcc / afl-clang / afl-clang-fast and enable custom
    optimizations in your code. Suggested by Pedro Corte-Real.

  - Subiu várias pequenas mudanças desenvolvidas por Franjo Ivancic para
    allow AFL to be built as a library. This is fairly use-specific and
    may have relatively little appeal to general audiences.

### Versão 2.05b:

  - Colocar o __sanitizer_cov_module_init & co por trás do #ifdef para evitar problemas
    with ASAN. Spotted by Christian Holler.

### Versão 2.04b:

  - Cobertura de chamadas indiretas removidas de -fsanitize-coverage (uma vez que é
    redundant). Spotted by Kostya Serebryany.

### Versão 2.03b:

  - Adicionado suporte experimental -fsanitize-coverage=trace-pc que acompanha
    some recent additions to LLVM, as implemented by Kostya Serebryany.
    Right now, this is cumbersome to use with common build systems, so
    the mode remains undocumented.

  - Realizaram várias melhorias substanciais para melhor apoiar o não-padrão
    map sizes in LLVM mode.

  - Modo LLVM comutado para rastreamento de execução local de thread, que pode oferecer
    better results in some multithreaded apps.

  - Corrigido um pequeno erro de digitação, relatado por Heiko Eissfeldt.

  - Simbolização desativada por força para ASAN, como sugerido por Christian Holler.

  - AFL_NOX86 renomeado para AFL_NO_X86 para consistência.

  - Adicionado AFL_LD_PRELOAD para permitir que LD_PRELOAD seja definido para alvos sem
    affecting AFL itself. Suggested by Daniel Godas-Lopez.

### Versão 2.02b:

  - Corrigido um erro "lcamtuf não pode contar até 16" na fase de destruição. Reportado
    by Guillaume Endignoux.

### Versão 2. 01b:

  - Fez uma melhoria na codificação de cores do contador do ciclo, com base no feedback
    from Shai Sarfaty.

  - Adicionado uma menção de aflize para sister_projects.txt.

  - Corrigido um problema de instalação com afl-as, como visto por ilovezfs.

### Versão 2.00b:

  - Limpei o manuseio de cor após um pequeno snafu em 1,99b (afetando alguns
    terminals).

  - Fiz pequenas atualizações para a documentação.

### Versão 1.99b:

  - Substantially reformulou a saída e a lógica interna do afl-analyze.

  - Limpei alguns dos códigos de manipulação de cores e adicionei suporte para
    background colors.

  - Removeu alguns arquivos perdidos (oops).

  - Documentos atualizados para melhor explicar afl-analyze.

### Versão 1.98b:

  - Melhorado para detecção de "cordas chatas" em afl-analyze.

  - Adicionado technical_details.txt para afl-analyze.

### Versão 1.97b:

  - Adicionado afl-analyze, uma ferramenta bacana para analisar a estrutura de um arquivo
    based on the feedback from AFL instrumentation. This is kinda experimental,
    so field reports welcome.

  - Acrescentou uma menção de afl-cygwin.

  - Corrigido um par de erros de digitação, como relatado por Jakub Wilk e outros.

### Versão 1.96b:

  - Adicionado -fpic para CFLAGS para o plugin clang, como sugerido por Hanno Boeck.

  - Fez outra mudança de clang (IRBuilder) sugerida por Jeff Trull.

  - Corrigido vários erros de digitação, manchado por Jakub Wilk.

  - Adicionado suporte para AFL_SHUFFLE_QUEUE, baseado em discussões com
    Christian Holler.

### Versão 1.95b:

  - Corrigido um bug inofensivo ao manusear -B. Manuseado por Jacek Wielemborek.

  - Tornou a mensagem de saída um pouco mais precisa quando AFL_EXIT_WHEN_DONE está definido.

  - Adicionado uma verificação de erros para a sintaxe do servidor de fork do estilo antigo. Sugerido por
    Ben Nagy.

  - Alternado de exit() para _exit() em código injetado para evitar snafus com
    destructors in C++ code. Spotted by sunblate.

  - Fez uma alteração para evitar a configuração espúria do __AFL_SHM_ID quando
    AFL_DUMB_FORKSRV is set in conjunction with -n. Spotted by Jakub Wilk.

### Versão 1.94b:

  - Alinhamento do alocador alterado para melhorar o suporte para sistemas não-x86 (agora
    that llvm_mode makes this more feasible).

  - Corrigido um pequeno erro de digitação em afl-cmin.

  - Corrigido um erro obscuro que afetaria as pessoas que tentam usar o afl-gcc
    with $TMP set but $TMPDIR absent. Spotted by Jeremy Barnes.

### Versão 1.93b:

  - Esperançosamente corrigir um problema com MacOS X e modo persistente, visto por
    Leo Barnes.

### Versão 1.92b:

  - Fez mais uma correção C++ (namespaces). Reportado por Daniel Lockyer.

### Versão 1.91b:

  - Fez outra correção para fazer 1.90b funcionar corretamente com C++ (d'oh).
    Problem spotted by Daniel Lockyer.

### Versão 1.90b:

  - Corrigido um pequeno erro de digitação manchado por Kai Zhao; e fez várias outras atualizações menores
    to docs.

  - Atualizado o URL do projeto para python-afl. Solicitado por Jakub Wilk.

  - Corrigido um problema potencial com assinaturas de modo diferido sendo otimizado
    out by the linker (with --gc-sections).

### Versão 1.89b:

  - Renovou o suporte para modos de forkserver persistentes e diferidos.
    Both now feature simpler syntax and do not require companion env
    variables. Suggested by Jakub Wilk.

  - Adicionado um pouco mais informações sobre afl-showmap. Sugerido por Jacek Wielemborek.

### Versão 1.88b:

  - Feito AFL_ EXIT_ WHEN_ DONE funcionar em modo não- tty. Problema visto por
    Jacek Wielemborek.

### Versão 1.87b:

  - Adicionado QuickStartGuide.txt, um doc de início rápido de uma página.

  - Corrigido vários erros de digitação detectados por Dominique Pelle.

  - Revogado várias partes do README.

### Versão 1.86b:

  - Adicionado suporte para AFL_SKIP_CRASHES, que é uma solução muito hackish para
    the problem of resuming sessions with intermittently crashing inputs.

  - Removeu a verificação do tamanho do terminal com falha difícil, substituída por uma dinâmica
    warning shown in place of the UI. Based on feedback from Christian Holler.

  - Corrigido um erro de digitação menor no show_stats. Marcado por Dingbao Xie.

### Versão 1.85b:

  - Corrigido uma sentença em notas em paralelo fuzzing. Graças a Jakub Wilk.

  - Corrigido um pequeno defeito na afl-cmin.

### Versão 1.84b:

  - Made SIMPLE_FILES comportar-se como esperado ao nomear diretórios de backup para
    crashes and hangs.

  - Adicionado o número total de caminhos favoritos para fuzzer_stats. Solicitado por
    Ben Nagy.

  - Afl-tmin, afl-fuzz, e afl-cmin rejeitam valores negativos passados para
    -t and -m, since they generally won't work as expected.

  - Fiz uma correção para nenhum suporte a lahf / sahf em versões mais antigas do FreeBSD.
    Patch contributed by Alex Moneger.

### Versão 1. 83b:

  - Corrigido um problema com xargs -d em sistemas não-Linux em afl-cmin.
    teor2345 and Ben Nagy.

  - Corrigido uma declaração implícita no modo LLVM no MacOS X. Reportado por
    Kai Zhao.

### Versão 1.82b:

  - Corrigido uma condição de raça inofensiva, mas irritante no modo persistente - sinal
    delivery is a bit more finicky than I thought.

  - Atualizou a documentação para explicar um pouco melhor o modo persistente.

  - AFL_PERSISTENTE alterado para forçar AFL_NO_VAR_CHECK.

### Versão 1.81b:

  - Adicionado modo persistente para o fuzzing em processo. Veja llvm_mode/README.llvm.
    Inspired by Kostya Serebryany and Christian Holler.

  - Alterou o código de currículo no local para preservar falhas/README.txt. Sugerido
    by Ben Nagy.

  - Incluído uma correção potencial para problemas de modo LLVM no MacOS X, com base no
    investigation done by teor2345.

### Versão 1.80b:

  - Tornou o afl- cmin tolerante aos espaços em branco nos nomes de arquivos. Sugerido por
    Jonathan Neuschafer and Ketil Froyn.

  - Adicionado suporte para AFL_EXIT_WHEN_DONE, como sugerido por Michael Rash.

### Versão 1.79b:

  - Adicionado suporte para níveis de dicionário, veja casos de teste/README.testcasos.

  - Retrabalhou o dicionário SQL para usar níveis.

  - Adicionei uma nota sobre Preeny.

### Versão 1.78b:

  - Adicionado um dicionário para PDF, contribuído por Ben Nagy.

  - Acrescentou várias referências ao afl-cov, uma nova ferramenta de Michael Rash.

  - Corrigido um problema com detecção de repórter de crash no MacOS X, como relatado por
    Louis Dassy.

### Versão 1.77b:

  - Estendi a opção -x para suportar dicionários de arquivo único.

  - Dicionários embalados em fábrica substituídos por variantes baseadas em arquivos.

  - Removeu novas linhas das palavras- chave HTML em casos de teste/_extras/html/.

### Versão 1.76b:

  - Reduzir significativamente o número de executivos duplicados durante
    deterministic checks, chiefly in int16 and int32 stages. Confirmed
    identical path yields. This should improve early-stage efficiency by
    around 5-10%.

  - Redução da probabilidade de duplicados executivos não deterministas por
    bumping up lowest stacking factor from 1 to 2. Quickly confirmed
    that this doesn't seem to have significant impact on coverage with
    libpng.

  - Acrescentou uma nota sobre integrar afl-fuzz com ferramentas de terceiros.

### Versão 1.75b:

  - Melhorar argv_fuzzing para permitir que emita args vazios.
    Wilk.

  - Afl-clang-fast define agora __AFL_HAVE_MANUAL_INIT. Sugerido por Jakub Wilk.

  - Corrigido um erro relacionado com a libtool com o afl-clang- fast que faria com que alguns
    ./configure invocations generate incorrect output. Spotted by Jakub Wilk.

  - Removido flock () no Solaris. Isto significa que não há bloqueio nesta plataforma,
    but so be it. Problem reported by Martin Carpenter.

  - Corrigido um erro de digitação, reportado por Jakub Wilk.

### Versão 1.74b:

  - Adicionado um exemplo argv[] fuzzing wrapper em exemplos/argv_fuzzing.
    Reworked the bash example to be faster, too.

  - Pré-requisitos de modo lvm_clarificado para o FreeBSD.

  - Melhor afl-tmin para usar /tmp se cwd não for escrevêvel.

  - A remoção redundante inclui o sys/fcntl.h, que causou avisos com
    some nitpicky versions of libc.

  - Adicionado um corpus de tags HTML básicas que os analisadores provavelmente prestarão atenção
    to (no attributes).

  - Adicionado EP_ EnabledOnOptLevel0 para llvm_mode, de modo que a instrumentação é
    inserted even when AFL_DONT_OPTIMIZE=1 is set.

  - Alternar o modo qemu_ para usar o recém- lançado QEMU 2.3.0, que contém
    a couple of minor bugfixes.

### Versão 1. 73b:

  - Corrigido um erro bastante estúpido em mapas efetor que às vezes poderia causar
    AFL to fuzz slightly more than necessary; and in very rare circumstances,
    could lead to SEGV if eff_map is aligned with page boundary and followed
    by an unmapped page. Spotted by Jonathan Gray.

### Versão 1.72b:

  - Corrigido uma falha na instalação não-x86, manchado por Tobias Ospelt.

  - Adicionado uma salvaguarda menor para lvm_mode Makefile após um relatório de
    Kai Zhao.

### Versão 1.71b:

  - Corrigido um erro com cópias instaladas da AFL a tentar usar o modo QEMU. Spotted
    by G.M. Lime.

  - Adicionado última pesquisa / falha / tempo de espera para fuzzer_ stats, sugerido por
    Richard Hipp.

  - Corrigi um erro de digitação, graças ao Jakub Wilk.

### Versão 1.70b:

  - Código de retomada modificado para reutilizar o valor de tempo- limite original ao retomar
    a session if -t is not given. This prevents timeout creep in continuous
    fuzzing.

  - Adicionadas mensagens de erro melhoradas para o aperto de mão falhou quando AFL_DEFER_FORKSRV
    is set.

  - Fez uma ligeira melhoria para llvm_mode/Makefile com base no feedback de
    Jakub Wilk.

  - Refrescou vários bits de documentação.

  - Adicionado uma nota mais proeminente sobre os trade-offs do MacOS X para Makefile.

### Versão 1.69b:

  - Adicionado suporte para inicialização diferida no modo LLVM. Sugerido por
    Richard Godbee.

### Versão 1.68b:

  - Corrigido uma falha PRNG menor que faria os primeiros segundos de um fuzzing
    job deterministic. Thanks to Andreas Stieger.

  - Made tmp[] estático no tempo de execução LLVM para manter o Valgrind feliz (isto tinha
    no impact on anything else). Spotted by Richard Godbee.

  - Esclareceu a nota de rodapé em README.

### Versão 1.67b:

  - Fez mais uma correção para llvm_mode Makefile, visto por Jakub Wilk.

### Versão 1.66b:

  - Adicionado suporte CC / CXX para llvm_ mode Makefile. Solicitado por Charlie Eriksen.

  - Corrigido 'fazer limpo' com gmake. Sugerido por Oliver Schneider.

  - Corrigido 'fazer - j n limpar tudo'. Sugerido por Oliver Schneider.

  - Data e hora de compilação removidas dos banners para dar às pessoas determinísticas
    builds. Requested by Jakub Wilk.

### Versão 1.65b:

  - Consertei um snafu com algum código sobrando em afl-clang-rápido.

  - Corrigimos até erros de digitação.

### Versão 1.64b:

  - Mais simplificado afl-clang-fast runtime, revertendo .init_array para
    __attribute__((constructor(0)). This should improve compatibility with
    non-ELF platforms.

  - Corrigido um problema com bibliotecas rápidas e compartilhadas afl-clang. Simplified
    the code by getting rid of .preinit_array and replacing it with a .comm
    object. Problem reported by Charlie Eriksen.

  - Ajuste desnecessário da densidade de instrumentação para o modo LLVM.
    Reported by Jonathan Neuschafer.

### Versão 1.63b:

  - Actualizado cgroups_asan/ com uma nova versão do Sam, fez algumas alterações
    to streamline it and keep parallel AFL instances in separate groups.

  - Erro de digitação, graças ao Jakub Wilk.

### Versão 1.62b:

  - Melhorar o manuseamento de -x em afl-clang-fast,

  - Melhorar o manuseio de configurações AFL_INST_RATIO baixas para QEMU e
    LLVM modes.

  - Corrigido o bug lvm-config para o bem (graças a Tobias Ospelt).

### Versão 1.61b:

  - Corrigido um erro obscuro que compila o OpenSSL com o afl- clang- fast. Patch by
    Laszlo Szekeres.

  - Corrigido um bug 'make install' em sistemas não-x86, graças a Tobias Ospelt.

  - Corrigido um problema com semi- quebrado lvm-config no Odroid, graças a
    Tobias Ospelt. (There is another odd bug there that hasn't been fully
    fixed - TBD).

### Versão 1.60b:

  - Exemplos permitidos/llvm_instrumentação/ para graduar-se em llvm_mode/.

  - Exemplos removidos/arm_support/, já que está completamente quebrado e provável
    unnecessary with LLVM support in place.

  - Adicionado script ASAN cgroups para exemplos/asan_cgroups/, atualizado existente
    docs. Courtesy Sam Hakim and David A. Wheeler.

  - Refactorou afl-tmin para reduzir o número de execs em casos de uso comum.
    Ideas from Jonathan Neuschafer and Turo Lamminen.

  - Acrescentou uma nota sobre CLAs na parte inferior do README.

  - Mudar o nome dos casos_readme.txt para README.testcasos para alguma aparência de
    consistency.

  - Fiz várias actualizações para os documentos.

  - Adicionado MEM_BARRIER() ao afl-showmap e afl-tmin, só para garantir.

### Versão 1.59b:

  - Importação da instrumentação experimental LLVM de Laszlo Szekeres para
    examples/llvm_instrumentation. I'll work on including it in the 
    "mainstream" version soon.

  - Corrigiu outro erro, graças ao Jakub Wilk.

### Versão 1.58b:

  - Adicionado uma solução para o comportamento abortar() em programas -lpthread no modo QEMU.
    Spotted by Aidan Thornton.

  - Foram feitas várias atualizações de documentação, incluindo links para a estática
    instrumentation tool (sister_projects.txt).

### Versão 1. 57b:

  - Corrigido um problema com exceção de manipulação em algumas versões do MacOS X.
    Spotted by Samir Aguiar and Anders Wang Kristensen.

  - Ajustei o afl- gcc para usar o BIN_ PATH em vez de um texto fixo na ajuda
    messages.

### Versão 1.56b:

  - Renomeado related_work.txt para historical_notes.txt.

  - Fez pequenas edições para o doutor da ASAN.

  - Adicionado docs/irmã_projects.txt com uma lista de inspirados ou de perto
    related utilities.

### Versão 1.55b:

  - Corrigido uma falha com abertura do afl- showmap /dev/null com O_RDONLY quando
    running in quiet mode. Spotted by Tyler Nighswander.

### Versão 1.54b:

  - Adicionado outro exemplo pós-processador para PNG.

  - Fez uma correção cosmética para realloc() manipulação em exemplos/post_library/,
    suggested by Jakub Wilk.

  - Melhor manipulação -ldl. Sugerido por Jakub Wilk.

### Versão 1.53b:

  - Corrigido um problema -l encomendando que aparentemente ainda é um problema no Ubuntu.
    Spotted by William Robinet.

### Versão 1.52b:

  - Adicionado suporte para pós-processadores de formato de arquivo. Solicitado por Ben Nagy. This
    feature is intentionally buried, since it's fairly easy to misuse and
    useful only in some scenarios. See examples/post_library/.

### Versão 1. 51b:

  - Tornou possível substituir corretamente LD_BIND_NOW depois de um muito incomum
    report of trouble.

  - Limpaste erros de digitação, graças ao Jakub Wilk.

  - Corrigido um erro em AFL_DUMB_FORKSRV.

### Versão 1.50b:

  - Corrigido um erro flock () que impediria que erros de reuso de dir chutassem
    in every now and then.

  - Referências renomeadas para ppvm (o projeto agora é chamado de reincidivm).

  - Fez melhorias no tratamento do descritor de arquivos para evitar deixar alguns fds
    unnecessarily open in the child process.

  - Corrigido um erro de digitação ou dois.

### Versão 1.49b:

  - Adicionado código para salvar a linha de comando original em fuzzer_stats e
    crashes/README.txt. Also saves fuzzer version in fuzzer_stats.
    Requested by Ben Nagy.

### Versão 1.48b:

  - Corrigido um erro com o servidor de garfos QEMU falha quando a tradução é tentada
    after a jump to an invalid pointer in the child process (i.e., after
    bumping into a particularly nasty security bug in the tested binary).
    Reported by Tyler Nighswander.

### Versão 1.47b:

  - Corrigido um erro com afl-cmin no modo -Q reclamando sobre não ser binário
    instrumented. Thanks to Jonathan Neuschafer for the bug report.

  - Corrigido outro erro com o manuseio do argv para o afl-fuzz no modo - Q. Reportado
    by Jonathan Neuschafer.

  - Melhorou o uso de cores ao mostrar a contagem de falhas no modo -C.

### Versão 1.46b:

  - Melhor desempenho de instrumentação em sistemas de 32 bits ao se livrar de
    xor-swap (oddly enough, xor-swap is still faster on 64-bit) and tweaking
    alignment.

  - Os números de profundidade do caminho foram mais precisos com os casos de teste importados.

### Versão 1.45b:

  - Adicionado suporte para SIMPLE_FILES em config.h para pessoas que não gostam
    descriptive file names. Generates very simple names without colons,
    commas, plus signs, dashes, etc.

  - Arquivos de tamanho zero substituídos por links simbólicos no estado de comportamento da variável
    dir to simplify examining the relevant test cases.

  - Alteração do período de operações de bloqueio de intervalo limitado de 5 para 10 minutos com base
    on a couple of experiments. The basic goal of this delay timer behavior
    is to better support jobs that are seeded with completely invalid files,
    in which case, the first few queue cycles may be completed very quickly
    without discovering new paths. Should have no effect on well-seeded jobs.

  - Fiz várias pequenas atualizações para os documentos.

### Versão 1.44b:

  - Corrigido duas tentativas confusas para obter o modo -C funcionar corretamente
    with afl-cmin (accounting for the short-lived releases tagged 1.42 and
    1.43b) - sorry.

  - Removido AFL_ALLOW_CRASHES em favor do modo -C na referida ferramenta.

  - Despediu-se da Hello Kitty, como solicitado por Padraig Brady.

### Versão 1.41b:

  - Adicionado AFL_ ALLOUW_ CRASHES=1 ao afl- cmin. Permite a quebra de entradas no
    output corpus. Changed the default behavior to disallow it.

  - Tornou a pasta de saída do afl-cmin padrão para 0700, não 0755, para ser consistente
    with afl-fuzz; documented the rationale for 0755 in afl-plot.

  - Reduziu o limite de tempo de reutilização da dir de saída para 25 minutos como um dado-rolo
    compromise after a discussion on afl-users@.

  - Feito afl-showmap aceitar -o /dev/null sem borking para fora.

  - Adicionado suporte para crash / hang info em códigos de saída do afl-showmap.

  - Operação de bloqueio ajustado escalando para também fator no tempo de execução do ballpark
    in cases where queue passes take very little time.

  - Corrigido erros de digitação e fez melhorias em vários documentos.

### Versão 1.40b:

  - Alternado para tamanhos menores de bloco op durante os primeiros passes sobre o
    queue. Helps keep test cases small.

  - Barreira de memória adicionada para run_target(), apenas no caso de compiladores obterem
    smarter than they are today.

  - Atualizei um monte de médicos.

### Versão 1.39b:

  - Adicionado a capacidade de pular entradas enviando SIGUSR1 para o fuzzer.

  - Retrabalhou várias porções da documentação.

  - Alterou o código para repor as pontuações de splicing perf entre as execuções a manter
    them closer to intended length.

  - Redução do valor mínimo de -t para 5 para afl-fuzz (~200 exec/sec)
    and to 10 for auxiliary tools (due to the absence of a fork server).

  - Alternado para timeouts padrão mais agressivos (em torno de até 25 ms
    versus 50 ms - ~40 execs/sec) and made several other cosmetic changes
    to the timeout code.

### Versão 1.38b:

  - Corrigido um bug no script de construção QEMU, visto por William Robinet.

  - Melhorou o relatório de bitflips ignorados para manter os contadores de UI um pouco
    more accurate.

  - Limpei related_work.txt e adicionei alguns não-objetivos.

  - Erro de digitação, graças ao Jakub Wilk.

### Versão 1.37b:

  - Adicionados mapas efetores, que detectam regiões que parecem não responder
    to bitflips and subsequently exclude them from more expensive steps
    (arithmetics, known ints, etc). This should offer significant performance
    improvements with quite a few types of text-based formats, reducing the
    number of deterministic execs by a factor of 2 or so.

  - Limpei o manuseamento de mem limit em afl-cmin.

  - Alternado de uname -i para uname -m para trabalhar em torno Gentoo-específico
    issues with coreutils when building QEMU. Reported by William Robinet.

  - Alternado da verificação PID para flock() para detectar sessões em execução.
    Problem, against all odds, bumped into by Jakub Wilk.

  - Adicionado SKIP_COUNTS e mudou o comportamento de COVERAGE_ONLY em config.h.
    Useful only for internal benchmarking.

  - Fez melhorias nas taxas de atualização da IU e estatísticas exec/sec para torná-las
    more stable.

  - Realizaram melhorias variadas na documentação e na compilação do QEMU
    script.

  - Alternado de perror() para strerror() em macros de erro, graças ao Jakub
    Wilk for the nag.

  - Mudou o Afl-cmin de volta para Bash, não estava a pensar bem.
    on bash because other shells may have restrictive limits on array sizes.

### Versão 1.36b:

  - Mudou o afl-cmin para /bin/sh. Graças ao Jonathan Gray.

  - Corrigido um erro off-by-one na verificação do limite de filas ao retomar as sessões
    (could cause NULL ptr deref if you are *really* unlucky).

  - Corrigido o script QEMU para tolerar i686 se retornado por uname -i. Baseado em
    a problem report from Sebastien Duquette.

  - Adicionado várias referências à ferramenta ppvm de Jakub.

  - Fez várias pequenas melhorias para o Makefile.

  - Acredites ou não, arranjei alguns erros, graças ao Jakub Wilk.

### Versão 1.35b:

  - Limpou expressões regulares em alguns dos scripts para evitar erros
    on *BSD systems. Spotted by Jonathan Gray.

### Versão 1. 34b:

  - Executou uma documentação substancial e limpeza de saída do programa para
    better explain the QEMU feature.

### Versão 1. 33b:

  - Adicionado suporte para AFL_INST_RATIO e AFL_INST_LIBS no modo QEMU.

  - Corrigido um erro de alocação de pilha no modo QEMU (bug in QEMU, corrigido com
    an extra patch applied to the downloaded release).

  - Código adicionado para testar a instrumentação QEMU uma vez o afl-qemu-trace
    binary is built.

  - Modificado afl-tmin e afl- showmap para pesquisar $PATH para binários e para
    better handle QEMU support.

  - Adicionado uma verificação de binários instrumentados ao passar -Q para afl-fuzz.

### Versão 1.32b:

  - Corrigido 'make install' após as alterações do QEMU. Manchado por Hanno Boeck.

  - Manipulação EXTRA_PAR fixa em afl-cmin.

### Versão 1. 31b:

  - Aleluia! Graças a Andrew Griffiths, agora apoiamos muito rápido, caixa preta
    instrumentation of binary-only code. See qemu_mode/README.qemu.

    To use this feature, you need to follow the instructions in that
    directory and then run afl-fuzz with -Q.

### Versão 1.30b:

  - Adicionado -s (síntese) opção para afl-whatsup. Sugerido por Jodie Cunningham.

  - Adicionado uma verificação de sanidade em afl-tmin para detectar minimização a zero len ou
    excess hangs.

  - Contador fixo do tamanho do alfabeto em afl-tmin.

  - Ligeiramente melhorou o manuseio de -B em afl-fuzz.

  - Corrigidas mensagens de falha de processo com - m nenhuma.

### Versão 1.29b:

  - Melhorado o nome dos casos de teste quando orig: já está presente no arquivo
    name.

  - Fez melhorias substanciais no technical_details.txt.

### Versão 1.28b:

  - Fez um pequeno ajuste na instrumentação para preservar a direcionalidade
    of tuples (i.e., A -> B != B -> A) and to maintain the identity of tight
    loops (A -> A). You need to recompile targeted binaries to leverage this.

  - Limpei algumas das estatísticas do afl-whatsup.

  - Acrescentou vários cheques de sanidade à afl-cmin.

### Versão 1.27b:

  - Graças ao Hanno Boeck pela dica.

  - Adicionado docs/technical_details.txt.

  - Mudança da estratégia de pesquisa do afl- showmap no afl- cmap para apenas olhar para o
    same place that afl-cmin is executed from. Thanks to Jakub Wilk.

  - Removeu o current_todo.txt e limpou os documentos restantes.

### Versão 1.26b:

  - Adicionado total execs/sec stat para afl-whatsup.

  - afl- cmin agora seleciona automaticamente entre cp ou ln. Com base no feedback de
    Even Huus.

  - Arranjei um erro de digitação, graças ao Jakub Wilk.

  - Feito afl-gotcpu um pouco mais preciso usando getrusage em vez de
    times. Thanks to Jakub Wilk.

  - Corrigido um problema de limite de memória durante o processo de compilação no NetBSD-current.
    Reported by Thomas Klausner.

### Versão 1.25b:

  - Introduziu o afl- whatsup, uma ferramenta simples para consultar o estado de
    local synced instances of afl-fuzz.

  - Adicionado -x compilador às opções de clang em Darwin. Sugerido por Filipe
    Cabecinhas.

  - Códigos de saída melhorados para afl-gotcpu.

  - Melhorou as verificações dos valores - m e - t no afl- cmin. Bug report
    from Evan Huus.

### Versão 1.24b:

  - Introduzido afl-getcpu, uma ferramenta experimental para medir empiricamente
    CPU preemption rates. Thanks to Jakub Wilk for the idea.

### Versão 1.23b:

  - Reverteu uma mudança para afl-cmin que realmente o tornou mais lento.

### Versão 1.22b:

  - Retrabalhado afl-showmap.c para suportar opções normais, incluindo -o, -q,
    -e. Also added support for timeouts and memory limits.

  - Fez alterações no afl-cmin e outros scripts para acomodar o novo
    semantics.

  - Oficialmente reformado AFL_EDGES_ONly.

  - Corrigi outro erro de digitação em afl-tmin, cortesia de Jakub Wilk.

### Versão 1.21b:

  - Graduado minimum_corpus.sh para afl-cmin. Agora é uma primeira classe
    utility bundled with the fuzzer. 

  - Fez melhorias significativas para afl-cmin para torná-lo mais rápido, mais
    robust, and more versatile.

  - Refatou algum do código afl-tmin para torná-lo um pouco mais legível.

  - Fez diversas alterações no documento para documentar afl-cmin e outras coisas.

### Versão 1.20b:

  - Adicionado AFL_ DUMB_ FORKSRV, conforme solicitado por Jakub Wilk. Isto só funciona
    in -n mode and allows afl-fuzz to run with "dummy" fork servers that
    don't output any instrumentation, but follow the same protocol.

  - Renomeado AFL_SKIP_CHECKS para AFL_SKIP_BIN_CHECK para torná-lo pelo menos
    somewhat descriptive.

  - Mudou para usando clang como o montador padrão no MacOS X para funcionar
    around Xcode issues with newer builds of clang. Testing and patch by
    Nico Weber.

  - Corrigido um erro de digitação (via Jakub Wilk).

### Versão 1.19b:

  - Melhor detecção de falhas exec em afl-fuzz e afl-showmap.

  - Melhor manipulação Ctrl-C no afl-showmap.

  - Adicionado afl-tmin, um minimizer útil habilitado para instrumentação.

### Versão 1.18b:

  - Corrigido um erro sério, mas de curta duração no comportamento de retomada introduzido
    in version 1.16b.

  - Adicionado o modo -t nn+ para caminhos de soft-skipping timing-out.

### Versão 1.17b:

  - Corrigido um aviso compilador introduzido em 1.16b para versões mais recentes do GCC.
    Thanks to Jakub Wilk and Ilfak Guilfanov.

  - Melhorou a consistência de salvar fuzzer_stats, informações de bitmap, e
    auto-dictionaries when aborting fuzzing sessions.

  - Fez várias melhorias de desempenho para aritismo determinístico
    and known int steps.

### Versão 1.16b:

  - Adicionado um pouco de código para fazer a retomada pegar do último conhecido
    offset in the queue, rather than always rewinding to the start. Suggested
    by Jakub Wilk.

  - Alternado para controle de tempo- limite mais apertado para programas lentos (3x ao invés de
    5x average exec speed at init).

### Versão 1.15b:

  - Adicionado suporte para AFL_NO_VAR_CHECK para acelerar a retomada e inibir
    variable path warnings for some programs.

  - O aparador foi executado mesmo para caminhos variáveis, uma vez que não existe nenhum
    harm in doing so and it can be very beneficial if the trimming still
    pans out.

  - Tornou a UI um pouco mais descritiva adicionando "n/a" em vez de "0" em um
    couple of corner cases.

### Versão 1.14b:

  - Adicionado um dicionário (parcial) para JavaScript.

  - Adicionado AFL_NO_CPU_RED, como sugerido por Jakub Wilk.

  - Ajustou a lógica de escala de estragos adicionado em 1.12b.

### Versão 1.13b:

  - Melhorou o desempenho de minimize_corpus.sh com a mudança para um
    sort-based approach.

  - Fez várias revisões menores aos documentos.

### Versão 1.12b:

  - Melhorou a geração de dicionários para evitar corridas idênticas
    bytes.

  - Adicionado escala de ciclo de estragos para ajudar com binários lentos em modo - d. Com base em
    a thread with Sami Liedes.

  - Adicionado AFL_ SYNC_ FIRST para afl- fuzz. Isto é útil para aqueles que obcecam
    over stats, no special purpose otherwise.

  - Mudou para códigos de desenho mais robustos, sugeridos por Jakub Wilk.

  - Criadas mais rápidas variantes de 64 bits de várias funções de bitmap de caminho crítico
    (sorry, no difference on 32 bits).

  - Erro de digitação de moar fixo, conforme relatado por Jakub Wilk.

### Versão 1.11b:

  - Adicionado um pouco mais informações sobre estratégias de dicionário para a tela de status.

### Versão 1.10b:

  - Revisou o comportamento do dicionário para usar a inserção e sobrescrever
    deterministic steps, rather than just the latter. This improves coverage
    with SQL and the like.

  - Adicionado uma menção de "*" no status_screen.txt, como sugerido por Jakub Wilk.

### Versão 1.09b:

  - Corrigido um problema cosmético com "extras" contagem de palco nem sempre sendo
    accurate in the stage yields view.

  - Corrigido um erro de digitação relatado por Jakub Wilk e feito alguma documentação menor
    improvements.

### Versão 1.08b:

  - Corrigido um erro div-by-zero no código recém-adicionado ao usar um dicionário.

### Versão 1.07b:

  - Adicionado código que encontra e extrai automaticamente os tokens de sintaxe do
    input corpus.

  - Corrigido um problema com a opção de remoção ld dead-code no MacOS X, relatado
    by Filipe Cabecinhas.

  - Erros de digitação detectados por Jakub Wilk.

  - Adicionado um par de amostras de formato de arquivo mais exótico.

### Versão 1.06b:

  - Alternado para um relatório ligeiramente mais preciso (se ainda não muito útil)
    of short read and short write errors. These theoretically shouldn't happen
    unless you kill the forkserver or run out of disk space. Suggested by
    Jakub Wilk.

  - Renovou alguns dos códigos de alocador e debug, adicionando comentários e
    cleaning up other mess.

  - Ajustou as chances de fuzzing casos de teste não favoritos para ter certeza de que
    baseline coverage of all inputs is reached sooner.

### Versão 1.05b:

  - Adicionado um dicionário para WebP.

  - Fez algumas melhorias de desempenho adicionais para minimizar_corpus.sh,
    getting deeper into the bash woods.

### Versão 1.04b:

  - Fez melhorias substanciais de desempenho para minimizar_corpus.sh com
    large datasets, albeit at the expense of having to switch back to bash
    (other shells may have limits on array sizes, etc).

  - Ajustei o afl-showmap para suportar o formato usado pelo novo script.

### Versão 1. 03b:

  - Adicionado código para pular README.txt no diretório de entrada para fazer o estoiro
    exploration mode work better. Suggested by Jakub Wilk.

  - Adicionado um dicionário para SQLite.

### Versão 1.02b:

  - Reverter o caminho ./ pesquisa em minimize_corpus.sh porque as pessoas fizeram
    not like it.

  - Adicionaram avisos muito explícitos para não executar vários scripts de shell que
    read or write to /tmp/ (since this is generally a pretty bad idea on
    multi-user systems).

  - Adicionado uma verificação de binários /tmp e -f locais em afl-fuzz.

### Versão 1.01b:

  - Adicionado dicionários para XML e GIF.

### Versão 1.00b:

  - Melhorou ligeiramente o desempenho de minimize_corpus.sh, especialmente sobre
    Linux.

  - Fez algumas melhorias nos timeouts de calibração para varreduras retomadas.

### Versão 0, 99b:

  - Corrigido minimum_corpus.sh para trabalhar com traço, como sugerido por Jakub Wilk.

  - Minimize_corpus.sh modificado para tentar localizar afl-showmap em $PATH e ./.
    The first part requested by Jakub Wilk.

  - Adicionado suporte para o afl-as --version, conforme exigido por uma compilação funky
    script. Reported by William Robinet.

### Versão 0,98b:

  - Adicionado um dicionário para TIFF.

  - Corrigido outro snafu cosmético com fase exec conta para -x.

  - Alternado afl-plot para /bin/sh, uma vez que parece livre de bashismo. Também tentou
    to remove any obvious bashisms from other examples/ scripts,
    most notably including minimize_corpus.sh and triage_crashes.sh.
    Requested by Jonathan Gray.

### Versão 0.97b:

  - Corrigido problemas cosméticos em torno da nomeação de arquivos de estratégia -x.

  - Adicionado um dicionário para JPEG.

  - Corrigido uma falha muito rara ao executar instrumentação 64-bit código que faz
    heavy use of xmm registers that are also touched by glibc.

### Versão 0.96b:

  - Adicionado suporte para dicionários extras, testcases fornecidos/_extras/png/
    as a demo.

  - Corrigido um pequeno erro em rotinas de formatação de números usadas pela UI.

  - Acrescentou vários casos adicionais de teste de PNG que são relativamente improváveis
    to be hit by chance.

  - Corrigido afl-plot sintaxe para gnuplot 5.x. Reportado por David Necas.

### Versão 0, 95b:

  - Limpei o código OSX ReportCrash. Graças a Tobias Ospelt por ajuda.

  - Adicionado algumas dicas extras para AFL_NO_FORKSERVER no OSX.

  - Refrescou o arquivo INSTALL.

### Versão 0.94b:

  - Adicionado currículo no local (-i-) para tratar de uma queixa comum do usuário.

  - Adicionado uma solução terrível para ReportCrash no MacOS X. Problema
    spotted by Joseph Gentle.

### Versão 0.93b:

  - Corrigido a solução link(), conforme relatado por Jakub Wilk.

### Versão 0.92b:

  - Adicionado suporte para leitura de casos de teste de outro sistema de arquivos.
    Requested by Jakub Wilk.

  - Adicionado ponteiros à lista de discussão.

  - Adicionado um documento PDF exemplo.

### Versão 0.91b:

  - Refatored minimize_corpus.sh para torná-lo um pouco mais fácil de usar e para
    select for smallest files, not largest bitmaps. Offers a modest corpus
    size improvement in most cases.

  - Um pouco melhorou o desempenho do código de splicing.

### Versão 0, 90b:

  - Moveu- se para um algoritmo onde os caminhos são marcados como preferencialmente baseados
    on size and speed, rather than bitmap coverage. This should offer
    noticeable performance gains in many use cases.

  - Código de calibração do caminho refatorado; calibração agora ocorre assim que um
    test case is discovered, to facilitate better prioritization decisions later
    on.

  - Mudou a forma de marcar caminhos variáveis para evitar metadados .state
    inconsistencies.

  - Certifique-se de que as rotinas de calibração sempre criem um novo caso de teste para evitar
    hypothetical problems with utilities that modify the input file.

  - Adicionada saturação de bitmap a estatísticas fuzzer e dados de gráfico.

  - Adicionado um caso de teste para JPEG XR.

  - Adicionado uma verificação tty para o aviso de cores no Makefile, para manter a compilação distro
    logs tidy. Suggested by Jakub Wilk.

### Versão 0,89b:

  - Renomeado afl-plot.sh para afl-plot, como solicitado por Padraig Brady.

  - Melhorou a compatibilidade do afl-plot com versões mais antigas do gnuplot.

  - Adicionada informação de banner para fuzzer_stats, povoou-o para afl-plot.

### Versão 0.88b:

  - Adicionado suporte para plotagem, com design e implementação com base em um
    prototype design proposed by Michael Rash. Huge thanks!

  - Adicionado afl-plot.sh, que permite que você, bem, gerar um bom gráfico usando
    this data.

  - Refactorou ligeiramente o código para fazer actualizações mais frequentes no fuzzer_stats
    and to provide more detail about synchronization.

  - Adicionado uma chamada fflush(stdout) para operação não-tty, conforme solicitado por
    Joonas Kuorilehto.

  - Adicionado algum detalhe para fuzzer_stats para paridade com plot_file.

### Versão 0.87b:

  - Adicionado suporte para MSAN, via AFL_USE_MSAN, o mesmo gotchas que para ASAN.

### Versão 0.86b:

  - Adicionado AFL_ NO_ FORKSRV, permitindo que o servidor de fork seja contornado. Sugerido
    by Ryan Govostes.

  - Afl-showmap.c simplificado para fazer uso do modo sem forkserver.

  - Fez pequenas melhorias para crash_triage.sh, como sugerido por Jakub Wilk.

### Versão 0.85b:

  - Corrigido o código de contagem de CPU - sem sysctlbyname () no OpenBSD, d'oh. Bug
    reported by Daniel Dickman.

  - Fez uma ligeira correcção às mensagens de erro - o conselho sobre os testes
    with ulimit was a tiny bit off by a factor of 1024.

### Versão 0. 84b:

  - Adicionado suporte para o widget de CPU em algumas plataformas não-Linux (espero).
    Based on feedback from Ryan Govostes.

  - Limpei o changelog (muito meta).

### Versão 0. 83b:

  - Adicionado exemplos/clang_asm_normalize/ e notas relacionadas em
    env_variables.txt and afl-as.c. Thanks to Ryan Govostes for the idea.

  - Adicionado conselhos sobre a utilização de hardware em README.

### Versão 0.82b:

  - Foram feitas correções adicionais para o suporte ao Xcode, malabarismo -Q e -q flags.
    Ryan Govostes.

  - Adicionado uma verificação para __asm__ blocos e muda para .intel_syntax na montagem.
    Based on feedback from Ryan Govostes.

### Versão 0.81b:

  - Uma solução para o Xcode 6 como falha na bandeira -Q. Encontrado por Ryan Govostes.

  - Instruções de construção da Solaris melhoradas, como sugerido por Martin Carpenter.

  - Consertar um caminho ligeiramente quebrado marcando condicionalmente.

### Versão 0.80b:

  - Adicionado uma verificação para $PATH-induzido loops. Problema notado por Kartik Agaram.

  - Adicionado AFL_KEEP_ASSEMBLY para solução de problemas mais fácil.

  - Adicionado um sobreposição para AFL_USE_ ASAN se definido no tempo de compilação AFL. Solicitado por
    Hanno Boeck.

### Versão 0,79b:

  - Fez pequenos ajustes para a lógica de pulo de caminho.

  - Foram feitas várias atualizações de documentação para refletir as alterações na seleção do caminho
    made in 0.78b.

### Versão 0, 78b:

  - Foi adicionada uma verificação do governador da CPU. Relatório de erros do Joe Zbiciak.

  - Caminhos favoritos agora são selecionados estritamente com base em novas bordas, não atingido
    counts. This speeds up the first pass by a factor of 3-6x without
    significantly impacting ultimate coverage (tested with libgif, libpng,
    libjpeg).

    It also allows some performance & memory usage improvements by making
    some of the in-memory bitmaps much smaller.

  - Fez várias melhorias significativas de desempenho para verificação de bitmap
    functions, plus switched to a faster hash.

  - Devido em grande parte a essas otimizações, bateu o tamanho do bitmap para
    64k and added a warning to detect older binaries that rely on smaller
    bitmaps.

### Versão 0, 77b:

  - Adicionado AFL_SKIP_CHECKS para ignorar as verificações binárias quando realmente justificadas.
    Feature requested by Jakub Wilk.

  - Arranjei uns erros de digitação.

  - Adicionado um aviso para as corridas que são abortadas no início.

### Versão 0, 76b:

  - Incorporou outra correção de manuseio de sinal para Solaris. Sugestão
    submitted by Martin Carpenter.

### Versão 0, 75b:

  - Implementou um kludge ligeiramente mais "elegant" para a falha %llu (ver
    types.h).

  - Avisos de carga de CPU relaxados para permanecer em sincronia com a realidade.

### Versão 0.74b:

  - Mudado para médias de velocidade exec mais responsivas e melhor velocidade de UI
    scaling.

  - Corrigido um erro com leituras interrompidas no Solaris. Problema detectado por Martin
    Carpenter.

### Versão 0.73b:

  - Corrigido um memcpy() perdido em vez de memmove() em buffers sobrepostos.
    Mostly harmless but still dumb. Mistake spotted thanks to David Higgs.

### Versão 0.72b:

  - Tamanho do mapa alterado até 32k. Você pode querer recompilar instrumentado
    binaries (but nothing horrible will happen if you don't).

  - Fez enormes melhorias de desempenho para funções de contagem de bits.

  - As otimizações padrão agora incluem - funroll- loops. Isto deve ter
    interesting effects on the instrumentation. Frankly, I'm just going to
    ship it and see what happens next. I have a good feeling about this.

  - Fez uma correção para falha de alinhamento de pilha no MacOS X 10.10; parece o
    rhetorical question in the comments in afl-as.h has been answered.
    Tracked down by Mudge Zatko.

### Versão 0.71b:

  - Adicionado uma correção para a verificação de ELF não-sensical MacOS.

  - Fiz algumas melhorias nos controlos ASAN.

### Versão 0, 70b:

  - Adicionado detecção explícita de binários ASANified.

  - Questões de compilação fixas em Solaris. Reportado por Martin Carpenter.

### Versão 0.69b:

  - Melhoria da detecção de binários não instrumentados.

  - Tornou o contador de colisão no modo -C preciso.

  - Corrigido um erro obscuro de instalação que tornou o afl- como não- funcional com a ferramenta
    installed to /usr/bin instead of /usr/local/bin. Found by Florian Kiersch.

  - Corrigido para um SIGFPE cosmético quando Ctrl- C é pressionado enquanto o servidor de garfos
    is spinning up.

### Versão 0. 68b:

  - Adicionado modo de exploração de crash! Woot!

### Versão 0.67b:

  - Corrigido vários erros de digitação mais, o projeto agora está totalmente livre de erros.
    Thanks to Thomas Jarosch and Jakub Wilk.

  - Fez uma mudança para escrever fuzzer_stats no início.

  - Corrigido uma falha quando (não!) estiver em execução no MacOS X como raiz.
    Ospelt.

  - Foi possível substituir o O3 em Makefile, sugerido por Jakub Wilk.

### Versão 0.66b:

  - Corrigido um problema muito obscuro com os sistemas de compilação que usam o gcc como montador
    for hand-written .s files; this would confuse afl-as. Affected nss, reported
    by Hanno Boeck.

  - Corrigido um erro ao limpar as pastas de saída sincronizadas do fuzzer. Problema relatado
    by Thomas Jarosch.

### Versão 0.65b:

  - Limpei os códigos de fuga da shell printf em Makefile.

  - Adicionado mais cor ao fuzzer_stats, fornecido documentação curta do arquivo
    format, and made several other stats-related improvements.

### Versão 0.64b:

  - Suporte GCC habilitado no MacOS X.

### Versão 0.63b:

  - Forneceu uma forma nova e simplificada de passar dados em arquivos (@@). Veja README.

  - Fizemos correções adicionais para o MacOS X de 64 bits, trabalhando em torno de um erro de bater
    their linker (umpf) and several other things. It's alive!

  - Adicionado uma pequena solução para um erro no FreeBSD de 64 bits (clang - m32 - g não
    work on that platform, but clang -m32 does, so we no longer insert -g).

  - Adicionado um aviso de tempo de construção para terminais de vídeo inversos e melhor
    instructions in status_screen.txt.

### Versão 0.62b:

  - Fez pequenas melhorias para o alocador, como sugerido por Tobias Ospelt.

  - Adicionado exemplo instrumentado memcmp() em exemplo/instrumentado_cmp.

  - Adicionado uma correção especulativa para MacOS X (detecção de clang, novamente).

  - Erros corrigidos em paralelo_fuzzing.txt. Problemas detectados por Thomas Jarosch.

### Versão 0.61b:

  - Corrigido um problema menor com detecção de clang em sistemas com um clang cc
    wrapper, so that afl-gcc doesn't confuse it with GCC.

  - Fez melhorias cosméticas para documentos e para o indicador de carga da CPU.

  - Corrigido uma falha com remoção de falha (README.txt deixado para trás, d'oh).

### Versão 0.60b:

  - Corrigido problemas com tabelas de salto geradas por versões exóticas do GCC. Isto
    solves an outstanding problem on OpenBSD when using afl-gcc + PIE (not
    present with afl-clang).

  - Permissões fixas em um dos arquivos de amostra.

  - Adicionado uma solução de trabalho lahf / sahf para o OpenBSD (seu montador não sabe
    about these opcodes).

  - Adicionado documentos/INSTALL.

### Versão 0.59b:

  - Modificado 'make install' para também instalar casos de teste.

  - Forneceu melhores ponteiros para instalado README em afl-fuzz.

  - Mais trabalho em RLIMIT_AS para OpenBSD.

### Versão 0.58b:

  - Adicionado uma verificação de contagem de núcleos no Linux.

  - Refinei o código para o caso da falta de RLIMIT_AS no OpenBSD.

  - Adicionado um medidor de utilização de CPU rudimentar para ajudar com o carregamento ideal.

### Versão 0.57b:

  - Corrigições feitas para suportar o FreeBSD e o OpenBSD: use_64bit agora é inferido se não
    explicitly specified when calling afl-as, and RLIMIT_AS is behind an #ifdef.
    Thanks to Fabian Keil and Jonathan Gray for helping troubleshoot this.

  - Modificado 'make install' para também instalar documentos (em /usr/local/share/doc/afl).

  - Corrigido um erro de erro no status_screen.txt.

  - Fez um par de melhorias Makefile como proposto por Jakub Wilk.

### Versão 0.56b:

  - Adicionada redução da densidade de instrumentação probabilística no modo ASAN.
    compensates for ASAN-specific branches in a crude but workable way.

  - Notas atualizadas_for_asan.txt.

### Versão 0.55b:

  - Comportamento out_dir mais inteligente implementado, apagando automaticamente diretórios
    that don't contain anything of special value. Requested by several folks,
    including Hanno Boeck.

  - Adicionado mais detalhes em fuzzer_stats (hora de início, tempo de execução, fuzzer PID).

  - Suporte implementado para prefixos de instalação configuráveis no Makefile
    ($PREFIX), as requested by Luca Barbato.

  - Tornou possível retomar fazendo -i <out_dir>, sem precisar especificar
    -i <out_dir>/queue/.

### Versão 0.54b:

  - Adicionado uma correção para -Wformat mensagens de aviso (oops, eu pensei que tinha sido em
    place for a while).

### Versão 0.53b:

  - Redesenhou o código de detecção duplicado para lidar melhor com
    fault conditions that can be reached in a multitude of ways.

    The old approach could be compared to hashing stack traces to de-dupe
    crashes, a method prone to crash count inflation. The alternative I
    wanted to avoid would be equivalent to just looking at crash %eip,
    which can have false negatives in common functions such as memcpy().

    The middle ground currently used in afl-fuzz can be compared to looking
    at every line item in the stack trace and tagging crashes as unique if
    we see any function name that we haven't seen before (or if something that
    we have *always* seen there suddenly disappears). We do the comparison
    without paying any attention to ordering or hit counts. This can still
    cause some crash inflation early on, but the problem will quickly taper
    off. So, you may get 20 dupes instead of 5,000.
    
  - Adicionado uma correção para razões de corte inofensivas, mas absurdas mostrado se o primeiro exec em
    the trimmer timed out. Spotted by @EspenGx.

### Versão 0.52b:

  - Adicionado um resumo rápido do conteúdo em exemplos/.

  - Fiz uma correção para o processo de escrita fuzzer_stats.

  - Ligeiramente reorganizado o diretório .state/, agora gravando caminhos redundantes,
    too. Note that this breaks the ability to properly resume older sessions 
    - sorry about that.

    (To fix this, simply move <out_dir>/.state/* from an older run
    to <out_dir>/.state/deterministic_done/*.)

### Versão 0.51b:

  - Alterou a ordem de pesquisa para afl-as para evitar o problema com cópias mais antigas
    installed system-wide; this also means that I can remove the Makefile check
    for that.

  - Tornou possível definir a razão de instrumentação de 0%.

  - Introduziu alguns erros de digitação, fixou outros.

  - Corrigido o alvo test_prev em Makefile, como relatado por Ozzy Johnson.

### Versão 0, 50b:

  - Melhorou a lógica de 'make install', como sugerido por Padraig Brady.

  - Renovou vários bits da documentação, especialmente em torno de perf_tips.txt;
    based on the feedback from Alexander Cherepanov.

  - Adicionado AFL_ INST_ RATIO ao afl- as. O único caso em que isto é útil é
    ffmpeg, at least as far as I can tell. (Trivia: the current version of 
    ffmpeg ./configure also ignores CC and --cc, probably unintentionally).

  - Documentação adicionada para todas as variáveis ambientais (env_variables.txt).

  - Implementou um aviso visual para densidade de bitmap excessiva ou insuficiente.

  - Alterou o afl- gcc para adicionar - O3 por padrão; use AFL_ DONT_ OPTIMIZE se não o fizer
    like that. Big speed gain for ffmpeg, so seems like a good idea.

  - Fez uma correção de regressão para afl-as para ignorar etiquetas .LB no modo gcc.

### Versão 0, 49b:

  - Corrigido mais erros de digitação, como encontrado por Jakub Wilk.

  - Adicionado apoio para clang!

  - Alterado AFL_ HARDEN para *not* incluem ASAN por padrão. Use AFL_ USE_ ASAN se
    needed. The reasons for this are in notes_for_asan.txt.

  - Alternado da autodetecção configure para isatty() para manter o afl-as e
    afl-gcc quiet.

  - Melhor processo de instalação para criar corretamente ligações simbólicas, em vez de
    copies of binaries.

### Versão 0, 48b:

  - Melhor afl- fuzz para o conjunto de forças ASAN_ OPTIONS=abort_ on_ error=1. Caso contrário,
    ASAN crashes wouldn't be caught at all. Reported by Hanno Boeck.

  - Melhora a lógica do Makefile mkdir, como sugerido por Hanno Boeck.

  - Melhorada a instrumentação de 64 bits para salvar corretamente os registros r8-r11
    the x86 setup code. The old behavior could cause rare problems running
    *without* instrumentation when the first function called in a particular
    .o file has 5+ parameters. No impact on code running under afl-fuzz or
    afl-showmap. Issue spotted by Padraig Brady.

### Versão 0, 47b:

  - Corrigido outro erro Makefile para compilações paralelas de afl. Problema identificado
    by Richard W. M. Jones.

  - Adicionado suporte para sufixos para -m.

  - Atualizou a documentação e adicionou notas_for_asan.txt. Com base no feedback
    from Hanno Boeck, Ben Laurie, and others.

  - Moveu o projeto para https://lcamtuf.coredump.cx/afl/.

### Versão 0.46b:

  - Limpa as dependências do Makefile para compilações paralelas.
    Richard W. M. Jones.

  - Adicionado suporte para o DESTDIR no Makefile. Mais uma vez sugerido por
    Richard W. M. Jones :-)

  - Removemos todas as coisas do USE_64BIT; agora apenas detectamos automaticamente o modo de compilação.
    As requested by many callers to the show.

  - Corrigidos problemas raros com programas que usam trechos de montagem e
    switch between .code32 and .code64. Addresses a glitch spotted by
    Hanno Boeck with compiling ToT gdb.

### Versão 0, 45b:

  - Implementou um aparador de caso de teste. Resultados em 20-30% de redução de tamanho para muitos
    types of work loads, with very pronounced improvements in path discovery
    speeds.

  - Adicionados avisos melhores para vários problemas com diretórios de entrada.

  - Adicionado um aviso Makefile para cópias mais antigas, baseado em contraintuitive
    behavior observed by Hovik Manucharyan.

  - Adicionado arquivo fuzzer_stats para monitoramento de status. Sugerido por @dronesec.

  - Erros moar fixos, graças a Alexander Cherepanov.

  - Implementou melhores avisos para os requisitos de memória ASAN, com base em chamadas
    from several angry listeners.

  - Alternado para comportamento sadio com stdout não-tty (menos saída gerada,
    no ANSI art).

### Versão 0.44b:

  - Adicionado suporte para AFL_CC e AFL_CXX, baseado em um patch de Ben Laurie.

  - Substituído afl-fuzz -S -D por -M para simplicidade.

  - Adicionado uma verificação para .section .text; falta disto impediu main() de
    getting instrumented for some users. Reported by Tom Ritter.

  - Reorganizar os casos de teste/ pasta.

  - Adicionado uma verificação extra para confirmar que a compilação está operacional.

  - Uso mais consistente de códigos de reset de cores, como sugerido por Oliver
    Kunz.

### Versão 0.43b:

  - Corrigido um bug com 64 bits de relocações compartilhadas por gcc.

  - Echo-e removido do Makefile para compatibilidade com o traço. Sugerido
    by Jakub Wilk.

  - Adicionado status_screen.txt.

  - Adicionado exemplos/canvas_harness.

  - Fiz uma pequena alteração na verificação de Makefile GCC. Sugerido por Hanno Boeck.

### Versão 0.42b:

  - Corrigido um erro com o tratamento da zona vermelha para 64- bits (oops!). Problema relatado por
    Felix Groebert.

  - Suporte ARM horrivelmente experimental implementado em exemplos/arm_support.

  - Fez várias melhorias nas mensagens de erro.

  - Adicionado AFL_QUIET para silenciar afl-gcc e afl-as ao usar build wonky
    systems. Reported by Hanno Boeck.

  - Verificação melhorada para 64-bit compilação, além de várias verificações de sanidade
    in Makefile.

### Versão 0.41b:

  - Corrigido um bug servido fork para processos que chamam execve().

  - Fez pequenas correções de compatibilidade para Makefile, afl-gcc; sugerido por Jakub
    Wilk.

  - Triage_crashes.sh fixo para trabalhar com o novo layout de diretórios de saída.
    Suggested by Jakub Wilk.

  - Realizaram várias melhorias relacionadas com o desempenho do injetado
    instrumentation.

  - Adicionada indicação visual do número de caminhos importados.

  - Corrigido afl-showmap para fazê-lo funcionar bem com nova instrumentação.

  - Foram adicionadas mensagens de erro muito melhores para falhas ao importar casos de teste
    or otherwise calibrating the binary.

### Versão 0, 40b:

  - Adicionado suporte para fuzzing paralelizado. Inspirado por patch anterior
    from Sebastian Roschke.

  - Adicionado um exemplo em exemplos/distributed_fuzzing/.

### Versão 0, 39b:

  - Tela de status redesenhada, agora 90% mais elegante.

  - Adicionado mais verbose e mensagens de fácil utilização para alguns problemas comuns.

  - Modificou o código de retomada para reconstruir a profundidade do caminho.

  - Alterou o código para inibir despejos de núcleo e melhorar a capacidade de detectar
    SEGVs.

  - Adicionado uma verificação para redirecionamento de lixões de núcleo para programas.

  - Fez uma pequena melhoria no manuseio de caminhos variáveis.

  - Fez ajustes de desempenho adicionais para afl-fuzz, principalmente em torno de limites de mem.

  - Adicionado performance_tips.txt.

### Versão 0, 38b:

  - Corrigido um vazamento de fd e +cov erro de rastreamento resultante de alterações em 0,37b.

  - Escalonamento automático implementado para a velocidade de atualização da tela.

  - Adicionado uma indicação visual ao executar em modo não-instrumentado.

### Versão 0, 37b:

  - Adicionado o rastreamento de estado do fuzz para uma retomada mais perfeita do abortado
    fuzzing sessions.

  - Removeu a opção -D, pois já não é necessário.

  - Código de calibração refatorado e relatórios de inicialização melhorados.

  - Intervalos de tempo dinamicamente implementados, para que você não precise
    play with -t except in some very rare cases.

  - Adicionada notificação visual para binários lentos.

  - Melhoria da instrumentação para cobrir explicitamente a outra parte de cada
    branch.

### Versão 0.36b:

  - Suporte ao servidor fork implementado para evitar a sobrecarga do execve(). A
    nearly-verbatim design from Jann Horn; still pending part 2 that would
    also skip initial setup steps (thinking about reliable heuristics now).

  - Adicionado uma verificação para os scripts de shell usados como alvos de fuzz.

  - Adicionado um cheque para trabalhos de fuzz que não parecem estar encontrando nada.

  - Corrigido a forma como o IGNORE_FINDS funciona (foi um pouco quebrado após adicionar o splicing
    and path skip heuristics).

### Versão 0, 35b:

  - Instrumentação de 64 bits devidamente integrada em afl-as.

### Versão 0.34b:

  - Adicionado um novo classificador de contagem de executivos (a teoria de trabalho é que ele recebe
    meaningful coverage with fewer test cases spewed out).

### Versão 0.33b:

  - Mudou para uma nova instrumentação experimental que tenta
    target only arcs, rather than every line. May be fragile, but is a lot
    faster (2x+).

  - Fiz várias outras correções cosméticas e correções de digitação, graças a
    Jakub Wilk.

### Versão 0.32b:

  - Outra tomada na reparação da excepção C++, relatada por Jakub Wilk.

### Versão 0.31b:

  - Fez outra correção para afl-as para resolver um problema potencial com mais novos
    versions of GCC (introduced in 0.28b). Thanks to Jann Horn.

### Versão 0, 30b:

  - Adicionado mais detalhes sobre as operações subjacentes em nomes de arquivos.

### Versão 0.29b:

  - Fez algumas melhorias gerais para operações de blocos.

### Versão 0.28b:

  - Tratamento de exceções C++ corrigido em versões mais recentes do GCC. Problema diagnosticado
    by Eberhard Mattes.

  - Corrigido o manuseio da bandeira de transbordamento. Mais uma vez, graças a
    Eberhard Mattes.

### Versão 0.27b:

  - Adicionada priorização de novos caminhos sobre os já fuzzed.

  - Incluído o ID do caso de teste spliced no nome do arquivo de saída.

  - Corrigido um raro, cosmético nulo ptr deref após Ctrl-C.

  - Refactorou o código para fazer cópias de casos de teste no diretório de saída.

  - Alternado para melhores nomes de arquivos de saída, mantendo o controle do palco e splicing
    sources.

### Versão 0.26b:

  - Armazenamento renovado de casos de teste, - u opção removida,

  - Adicionado um minimizador de esforço incorporado para se livrar de potencialmente redundante
    inputs,

  - Desde que um programa de minimização da contagem de casos de teste em exemplos/,

  - Fez melhorias diversas no diretório e no processamento de arquivos.

  - Corrigido um erro na detecção de tempo- limite.

### Versão 0.25b:

  - Melhoria da instrumentação baseada na contagem.

  - Melhorou a lógica de desduplicação.

  - Prefixos de - cov adicionados para casos de teste.

  - Alternado de readdir() para scandir() + alfasort() para preservar a ordenação de
    test cases.

  - Adicionado uma estratégia de splicing.

  - Fez várias melhorias menores de UI e várias outras correções de bugs.

### Versão 0.24b:

  - Adicionado o nome do programa à tela de status, mais o parâmetro -T para ir com
    it.

### Versão 0.23b:

  - Melhorou a detecção de comportamentos variáveis.

  - Adicionado rastreamento de profundidade do caminho,

  - Melhorou um pouco a UI,

  - Mudada para instrumentação tupla simplificada (baseada em XOR).

### Versão 0.22b:

  - Refactorou o manuseio de bitflips longos e algumas trocas.

  - Consertou o manuseio do tubo de gcc, graças ao repórter anônimo.

### Versão 0.21b (2013-11-12):

  - Lançamento público inicial.

  - Adicionado suporte para o uso de mutadores personalizados múltiplos que podem ser especificados usando
    the environment variable AFL_CUSTOM_MUTATOR_LIBRARY.


---

## Procedência desta tradução

Fonte: [https://github.com/AFLplusplus/AFLplusplus](https://github.com/AFLplusplus/AFLplusplus/blob/d0070729206a80a9af297b2341edd63f68fdac35/docs/Changelog.md). Licença: [AGPL-3.0](../../99-Assets/upstream/aflplusplus/LICENSE.txt). Commit: d0070729206a80a9af297b2341edd63f68fdac35.

O original preservado, a lista de mudanças de apresentação e os hashes constam no manifesto do projeto. Nenhum exemplo desta documentação foi executado automaticamente.
