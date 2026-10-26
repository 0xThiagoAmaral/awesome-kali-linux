---
title: "aflplusplus — comandos essenciais upstream"
type: "cheatsheet"
tool: "aflplusplus"
status: "source-checked"
reviewed: "2026-10-26"
language: "pt-BR"
tags: ["cheatsheet", "tool/aflplusplus"]
cssclasses: ["fieldbook"]
source_commit: "d0070729206a80a9af297b2341edd63f68fdac35"
license_spdx: "AGPL-3.0"
test_status: "not-executed"
source_scope: "Selected exact upstream examples; not full documentation"
---

# aflplusplus — comandos essenciais

Seleção de exemplos da fonte oficial fixada no commit indicado abaixo. Os blocos são transcritos sem alterações; títulos e organização são autorais em português. Esta folha complementa a documentação e não a substitui.

> Exemplos não executados nesta verificação. Caminhos, domínios e arquivos são os exemplos originais upstream. Blocos de sintaxe podem conter marcadores, prompts e argumentos que precisam ser preenchidos antes da execução.

## Navegação

[Documentação offline](aflplusplus-documentacao.md) · [Acervo](../../01-Maps/documentacao-offline.md).

## Compilar com instrumentação

```text
   CC=/path/to/afl-cc CXX=/path/to/afl-c++ ./configure --disable-shared
   make clean all
```

## Iniciar a sessão de fuzzing

```text
   ./afl-fuzz -i seeds_dir -o output_dir -- \
   /path/to/tested/program [...program's cmdline...]
```

## Reproduzir uma entrada que causou falha

```text
   cat output_dir/crashes/id:000000,* | /path/to/tested/program [...program's cmdline...]
```

## Procedência

- [Fonte oficial](https://github.com/AFLplusplus/AFLplusplus/blob/d0070729206a80a9af297b2341edd63f68fdac35/README.md).
- [Licença da fonte: AGPL-3.0](../../99-Assets/upstream/aflplusplus/LICENSE.txt). Os exemplos mantêm essa licença; não são relicenciados como texto autoral.
- Commit: `d0070729206a80a9af297b2341edd63f68fdac35`.
- SHA-256 do documento original: `1e6bc1d9e5870d70052165fe1004345c56743851ad4b930cacc44a744d884866`.
