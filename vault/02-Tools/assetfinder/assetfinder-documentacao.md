---
title: "assetfinder — documentação oficial"
type: "official-documentation"
tool: "assetfinder"
status: "translated-machine"
reviewed: "2026-10-26"
language: "pt-BR"
tags: ["documentation", "tool/assetfinder"]
cssclasses: ["fieldbook"]
source_url: "https://github.com/tomnomnom/assetfinder/blob/4e95d8701aae8cff1c27af2626eb22ba110ad583/README.md"
source_commit: "4e95d8701aae8cff1c27af2626eb22ba110ad583"
source_sha256: "6a5f2f6b3beb4e8510d234392001dd8059b49dd334719203980f039a588cf063"
license_spdx: "MIT"
human_review: "pending"
source_scope: "Official English repository README/docs and available upstream Portuguese README; external manuals/wiki coverage tracked separately"
---

> Tradução automática local para português, ainda sem revisão humana integral. Estrutura e blocos de código preservados; referências externas não significam conteúdo espelhado.

# assetfinder

Encontre domínios e subdomínios potencialmente relacionados a um dado domínio.


<a id="install"></a>
## Instalar

Se tiver o Go instalado e configurado (ou seja, com o `$GOPATH/bin` no seu `$PATH`):

```text
go get -u github.com/tomnomnom/assetfinder
```

Caso contrário, [baixar um lançamento para sua plataforma](https://github.com/tomnomnom/assetfinder/releases).
Para facilitar a execução, você pode colocar o binário no seu `$PATH`.

<a id="usage"></a>
## Uso

```text
assetfinder [--subs-only] <domain>
```

<a id="sources"></a>
## Fontes

Por favor, sinta-se livre para emitir pedidos com novas fontes! :)

<a id="implemented"></a>
### Implementação
* crt.sh
* certspotter
* alvo hacker
* ameaturecrowd
* máquina wayback
* dns.bufferover.run
* facebook
    * Needs `FB_APP_ID` and `FB_APP_SECRET` environment variables set (https://developers.facebook.com/)
    * You need to be careful with your app's rate limits
* virustotal
    * Needs `VT_API_KEY` environment variable set (https://developers.virustotal.com/reference)
* findsubdomínios
    * Needs `SPYSE_API_TOKEN` environment variable set (the free version always gives the first response page, and you also get "25 unlimited requests") — (https://spyse.com/apidocs)

<a id="sources-to-be-implemented"></a>
### Fontes a implementar
* http://api.passivetotal.org/api/docs/
* https://community.riskiq.com/ (?)
* https://riddler.io/
* http://www.dnsdb.org/
* https://certdb.com/api-documentation

## TODO
* Bandeiras para controlar as fontes utilizadas
    * Likely to be all on by default and a flag to disable
* Ler os domínios do stdin


---

## Procedência desta tradução

Fonte: [https://github.com/tomnomnom/assetfinder](https://github.com/tomnomnom/assetfinder/blob/4e95d8701aae8cff1c27af2626eb22ba110ad583/README.md). Licença: [MIT](../../99-Assets/upstream/assetfinder/LICENSE.txt). Commit: 4e95d8701aae8cff1c27af2626eb22ba110ad583.

O original preservado, a lista de mudanças de apresentação e os hashes constam no manifesto do projeto. Nenhum exemplo desta documentação foi executado automaticamente.
