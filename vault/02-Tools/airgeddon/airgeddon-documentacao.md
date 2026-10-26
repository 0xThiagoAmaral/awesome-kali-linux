---
title: "airgeddon — documentação oficial"
type: "official-documentation"
tool: "airgeddon"
status: "translated-machine"
reviewed: "2026-10-26"
language: "pt-BR"
tags: ["documentation", "tool/airgeddon"]
cssclasses: ["fieldbook"]
source_url: "https://github.com/v1s1t0r1sh3r3/airgeddon/blob/700ad7d63df04e565bcd14d2aec6f935fcec5185/README.md"
source_commit: "700ad7d63df04e565bcd14d2aec6f935fcec5185"
source_sha256: "c47046de73be7b4562376e5cb195ad2b08b23ba3aa758b7d2de61277f14c78f2"
license_spdx: "GPL-3.0"
human_review: "pending"
source_scope: "Official English repository README/docs and available upstream Portuguese README; external manuals/wiki coverage tracked separately"
---

> Tradução automática local para português, ainda sem revisão humana integral. Estrutura e blocos de código preservados; referências externas não significam conteúdo espelhado.

# airgeddon
[![Version-shield]](https://raw.githubusercontent.com/v1s1t0r1sh3r3/airgeddon/master/CHANGELOG.md) [![Bash4.2-shield]](http://tldp.org/LDP/abs/html/bashver4.html#AEN21220) [![License-shield]](https://raw.githubusercontent.com/v1s1t0r1sh3r3/airgeddon/master/LICENSE.md) [![Docker-shield]](https://github.com/v1s1t0r1sh3r3/airgeddon/actions/worklows/master.yml) [![Discord-shield]](https://discord.gg/sQ9dgt9)

[![Paypal-shield]](https://www.paypal.com/paypalme/airgeddon) [![Cryptocurrencies-shield]](https://github.com/v1s1t0r1sh3r3/airgeddon/wiki/Contributing-&-Code-of-Conduct)


> Este é um script bash multi-uso para sistemas Linux para auditar redes sem fio.

[Banner]

---

Todas as informações necessárias sobre como "instalar o uso do `airgeddon`" estão presentes no Wiki [GitHub].

- *I. Conteúdo e funcionalidades*
  - [Home]
  - [Características]
  - [Screenshots]
  - [Papel de parede]


- *II. Requisitos*
  - [Requisitos]
  - [Compatibilidade]
	 - [Cards and Chipsets]
	 - [Wayland]
	 - [Consistent Network Device Naming]
	 - [Kali Nethunter]
  - [Ferramentas Essenciais]
  - [Ferramentas Opcionais]
	 - [BeEF Tips]
	 - [Hashcat Tips]
	 - [Bettercap Tips]
  - [Atualizar ferramentas]
  - [Ferramentas Internas]
  - [Conhecida incompatibilidades]


- *III. Começar*
  - [Instalação e Uso]
  - [Opções]
  - [Docker]
	 - [Linux]
	 - [Mac OSX]
	 - [Windows]
  - [Outras fontes]
  - [FAQ e solução de problemas]


- *IV. Learning*
  - [Certificação CWP]


- *V. Projeto e Desenvolvimento*
  - [Site oficial]
  - [Sistema de Plugins]
	 - [Plugins development]
	 - [Plugins Hall of Fame]
  - [Línguas Suportadas]
  - [Contribuir & Código de Conduta]
  - [Política de segurança]
  - [Merchandising Loja Online]
  - [Changelog]
  - [Disclaimer & Licença]
  - [Contacto]


- *VI. Agradecimentos e Referências*
  - [Ponto para chapéu]
  - [Inspiração]

---

https://raw.githubusercontent.com/v1s1t0r1sh3r3/airgeddon/master/imgs/banners/airgeddon_banner.png "Nós conquistaremos a Terra!"
[ Wiki do GitHub]: https://github.com/v1s1t0r1sh3r3/airgeddon/wiki

[Home]: https://github.com/v1s1t0r1sh3r3/airgeddon/wiki
[Recursos]: https://github.com/v1s1t0r1sh3r3/airgeddon/wiki/Features
[Gritos]: https://github.com/v1s1t0r1sh3r3/airgeddon/wiki/Screenshots
[Papéis]: https://github.com/v1s1t0r1sh3r3/airgeddon/wiki/Wallpapers
[Requisitos]: https://github.com/v1s1t0r1sh3r3/airgeddon/wiki/Requirements
[Compatibilidade]: https://github.com/v1s1t0r1sh3r3/airgeddon/wiki/Compatibility
[Cartões e fichas]: https://github.com/v1s1t0r1sh3r3/airgeddon/wiki/Cards%20and%20Chipsets
[Wayland]: https://github.com/v1s1t0r1sh3r3/airgeddon/wiki/Wayland
[Nome do dispositivo de rede consistente]: https://github.com/v1s1t0r1sh3r3/airgeddon/wiki/Consistent%20Network%20Device%20Naming
[Kali Nethunter]: https://github.com/v1s1t0r1sh3r3/airgeddon/wiki/Kali%20Nethunter
[Ferramentas Essenciais]: https://github.com/v1s1t0r1sh3r3/airgeddon/wiki/Essential%20Tools
[Ferramentas Opcionais]: https://github.com/v1s1t0r1sh3r3/airgeddon/wiki/Optional%20Tools
[Dicas BeEF]: https://github.com/v1s1t0r1sh3r3/airgeddon/wiki/BeEF%20Tips
[Dicas de gato]: https://github.com/v1s1t0r1sh3r3/airgeddon/wiki/Hashcat%20Tips
[Dicas para melhor uso]: https://github.com/v1s1t0r1sh3r3/airgeddon/wiki/Bettercap%20Tips
[Atualizar Ferramentas]: https://github.com/v1s1t0r1sh3r3/airgeddon/wiki/Update%20Tools
[Ferramentas internas]: https://github.com/v1s1t0r1sh3r3/airgeddon/wiki/Internal%20Tools
[Conhecidos incompatibilidades]: https://github.com/v1s1t0r1sh3r3/airgeddon/wiki/Known%20incompatibilities
[Instalação & Utilização]: https://github.com/v1s1t0r1sh3r3/airgeddon/wiki/Installation%20&%20Usage
[Opções]: https://github.com/v1s1t0r1sh3r3/airgeddon/wiki/Options
[Docker]: https://github.com/v1s1t0r1sh3r3/airgeddon/wiki/Docker
[Linux]: https://github.com/v1s1t0r1sh3r3/airgeddon/wiki/Docker%20Linux
[Mac OSX]: https://github.com/v1s1t0r1sh3r3/airgeddon/wiki/Docker%20Mac%20OSX
[Windows]: https://github.com/v1s1t0r1sh3r3/airgeddon/wiki/Docker%20Windows
[Outras fontes]: https://github.com/v1s1t0r1sh3r3/airgeddon/wiki/Other%20Sources
[FAQ & Resolução de Problemas]: https://github.com/v1s1t0r1sh3r3/airgeddon/wiki/FAQ%20&%20Troubleshooting
[Certificação PCP]: https://github.com/v1s1t0r1sh3r3/airgeddon/wiki/CWP%20Certification
[Sistema de Plugins]: https://github.com/v1s1t0r1sh3r3/airgeddon/wiki/Plugins%20System
[Desenvolvimento de Plugins]: https://github.com/v1s1t0r1sh3r3/airgeddon/wiki/Plugins%20Development
[Plugins Hall of Fame]: https://github.com/v1s1t0r1sh3r3/airgeddon/wiki/Plugins%20Hall%20of%20Fame
[Línguas suportadas]: https://github.com/v1s1t0r1sh3r3/airgeddon/wiki/Supported%20Languages
[Contribuindo & Código de Conduta]: https://github.com/v1s1t0r1sh3r3/airgeddon/wiki/Contributing-&-Code-of-Conduct
[Política de segurança]: https://github.com/v1s1t0r1sh3r3/airgeddon/security/policy
[Merchandising Online Shop]: https://airgeddon.creator-spring.com/
[Alteração]: https://github.com/v1s1t0r1sh3r3/airgeddon/wiki/Changelog
[Licença & Renúncia]: https://github.com/v1s1t0r1sh3r3/airgeddon/wiki/Disclaimer%20&%20License
[Contato]: https://github.com/v1s1t0r1sh3r3/airgeddon/wiki/Contact
[Dica do chapéu para]: https://github.com/v1s1t0r1sh3r3/airgeddon/wiki/Hat%20Tip%20To
[Inspiração]: https://github.com/v1s1t0r1sh3r3/airgeddon/wiki/Inspiration
[Site oficial]: https://airgeddon.pro/

[Version-shield]: https://img.shields.io/badge/version-12.02-blue.svg?style=flat-square&colorA=273133&colorB=0093ee "Última versão"
[Bash4.2-shield]: https://img.shields.io/badge/bash-4.2%2B-blue.svg?style=flat-square&colorA=273133&colorB=00db00 "Bash 4.2 ou mais tarde"
https://img.shields.io/badge/license-GPL%20v3%2B-blue.svg?style=flat-square&colorA=273133&colorB=bd0000 "GPL v3+"
https://github.com/v1s1t0r1sh3r3/airgeddon/actions/workflows/master.yml/badge.svg?branch=master "Docker CI master"
[Discord-shield]: https://img.shields.io/discord/629812069964840991.svg?style=flat-square&colorA=273133&colorB=CBA317&logo=discord&label=Discord%20chat
https://img.shields.io/badge/donate-paypal-blue.svg?style=flat-square&colorA=273133&colorB=b008bb "Paypal"
[Cryptocurrencies-shield]: https://img.shields.io/badge/donate-cryptocurrencies-blue.svg?style=flat-square&colorA=273133&colorB=f7931a "Cryptocurrencies"


---

## Procedência desta tradução

Fonte: [https://github.com/v1s1t0r1sh3r3/airgeddon](https://github.com/v1s1t0r1sh3r3/airgeddon/blob/700ad7d63df04e565bcd14d2aec6f935fcec5185/README.md). Licença: [GPL-3.0](../../99-Assets/upstream/airgeddon/LICENSE.txt). Commit: 700ad7d63df04e565bcd14d2aec6f935fcec5185.

O original preservado, a lista de mudanças de apresentação e os hashes constam no manifesto do projeto. Nenhum exemplo desta documentação foi executado automaticamente.
