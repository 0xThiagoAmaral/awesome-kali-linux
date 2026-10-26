---
title: "aflplusplus — documentação oficial"
type: "official-documentation"
tool: "aflplusplus"
status: "translated-machine"
reviewed: "2026-10-26"
language: "pt-BR"
tags: ["documentation", "tool/aflplusplus"]
cssclasses: ["fieldbook"]
source_url: "https://github.com/AFLplusplus/AFLplusplus/blob/d0070729206a80a9af297b2341edd63f68fdac35/README.md"
source_commit: "d0070729206a80a9af297b2341edd63f68fdac35"
source_sha256: "1e6bc1d9e5870d70052165fe1004345c56743851ad4b930cacc44a744d884866"
license_spdx: "AGPL-3.0"
human_review: "pending"
source_scope: "Repository root README and owned doc/docs/documentation Markdown or RST files; not a claim of full wiki/site coverage"
---

> Tradução automática local para português, ainda sem revisão humana integral. Estrutura e blocos de código preservados; referências externas não significam conteúdo espelhado.

# American Fuzzy Lop plus plus (AFL++)



Versão de lançamento: [5.03c](https://github.com/AFLplusplus/AFLplusplus/releases)

Versão GitHub: 5.04a

Repositório:
[https://github.com/AFLplusplus/AFLplusplus](https://github.com/AFLplusplus/AFLplusplus)

O AFL++ é mantido por:

* Marc "van Hauser" Heuse <mh@mh-sec.de>
* Dominik Maier <mail@dmnk.co>
* Andrea Fioraldi <andreafioraldi@gmail.com>
* Heiko "hexcoder-" Eissfeldt <heiko.eissfeldt@hexco.de>
* o modo_frida é mantido por @Worksbutnottested

Originalmente desenvolvido por Michal "lcamtuf" Zalewski.

AFL++ é um garfo superior à AFL do Google - mais velocidade, mais e melhor
mutações, mais e melhor instrumentação, suporte de módulo personalizado, etc.

AFL++ está licenciada sob o **AGPL-3.0-ou-later**, e também contém arquivos sob a Licença Apache-2.0.
**Tudo compilado em um arnês fuzzing é e vai permanecer Apache 2.0 licenciado.**
Cada arquivo declara sua própria licença em seu cabeçalho `SPDX-License-Identifier` — que
é a licença que você deve seguir para esse arquivo.
Uma licença comercial opcional **Z** está disponível para organizações que
não pode utilizar a AGPL (obtida através da doação a uma boa causa — o projecto e a sua
os mantenedores não recebem dinheiro).
Ver [LICENÇAS. md](https://github.com/AFLplusplus/AFLplusplus/blob/d0070729206a80a9af297b2341edd63f68fdac35/LICENSING.md) para uma visão geral em linguagem simples e
[Seção de licença](#licença) abaixo para obter detalhes.

<a id="getting-started"></a>
## Começar

Aqui está alguma informação para você começar:

* Para uma visão geral da documentação AFL++ e um guia gráfico muito útil,
por favor visite [docs/README.md](aflplusplus-docs-readme-md.md).
* Para começar com tutoriais, vá para
[docs/tutorials.md](aflplusplus-docs-tutorials-md.md).
* Para lançamentos, ver o
[Página de versões](https://github.com/AFLplusplus/AFLplusplus/releases) e
[ramos](#ramos). Os melhores ramos a usar são, no entanto, `stable` ou
`dev` - dependendo do seu apetite de risco. Também dê uma olhada na lista de
[mudanças importantes em AFL++](aflplusplus-docs-important-changes-md.md) e a lista de
[funcionalidades](aflplusplus-docs-features-md.md).
* Se você quiser usar AFL++ para seu trabalho acadêmico, confira
[papers page](https://aflplus.plus/papers/) no site.
* Para citar nosso trabalho, veja a seção [Cite](#cite).
* Para comparações, use a configuração do fuzzbench `aflplusplus`, ou use
`afl-clang-fast` com `AFL_LLVM_CMPLOG=1`. Você pode encontrar o `aflplusplus`
configuração padrão no Google
[fuzzbench](https://github.com/google/fuzzbench/tree/master/fuzzers/aflplusplus).

<a id="building-and-installing-afl"></a>
## Construindo e instalando AFL++

Para ter AFL++ facilmente disponível com tudo compilado, puxe a imagem diretamente
a partir do Docker Hub (disponível tanto para x86_64 e arm64):

```shell
docker pull aflplusplus/aflplusplus
docker run -ti -v /location/of/your/target:/src aflplusplus/aflplusplus
```

Esta imagem é publicada automaticamente quando acontece um push para o ramo estável
(veja [ramos](#ramos)). Se você usar o comando acima, você encontrará o seu
código-fonte alvo em `/src` no recipiente.

Nota: você também pode puxar `aflplusplus/aflplusplus:dev` que é o mais atual
estado de desenvolvimento de AFL++.

Para construir AFL++ - *que recomendamos* - continue em
[docs/INSTALL.md](aflplusplus-docs-install-md.md).

<a id="quick-start-fuzzing-with-afl"></a>
## Início rápido: Fuzzing com AFL++

*NOTE: Antes de começar, leia sobre o
[riscos de senso comum de fuzzing](aflplusplus-docs-fuzzing-in-depth-md.md#0-common-sense-risks).*

Este é um começo rápido para alvos fuzzing com o código fonte disponível. Para
ler sobre o processo em detalhe, ver
[docs/fuzzing_in_profund.md](aflplusplus-docs-fuzzing-in-depth-md.md).

Para saber mais sobre o fuzzing, consulte:
* Alvos apenas binários:
[docs/fuzzing_binary-only_targets.md](aflplusplus-docs-fuzzing-binary-only-targets-md.md)
* Serviços de rede:
[docs/best_ practices.md#fuzzing-a-network-service](aflplusplus-docs-best-practices-md.md#fuzzing-a-network-service)
* Programas GUI:
[docs/best_ practices.md#fuzzing-a-gui-program](aflplusplus-docs-best-practices-md.md#fuzzing-a-gui-program)

Início rápido passo a passo:

1. Compilar o programa ou biblioteca a ser fuzzed usando `afl-cc`. Uma maneira comum de
fazer isto seria:

   ```text
   CC=/path/to/afl-cc CXX=/path/to/afl-c++ ./configure --disable-shared
   make clean all
   ```

2. Obter um arquivo de entrada pequeno mas válido que faça sentido para o programa. Quando
fuzzing verbose sintaxe (SQL, HTTP, etc.), criar um dicionário como descrito em
[dicionários/REDME.md](https://github.com/AFLplusplus/AFLplusplus/blob/d0070729206a80a9af297b2341edd63f68fdac35/dictionaries/README.md), também.

3. Se o programa ler do stdin, execute o `afl-fuzz` assim:

   ```text
   ./afl-fuzz -i seeds_dir -o output_dir -- \
   /path/to/tested/program [...program's cmdline...]
   ```

Para adicionar um dicionário, adicione `-x /path/to/dictionary.txt` ao afl-fuzz.

Se o programa recebe entrada de um arquivo, você pode colocar `@@` no programa
linha de comando; O AFL++ irá colocar um nome de arquivo gerado automaticamente para você.

4. Investigue qualquer coisa mostrada em vermelho no fuzzer UI, consultando prontamente
[docs/afl-fuzz_approach.md# compreending-the-status-screen](aflplusplus-docs-afl-fuzz-approach-md.md#understanding-the-status-screen).

5. Você encontrará falhas encontradas e travas nos subdiretórios `crashes/` e
`hangs/` na pasta `-o output_dir`. Você pode reproduzir as falhas por
alimentando-os para o alvo, por exemplo, se o seu alvo estiver a utilizar stdin:

   ```text
   cat output_dir/crashes/id:000000,* | /path/to/tested/program [...program's cmdline...]
   ```

Você pode gerar núcleos ou usar o gdb diretamente para acompanhar as falhas.

6. Para análise de cobertura do seu fuzzing recomendamos nossas ferramentas de parceiros
[cov-análise](https://github.com/AFLplusplus/cov-analysis) (baseado na fonte
relatórios de cobertura de um corpus fuzzing) e
[fuzz-alcanabilidade](https://github.com/AFLplusplus/fuzz-reachability) (estático
análise de quais funções um arnês pode alcançar, para dizer cobertura acionável
lacunas para além do código morto e para gerar listas de autorização de instrumentação)

7. Não podemos sublinhar isto o suficiente - se você quiser fuzz eficazmente, leia o
Documento [docs/fuzzing_in_profund.md](aflplusplus-docs-fuzzing-in-depth-md.md)!

<a id="contact"></a>
## Contacto

Perguntas, preocupações, relatórios de insectos?

* Os contribuidores podem ser alcançados via (por exemplo, criando um problema - mas apenas para defeitos de AFL++!):
[https://github.com/AFLplusplus/AFLplusplus](https://github.com/AFLplusplus/AFLplusplus).
* Dê uma olhada no nosso [Perguntas Frequentes](aflplusplus-docs-faq-md.md) e [Melhores Práticas](aflplusplus-docs-best-practices-md.md).
* **Melhor: junte-se ao [Servidor Zulip fuzzing](https://fuzz.zulipchat.com/)!**

<a id="branches"></a>
## Ramos

Existem os seguintes ramos:

* [lançamento](https://github.com/AFLplusplus/AFLplusplus/tree/release): o mais recente
lançamento
* [estável](https://github.com/AFLplusplus/AFLplusplus/): estado estável de
AFL++ - é sincronizado do dev de vez em quando quando estamos satisfeitos com o seu
estabilidade. Este é o ramo padrão.
* [dev](https://github.com/AFLplusplus/AFLplusplus/tree/dev): estado de desenvolvimento
de AFL++ - borda sangrando e você pode pegar um checkout que não compila
ou tem um erro. **Somente aceitamos PRs (pedidos de execução) para o ramo 'dev'!**
* (qualquer outra): ramos experimentais para trabalhar em características específicas ou testar novos
funcionalidade ou alterações.

<a id="help-wanted"></a>
## Ajuda desejada

Vejam o nosso [lista de problemas com a tag "ajuda desejada"](https://github.com/AFLplusplus/AFLplusplus/issues?q=is%3Aissue%20state%3Aopen%20label%3A%22help%20wanted%22).
Esta pode ser a sua maneira de suportar e contribuir para AFL++ - estendê-lo para fazer
algo legal. Se você tem outras idéias - apenas crie um problema e proponha-o!

Para todos que querem contribuir (e enviar pedidos de pull), por favor leia o nosso
[Orientações para as contribuições](https://github.com/AFLplusplus/AFLplusplus/blob/d0070729206a80a9af297b2341edd63f68fdac35/CONTRIBUTING.md) antes de enviar.

<a id="special-thanks"></a>
## Obrigado especiais.

Muitas das melhorias para a AFL original e AFL++ não seria possível
sem feedback, relatórios de erros ou patches de nossos colaboradores.

Obrigado! (Para pessoas enviando pedidos de pull - por favor, adicione-se a esta lista
:-)

<details>

<summary>Lista dos contribuintes</summary>

  ```text
    Jann Horn                             Hanno Boeck
    Felix Groebert                        Jakub Wilk
    Richard W. M. Jones                   Alexander Cherepanov
    Tom Ritter                            Hovik Manucharyan
    Sebastian Roschke                     Eberhard Mattes
    Padraig Brady                         Ben Laurie
    @dronesec                             Luca Barbato
    Tobias Ospelt                         Thomas Jarosch
    Martin Carpenter                      Mudge Zatko
    Joe Zbiciak                           Ryan Govostes
    Michael Rash                          William Robinet
    Jonathan Gray                         Filipe Cabecinhas
    Nico Weber                            Jodie Cunningham
    Andrew Griffiths                      Parker Thompson
    Jonathan Neuschaefer                  Tyler Nighswander
    Ben Nagy                              Samir Aguiar
    Aidan Thornton                        Aleksandar Nikolich
    Sam Hakim                             Laszlo Szekeres
    David A. Wheeler                      Turo Lamminen
    Andreas Stieger                       Richard Godbee
    Louis Dassy                           teor2345
    Alex Moneger                          Dmitry Vyukov
    Keegan McAllister                     Kostya Serebryany
    Richo Healey                          Martijn Bogaard
    rc0r                                  Jonathan Foote
    Christian Holler                      Dominique Pelle
    Jacek Wielemborek                     Leo Barnes
    Jeremy Barnes                         Jeff Trull
    Guillaume Endignoux                   ilovezfs
    Daniel Godas-Lopez                    Franjo Ivancic
    Austin Seipp                          Daniel Komaromy
    Daniel Binderman                      Jonathan Metzman
    Vegard Nossum                         Jan Kneschke
    Kurt Roeckx                           Marcel Boehme
    Van-Thuan Pham                        Abhik Roychoudhury
    Joshua J. Drake                       Toby Hutton
    Rene Freingruber                      Sergey Davidoff
    Sami Liedes                           Craig Young
    Andrzej Jackowski                     Daniel Hodson
    Nathan Voss                           Dominik Maier
    Andrea Biondo                         Vincent Le Garrec
    Khaled Yakdan                         Kuang-che Wu
    Josephine Calliotte                   Konrad Welc
    Thomas Rooijakkers                    David Carlier
    Ruben ten Hove                        Joey Jiao
    fuzzah                                @intrigus-lgtm
    Yaakov Saxon                          Sergej Schumilo
    Ziqiao Kong                           Ryan Berger
    Sangjun Park                          Scott Guest
    Fabian Keil                           @Jay-1409
    Gergely Nagy
  ```

</details>

## Cite

Se você usar AFL++ em trabalhos científicos, considere citar
[o nosso trabalho](https://www.usenix.org/conference/woot20/presentation/fioraldi)
apresentado em WOOT'20:

    Andrea Fioraldi, Dominik Maier, Heiko Eißfeldt, and Marc Heuse. “AFL++: Combining incremental steps of fuzzing research”. In 14th USENIX Workshop on Offensive Technologies (WOOT 20). USENIX Association, Aug. 2020.

<details>

<summary>BibTeX</summary>

  ```bibtex
  @inproceedings {AFLplusplus-Woot20,
  author = {Andrea Fioraldi and Dominik Maier and Heiko Ei{\ss}feldt and Marc Heuse},
  title = {{AFL++}: Combining Incremental Steps of Fuzzing Research},
  booktitle = {14th {USENIX} Workshop on Offensive Technologies ({WOOT} 20)},
  year = {2020},
  publisher = {{USENIX} Association},
  month = aug,
  }
  ```

</details>

Para comparações, use a configuração do fuzzbench `aflplusplus`, ou use pelo menos `afl-clang-fast` com `AFL_LLVM_CMPLOG=1`.
Você pode encontrar a configuração padrão AFL++ no [fuzzbench](https://github.com/google/fuzzbench/tree/master/fuzzers/aflplusplus) do Google.

[zread](https://zread.ai/AFLplusplus/AFLplusplus)
[Ask DeepWiki](https://deepwiki.com/AFLplusplus/AFLplusplus)

<a id="license"></a>
## Licença

AFL++ está licenciada sob a licença **GNU AGPL-3.0-ou-later**. Em suma, você pode usar
AFL++ três maneiras:

1. **Free, sob o AGPL-3.0-ou-later**: o padrão. Use, modifique e compartilhe
AFL++; se você executar uma versão modificada como um serviço de rede, a AGPL requer
você para oferecer aos seus usuários a fonte correspondente. Texto completo: [LICENÇA](../../99-Assets/upstream/aflplusplus/LICENSE.txt).

2. **Per arquivo, sob a licença em seu header**: o projeto contém arquivos
em `SPDX-License-Identifier: AGPL-3.0-or-later` e
`SPDX-License-Identifier: Apache-2.0`. Verifique sempre o cabeçalho do arquivo que você
usar e aderir à licença indicada lá; os arquivos marcados Apache-2.0 podem ser
reutilizado individualmente sob o [Licença Apache- 2.0](../../99-Assets/upstream/aflplusplus/LICENSE.txt). (Alguns
arquivos de terceiros empacotados carregam outras licenças, por exemplo, o plugin GCC sob
GPL-3.0-ou-posterior e o LLVM SanitizerCoverage passa por baixo
Apache-2.0-WITH-LLVM-exception — cada um marcado pelo seu próprio identificador SPDX.)
que o binário combinado `afl-fuzz` inclui arquivos AGPL, de modo que o programa como um
Todo é AGPL.

3. **Licença comercial**: * opcional*, para organizações que não podem ou não podem
quer cumprir com a AGPL. **O projeto não recebe dinheiro.** Em vez disso, você
Doar **EUR 20.000** (20.000 €) para **
[EFF](https://www.eff.org/) ou o [CCC](https://www.ccc.de/)** e e-mail
prova para **afl@aflplus.plus**; sua licença é então eficaz a partir do
data de doação para o ano **one** (renovável doando novamente). Termos completos:
[LICENÇA.COMERCIAL](../../99-Assets/upstream/aflplusplus/LICENSE.txt).

Componentes de terceiros agrupados (por exemplo, xxHash, t1ha, libFuzzer, submódulos) manter
suas próprias licenças. Para uma visão geral completa em linguagem simples, consulte
[LICENÇAS. md](https://github.com/AFLplusplus/AFLplusplus/blob/d0070729206a80a9af297b2341edd63f68fdac35/LICENSING.md).


---

## Procedência desta tradução

Fonte: [https://github.com/AFLplusplus/AFLplusplus](https://github.com/AFLplusplus/AFLplusplus/blob/d0070729206a80a9af297b2341edd63f68fdac35/README.md). Licença: [AGPL-3.0](../../99-Assets/upstream/aflplusplus/LICENSE.txt). Commit: d0070729206a80a9af297b2341edd63f68fdac35.

O original preservado, a lista de mudanças de apresentação e os hashes constam no manifesto do projeto. Nenhum exemplo desta documentação foi executado automaticamente.
