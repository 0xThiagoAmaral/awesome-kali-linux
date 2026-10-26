---
title: "aflplusplus — documentação oficial"
type: "official-documentation"
tool: "aflplusplus"
status: "translated-machine"
reviewed: "2026-10-26"
language: "pt-BR"
tags: ["documentation", "tool/aflplusplus"]
cssclasses: ["fieldbook"]
source_url: "https://github.com/AFLplusplus/AFLplusplus/blob/d0070729206a80a9af297b2341edd63f68fdac35/docs/features.md"
source_commit: "d0070729206a80a9af297b2341edd63f68fdac35"
source_sha256: "782c30afb7b85e7a3ad9b51e3ef277bc2202b7d268d1570243d1377e2d3b8ae0"
license_spdx: "AGPL-3.0-or-later"
human_review: "pending"
source_scope: "Repository root README and owned doc/docs/documentation Markdown or RST files; not a claim of full wiki/site coverage"
---

> Tradução automática local para português, ainda sem revisão humana integral. Estrutura e blocos de código preservados; referências externas não significam conteúdo espelhado.

# Important features of AFL++

O AFL++ suporta o lvm do 3.8 até à versão 12, o fuzzing binário muito rápido com
QEMU 5.1 com laf-intel e Redqueen, modo FRIDA, modo unicórnio, plugin gcc, completo
*BSD, Mac OS, Solaris e suporte Android e muito, muito, muito mais.

## Características e instrumentação

Note-se que o afl-gcc e o afl-clang foram removidos porque sua instrumentação está absolutamente desatualizada.

|Característica/Instrumentação|lvm|gcc_plugin|Modo FRIDA(9)|Modo QEMU(10)|unicórnio_ modo(10)|nyx_mode(12)|coresight_mode(11)|
| ------------------------------|:---------:|:----------:|:--------------:|:----------------:|:----------------:|:------------:|:------------------:|
|Contadores de segurança de thread [A]|x(3)|||||x||
|NeverZero [B]|x(1)|x|x|x|x|||
|Modo persistente [C]|x|x|x86[_64]/arm64|x86[_64]/braço[64]|x|||
|LAF-Intel / CompCov [D]|x|||x86[_64]/braço[64]|x86[_64]/braço[64]|x86[_64]||
|CmpLog [E]|x|x|x86[_64]/arm64|x86[_64]/braço[64]|x86[_64]/braço[64]|||
|Instrumentação Seletiva [F]|x|x|x|x||||
|Cobertura não-colaborante [G]|x(4)|||(x)(5)||||
|Cobertura de Contexto [I]|x(6)|||||||
|Dicionário Automático [J]|x(7)|||||||
|Suporte a instantâneos [K]|(x)(8)|(x)(8)||(x)(5)||x||
|Casos de teste de memória partilhada [L]|x|x|x86[_64]/arm64|x|x|x||

## Mais informações sobre os recursos

A. O padrão não é a cobertura thread-safe contra atualizações para melhor desempenho,
ver [instrumentação/README.llvm.md](https://github.com/AFLplusplus/AFLplusplus/blob/d0070729206a80a9af297b2341edd63f68fdac35/instrumentation/README.llvm.md)

B. Nos contadores de cobertura de embrulho (255 + 1), salte o valor 0 e salte para 1
Em vez disso. Isto mostrou dar melhores dados de cobertura e é o padrão; veja
[instrumentação/README.llvm.md](https://github.com/AFLplusplus/AFLplusplus/blob/d0070729206a80a9af297b2341edd63f68fdac35/instrumentation/README.llvm.md).

C. Em vez de bifurcar, reitere a função alvo fuzz em um loop (como
`LLVMFuzzerTestOneInput`. Grande aumento de velocidade, mas só funciona com o alvo
funções que não mantêm estado, memória de fuga ou saída; ver
[instrumentação/README.persistant_mode.md](https://github.com/AFLplusplus/AFLplusplus/blob/d0070729206a80a9af297b2341edd63f68fdac35/instrumentation/README.persistent_mode.md)

D. Dividir qualquer comparação não--8 bits com a comparação de 8 bits; ver
[instrumentação/README.laf-intel.md](https://github.com/AFLplusplus/AFLplusplus/blob/d0070729206a80a9af297b2341edd63f68fdac35/instrumentation/README.laf-intel.md)

E. CmpLog é o nosso melhorado
[Redqueen](https://www.ndss-symposium.org/ndss-paper/redqueen-fuzzing-with-input-to-state-correspondence/)
Implementação, ver
[instrumentação/README.cmplog.md](https://github.com/AFLplusplus/AFLplusplus/blob/d0070729206a80a9af297b2341edd63f68fdac35/instrumentation/README.cmplog.md)

F. Semelhante e compatível com clang 14+ sancov sanitize-coverage-allow/deny mas
para todas as versões do llvm e todos os nossos modos de compilação,
ser instrumentado, para mais velocidade, fuzzing dirigido e menos instabilidade; ver
[instrumentação/README.instrument_list.md](https://github.com/AFLplusplus/AFLplusplus/blob/d0070729206a80a9af297b2341edd63f68fdac35/instrumentation/README.instrument_list.md)

G. Vanilla AFL usa cobertura onde as bordas podem colidir para a mesma cobertura
bytes quanto maior for o alvo. Nossa instrumentação padrão em LTO e
afl-clang-fast (PCGUARD) usa cobertura não colidindo que também o torna
mais rápido; ver
[instrumentação/README.llvm.md](https://github.com/AFLplusplus/AFLplusplus/blob/d0070729206a80a9af297b2341edd63f68fdac35/instrumentation/README.llvm.md).

I. Cobertura alternativa, dependendo do chamador (CTX); ver
[instrumentação/README.lto.md](https://github.com/AFLplusplus/AFLplusplus/blob/d0070729206a80a9af297b2341edd63f68fdac35/instrumentation/README.lto.md).

J. Um recurso LTO que cria um dicionário fuzzing baseado em comparações encontradas
durante a compilação/instrumentação. Funcionalidade automática :) Ver
[instrumentação/README.lto.md](https://github.com/AFLplusplus/AFLplusplus/blob/d0070729206a80a9af297b2341edd63f68fdac35/instrumentation/README.lto.md)

K. O recurso de instantâneo requer um módulo do kernel que foi muito trabalho para obter
por isso já não é apoiado.
[nyx_mode](https://github.com/AFLplusplus/AFLplusplus/blob/d0070729206a80a9af297b2341edd63f68fdac35/nyx_mode/README.md) em vez disso.

L. fuzzing mais rápido e menos syscall do kernel em cima pelo caso de fuzz na memória
entrega, ver
[instrumentação/README.persistant_mode.md](https://github.com/AFLplusplus/AFLplusplus/blob/d0070729206a80a9af297b2341edd63f68fdac35/instrumentation/README.persistent_mode.md)

## Mais informações sobre instrumentação

1. Padrão para LLVM >= 9.0, variável de ambiente para versão mais antiga devido a uma
erro de eficiência nas versões anteriores do lvm
2. O GCC cria código não- eficiente, daí estar desactivado no gcc_plugin
3. Com o `AFL_LLVM_THREADSAFE_INST`, desactiva o NeverZero
4. Com modo pcguard e modo LTO para LLVM 11 e mais recente
5. Próximo, desenvolvimento na ramificação
6. Apenas disponível no modo LTO (afl-clang-lto)
7. Automático no modo LTO com LLVM 11 e mais recente, um passe extra para todos LLVM
versões que escrevem para um arquivo para usar com o afl-fuzz' `-x`
8. O instantâneo LKM está atualmente sem manutenção devido a muitas alterações no kernel
vindo muito rápido :-(
9. O modo FRIDA é suportado em Linux e MacOS para Intel e ARM
10. QEMU/Unicorn só é suportado no Linux
11. O modo Coresight só está disponível no Linux AARCH64 com uma CPU com Coresight
    extension
12. O modo Nyx só é suportado no Linux e atualmente restrito ao x86_x64

## Características e patches integrados

Entre outros, os seguintes recursos e patches foram integrados:

* NeverZero para instrumentação lvm/gcc, modo QEMU e modo unicórnio_ que
impede um valor de mapa de embrulho a zero, aumenta a cobertura
* Modo persistente, servidor de fork diferido e fuzzing em memória para o modo QEMU
* Modo unicórnio que permite fuzzing de binários completamente diferentes
plataformas (integração fornecida pelo domenukk)
* A nova instrumentação CmpLog para LLVM e QEMU inspirada em
[Redqueen](https://github.com/RUB-SysSec/redqueen)
* Win32 PE só binário fuzzing com QEMU e vinho
* Horários de energia da AFLfast por Marcel Böhme:
[https://github.com/mboehme/aflfast](https://github.com/mboehme/aflfast)
* O estágio determinístico rápido por Han Zheng: [https://github.com/hexhive/mendelFuzz-Artifact/](https://github.com/hexhive/mendelFuzz-Artifact/)
* Um programador adaptativo de mutações inspirado no mutador MOpt
([https://github.com/puppet-meteor/MOpt-AFL](https://github.com/puppet-meteor/MOpt-AFL)),
habilitado com o interruptor `-L` (padrão: caos padrão)
* Suporte LAF-Intel/CompCov para instrumentação, modo QEMU e unicórnio_mode
(com capacidades melhoradas)
* mutador honggfuzz (como um mutador personalizado).
* Modo QBDI para fuzz android bibliotecas nativas via Quarkslab
Estrutura [QBDI](https://github.com/QBDI/QBDI)
* Modo frida e ptrace para bibliotecas somente para binários, etc.

Então tudo em tudo isso é o melhor de AFL que está lá fora :-)

---

## Procedência desta tradução

Fonte: [https://github.com/AFLplusplus/AFLplusplus](https://github.com/AFLplusplus/AFLplusplus/blob/d0070729206a80a9af297b2341edd63f68fdac35/docs/features.md). Licença: [AGPL-3.0](../../99-Assets/upstream/aflplusplus/LICENSE.txt). Commit: d0070729206a80a9af297b2341edd63f68fdac35.

O original preservado, a lista de mudanças de apresentação e os hashes constam no manifesto do projeto. Nenhum exemplo desta documentação foi executado automaticamente.
