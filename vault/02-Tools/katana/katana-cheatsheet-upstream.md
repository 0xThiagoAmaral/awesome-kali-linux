---
title: "katana — comandos essenciais upstream"
type: "cheatsheet"
tool: "katana"
status: "source-checked"
reviewed: "2026-10-26"
language: "pt-BR"
tags: ["cheatsheet", "tool/katana"]
cssclasses: ["fieldbook"]
source_commit: "4b41dd02a095df15ae0cd04cbb658af457d3c1ab"
license_spdx: "MIT"
test_status: "not-executed"
source_scope: "Selected exact upstream examples; not full documentation"
---

# katana — comandos essenciais

Seleção de exemplos da fonte oficial fixada no commit indicado abaixo. Os blocos são transcritos sem alterações; títulos e organização são autorais em português. Esta folha complementa a documentação e não a substitui.

> Exemplos não executados nesta verificação. Caminhos, domínios e arquivos são os exemplos originais upstream. Blocos de sintaxe podem conter marcadores, prompts e argumentos que precisam ser preenchidos antes da execução.

## Navegação

[Documentação offline](katana-documentacao.md) · [Acervo](../../01-Maps/documentacao-offline.md).

## Consultar a ajuda

```console
katana -h
```

## Um endereço de entrada

```sh
katana -u https://tesla.com
```

## Lista de endereços

```text
katana -list url_list.txt
```

## Profundidade de navegação

```text
katana -u https://tesla.com -d 5
```

## Análise de JavaScript

```text
katana -u https://tesla.com -jc
```

## Limite de requisições

```text
katana -u https://tesla.com -rl 100
```

## Salvar endereços

```console
katana -u https://example.com -no-scope -output example_endpoints.txt
```

## Procedência

- [Fonte oficial](https://github.com/projectdiscovery/katana/blob/4b41dd02a095df15ae0cd04cbb658af457d3c1ab/README.md).
- [Licença da fonte: MIT](../../99-Assets/upstream/katana/LICENSE.txt). Os exemplos mantêm essa licença; não são relicenciados como texto autoral.
- Commit: `4b41dd02a095df15ae0cd04cbb658af457d3c1ab`.
- SHA-256 do documento original: `7f6cf81d98053ab01a802aecb0bf3f01fca797e7b0313b82f692625959188c5b`.
