---
title: "above — comandos essenciais upstream"
type: "cheatsheet"
tool: "above"
status: "source-checked"
reviewed: "2026-10-26"
language: "pt-BR"
tags: ["cheatsheet", "tool/above"]
cssclasses: ["fieldbook"]
source_commit: "313f550ebb87d815aeece6792104b8c3f2a9db8f"
license_spdx: "Apache-2.0"
test_status: "not-executed"
source_scope: "Selected exact upstream examples; not full documentation"
---

# above — comandos essenciais

Seleção de exemplos da fonte oficial fixada no commit indicado abaixo. Os blocos são transcritos sem alterações; títulos e organização são autorais em português. Esta folha complementa a documentação e não a substitui.

> Exemplos não executados nesta verificação. Caminhos, domínios e arquivos são os exemplos originais upstream. Blocos de sintaxe podem conter marcadores, prompts e argumentos que precisam ser preenchidos antes da execução.

## Navegação

[Documentação offline](above-documentacao.md) · [Acervo](../../01-Maps/documentacao-offline.md).

## Captura por interface e duração

```bash
caster@kali:~$ sudo above --interface eth0 --timer 120
```

## Gravar a captura

```bash
caster@kali:~$ sudo above --interface eth0 --timer 120 --output above.pcap
```

## Analisar uma captura existente

```bash
caster@kali:~$ above --input hsrp.cap
```

## Identificar segmentos VLAN

```bash
caster@kali:~$ sudo above --interface eth0 --search-vlan 
```

## Procedência

- [Fonte oficial](https://github.com/caster0x00/Above/blob/313f550ebb87d815aeece6792104b8c3f2a9db8f/README.md).
- [Licença da fonte: Apache-2.0](../../99-Assets/upstream/above/LICENSE.txt). Os exemplos mantêm essa licença; não são relicenciados como texto autoral.
- Commit: `313f550ebb87d815aeece6792104b8c3f2a9db8f`.
- SHA-256 do documento original: `7dec6e01263ed4064e2ba2428c1e6a011b0a17539db14b3c88da2df90d02633e`.
