---
title: "fping6 — manual de referência"
type: "official-documentation"
tool: "fping"
status: "source-checked"
reviewed: "2026-10-26"
language: "pt-BR"
tags: ["documentation", "tool/fping"]
cssclasses: ["fieldbook"]
source_url: "https://www.fping.org/"
source_kind: "installed-kali-package"
package: "fping"
binary_version: "5.1-1"
source_package: "fping"
source_version: "5.1-1"
source_snapshot_sha256: "2089b46418648044247b1d5e894c5c7d99fd81fdcdffe2872948dab74ef6da57"
source_sha256: "51970fc71574ef3e370041c2660df7e720a2607d95a1aec7ed83ac7b52987271"
license_spdx: "LicenseRef-Fping-Stanford-Variant"
human_review: "pending"
source_scope: "Complete selected installed English manuals fping(8) and fping6(8); upstream README, websites and other documentation remain pending coverage"
binary: "fping6"
source_manual_date: "2022-02-07"
manual_section: "8"
test_status: "help-only"
tested_version: "fping6; pacote fping 5.1-1"
---

> Tradução para português produzida por assistente de IA e conferida seção por seção contra a fonte. Revisão humana independente: pendente. Opções e exemplos originais foram preservados; nenhum exemplo foi executado automaticamente.

> **Compatibilidade observada:** fping6; pacote fping 5.1-1. Confirmado que fping6 é link simbólico para o executável fping nesta instalação. A página de compatibilidade não lista opções; a listagem do executável não foi tratada como opções omitidas dessa página. Somente ajuda e versão foram executadas, sem alvo. [Evidência e limites do teste](../../99-Assets/evidence/fping6-help-tests.json).

<!-- SPDX-License-Identifier: LicenseRef-Fping-Stanford-Variant -->
> **Reconhecimento da licença:** This software was developed by Stanford University.

# fping6

<a id="name"></a>
## NOME

fping6 - compatibilidade retroativa com fping anterior à versão 4.0

<a id="synopsis"></a>
## SINOPSE

```text
fping6 [ options ] [ systems... ]
```

<a id="description"></a>
## DESCRIÇÃO

fping6 é um link simbólico de compatibilidade retroativa para fping, destinado exclusivamente a permitir configurações remotas do Smokeping que funcionem tanto em sistemas com fping ≥ 4.0 quanto em sistemas com fping < 4.0.

Não use fping em scripts ou configurações que não exijam essa compatibilidade com versões antigas. Ele desaparecerá assim que não for mais necessário nas configurações mencionadas acima.

> **Nota editorial:** o original escreve "fping in in" nesta advertência, embora a página trate de `fping6`. O nome citado foi mantido; a frase é uma declaração histórica da fonte, não a confirmação de uma data de remoção.

<a id="see-also"></a>
## VEJA TAMBÉM

fping(8)

<a id="author"></a>
## AUTOR

Esta página de manual foi escrita por Axel Beckert <abe@debian.org> para o Projeto Debian, mas pode ser usada por outros.


---

## Procedência desta tradução

Fonte primária: [manual preservado](../../../sources/upstream/fping/fping6.8.source), extraído de `/usr/share/man/man8/fping6.8.gz`. Pacote `fping`, versão `5.1-1`; pacote-fonte `fping`, versão `5.1-1`. Aquisição de pacote instalado, sem atribuição de commit Git.

Licença: [LicenseRef-Fping-Stanford-Variant](../../99-Assets/upstream/fping/LICENSE.txt); [copyright e condições do pacote](../../99-Assets/upstream/fping/COPYRIGHT.package.txt). [Página de referência do pacote, não a origem exata do arquivo](https://www.fping.org/). Hashes do original, gzip e avisos no registro de fontes. A data do manual é histórica; não implica que todos os serviços externos mantenham esse comportamento.
