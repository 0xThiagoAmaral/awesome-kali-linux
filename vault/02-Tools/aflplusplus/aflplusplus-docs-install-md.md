---
title: "aflplusplus — documentação oficial"
type: "official-documentation"
tool: "aflplusplus"
status: "translated-machine"
reviewed: "2026-10-26"
language: "pt-BR"
tags: ["documentation", "tool/aflplusplus"]
cssclasses: ["fieldbook"]
source_url: "https://github.com/AFLplusplus/AFLplusplus/blob/d0070729206a80a9af297b2341edd63f68fdac35/docs/INSTALL.md"
source_commit: "d0070729206a80a9af297b2341edd63f68fdac35"
source_sha256: "4cac783c3be5777aa10051066ad05c593a22f1db30f3439d91acb43a1123b4f9"
license_spdx: "AGPL-3.0-or-later"
human_review: "pending"
source_scope: "Repository root README and owned doc/docs/documentation Markdown or RST files; not a claim of full wiki/site coverage"
---

> Tradução automática local para português, ainda sem revisão humana integral. Estrutura e blocos de código preservados; referências externas não significam conteúdo espelhado.

# Building and installing AFL++

<a id="linux-on-x86"></a>
## Linux em x86

Uma maneira fácil de instalar AFL++ com tudo compilado está disponível via docker:
Você pode usar o [arquivo de Docker](https://github.com/AFLplusplus/AFLplusplus/blob/d0070729206a80a9af297b2341edd63f68fdac35/Dockerfile) ou apenas puxar diretamente do
Docker Hub (para x86_64 e arm64):

```shell
docker pull aflplusplus/aflplusplus:latest
docker run -ti -v /location/of/your/target:/src aflplusplus/aflplusplus
```

Esta imagem é gerada automaticamente quando um push para o branch estável acontece.
Você encontrará seu código fonte alvo no `/src` no recipiente.

Nota: você também pode puxar `aflplusplus/aflplusplus:dev` que é o mais atual
estado de desenvolvimento de AFL++.

Se você quiser construir o AFL++, você tem muitas opções. A escolha mais fácil
é construir e instalar tudo:

NOTA: dependendo da sua versão Debian/Ubuntu/Kali/..., substitua `-18` por
qualquer versão lvm está disponível. Recomendamos lvm 18 ou mais novo, mínimo é 14.

```shell
sudo apt-get update
sudo apt-get install -y build-essential python3-dev automake cmake git flex bison libglib2.0-dev libpixman-1-dev python3-setuptools cargo libgtk-3-dev
# try to install llvm-18 and install the distro default if that fails
sudo apt-get install -y lld-18 llvm-18 llvm-18-dev clang-18 || sudo apt-get install -y lld llvm llvm-dev clang
sudo apt-get install -y gcc-$(gcc --version|head -n1|sed 's/\..*//'|sed 's/.* //')-plugin-dev libstdc++-$(gcc --version|head -n1|sed 's/\..*//'|sed 's/.* //')-dev
sudo apt-get install -y meson ninja-build # for QEMU mode
sudo apt-get install -y cpio libcapstone-dev # for Nyx mode
sudo apt-get install -y wget curl # for Frida mode
sudo apt-get install -y python3-pip # for Unicorn mode
git clone https://github.com/AFLplusplus/AFLplusplus
cd AFLplusplus
git submodule update --init
make distrib
sudo make install
```

Recomenda-se instalar o mais novo gcc disponível, clang e llvm-dev
possível na sua distribuição!

Note que `make distrib` também constrói modo FRIDA, modo QEMU, unicórnio_modo, e
mais. Se você apenas quer AFL++ simples, em seguida, faça `make all`.
ajudando tooling compilado, mas não estão interessados em alvos somente binários, então
em vez disso, escolha:

```shell
make source-only
```

Estes objectivos de construção existem:

* todos: os principais binários AFL++ e instrumentação llvm/gcc
* somente binário: tudo para somente binário fuzzing: frida_mode, nyx_mode,
qemu_mode, frida_mode, unicórnio_mode, coresight_mode, libdislocator,
libtokencap
* código fonte: tudo para o código fonte fuzzing: nyx_mode, libdislocator,
libtokencap
* distribuição: tudo (para fuzzing somente binário e código fonte)
* man: cria páginas de man simples a partir da opção de ajuda dos programas
* instalar: instala tudo o que compilou com as opções de compilação acima
* limpo: limpa tudo compilado, não downloads (a menos que não em um checkout)
* Deepclean: limpa tudo, incluindo downloads
* code-format: formate o código, faça isso antes de commit e envie um PR por favor!
* testes: executa casos de teste para garantir que todos os recursos ainda estão funcionando como eles
deve
* Unidade: realizar testes unitários (com base em cmocka)
* help: mostra estas opções de compilação

[A não ser que esteja a tomar macOS](https://developer.apple.com/library/archive/qa/qa1118/_index.html),
você também pode construir versões estaticamente vinculadas dos binários AFL++ passando
o argumento `PERFORMANCE=1` a fazer:

```shell
make PERFORMANCE=1
```

Estas opções de compilação existem:

* DESEMPENHO - compilar com opções de desempenho que tornam o binário não transferível para outros sistemas. Recomendado (exceto no macOS)!
* Static - compilar estática AFL++ (não funciona no macOS)
* CODE_COVERAGE - compilar o alvo para cobertura de código (ver [README.llvm.md](https://github.com/AFLplusplus/AFLplusplus/blob/d0070729206a80a9af297b2341edd63f68fdac35/instrumentation/README.llvm.md))
* ASAN_BUILD - compila AFL++ com higienizador de endereços para fins de depuração
* UBSAN_BUILD - compila ferramentas AFL++ com higienizador de comportamento indefinido para fins de depuração
* DEBUG - sem otimização, -ggdb3, todos os avisos e -Werror
* LLVM_DEBUG - mostra advertências de deprecação llvm
* PROFILING - compilar afl-fuzz com informações de perfil
* INTROSPECÇÃO - compilar afl-fuzz com introspecção de mutação
* NO_ PYTHON - desabilitar suporte a python
* NO_UTF - não use UTF-8 para renderização de linha na tela de status (fallback para desenho de caixa G1, de baunilha AFL)
* NO_NYX - desabilitar dependências do modo nyx de construção
* NO_CORESIGHT - desabilitar a visão de núcleos de construção (apenas o arm64)
* NO_QEMU - desactivar o suporte ao QEMU de compilação
* NO_FRIDA - desactivar o suporte à construção da FRIDA
* NO_ UNICORN - desabilitar o unicórnio de construção
* NO_UNICORN_ ARM64 - desabilitar a construção de unicórnio no braço64
* AFL_NO_X86 - se compilar em plataformas não-Intel/AMD
* LLVM_CONFIG - se sua distro não usar o nome padrão para llvm-config (por exemplo, Debian)

Por exemplo: `make LLVM_CONFIG=llvm-config-18`

<a id="macos-on-x86_64-and-arm64"></a>
## macOS em x86_64 e arm64

o macOS tem algumas gotchas devido às idiossincrasias da plataforma.

macOS suporta memória compartilhada SYSV usada pela instrumentação de AFL++, mas o
as configurações padrão não são suficientes. Antes mesmo de construir, aumente
executando o script fornecido:

```shell
sudo afl-system-config
```

Ver
[https://www.spy-hill.com/help/apple/SharedMemory.html](https://www.spy-hill.com/help/apple/SharedMemory.html)
para documentação das configurações de memória compartilhada e como torná-las permanentes.

Em seguida, para construir AFL++, instale os seguintes pacotes da cerveja (use `@version`
instalar uma versão específica):

```shell
brew install wget git make cmake llvm lld gdb coreutils
```

Dependendo do seu sistema macOS + versão de cerveja, a cerveja pode ser instalada em diferentes lugares.
Você pode verificar com `brew info llvm` para saber onde, em seguida, criar uma variável para ele:

```shell
export HOMEBREW_BASE="/opt/homebrew/opt"
```

ou

```shell
export HOMEBREW_BASE="/usr/local/opt"
```

Defina `PATH` para apontar para o clang brew, clang++, llvm-config, gmake e coreutils.
Também use o compilador brew clang; o compilador Xcode clang não deve ser usado.

```shell
export PATH="$HOMEBREW_BASE/coreutils/libexec/gnubin:/usr/local/bin:$HOMEBREW_BASE/llvm/bin:$PATH"
export CC=clang
export CXX=clang++
```

Em seguida, construa seguindo as instruções gerais do Linux.

Se tudo funcionou, você deve ter `afl-clang-fast` instalado, que você pode verificar com:

```shell
which afl-clang-fast
```

Note que `afl-clang-lto`, `afl-gcc-fast` e `qemu_mode` não estão trabalhando no macOS.

O daemon de relatórios de falhas que vem por padrão com macOS causará
problemas com o fuzzing. Você precisa desligá-lo, o que você pode fazer com o `afl-system-config`.

A semântica `fork()` no macOS são um pouco incomuns em comparação com outros sistemas unix
Isso significa duas coisas:

  - Fuzzing será provavelmente mais lento do que no Linux. Na verdade, algumas pessoas relatam
    considerable performance gains by running the jobs inside a Linux VM on
    macOS.
  - Algum código não portátil específico da plataforma pode ser incompatível com o AFL++
    forkserver. If you run into any problems, set `AFL_NO_FORKSRV=1` in the
    environment before starting afl-fuzz.

Modo de emulação do usuário de QEMU não parece ser suportado no macOS, então
O modo de instrumentação da caixa preta (`-Q`) não irá funcionar. Contudo, o modo FRIDA (`-O`)
funciona em caixas de macOS x86 e arm64.

<a id="ios-on-arm64-and-arm64e"></a>
## iOS no braço64 e arm64e

**Opção 1: Compilação no iOS de cadeia quebrada (recomendado)**

Para compilar diretamente em um dispositivo iOS jailbreaked, é recomendável usar uma jailbreak que suporta Procurasus,
como o Procurasus fornece pacotes pré-construídos atualizados para as ferramentas necessárias.

Certifique-se de que o `openssh` está instalado em seu dispositivo iOS e, em seguida, o SSH nele.
Instalar os seguintes pacotes:

```shell
sudo apt install wget git make cmake clang gawk llvm ldid coreutils build-essential xz-utils
```

Configurar o ambiente para compilação:

```shell
export IOS_SDK_PATH="/usr/share/SDKs/iPhoneOS.sdk"
export CC=clang
export CXX=clang++
```

Em seguida, construa seguindo as instruções gerais do Linux.

**Option 2: Compilação cruzada no macOS para o iOS**

Além dos pacotes necessários para uma compilação macOS, instale `ldid` para assinar binários:

```shell
brew install ldid-procursus
```

Configurar o ambiente para compilação:

```shell
export IOS_SDK_PATH="$(xcrun --sdk iphoneos --show-sdk-path)"
export CC="$(xcrun --sdk iphoneos -f clang) -target arm64-apple-ios14.0"
export CXX="$(xcrun --sdk iphoneos -f clang++) -target arm64-apple-ios14.0"
export HOST_CC=cc
```

Em seguida, construa seguindo as instruções gerais do Linux.
Finalmente, transfira os binários para o dispositivo iOS.


---

## Procedência desta tradução

Fonte: [https://github.com/AFLplusplus/AFLplusplus](https://github.com/AFLplusplus/AFLplusplus/blob/d0070729206a80a9af297b2341edd63f68fdac35/docs/INSTALL.md). Licença: [AGPL-3.0-or-later](../../99-Assets/upstream/aflplusplus/LICENSE.txt). Commit: d0070729206a80a9af297b2341edd63f68fdac35.

O original preservado, a lista de mudanças de apresentação e os hashes constam no manifesto do projeto. Nenhum exemplo desta documentação foi executado automaticamente.
