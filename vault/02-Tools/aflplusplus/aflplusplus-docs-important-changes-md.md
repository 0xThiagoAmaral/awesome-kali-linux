---
title: "aflplusplus — documentação oficial"
type: "official-documentation"
tool: "aflplusplus"
status: "translated-machine"
reviewed: "2026-10-26"
language: "pt-BR"
tags: ["documentation", "tool/aflplusplus"]
cssclasses: ["fieldbook"]
source_url: "https://github.com/AFLplusplus/AFLplusplus/blob/d0070729206a80a9af297b2341edd63f68fdac35/docs/important_changes.md"
source_commit: "d0070729206a80a9af297b2341edd63f68fdac35"
source_sha256: "4293f8c719197eb8c9d574bf4c3f481b559531cac6826620d7750e2158b78f2e"
license_spdx: "AGPL-3.0-or-later"
human_review: "pending"
source_scope: "Repository root README and owned doc/docs/documentation Markdown or RST files; not a claim of full wiki/site coverage"
---

> Tradução automática local para português, ainda sem revisão humana integral. Estrutura e blocos de código preservados; referências externas não significam conteúdo espelhado.

# Important changes in AFL++

Este documento lista mudanças importantes em AFL++, por exemplo, comportamento principal
alterações.

<a id="from-version-300-onwards"></a>
## A partir da versão 3.00 em diante

### AFL++ 4.00

Com o AFL++ 4.00, introduzimos as seguintes alterações de comportamentos anteriores:

- A documentação completa foi reformulada e reestruturada graças a @llzmb
- Um novo formato alvo CMPLOG requer recompilação de alvos CMPLOG para uso com
AFL++ 4.0 em diante
- Melhor nomeação para vários campos na UI

### AFL++ 3.15

Com o AFL++ 3.15, introduzimos as seguintes alterações de comportamentos anteriores:

- afl-cmin e afl- showmap `-Ci` agora descem para subdiretórios como `afl-fuzz`
`-i` faz (mas note que `afl-cmin.bash` não faz)

### AFL++ 3.14

Com o AFL++ 3.14, introduzimos as seguintes alterações de comportamentos anteriores:

- `afl-fuzz`: o determinístico fuzzing não é mais um padrão para o `-M main`
- o afl-cmin/afl-showmap `-i` agora desce para subdiretórios (`afl-cmin.bash`,
no entanto, não)

### AFL++ 3.10

Com o AFL++ 3.10, introduzimos as seguintes alterações de comportamentos anteriores:

- O recurso `+` da opção `-t` agora significa auto-calcular o tempo- limite,
com o valor dado sendo o tempo limite máximo. O significado original de
"tempo limite de skipping em vez de abortar" agora é inerente à opção `-t`.

### AFL++ 3.00

Com AFL++ 3.00, introduzimos alterações que quebram algumas AFL anteriores e AFL++
comportamentos e padrões:

- Não existem mais subdiretórios `llvm_mode` e `gcc_plugin` e existe
apenas um compilador: `afl-cc`. Todos os compiladores anteriores agora simlink para este.
Todo o código fonte de instrumentação está agora na pasta `instrumentation/`.
- O `gcc_plugin` foi substituído por uma nova versão enviada pela AdaCore que
suporta mais recursos. Obrigado!
- O modo QEMU foi atualizado para QEMU 5.1, mas para ser capaz de compilar isto uma corrente
A versão da ferramenta de compilação ninja e as ferramentas de configuração python3 são necessárias.
tem novas opções como instantâneo, instrumentação de bibliotecas compartilhadas específicas,
Além disso QEMU 5.1 suporta mais alvos de CPU para que isso realmente vale a pena
Ele.
- Ao instrumentar alvos, `afl-cc` não substituirá mais otimizações
se algum foi dado. Isto permite que os alvos do fuzzing sejam construídos regularmente, como
debug ou versões de lançamento.
- **afl-fuzz**:
  - Se nem `-M` nem `-S` for especificado, o padrão `-S` é assumido, então mais
    fuzzers can easily be added later
  - A opção de diretório `-i` agora desce em subdiretórios.
    does not fail on crashes and too large files; instead, it skips them and
    uses them for splicing mutations
  - `-m none` é agora o padrão; defina limites de memória (em MB) com, por exemplo, `-m 250`
  - O fuzzing determinístico está agora desactivado por omissão (a menos que use o `-M`) e
    can be enabled with `-D`
  - Um cache de casos de teste agora pode ser realizado e pode ser modificado através da edição
    `config.h` for `TESTCASE_CACHE` or by specifying the environment variable
    `AFL_TESTCACHE_SIZE` (in MB). Good values are between 50–500 (default: 50).
  - As redes `-M` não executam aparamento
- `examples/` foi renomeado para `utils/`
- `libtokencap/`, `libdislocator/` e `qdbi_mode/` foram transferidos para `utils/`
- afl-cmin/afl-cmin.bash procura agora primeiro no `PATH` e último no `AFL_PATH`

---

## Procedência desta tradução

Fonte: [https://github.com/AFLplusplus/AFLplusplus](https://github.com/AFLplusplus/AFLplusplus/blob/d0070729206a80a9af297b2341edd63f68fdac35/docs/important_changes.md). Licença: [AGPL-3.0-or-later](../../99-Assets/upstream/aflplusplus/LICENSE.txt). Commit: d0070729206a80a9af297b2341edd63f68fdac35.

O original preservado, a lista de mudanças de apresentação e os hashes constam no manifesto do projeto. Nenhum exemplo desta documentação foi executado automaticamente.
