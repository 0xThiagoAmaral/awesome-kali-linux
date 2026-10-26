<!-- SPDX-License-Identifier: LicenseRef-Fping-Stanford-Variant -->
> **Reconhecimento da licença:** This software was developed by Stanford University.

# fping6

## NOME

fping6 - compatibilidade retroativa com fping anterior à versão 4.0

## SINOPSE

```text
fping6 [ options ] [ systems... ]
```

## DESCRIÇÃO

fping6 é um link simbólico de compatibilidade retroativa para fping, destinado exclusivamente a permitir configurações remotas do Smokeping que funcionem tanto em sistemas com fping ≥ 4.0 quanto em sistemas com fping < 4.0.

Não use fping em scripts ou configurações que não exijam essa compatibilidade com versões antigas. Ele desaparecerá assim que não for mais necessário nas configurações mencionadas acima.

> **Nota editorial:** o original escreve "fping in in" nesta advertência, embora a página trate de `fping6`. O nome citado foi mantido; a frase é uma declaração histórica da fonte, não a confirmação de uma data de remoção.

## VEJA TAMBÉM

fping(8)

## AUTOR

Esta página de manual foi escrita por Axel Beckert <abe@debian.org> para o Projeto Debian, mas pode ser usada por outros.
