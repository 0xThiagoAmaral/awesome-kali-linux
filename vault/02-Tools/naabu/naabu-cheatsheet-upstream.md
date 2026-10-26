---
title: "naabu — comandos essenciais upstream"
type: "cheatsheet"
tool: "naabu"
status: "source-checked"
reviewed: "2026-10-26"
language: "pt-BR"
tags: ["cheatsheet", "tool/naabu"]
cssclasses: ["fieldbook"]
source_commit: "a4df9f40ba77bd08920bd47c2adf9f5939edcebb"
license_spdx: "MIT"
test_status: "not-executed"
source_scope: "Selected exact upstream examples; not full documentation"
---

# naabu — comandos essenciais

Seleção de exemplos da fonte oficial fixada no commit indicado abaixo. Os blocos são transcritos sem alterações; títulos e organização são autorais em português. Esta folha complementa a documentação e não a substitui.

> Exemplos não executados nesta verificação. Caminhos, domínios e arquivos são os exemplos originais upstream. Blocos de sintaxe podem conter marcadores, prompts e argumentos que precisam ser preenchidos antes da execução.

## Navegação

[Documentação offline](naabu-documentacao.md) · [Acervo](../../01-Maps/documentacao-offline.md).

## Consultar a ajuda

```sh
naabu -h
```

## Um host de entrada

```sh
naabu -host hackerone.com
```

## Selecionar portas TCP e UDP

```sh
naabu -p 80,443,21-23,u:53 -host hackerone.com
```

## Ler uma lista de hosts

```sh
naabu -list hosts.txt
```

## Identificar versões de serviços

```sh
naabu -host scanme.sh -sV
```

## Sondas de serviços UDP

```sh
naabu -host scanme.sh -p u:53,u:123,u:161 -uP
```

## Procedência

- [Fonte oficial](https://github.com/projectdiscovery/naabu/blob/a4df9f40ba77bd08920bd47c2adf9f5939edcebb/README.md).
- [Licença da fonte: MIT](../../99-Assets/upstream/naabu/LICENSE.txt). Os exemplos mantêm essa licença; não são relicenciados como texto autoral.
- Commit: `a4df9f40ba77bd08920bd47c2adf9f5939edcebb`.
- SHA-256 do documento original: `f61b2cfdd205798a236715d3a20ef54ffaa2e7ac7f5880b0f9170b1bfcb62180`.
