---
title: "aflplusplus — documentação oficial"
type: "official-documentation"
tool: "aflplusplus"
status: "translated-machine"
reviewed: "2026-10-26"
language: "pt-BR"
tags: ["documentation", "tool/aflplusplus"]
cssclasses: ["fieldbook"]
source_url: "https://github.com/AFLplusplus/AFLplusplus/blob/d0070729206a80a9af297b2341edd63f68fdac35/docs/fuzzing_binary-only_targets.md"
source_commit: "d0070729206a80a9af297b2341edd63f68fdac35"
source_sha256: "b3517d0e5191dd5facd31ec53ae4a0968805353365a69046b79308055cebf428"
license_spdx: "AGPL-3.0-or-later"
human_review: "pending"
source_scope: "Repository root README and owned doc/docs/documentation Markdown or RST files; not a claim of full wiki/site coverage"
---

> Tradução automática local para português, ainda sem revisão humana integral. Estrutura e blocos de código preservados; referências externas não significam conteúdo espelhado.

# Fuzzing binary-only targets

AFL++, libfuzzer e outros fuzzers são ótimos se você tiver o código fonte do
alvo. Isso permite muito rápido e cobertura guiada fuzzing.

No entanto, se houver apenas o programa binário e nenhum código fonte disponível, então
`afl-fuzz -n` padrão (modo não instrumentado) não é eficaz.

Para instrumentação rápida e em tempo real de binários de caixa preta, AFL++ ainda oferece
vários suportes. O seguinte é uma descrição de como estes binários podem ser
Fuzzed com AFL++.

## TL;DR:

Modo FRIDA e modo QEMU em modo persistente são os mais rápidos - se o modo persistente
é possível e a estabilidade é alta o suficiente.

Caso contrário, tente Zafl, RetroWrite, Dyninst, e se estes falharem, também, tente
modo padrão FRIDA/QEMU com `AFL_ENTRYPOINT` + `AFL_EXITPOINT` para onde você
Preciso dela.

Se o seu alvo não for linux, então use o modo unicórnio_.

## Alvos fuzzing apenas binários com AFL++

### Modo QEMU

O modo QEMU é a solução "nativa" para o programa.
./qemu_mode/ directório e, uma vez compilado, pode ser acessado pelo afl-fuzz -Q
opção de linha de comando. É a alternativa mais fácil de usar e até mesmo funciona para
binários multiplataforma.

Para os programas linux e suas bibliotecas, isso é realizado com uma versão de
O QEMU em execução no modo de "emulação de espaço do usuário" menos conhecido. O QEMU é um projecto
separado de AFL++, mas você pode convenientemente construir o recurso, fazendo:

```shell
cd qemu_mode
./build_qemu_support.sh
```

Recomenda-se a seguinte configuração para usar o modo QEMU:

* executar 1 instância afl-fuzz - Q com CMPLOG (`-c 0` + `AFL_COMPCOV_LEVEL=2`)
* execute 1 instância afl-fuzz - Q com QASAN (`AFL_USE_QASAN=1`)
* executar 1 instância afl-fuzz - Q com LAF (`AFL_PRELOAD=libcmpcov.so` +
`AFL_COMPCOV_LEVEL=2`), alternativamente você pode usar o modo FRIDA, basta alternar `-Q`
com `-O` e remover a instância LAF

Em seguida, execute quantas instâncias você tiver núcleos restantes com o modo `-Q` ou use
um reescritor binário estático como Dyninst, RetroWrite, ZAFL, etc.
Os reescritores binários todos têm suas próprias vantagens e ressalvas, mas ZAFL é uma boa escolha.

Se um reescritor binário funciona para o seu alvo, então você pode usar afl-fuzz normalmente
e terá o dobro da velocidade em comparação com o modo QEMU (mas mais lento do que o QEMU
modo persistente).

A redução de velocidade do modo QEMU é de cerca de 50%. No entanto, existem várias opções
aumentar a velocidade:
- usando AFL_ENTRYPOINT para mover a entrada do servidor de garfos para um bloco básico posterior
a velocidade binária (+5-10%)
- usando o modo persistente
[qemu_mode/README.persistant.md](https://github.com/AFLplusplus/AFLplusplus/blob/d0070729206a80a9af297b2341edd63f68fdac35/qemu_mode/README.persistent.md) isto irá
resultado em um 150-300% aumento de velocidade global - assim 3-8x o modo QEMU original
Velocidade!
- usando AFL_CODE_START/AFL_CODE_END para apenas partes específicas do instrumento

Para instruções e advertências adicionais, ver
[qemu_mode/README.md](https://github.com/AFLplusplus/AFLplusplus/blob/d0070729206a80a9af297b2341edd63f68fdac35/qemu_mode/README.md). Se possível, você deve usar o
modo persistente, ver
[qemu_mode/README.persistant.md](https://github.com/AFLplusplus/AFLplusplus/blob/d0070729206a80a9af297b2341edd63f68fdac35/qemu_mode/README.persistent.md). O modo é
aproximadamente 2-5x mais lento do que a instrumentação em tempo de compilação, e é menos
conduz à paralelização.

Note que há também hongggfuzz:
[https://github.com/google/honggfuzz](https://github.com/google/honggfuzz) que
agora tem um modo QEMU, mas seu desempenho é apenas 1.5% ...

Se você gosta de codificar um fuzzer personalizado sem muito trabalho, recomendamos
para verificar a nossa irmã projeto libafl que suporta QEMU, também:
[https://github.com/AFLplusplus/LibAFL](https://github.com/AFLplusplus/LibAFL)

### VINHO+QEMU

Modo de vinho pode executar binários Win32 PE com a instrumentação QEMU.
Vinho, python3, e o pacote python pefile instalado.

Está incluído em AFL++.

Para mais informações, consultar
[qemu_mode/README.wine.md](https://github.com/AFLplusplus/AFLplusplus/blob/d0070729206a80a9af297b2341edd63f68fdac35/qemu_mode/README.wine.md).

### Modo FRIDA

No modo FRIDA, você pode fuzz alvos apenas binários tão facilmente como com o modo QEMU.
O modo FRIDA é na maioria das vezes ligeiramente mais rápido do que o modo QEMU.
mais recente, e tem a vantagem de que ele funciona no MacOS (intel e M1).

Para compilar o modo FRIDA:

```shell
cd frida_mode
gmake
```

Para instruções e advertências adicionais, ver
[frida_mode/README.md](https://github.com/AFLplusplus/AFLplusplus/blob/d0070729206a80a9af297b2341edd63f68fdac35/frida_mode/README.md).

Se possível, você deve usar o modo persistente, veja
[instrumentação/README.persistant_mode.md](https://github.com/AFLplusplus/AFLplusplus/blob/d0070729206a80a9af297b2341edd63f68fdac35/instrumentation/README.persistent_mode.md).
O modo é aproximadamente 2-5x mais lento do que a instrumentação em tempo de compilação, e é
menos propício à paralelização. Mas para apenas binário fuzzing, dá um enorme
melhoria da velocidade se for possível utilizar.

Você também pode executar fuzzing remoto com frida, por exemplo, se você quiser fuzz on
iPhone ou dispositivos Android, para isso você pode usar
[https://github.com/ttdennis/fpicker/](https://github.com/ttdennis/fpicker/) como
um intermediário que usa AFL++ para fuzzing.

Se você gosta de codificar um fuzzer personalizado sem muito trabalho, recomendamos
para verificar a nossa irmã projeto libafl que suporta Frida, também:
[https://github.com/AFLplusplus/LibAFL](https://github.com/AFLplusplus/LibAFL).
Já existem exemplos de trabalho :-)

### Modo Nyx

Nyx é uma emulação completa do sistema fuzzing ambiente com suporte instantâneo que é
construído sobre KVM e QEMU. Ele só está disponível no Linux e atualmente restrito
até x86_x64.

Para fuzzing somente binário é necessário um kernel especial 5.10.

Ver [nyx_mode/README.md](https://github.com/AFLplusplus/AFLplusplus/blob/d0070729206a80a9af297b2341edd63f68fdac35/nyx_mode/README.md).

### Unicórnio

O unicórnio é um garfo de QEMU. A instrumentação é, portanto, muito semelhante.
contraste com QEMU, Unicorn não oferece um sistema completo ou mesmo userland
emulação. Ambiente de execução e/ou carregadores têm de ser gravados do zero,
se necessário. No topo, foi removido o encadeamento do bloco. Isto significa o aumento de velocidade
introduzido no modo QEMU patched de AFL++ não pode ser portado para o Unicórnio.

Para binários não-Linux, você pode usar o unicórnio_modo do AFL++ que pode emular
qualquer coisa que você quiser - pelo preço da velocidade e scripts escritos pelo usuário.

Para compilar o modo_ unicórnio:

```shell
cd unicorn_mode
./build_unicorn_support.py
```

Para mais informações, confira
[unicórnio_modo/README.md](https://github.com/AFLplusplus/AFLplusplus/blob/d0070729206a80a9af297b2341edd63f68fdac35/unicorn_mode/README.md).

### Bibliotecas compartilhadas

Se o objetivo é fuzz uma biblioteca dinâmica, então há duas opções disponíveis.
Para ambos, você precisa escrever um pequeno arnês que carrega e chama a biblioteca.
Então você faz isso com o modo FRIDA ou o modo QEMU e usa
`AFL_INST_LIBS=1` ou `AFL_QEMU/FRIDA_INST_RANGES`.

Outra opção, menos precisa e mais lenta é fuzz-lo com utils/afl_untracer/
e usar afl-untracer.c como um modelo. É mais lento do que o modo FRIDA.

Para mais informações, consultar
[utils/afl_untracer/README.md](https://github.com/AFLplusplus/AFLplusplus/blob/d0070729206a80a9af297b2341edd63f68fdac35/utils/afl_untracer/README.md).

### Coresight

Coresight é a resposta do ARM ao PT da Intel. Com AFL++ v3.15, há uma visão do núcleo
implementação do marcador disponível no `coresight_mode/` que é mais rápido do que o QEMU,
no entanto, não pode ser executado em paralelo. Atualmente, apenas um processo pode ser rastre
é a WIP.

Para mais informações, consultar
[coresight_mode/README.md](https://github.com/AFLplusplus/AFLplusplus/blob/d0070729206a80a9af297b2341edd63f68fdac35/coresight_mode/README.md).

## Reescritores binários

Uma solução alternativa são reescritores binários. Eles são mais rápidos do que as soluções
Nativo do AFL++, mas nem sempre funciona.

### ZAFL

ZAFL é uma plataforma de reescrita estática que suporta x86-64 C/C++,
e binários PIE/non-PIE. Para além do convencional
instrumentação, API da ZAFL permite passes de transformação (por exemplo, laf-Intel,
sensibilidade de contexto, InsTrim, etc.).

A sua velocidade de instrumentação de base é geralmente a média de 90-95% de
Afl-clang-fast.

[https://git.zephyr-software.com/opensrc/zafl](https://git.zephyr-software.com/opensrc/zafl)

### RetroWrite

O RetroWrite é um reescritor binário estático que pode ser combinado com o AFL++.
tem um binário x86_64 ou arm64 que não contém exceções em C++ e - se
x86_64 - ainda tem seus símbolos e compilado com código independente de posição
(PIC/PIE), então a solução RetroWrite pode ser para você.
Ele descompila para arquivos ASM que podem então ser instrumentados com afl-gcc.
Note-se que o afl-gcc só está presente até AFL++ v4.21c e foi posteriormente removido por ser obsoleto.

Binários que são estaticamente instrumentados para fuzzing usando RetroWrite são próximos
em desempenho para binários instrumentados por compiladores e superando o QEMU-based
instrumentação.

[https://github.com/HexHive/retrowrite](https://github.com/HexHive/retrowrite)

### Dyninst

Dyninst é um framework de instrumentação binária semelhante ao Pintool e DynamoRIO.
No entanto, enquanto Pintool e DynamoRIO trabalham em tempo de execução, Dyninst instrumenta o
alvo no tempo de carga e, em seguida, deixá-lo executar - ou salvar o binário com as alterações.
Isto é ótimo para algumas coisas, por exemplo, fuzzing, e não tão eficaz para outras,
Por exemplo, análise de malware.

Então, o que você pode fazer com Dyninst é pegar cada bloco básico e colocar AFL++
código de instrumentação lá dentro - e depois salvar o binário. Depois, apenas fuzz
o binário alvo recém-salvado com afl-fuzz. Parece ótimo? É. O problema
embora - é um problema não trivial para inserir instruções, que mudam
aborda no espaço do processo, de modo que tudo ainda está funcionando depois.
Assim, mais frequentemente do que não os binários falham quando são executados.

A redução de velocidade é de cerca de 15-35%, dependendo das opções de otimização utilizadas
com afl-dyninst.

[https://github.com/vanhauser-thc/afl-dyninst](https://github.com/vanhauser-thc/afl-dyninst)

### Mcsema

Teoricamente, você também pode descompilar para lvm IR com mcsema, e em seguida, usar
lvm_mode para instrumentar o binário. Boa sorte com isso.

[https://github.com/lifting-bits/mcsema](https://github.com/lifting-bits/mcsema)

## Marcadores binários

### Pintool & DynamoRIO

Pintool e DynamoRIO são motores de instrumentação dinâmicos.
obter informações básicas do bloco em tempo de execução. Pintool só está disponível para a Intel
x32/x64 no Linux, Mac OS e Windows, enquanto DynamoRIO é adicionalmente
disponível para ARM e AARCH64. DynamoRIO também é 10x mais rápido do que Pintool.

O grande problema com DynamoRIO (e, portanto, Pintool, também) é a velocidade.
tem uma diminuição de velocidade de 98-99%, Pintool tem uma diminuição de velocidade de 99.5%.

Assim, DynamoRIO é a opção para ir para se tudo mais falhar e Pintool
Só se o DynamoRIO também falhar.

Soluções DynamoRIO:
* [https://github.com/vanhauser-thc/afl-dynamorio](https://github.com/vanhauser-thc/afl-dynamorio)
* [https://github.com/mxmssh/drAFL](https://github.com/mxmssh/drAFL)
* [https://github.com/googleprojectzero/winafl/](https://github.com/googleprojectzero/winafl/)
  <= very good but windows only

Soluções Pintool:
* [https://github.com/vanhauser-thc/afl-pin](https://github.com/vanhauser-thc/afl-pin)
* [https://github.com/mothran/aflpin](https://github.com/mothran/aflpin)
* [https://github.com/spinpx/afl_pin_mode](https://github.com/spinpx/afl_pin_mode)
  <= only old Pintool version supported

### Intel PT

Se você tiver uma CPU Intel mais recente, você pode fazer uso do rastreamento do processador da Intel.
grande problema com o PT da Intel é o tamanho pequeno do buffer e a codificação complexa de
a informação de depuração recolhida através do PT. Isto faz com que a decodificação seja muito CPU
Consequentemente, a redução global da velocidade é de cerca de
70-90% (dependendo da implementação e de outros fatores).

Existem duas implementações de Intel-pt da AFL:

1. [https://github.com/junxzm1990/afl-pt](https://github.com/junxzm1990/afl-pt)
    => This needs Ubuntu 14.04.05 without any updates and the 4.4 kernel.

2. [https://github.com/hunter-ht-2018/ptfuzzer](https://github.com/hunter-ht-2018/ptfuzzer)
    => This needs a 4.14 or 4.15 kernel. The "nopti" kernel boot option must be
    used. This one is faster than the other.

Note que há também hongggfuzz:
[https://github.com/google/honggfuzz](https://github.com/google/honggfuzz).
seu desempenho IPT é de apenas 6%!

## Soluções não-AFL++

Existem muitos frameworks apenas para binários fuzzing. Alguns são ótimos para CTFs, mas não
trabalhar com grandes binários, outros são muito lentos, mas têm uma boa descoberta do caminho,
Alguns são muito difíceis de montar...

* Chacalope:
[https://github.com/googleprojectzero/Jackalope](https://github.com/googleprojectzero/Jackalope)
* Manticore:
[https://github.com/trailofbits/manticore](https://github.com/trailofbits/manticore)
* QSYM:
[https://github.com/sslab-gatech/qsym](https://github.com/sslab-gatech/qsym)
* S2E: [https://github.com/S2E](https://github.com/S2E)
* TinyInst:
[https://github.com/googleprojectzero/TinyInst](https://github.com/googleprojectzero/TinyInst)
*  Por favor, mande-me qualquer desaparecido que seja bom.

## Palavras finais

É isso! Notícias, correções, atualizações? Envie um email para vh@thc.org.


---

## Procedência desta tradução

Fonte: [https://github.com/AFLplusplus/AFLplusplus](https://github.com/AFLplusplus/AFLplusplus/blob/d0070729206a80a9af297b2341edd63f68fdac35/docs/fuzzing_binary-only_targets.md). Licença: [AGPL-3.0](../../99-Assets/upstream/aflplusplus/LICENSE.txt). Commit: d0070729206a80a9af297b2341edd63f68fdac35.

O original preservado, a lista de mudanças de apresentação e os hashes constam no manifesto do projeto. Nenhum exemplo desta documentação foi executado automaticamente.
