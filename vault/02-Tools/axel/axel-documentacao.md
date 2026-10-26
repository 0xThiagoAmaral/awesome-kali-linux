---
title: "axel — documentação oficial"
type: "official-documentation"
tool: "axel"
status: "translated-machine"
reviewed: "2026-10-26"
language: "pt-BR"
tags: ["documentation", "tool/axel"]
cssclasses: ["fieldbook"]
source_url: "https://github.com/axel-download-accelerator/axel/blob/dc10ba0c8f8d804c1568df5dba3cdd6fa89572b1/README.md"
source_commit: "dc10ba0c8f8d804c1568df5dba3cdd6fa89572b1"
source_sha256: "bfb19b48b5d60fe43691c0d13fd930055be2afdc74923dd7b3a6e6235911c2d6"
license_spdx: "GPL-2.0"
human_review: "pending"
source_scope: "Pinned root README plus the complete doc/axel.txt reference manual; external sites and all other sources still require separate coverage review"
---

> Tradução automática local para português, ainda sem revisão humana integral. Estrutura e blocos de código preservados; referências externas não significam conteúdo espelhado.

# AXEL - Lightweight CLI download accelerator

<a id="about"></a>
## Sobre

Axel tenta acelerar o processo de download usando múltiplos
conexões por arquivo, e também pode equilibrar a carga entre
servidores diferentes.

Axel tenta ser o mais leve possível, por isso pode ser útil em
Sistemas bytes-críticos.

O Axel suporta protocolos HTTP, HTTPS, FTP e FTPS.

Graças ao desenvolvedor original de Axel, Wilmer van der Gaast, e todos
outros que contribuíram para isso ao longo dos anos.

<a id="usage"></a>
## Uso

Para informações de uso, consulte a página de manual:

    man axel

<a id="how-to-help"></a>
## Como ajudar
Se você pode codificar e estiver interessado em melhorar Axel, leia o
Arquivo [CONTRIBUIÇÃO. md](https://github.com/axel-download-accelerator/axel/blob/dc10ba0c8f8d804c1568df5dba3cdd6fa89572b1/CONTRIBUTING.md); se você estiver procurando por idéias verifique o nosso
[tickets abertos](https://github.com/axel-download-accelerator/axel/issues/).

Além disso, existe uma
[grupo google](https://groups.google.com/forum/#!forum/axel-accelerator-dev) para
discutir e coordenar o desenvolvimento. Você também pode encontrar outros desenvolvedores no
Canal `#axel` no [Freenode](https://freenode.net/).

A sustentabilidade do projeto depende principalmente de desenvolvedores dedicando tempo,
então se você quiser contribuir, mas não pode codificar, há também a opção de financiar
tempo de desenvolvimento pago através de:

- *Ismael Luceno*
  + [Patrocinadores Github](https://github.com/sponsors/ismaell)
  + [[Patreon](https://c5.patreon.com/external/logo/become_a_patron_button.png)](https://www.patreon.com/ismaell)
  + [[Liberapay](https://liberapay.com/assets/widgets/donate.svg)](https://liberapay.com/ismael/donate)

<a id="installing-from-binaries"></a>
## Instalar a partir de binários
Seu sistema operacional pode conter uma versão pré-compilada do Axel, e se assim for você
Deve provavelmente usá-lo. Se o pacote está desatualizado, entre em contato com o
mantenedor de pacotes ou abrir um ticket de suporte com sua distro.

<a id="building-from-source"></a>
## Construindo a partir da fonte
AVISO: A compilação a partir do repositório de código fonte só é recomendada quando se faz
desenvolvimento, caso contrário apenas usar tarballs liberação.

O Axel usa autotools GNU para o seu buildsystem; as instruções são fornecidas no
Arquivo [INSTALAÇÃO](https://github.com/axel-download-accelerator/axel/blob/dc10ba0c8f8d804c1568df5dba3cdd6fa89572b1/INSTALL). As ações básicas para a maioria dos usuários são:

    ./configure && make && make install

Para construir sem suporte SSL/TLS, passe para `configure` a bandeira `--without-ssl`.

Se você estiver trabalhando a partir do repositório de código fonte em vez de um tarball de lançamento,
você precisa gerar o buildsystem primeiro com:

    autoreconf -i

Ao trabalhar a partir de um repositório git, o sistema de compilação detectará isso e irá
add -Werror para o CFLAGS se suportado; por isso, se você não estiver fazendo desenvolvimento você
provavelmente deve considerar passar `--disable-Werror` para `configure` para
evitar falhas de construção devido a meros avisos.

<a id="dependencies"></a>
### Dependência
* `gettext` (ou `gettext-tiny`)
* `pkg-config`

Opcional:

* `libssl` (OpenSSL, LibreSSL ou compatível) -- para suporte a SSL/TLS.

<a id="extra-dependencies-for-building-from-snapshots"></a>
#### Dependências adicionais para a construção a partir de instantâneos
* `autoconf-archive`
* `autoconf`
* `automake`
* `autopoint`
* `txt2man`

<a id="packages-on-debian-based-systems"></a>
#### Pacotes em sistemas baseados em Debian
* `build-essential`
* `autoconf`
* `autoconf-archive`
* `automake`
* `autopoint`
* `gettext`
* `libssl-dev`
* `pkg-config`
* `txt2man`


<a id="packages-on-mac-os-x-homebrew"></a>
#### Pacotes no Mac OS X (Homebrew)
* `autoconf-archive`
* `automake`
* `gettext`
* `openssl`

<a id="building-on-mac-os-x-homebrew"></a>
### Com base no Mac OS X (Homebrew)

Você precisará fornecer algumas opções extras para autotools para que ele possa encontrar gettext
e abre.

	GETTEXT=/usr/local/opt/gettext
	OPENSSL=/usr/local/opt/openssl
	PATH="$GETTEXT/bin:$PATH"

	[ -x configure ] || autoreconf -fiv -I$GETTEXT/share/aclocal/

	CFLAGS="-I$GETTEXT/include -I$OPENSSL/include" \
	LDFLAGS=-L$GETTEXT/lib ./configure

Você pode apenas executar `make` como de costume após estes passos.

<a id="related-projects-"></a>
## Projetos relacionados #

* [aria2](https://github.com/aria2/aria2)
* [hget](https://github.com/huydx/hget)
* [Iftp](https://github.com/lavv17/lftp)
* [nugget](https://github.com/maxogden/nugget)
* [pget](https://github.com/Code-Hex/pget)

<a id="license-"></a>
## Licença # #

Axel está licenciado sob GPL-2+ com a exceção OpenSSL.


---

## Procedência desta tradução

Fonte: [https://github.com/axel-download-accelerator/axel](https://github.com/axel-download-accelerator/axel/blob/dc10ba0c8f8d804c1568df5dba3cdd6fa89572b1/README.md). Licença: [GPL-2.0](../../99-Assets/upstream/axel/LICENSE.txt). Commit: dc10ba0c8f8d804c1568df5dba3cdd6fa89572b1.

O original preservado, a lista de mudanças de apresentação e os hashes constam no manifesto do projeto. Nenhum exemplo desta documentação foi executado automaticamente.
