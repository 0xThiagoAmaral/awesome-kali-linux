---
title: "gobuster — comandos essenciais upstream"
type: "cheatsheet"
tool: "gobuster"
status: "source-checked"
reviewed: "2026-10-26"
language: "pt-BR"
tags: ["cheatsheet", "tool/gobuster"]
cssclasses: ["fieldbook"]
source_commit: "c77583fbb8824058d74d38240896eff610683c8e"
license_spdx: "Apache-2.0"
test_status: "not-executed"
source_scope: "Selected exact upstream examples; not full documentation"
---

# gobuster — comandos essenciais

Seleção de exemplos da fonte oficial fixada no commit indicado abaixo. Os blocos são transcritos sem alterações; títulos e organização são autorais em português. Esta folha complementa a documentação e não a substitui.

> Exemplos não executados nesta verificação. Caminhos, domínios e arquivos são os exemplos originais upstream. Blocos de sintaxe podem conter marcadores, prompts e argumentos que precisam ser preenchidos antes da execução.

## Navegação

[Documentação offline](gobuster-documentacao.md) · [Acervo](../../01-Maps/documentacao-offline.md).

## Ajuda por modo

```bash
gobuster help                   # Show general help
gobuster help [mode]            # Show help for specific mode
gobuster [mode] --help          # Alternative help syntax
```

## Diretórios

```bash
gobuster dir -u https://example.com -w wordlist.txt
```

## Subdomínios DNS

```bash
gobuster dns -do example.com -w wordlist.txt
```

## Virtual hosts

```bash
gobuster vhost -u https://example.com --append-domain -w wordlist.txt
```

## Fuzzing de parâmetros

```bash
gobuster fuzz -u https://example.com?FUZZ=test -w wordlist.txt
```

## Gravar resultados

```bash
# Save results to file
gobuster dir -u https://example.com -w wordlist.txt -o results.txt

# Use quiet mode for clean output
gobuster dir -u https://example.com -w wordlist.txt -q
```

## Procedência

- [Fonte oficial](https://github.com/OJ/gobuster/blob/c77583fbb8824058d74d38240896eff610683c8e/README.md).
- [Licença da fonte: Apache-2.0](../../99-Assets/upstream/gobuster/LICENSE.txt). Os exemplos mantêm essa licença; não são relicenciados como texto autoral.
- Commit: `c77583fbb8824058d74d38240896eff610683c8e`.
- SHA-256 do documento original: `9c5b67cdd42cd59eb9d4c3c0ed9c90aae05fce56803ff92d81e8fd097a6fff0d`.
