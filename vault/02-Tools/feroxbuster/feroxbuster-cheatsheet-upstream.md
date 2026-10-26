---
title: "feroxbuster — comandos essenciais upstream"
type: "cheatsheet"
tool: "feroxbuster"
status: "source-checked"
reviewed: "2026-10-26"
language: "pt-BR"
tags: ["cheatsheet", "tool/feroxbuster"]
cssclasses: ["fieldbook"]
source_commit: "b07a7662d588bd8e4371e9be4704a02d976c89bb"
license_spdx: "MIT"
test_status: "not-executed"
source_scope: "Selected exact upstream examples; not full documentation"
---

# feroxbuster — comandos essenciais

Seleção de exemplos da fonte oficial fixada no commit indicado abaixo. Os blocos são transcritos sem alterações; títulos e organização são autorais em português. Esta folha complementa a documentação e não a substitui.

> Exemplos não executados nesta verificação. Caminhos, domínios e arquivos são os exemplos originais upstream. Blocos de sintaxe podem conter marcadores, prompts e argumentos que precisam ser preenchidos antes da execução.

## Navegação

[Documentação offline](feroxbuster-documentacao.md) · [Acervo](../../01-Maps/documentacao-offline.md).

## Extensões de arquivo

```text
./feroxbuster -u http://127.1 -x pdf -x js,html -x php txt json,docx
```

## Cabeçalhos HTTP

```text
./feroxbuster -u http://127.1 -H Accept:application/json "Authorization: Bearer {token}"
```

## IPv6 sem recursão

```text
./feroxbuster -u http://[::1] --no-recursion -vv
```

## Encaminhar tráfego ao proxy

```text
./feroxbuster -u http://127.1 --insecure --proxy http://127.0.0.1:8080
```

## Parâmetro na URL

```text
./feroxbuster -u http://127.1 --query token=0123456789ABCDEF
```

## Corpo JSON ou formulário

```text
./feroxbuster -u http://127.1 --data-json '{"some": "payload"}'
./feroxbuster -u http://127.1 --data-json @payload.json
./feroxbuster -u http://127.1 --data-urlencoded 'some=payload'
./feroxbuster -u http://127.1 --data-urlencoded @file.payload
```

## Procedência

- [Fonte oficial](https://github.com/epi052/feroxbuster/blob/b07a7662d588bd8e4371e9be4704a02d976c89bb/README.md).
- [Licença da fonte: MIT](../../99-Assets/upstream/feroxbuster/LICENSE.txt). Os exemplos mantêm essa licença; não são relicenciados como texto autoral.
- Commit: `b07a7662d588bd8e4371e9be4704a02d976c89bb`.
- SHA-256 do documento original: `dd28579002e3cfb0753706423e15f1671cbd27f852494879efe3cc53671a5457`.
