---
title: "aflplusplus — documentação oficial"
type: "official-documentation"
tool: "aflplusplus"
status: "translated-machine"
reviewed: "2026-10-26"
language: "pt-BR"
tags: ["documentation", "tool/aflplusplus"]
cssclasses: ["fieldbook"]
source_url: "https://github.com/AFLplusplus/AFLplusplus/blob/d0070729206a80a9af297b2341edd63f68fdac35/docs/tutorials.md"
source_commit: "d0070729206a80a9af297b2341edd63f68fdac35"
source_sha256: "6fed8eb785b45b37bf433fee65c39261465be61a9417632098a672abbb2da972"
license_spdx: "AGPL-3.0-or-later"
human_review: "pending"
source_scope: "Repository root README and owned doc/docs/documentation Markdown or RST files; not a claim of full wiki/site coverage"
---

> Tradução automática local para português, ainda sem revisão humana integral. Estrutura e blocos de código preservados; referências externas não significam conteúdo espelhado.

# Tutorials

Se você é um novato total, tente este guia:

* [https://github.com/alex-maleno/Fuzzing-Module](https://github.com/alex-maleno/Fuzzing-Module)

Aqui estão alguns bons write-ups para mostrar como usar efetivamente AFL++:

* [https://aflplus.plus/docs/tutorials/libxml2_tutorial/](https://aflplus.plus/docs/tutorials/libxml2_tutorial/)
* [https://bananamafia.dev/post/gb-fuzz/](https://bananamafia.dev/post/gb-fuzz/)
* [https://bushido-sec.com/index.php/2023/06/19/the-art-of-fuzzing/](https://bushido-sec.com/index.php/2023/06/19/the-art-of-fuzzing/)
* [https://securitylab.github.com/research/fuzzing-challenges-solutions-1](https://securitylab.github.com/research/fuzzing-challenges-solutions-1)
* [https://securitylab.github.com/research/fuzzing-software-2](https://securitylab.github.com/research/fuzzing-software-2)
* [https://securitylab.github.com/research/fuzzing-sockets-FTP](https://securitylab.github.com/research/fuzzing-sockets-FTP)
* [https://securitylab.github.com/research/fuzzing-sockets-FreeRDP](https://securitylab.github.com/research/fuzzing-sockets-FreeRDP)
* [https://securitylab.github.com/research/fuzzing-apache-1](https://securitylab.github.com/research/fuzzing-apache-1)
* [https://mmmds.pl/fuzzing-map-parser-part-1-teeworlds/](https://mmmds.pl/fuzzing-map-parser-part-1-teeworlds/)
* [https://srlabs.de/blog/unlocking-secrets-effective-fuzzing-harness](https://srlabs.de/blog/unlocking-secrets-effective-fuzzing-harness)
* [https://srlabs.de/blog/coverage-analysis](https://srlabs.de/blog/coverage-analysis)

Se você não quiser seguir um tutorial, mas tente um tipo de exercício
formação, então podemos altamente recomendar o seguinte:

* [https://github.com/antonio-morales/Fuzzing101](https://github.com/antonio-morales/Fuzzing101)

Uma boa visão geral do fluxo de trabalho (como o nosso [fuzzing_in_profundish.md](aflplusplus-docs-fuzzing-in-depth-md.md)):
* [https://appsec.guide/docs/fuzzing/c-cpp/aflpp/](https://appsec.guide/docs/fuzzing/c-cpp/aflpp/)

Aqui está uma boa descrição do fluxo de trabalho (e tutorial) para qemu_mode:

* [https://airbus-seclab.github.io/AFLplusplus-blogpost/](https://airbus-seclab.github.io/AFLplusplus-blogpost/)

Aqui está uma boa descrição do fluxo de trabalho para o modo_ frida:

* [https://blog.quarkslab.com/android-greybox-fuzzing-with-afl-frida-mode.html](https://blog.quarkslab.com/android-greybox-fuzzing-with-afl-frida-mode.html)

Se você está interessado em dados estruturados fuzzing (onde você define o que o
estrutura é), estes links têm você coberto (alguns estão desatualizados though):

* libprotobuf para AFL++:
[https://github.com/P1umer/AFLplusplus-protobuf-mutator](https://github.com/P1umer/AFLplusplus-protobuf-mutator)
* libprotobuf em bruto:
[https://github.com/bruce30262/libprotobuf-mutator_fuzzing_learning/tree/master/4_libprotobuf_aflpp_custom_mutator](https://github.com/bruce30262/libprotobuf-mutator_fuzzing_learning/tree/master/4_libprotobuf_aflpp_custom_mutator)
* libprotobuf para o antigo AFL++ API:
[https://github.com/thebabush/afl-libprotobuf-mutator](https://github.com/thebabush/afl-libprotobuf-mutator)
* Superion para AFL++:
[https://github.com/adrian-rt/superion-mutator](https://github.com/adrian-rt/superion-mutator)

Para uma explicação muito aprofundada sobre como funciona o AFL++, confira:
[https://blog.ritsec.club/posts/afl-under-hood/](https://blog.ritsec.club/posts/afl-under-hood/)

<a id="video-tutorials"></a>
## Tutoriais de Vídeo

* [Instalar o Ubuntu AFL++](https://www.youtube.com/watch?v=5dCvhkbi3RA)
* [[Fuzzing with AFLplusplus] Instalando AFLPlusplus e fuzzing um programa C simples] (https://www.youtube.com/watch?v=9wRVo0kYSlc)
* [[Fuzzing with AFLplusplus] Como fuzz um binário sem código fonte no Linux em modo persistente](https://www.youtube.com/watch?v=LGPJdEO02p4)
* [Blackbox Fuzzing # 1: Iniciar apenas o Fuzzing Binário usando o modo QEMU AFL++](https://www.youtube.com/watch?v=sjLFf9q2NRc)
* [ESPERANÇA 2020 (2020): Caçando insetos em seu sono - Como Fuzz (Quase) Qualquer coisa com AFL/AFL++](https://www.youtube.com/watch?v=A8ex1hqaQ7E)
* [Como Fuzzing com AFL funciona!](https://www.youtube.com/watch?v=COHUWuLTbdk)
* [WOOT '20 - AFL++ : Combinando os Passos Incrementais da Pesquisa Fuzzing](https://www.youtube.com/watch?v=cZidm6I7KWU)

Se você encontrar outros bons, por favor, envie-os para nós :-)


---

## Procedência desta tradução

Fonte: [https://github.com/AFLplusplus/AFLplusplus](https://github.com/AFLplusplus/AFLplusplus/blob/d0070729206a80a9af297b2341edd63f68fdac35/docs/tutorials.md). Licença: [AGPL-3.0-or-later](../../99-Assets/upstream/aflplusplus/LICENSE.txt). Commit: d0070729206a80a9af297b2341edd63f68fdac35.

O original preservado, a lista de mudanças de apresentação e os hashes constam no manifesto do projeto. Nenhum exemplo desta documentação foi executado automaticamente.
