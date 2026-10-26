---
title: "aflplusplus — documentação oficial"
type: "official-documentation"
tool: "aflplusplus"
status: "translated-machine"
reviewed: "2026-10-26"
language: "pt-BR"
tags: ["documentation", "tool/aflplusplus"]
cssclasses: ["fieldbook"]
source_url: "https://github.com/AFLplusplus/AFLplusplus/blob/d0070729206a80a9af297b2341edd63f68fdac35/docs/third_party_tools.md"
source_commit: "d0070729206a80a9af297b2341edd63f68fdac35"
source_sha256: "990a648dae247ecf5ae9e8f9af30062ce8257e994330222d7bf0a9c0e958e41b"
license_spdx: "AGPL-3.0-or-later"
human_review: "pending"
source_scope: "Repository root README and owned doc/docs/documentation Markdown or RST files; not a claim of full wiki/site coverage"
---

> Tradução automática local para português, ainda sem revisão humana integral. Estrutura e blocos de código preservados; referências externas não significam conteúdo espelhado.

# Tools that help fuzzing with AFL++

## AFL++ e outras linguagens de desenvolvimento

* [afl-rs](https://github.com/rust-fuzz/afl.rs) - AFL++ para RUST
* [WASM](https://github.com/fgsect/WAFL) - AFL++ para WASM

## Iniciando várias instâncias AFL++ em paralelo com as configurações recomendadas:
* [https://github.com/0xricksanchez/AFL_Runner](https://github.com/0xricksanchez/AFL_Runner)
* [https://github.com/MegaManSec/AFLplusplus-Parallel-Gen](https://github.com/MegaManSec/AFLplusplus-Parallel-Gen)

## Acelerando fuzzing

* [libfiowrapper](https://github.com/marekzmyslowski/libfiowrapper) - se o
function you want to fuzz requires loading a file, this permits using the
memória compartilhada recurso de teste de caso :-) - recomendado.

## Análise da cobertura e da acessibilidade

* [cov-análise](https://github.com/AFLplusplus/cov-analysis) - gera LLVM
relatórios de cobertura de código fonte (HTML/text/JSON) de um AFL++, libFuzzer,
libafl ou honggfuzz corpus, com diffing, análise de estabilidade e entrada por linha
pesquisa. Substitui o `afl-cov`.
* [fuzz-alcanabilidade](https://github.com/AFLplusplus/fuzz-reachability) - estática
análise (C/C++/Rust) das quais funções um arnês pode alcançar. Diz
lacunas de cobertura acionáveis, para além do código morto (alimente o seu relatório para
`cov-analysis --reachability`) e emite arquivos `AFL_LLVM_ALLOWLIST`/`DENYLIST`
instrumentar apenas as partes alcançáveis de um alvo.

## Minimização dos casos de teste

* [afl-pytmin](https://github.com/ilsani/afl-pytmin) - um invólucro para afl-tmin
que tenta acelerar o processo de minimização de um único
usando muitos núcleos de CPU.
* [afl-ddmin-mod](https://github.com/MarkusTeufelberger/afl-ddmin-mod) - a
variação de afl-tmin com base no algoritmo ddmin.
* [semi- vazio](https://github.com/googleprojectzero/halfempty) - é um rápido
utilitário para minimizar casos de teste por Tavis Ormandy baseado na paralelização.

## Execução distribuída

* [disfuzz-afl](https://github.com/MartijnB/disfuzz-afl) - distribuído fuzzing
para a AFL.
* [AFLDFF](https://github.com/quantumvm/AFLDFF) - AFL distribuído fuzzing
quadro.
* [afl-lançamento](https://github.com/bnagy/afl-launch) - uma ferramenta para a execução
de muitas instâncias da AFL.
* [afl-mothership](https://github.com/afl-mothership/afl-mothership)
gerenciamento e execução de muitos fuzzers AFL sincronizados na nuvem AWS.
* [afl-in-the-cloud](https://github.com/abhisek/afl-in-the-cloud) - outro
script para executar AFL em AWS.

## Implantação, gestão, acompanhamento, comunicação de informações

* [afl-utils](https://gitlab.com/rc0r/afl-utils) - um conjunto de utilitários para
processamento/análise automático de falhas e redução do número de ensaios
Casos.
* [afl-other-arch](https://github.com/shellphish/afl-other-arch) - é um conjunto de
patches e scripts para adicionar facilmente suporte para vários não- x86
arquiteturas para AFL.
* [afl-trivia](https://github.com/bnagy/afl-trivia) - alguns pequenos scripts para
simplificar a gestão da AFL.
* [afl- monitor](https://github.com/reflare/afl-monitor) - um script para
monitorização da AFL.
* [afl-manager](https://github.com/zx1340/afl-manager) - um servidor web em Python
para a gestão de multi-afl.
* [afl-remote](https://github.com/block8437/afl-remote) - um servidor web para o
gestão remota de instâncias AFL.
* [afl-extras](https://github.com/fekir/afl-extras) - scripts de shell para
paralelizar afl-tmin, inicialização e coleta de dados.

## Processamento de falhas

* [AFLTriage](https://github.com/quic/AFLTriage)
triagem falhando arquivos de entrada usando o gdb.
* [afl-crash-analisador](https://github.com/floyd-fuh/afl-crash-analyzer)
outro analisador de colisão para a AFL.
* [fuzzer-utils](https://github.com/ThePatrickStar/fuzzer-utils) - um conjunto de
roteiros para a análise dos resultados.
* [atriagem](https://github.com/Ayrx/atriage) - uma ferramenta de triagem simples.
* [afl-kit](https://github.com/kcwu/afl-kit) - afl-cmin em Python.
* [AFLize](https://github.com/d33tah/aflize) - uma ferramenta que automaticamente
gera builds de pacotes debian adequados para AFL.
* [afl-fid](https://github.com/FoRTE-Research/afl-fid) - um conjunto de ferramentas para
trabalhar com dados de entrada.
* [CASR](https://github.com/ispras/casr) - um conjunto de ferramentas para triagem de crash e
análise.


---

## Procedência desta tradução

Fonte: [https://github.com/AFLplusplus/AFLplusplus](https://github.com/AFLplusplus/AFLplusplus/blob/d0070729206a80a9af297b2341edd63f68fdac35/docs/third_party_tools.md). Licença: [AGPL-3.0](../../99-Assets/upstream/aflplusplus/LICENSE.txt). Commit: d0070729206a80a9af297b2341edd63f68fdac35.

O original preservado, a lista de mudanças de apresentação e os hashes constam no manifesto do projeto. Nenhum exemplo desta documentação foi executado automaticamente.
