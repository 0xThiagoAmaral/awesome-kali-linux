---
title: "nuclei — comandos essenciais upstream"
type: "cheatsheet"
tool: "nuclei"
status: "source-checked"
reviewed: "2026-10-26"
language: "pt-BR"
tags: ["cheatsheet", "tool/nuclei"]
cssclasses: ["fieldbook"]
source_commit: "263bc134120af1548023c23a9b55ec14f9217295"
license_spdx: "MIT"
test_status: "not-executed"
source_scope: "Selected exact upstream examples; not full documentation"
---

# nuclei — comandos essenciais

Seleção de exemplos da fonte oficial fixada no commit indicado abaixo. Os blocos são transcritos sem alterações; títulos e organização são autorais em português. Esta folha complementa a documentação e não a substitui.

> Exemplos não executados nesta verificação. Caminhos, domínios e arquivos são os exemplos originais upstream. Blocos de sintaxe podem conter marcadores, prompts e argumentos que precisam ser preenchidos antes da execução.

## Navegação

[Documentação offline](nuclei-documentacao.md) · [Acervo](../../01-Maps/documentacao-offline.md).

## Consultar as opções

```sh
nuclei -h
```

## Um endereço de entrada

```sh
nuclei -target https://example.com
```

## Lista de endereços

```sh
nuclei -list urls.txt
```

## Template personalizado

```sh
nuclei -u https://example.com -t /path/to/your-template.yaml
```

## Procedência

- [Fonte oficial](https://github.com/projectdiscovery/nuclei/blob/263bc134120af1548023c23a9b55ec14f9217295/README.md).
- [Licença da fonte: MIT](../../99-Assets/upstream/nuclei/LICENSE.txt). Os exemplos mantêm essa licença; não são relicenciados como texto autoral.
- Commit: `263bc134120af1548023c23a9b55ec14f9217295`.
- SHA-256 do documento original: `d9fa7d06e5c6fc9734f84521c72b1959a27b0bc39752bf1c36f4fbfb321bde07`.
