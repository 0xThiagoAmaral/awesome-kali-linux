---
title: "subfinder — comandos essenciais upstream"
type: "cheatsheet"
tool: "subfinder"
status: "source-checked"
reviewed: "2026-10-26"
language: "pt-BR"
tags: ["cheatsheet", "tool/subfinder"]
cssclasses: ["fieldbook"]
source_commit: "98ef8711acb91f52bc27a979e6c5320a6e1365ae"
license_spdx: "MIT"
test_status: "not-executed"
source_scope: "Selected exact upstream examples; not full documentation"
---

# subfinder — comandos essenciais

Seleção de exemplos da fonte oficial fixada no commit indicado abaixo. Os blocos são transcritos sem alterações; títulos e organização são autorais em português. Esta folha complementa a documentação e não a substitui.

> Exemplos não executados nesta verificação. Caminhos, domínios e arquivos são os exemplos originais upstream. Blocos de sintaxe podem conter marcadores, prompts e argumentos que precisam ser preenchidos antes da execução.

## Navegação

[Documentação offline](subfinder-documentacao.md) · [Acervo](../../01-Maps/documentacao-offline.md).

## Consultar a ajuda

```sh
subfinder -h
```

## Filtrar subdomínios por expressão regular

```sh
subfinder -d example.com -match-regex '^(api|web)[0-9]{1,3}\.' -filter-regex '(^|\.)dev\.'
```

## Procedência

- [Fonte oficial](https://github.com/projectdiscovery/subfinder/blob/98ef8711acb91f52bc27a979e6c5320a6e1365ae/README.md).
- [Licença da fonte: MIT](../../99-Assets/upstream/subfinder/LICENSE.txt). Os exemplos mantêm essa licença; não são relicenciados como texto autoral.
- Commit: `98ef8711acb91f52bc27a979e6c5320a6e1365ae`.
- SHA-256 do documento original: `38c2ad7da121806ed1594fbfb8a6f268eb213c337a90edc2c249fd6065c49fe0`.
