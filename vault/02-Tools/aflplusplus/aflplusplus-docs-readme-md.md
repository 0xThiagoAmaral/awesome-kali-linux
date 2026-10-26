---
title: "aflplusplus — documentação oficial"
type: "official-documentation"
tool: "aflplusplus"
status: "translated-machine"
reviewed: "2026-10-26"
language: "pt-BR"
tags: ["documentation", "tool/aflplusplus"]
cssclasses: ["fieldbook"]
source_url: "https://github.com/AFLplusplus/AFLplusplus/blob/d0070729206a80a9af297b2341edd63f68fdac35/docs/README.md"
source_commit: "d0070729206a80a9af297b2341edd63f68fdac35"
source_sha256: "ab7474ae77f5168ff21fc851e4c14fb7c752d8baf6564212b8df065cb0af91ee"
license_spdx: "AGPL-3.0-or-later"
human_review: "pending"
source_scope: "Repository root README and owned doc/docs/documentation Markdown or RST files; not a claim of full wiki/site coverage"
---

> Tradução automática local para português, ainda sem revisão humana integral. Estrutura e blocos de código preservados; referências externas não significam conteúdo espelhado.

# AFL++ documentation

Esta é a visão geral do conteúdo do documento AFL++.

Para informações gerais sobre AFL++, consulte
[README.md do repositório](aflplusplus-documentacao.md).

Também dê uma olhada em nosso [FAQ.md](aflplusplus-docs-faq-md.md) e
[best_ practices.md](aflplusplus-docs-best-practices-md.md).

<a id="fuzzing-targets-with-the-source-code-available"></a>
## Alvos fuzzing com o código fonte disponível

Você pode encontrar um start rápido para alvos fuzzing com o código fonte disponível em
[README.md do repositório](aflplusplus-documentacao.md#quick-start-fuzzing-with-afl).

Para informações detalhadas sobre as etapas do processo fuzzing, consulte
[fuzzing_in_profundish.md](aflplusplus-docs-fuzzing-in-depth-md.md) ou clique no seguinte
imagem e selecione um passo.

[Imagem/recurso externo: Fuzzing process overview](https://raw.githubusercontent.com/AFLplusplus/AFLplusplus/dev/docs/resources/0_fuzzing_process_overview.drawio.svg "Fuzzing process overview")

Para mais informações sobre instrumentação, consultar
[READMEs na instrumentação/ pasta](https://github.com/AFLplusplus/AFLplusplus/blob/d0070729206a80a9af297b2341edd63f68fdac35/instrumentation).

<a id="instrumenting-the-target"></a>
### Instrumentação do objectivo

Para mais informações, clique na imagem a seguir e selecione um passo.

[Imagem/recurso externo: Instrumenting the target](https://raw.githubusercontent.com/AFLplusplus/AFLplusplus/dev/docs/resources/1_instrument_target.drawio.svg "Instrumenting the target")

<a id="preparing-the-fuzzing-campaign"></a>
### Preparação da campanha fuzzing

Para mais informações, clique na imagem a seguir e selecione um passo.

[Imagem/recurso externo: Preparing the fuzzing campaign](https://raw.githubusercontent.com/AFLplusplus/AFLplusplus/dev/docs/resources/2_prepare_campaign.drawio.svg "Preparing the fuzzing campaign")

<a id="fuzzing-the-target"></a>
### Fuzzing o alvo

Para mais informações, clique na imagem a seguir e selecione um passo.

[Imagem/recurso externo: Fuzzing the target](https://raw.githubusercontent.com/AFLplusplus/AFLplusplus/dev/docs/resources/3_fuzz_target.drawio.svg "Fuzzing the target")

<a id="managing-the-fuzzing-campaign"></a>
### Gerenciando a campanha fuzzing

Para mais informações, clique na imagem a seguir e selecione um passo.

[Imagem/recurso externo: Managing the fuzzing campaign](https://raw.githubusercontent.com/AFLplusplus/AFLplusplus/dev/docs/resources/4_manage_campaign.drawio.svg "Managing the fuzzing campaign")

<a id="fuzzing-other-targets"></a>
## Fuzzing outros alvos

Para saber mais sobre o fuzzing, consulte:

* Apenas binário: [fuzzing_binary- only_targets. md](aflplusplus-docs-fuzzing-binary-only-targets-md.md)
* Programas GUI:
[best_ practices.md#fuzzing-a-gui-program](aflplusplus-docs-best-practices-md.md#fuzzing-a-gui-program)
* Bibliotecas: [frida_mode/README.md](https://github.com/AFLplusplus/AFLplusplus/blob/d0070729206a80a9af297b2341edd63f68fdac35/frida_mode/README.md)
* Serviços de rede:
[best_ practices.md#fuzzing-a-network-service](aflplusplus-docs-best-practices-md.md#fuzzing-a-network-service)
* Não- linux: [unicórnio_modo/README.md](https://github.com/AFLplusplus/AFLplusplus/blob/d0070729206a80a9af297b2341edd63f68fdac35/unicorn_mode/README.md)

<a id="additional-information"></a>
## Informações adicionais

* Perfil de valor:
[value_profiling.md](aflplusplus-docs-value-profiling-md.md)
* Ferramentas que ajudam fuzzing com AFL++:
[terceir_party_tools.md](aflplusplus-docs-third-party-tools-md.md)
* Tutoriais: [tutoriais. md](aflplusplus-docs-tutorials-md.md)


---

## Procedência desta tradução

Fonte: [https://github.com/AFLplusplus/AFLplusplus](https://github.com/AFLplusplus/AFLplusplus/blob/d0070729206a80a9af297b2341edd63f68fdac35/docs/README.md). Licença: [AGPL-3.0-or-later](../../99-Assets/upstream/aflplusplus/LICENSE.txt). Commit: d0070729206a80a9af297b2341edd63f68fdac35.

O original preservado, a lista de mudanças de apresentação e os hashes constam no manifesto do projeto. Nenhum exemplo desta documentação foi executado automaticamente.
