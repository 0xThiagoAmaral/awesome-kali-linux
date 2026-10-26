---
title: "arp-scan — documentação oficial"
type: "official-documentation"
tool: "arp-scan"
status: "translated-machine"
reviewed: "2026-10-26"
language: "pt-BR"
tags: ["documentation", "tool/arp-scan"]
cssclasses: ["fieldbook"]
source_url: "https://github.com/royhills/arp-scan/blob/a0466d5fc7fa8a1e5625b7aae568ffb384e3f5a5/README.md"
source_commit: "a0466d5fc7fa8a1e5625b7aae568ffb384e3f5a5"
source_sha256: "a3a2c3d25999b32e06cfa8e6eab786fc3d84038b56d5e868310dbaa1ec094a58"
license_spdx: "GPL-3.0"
human_review: "pending"
source_scope: "Pinned README plus complete arp-fingerprint.1 and main arp-scan.1.dist manuals, each with its own preserved copying notice. Wiki, additional utilities and remaining sources still require coverage review."
---

> Tradução automática local para português, ainda sem revisão humana integral. Estrutura e blocos de código preservados; referências externas não significam conteúdo espelhado.

# arp-scan

[Build](https://github.com/royhills/arp-scan/actions/workflows/c-cpp.yml)
[Coverage Status](https://coveralls.io/github/royhills/arp-scan?branch=master)
[CodeQL](https://github.com/royhills/arp-scan/actions/workflows/codeql.yml)

---

# About

*arp-scan* é uma ferramenta de digitalização de rede que usa o protocolo ARP para descobrir e digitalizar as máquinas IPv4 na rede local. Está disponível para Linux, BSD, macOS e Solaris sob a licença [GPLv3](https://www.gnu.org/licenses/gpl-3.0.en.html).

Esta é a versão `README.md` para *arp-scan* `1.10.1-git`.

# Installation

<a id="building-and-installing-from-source"></a>
## Construindo e Instalando a partir de Fonte

*arp- scan* usa as ferramentas GNU *automake* e *autoconf*. O processo de instalação da mais recente fonte *github* é:

- `git clone https://github.com/royhills/arp-scan.git` para obter o código fonte mais recente.
- `cd arp-scan` para inserir o diretório de código fonte.
- `autoreconf --install` para gerar um arquivo de configuração (se você não tiver `autoreconf` você pode baixar um tarball em vez disso como detalhado abaixo).
- `./configure` para criar um makefile para o seu sistema (veja as opções de configuração abaixo).
- `make` para construir o projeto.
- Opcionalmente `make check` para verificar se tudo funciona como esperado.
- `make install` para instalar (você precisará ser root ou usar sudo/doas para esta parte).

Você precisará dessas ferramentas de desenvolvimento e bibliotecas:

- GNU *automake* e *autoconf* (se você não tiver estes, você pode baixar o último tarball que inclui `configure` em vez disso: [arp- scan- 1.10.0.tar. gz](https://github.com/royhills/arp-scan/releases/download/1.10.0/arp-scan-1.10.0.tar.gz)). Note que este pode não estar tão atualizado quanto o mais recente *github* versão de desenvolvimento.
- O utilitário *make* (testado com BSD make e GNU make).
- Um compilador C (testado em *gcc* e *clang*, deve trabalhar em qualquer compilador C que suporte C99).
- Bibliotecas e incluir arquivos para *libpcap* versão 1.5 ou posterior. Todas as distros modernas têm um pacote binário, alguns dividem o pacote em execução `libpcap` e pacotes de desenvolvimento `libpcap-dev` ou `libpcap-devel`, neste caso você precisa instalar a versão de desenvolvimento para compilar.
- *libcap* para criar com o suporte [Capacidades POSIX.1e](https://sites.google.com/site/fullycapable/) no Linux. A maioria dos distros Linux vem com suporte em tempo de execução por padrão e tem um pacote de desenvolvimento disponível. Linux tem suporte de recursos desde a versão do kernel `2.6.24`.

Para executar os scripts Perl `arp-fingerprint` e `get-oui`, você também precisará do interpretador *perl* e dos módulos Perl `LWP::UserAgent` e `Text::CSV`.

Você pode passar opções para `configure` para controlar o processo de compilação. Execute `./configure --help` para uma lista de opções. *arp- scan* tem uma opção de configuração específica do pacote:

- `--with-libcap[=auto/yes/no]` Build with libcap POSIX.1e capacitys support [default=`auto`]

    With `auto`, configure will enable capability support if the `libcap` library and headers are installed. Specifying `--with-libcap` will enable support and `--without-libpcap` will disable it.

*arp- scan* é conhecido por construir e executar:

 - **Linux** (deve funcionar em qualquer distribuição e em todas as arquiteturas).
 - **FreeBSD**
 - **OpenBSD**
 - **NetBSD**
 - **DragonflyBSD**
 - **macOS**
 - **Solaris 10** (há problemas conhecidos com Solaris 11. Se alguém se importa, por favor, comentar sobre [número # 31](https://github.com/royhills/arp-scan/issues/31)).

Deve ser possível criar o *arp-scan* em qualquer sistema operacional que o *libpcap* suporte. Se o seu sistema operacional suporta o *libpcap*, mas configurar dá o erro `configure: error: Host operating system your-os-name is not supported` por favor abra um [questão](https://github.com/royhills/arp-scan/issues) para solicitar a portagem para o seu sistema operacional.

<a id="installing-from-a-binary-package"></a>
## Instalando a partir de um pacote binário

Muitas distribuições fornecem pacotes binários para o *arp-scan* Estes não serão tão atualizados quanto a última fonte no github e podem não estar tão atualizados quanto a última versão, mas eles são mais convenientes e serão mantidos atualizados pelo gerenciador de pacotes. Assim, usar um pacote binário é muitas vezes uma boa escolha se você não precisar dos recursos mais recentes.

Se você instalou um pacote binário e se pergunta se existem novas funcionalidades úteis no github, use `arp-scan --version` para verificar a versão que você tem em seguida, veja os arquivos [NEWS](https://github.com/royhills/arp-scan/blob/a0466d5fc7fa8a1e5625b7aae568ffb384e3f5a5/NEWS.md) e [ChangeLog](https://github.com/royhills/arp-scan/blob/a0466d5fc7fa8a1e5625b7aae568ffb384e3f5a5/ChangeLog) no github para detalhes do que é alterado.

Os detalhes sobre como instalar um pacote binário *arp-scan* dependem de sua distribuição.

<a id="installing-from-a-bsd-port"></a>
## Instalando a partir de uma porta BSD

Se você estiver usando um sistema operacional BSD você pode ter a opção de instalar a partir de uma coleção de portas de origem, bem como de um pacote binário.

As portas automatizam a construção e instalação do código- fonte e gerenciam as atualizações como um pacote binário. Elas também dão a flexibilidade de instalar a partir do código- fonte. Uma porta- fonte não estará tão atualizada quanto o último github, mas pode ser mais atualizada do que o pacote binário correspondente.

Os detalhes de como instalar uma porta fonte *arp-scan* dependem de sua distribuição.

# Documentation

Utilização da informação de utilização:

`arp-scan --help`

Para informações detalhadas, consulte as páginas de manual: `arp-scan(1)`, `arp-fingerprint(1)`, `get-oui(1)` e `mac-vendor(5)`.

Ver a wiki *arp-scan* em [https://github.com/royhills/arp-scan/wiki](https://github.com/royhills/arp-scan/wiki)

Veja [`CONTRIBUTING.md`](https://github.com/royhills/arp-scan/blob/a0466d5fc7fa8a1e5625b7aae568ffb384e3f5a5/CONTRIBUTING.md) se você está interessado em contribuir para *arp-scan*. Se você acha que encontrou uma vulnerabilidade de segurança, por favor veja [`SECURITY.md`](https://github.com/royhills/arp-scan/blob/a0466d5fc7fa8a1e5625b7aae568ffb384e3f5a5/SECURITY.md).

# Notes for Package Maintainers

 - Por favor levante um problema github ou crie uma solicitação de pull se você tiver algum patch local que possa ser aplicável a montante.
 - Se você está construindo em Linux, por favor, construa com suporte de recursos `libcap` POSIX.1e se você puder. Você pode precisar instalar os cabeçalhos de desenvolvimento `libcap`, bem como os cabeçalhos de desenvolvimento `libpcap` antes de executar o `configure`.
 - Note que `Makefile.am` contém um `install-exec-hook` que irá instalar *arp-scan* com recursos `CAP_NET_RAW` se puder, e falhando que ele irá instalá-lo raiz suid.


---

## Procedência desta tradução

Fonte: [https://github.com/royhills/arp-scan](https://github.com/royhills/arp-scan/blob/a0466d5fc7fa8a1e5625b7aae568ffb384e3f5a5/README.md). Licença: [GPL-3.0](../../99-Assets/upstream/arp-scan/LICENSE.txt). Commit: a0466d5fc7fa8a1e5625b7aae568ffb384e3f5a5.

O original preservado, a lista de mudanças de apresentação e os hashes constam no manifesto do projeto. Nenhum exemplo desta documentação foi executado automaticamente.
