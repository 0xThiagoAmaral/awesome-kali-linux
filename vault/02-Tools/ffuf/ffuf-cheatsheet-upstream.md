---
title: "ffuf — comandos essenciais upstream"
type: "cheatsheet"
tool: "ffuf"
status: "source-checked"
reviewed: "2026-10-26"
language: "pt-BR"
tags: ["cheatsheet", "tool/ffuf"]
cssclasses: ["fieldbook"]
source_commit: "8d65e0373e5f223530174e5694285af849770078"
license_spdx: "MIT"
test_status: "not-executed"
source_scope: "Selected exact upstream examples; not full documentation"
---

# ffuf — comandos essenciais

Seleção de exemplos da fonte oficial fixada no commit indicado abaixo. Os blocos são transcritos sem alterações; títulos e organização são autorais em português. Esta folha complementa a documentação e não a substitui.

> Exemplos não executados nesta verificação. Caminhos, domínios e arquivos são os exemplos originais upstream. Blocos de sintaxe podem conter marcadores, prompts e argumentos que precisam ser preenchidos antes da execução.

## Navegação

[Documentação offline](ffuf-documentacao.md) · [Acervo](../../01-Maps/documentacao-offline.md).

## Descoberta de diretórios

```text
ffuf -w /path/to/wordlist -u https://target/FUZZ
```

## Virtual hosts

```text
ffuf -w /path/to/vhost/wordlist -u https://target -H "Host: FUZZ" -fs 4242
```

## Parâmetros GET

```text
ffuf -w /path/to/paramnames.txt -u https://target/script.php?FUZZ=test_value -fs 4242
```

## Limite de duração

```text
ffuf -w /path/to/wordlist -u https://target/FUZZ -maxtime 60
```

## Recursão com limite

```text
ffuf -w /path/to/wordlist -u https://target/FUZZ -maxtime-job 60 -recursion -recursion-depth 2
```

## Procedência

- [Fonte oficial](https://github.com/ffuf/ffuf/blob/8d65e0373e5f223530174e5694285af849770078/README.md).
- [Licença da fonte: MIT](../../99-Assets/upstream/ffuf/LICENSE.txt). Os exemplos mantêm essa licença; não são relicenciados como texto autoral.
- Commit: `8d65e0373e5f223530174e5694285af849770078`.
- SHA-256 do documento original: `2419b892f8a77ba3c5021300dcf5c37f2587ac9b7d579303c9add707fc0b93e4`.
