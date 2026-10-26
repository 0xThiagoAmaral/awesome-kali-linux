---
title: "aflplusplus — documentação oficial"
type: "official-documentation"
tool: "aflplusplus"
status: "translated-machine"
reviewed: "2026-10-26"
language: "pt-BR"
tags: ["documentation", "tool/aflplusplus"]
cssclasses: ["fieldbook"]
source_url: "https://github.com/AFLplusplus/AFLplusplus/blob/d0070729206a80a9af297b2341edd63f68fdac35/docs/FrameShift.md"
source_commit: "d0070729206a80a9af297b2341edd63f68fdac35"
source_sha256: "3da15c4dc3621b7c3843cc6b7880d9db7ffec7860444d0c5a0cfd60fc482fdab"
license_spdx: "AGPL-3.0-or-later"
human_review: "pending"
source_scope: "Repository root README and owned doc/docs/documentation Markdown or RST files; not a claim of full wiki/site coverage"
---

> Tradução automática local para português, ainda sem revisão humana integral. Estrutura e blocos de código preservados; referências externas não significam conteúdo espelhado.

# FrameShift – Automatic Size/Offset Field Tracking for AFL++

FrameShift é uma etapa de análise **runtime** em AFL++ que descobre automaticamente
campos de tamanho e offset em entradas binárias estruturadas e os mantém consistentes como
as mutações devastadoras inserem ou apagam bytes.

Muitos formatos binários (ELF, PNG, PDF, buffers de protocolo, codificações TLV, ...) incorporar
campos de comprimento ou deslocamento que descrevem o layout dos dados que se seguem. Quando
um fuzzer insere ou remove bytes cegamente, estes campos tornam-se obsoletos e o
O analisador do alvo rejeita a entrada muito antes de atingir o código mais profundo. FrameShift
resolve isto por:

1. **Discovering** que bytes em uma entrada funcionam como campos de tamanho/offset.
2. **Tracking** como as mutações em fase de destruição (inserções e deleções) afectam
Aqueles campos.
3. **Sanitising** o buffer mutado para que cada campo rastreado seja atualizado para
refletir o novo layout antes da execução do caso de teste.

Isto é totalmente automático -- nenhuma especificação de formato, gramática ou mutador personalizado
é necessário.

* Detalhes e avaliações mais abrangentes em nosso trabalho de pesquisa: [FrameShift: Aprendendo a redimensionar entradas de fuzzer sem quebrá-los](https://arxiv.org/abs/2507.05421v1)

<a id="how-it-works"></a>
## Como funciona

<a id="discovery-the-frameshift-stage"></a>
### Descoberta (a etapa de mudança de quadro)

Quando o afl- fuzz escolhe pela primeira vez um item de fila que ainda não foi analisado, ele é executado
o estágio **frameshift** antes do loop de destruição. O estágio funciona da seguinte forma:

1. **Baseline coverage** -- Execute a entrada e registro originais que cobrem
os índices do mapa são atingidos. Subtraia os índices que também são atingidos por um trivial
entrada inválida (um único byte `"a"`) para isolar a cobertura exclusiva da corrente
Caso de teste.

2. **Candidate scan** -- Para cada deslocamento de byte na entrada, tente interpretar
os bytes nessa posição como um valor u8, u16, u32, ou u64 em ambos
e ordem big- endian (maior primeiro). Se o valor descodificado não for zero e
não excede o comprimento de entrada, é um campo de tamanho/offset plausível.

3. **Loss test** -- Corrompe o campo candidato (adiciona uma quantidade de deslocamento ao seu
valor) e re-executar o input. Se mais de 5% da cobertura de base
índices são perdidos, o campo pode ser estrutural.

4. **Anchor search** -- Para determinar *where* bytes devem ser contados a partir de, o
fase tenta vários pontos âncora. Para cada âncora candidata, constrói uma
caso de teste com o valor do campo atualizado e bytes de enchimento inseridos no
ponto de inserção correspondente. Se a inserção **Recovers** mais de 20%
a cobertura perdida, o triplo (campo, âncora, ponto de inserção)
um **relation**.

5. **Iteration** -- A pesquisa repete (até 10 iterações) porque descobrindo
uma relação pode desbloquear posições que estavam anteriormente dentro de um rastreado
Campo.

Cada entrada analisada recebe uma `fs_meta_t` per-queue que armazena todas as descobertas
relações. Os campos já analisados estão marcados em um bitmap de pontos bloqueados para que eles
não são re-testados.

<a id="tracking-during-havoc"></a>
### Rastreamento (durante a destruição)

Durante os estágios de destruição e splice, cada mutação de inserção e deleção é
reportado ao rastreador de relações:

- **Inserções** ajuste `pos`, `anchor`, `insert` e `val` de cada relação
que abrange a região afectada.
- **Deleções** fazem o mesmo ao contrário, encolhendo os intervalos relevantes.

Se uma mutação quebrar uma relação (por exemplo, inserir dentro de um campo rastreado),
Essa relação está desactivada durante o resto da ronda de destruição actual.

<a id="sanitization-before-execution"></a>
### Saneamento (antes da execução)

Após todas as mutações numa única iteração de destruição, `fs_sanitize()`
escreve os valores atualizados do campo de volta para o buffer. Isto significa que o alvo vê
uma entrada cujos campos de tamanho/offset sejam consistentes com a disposição real do byte,
aumentando drasticamente a chance de alcançar código de processamento profundo.

No início de cada nova iteração de estragos, os metadados da relação são restaurados para
o seu estado original, para que as relações nunca se percam permanentemente.

<a id="relation-model"></a>
## Modelo de relação

Um campo de relação é descrito por quatro valores dinâmicos:

|Campo|Significado|
|----------|---------|
|`pos`|Deslocamento do bytes do campo tamanho/offset na entrada.|
|`val`|Valor numérico atual do campo.|
|`anchor`|O ponto de referência a partir do qual a distância é medida.|
|`insert`|O ponto no qual bytes inseridos são contados em direção ao valor do campo.|

Juntamente com atributos fixos:

|Campo|Significado|
|--------|---------|
|`size`|Largura do campo em bytes (1, 2, 4 ou 8).|
|`le`|Se o campo é pequeno (`1`) ou big-end (`0`).|

Quando os bytes são inseridos entre `anchor` e `insert`, o valor do campo é
incrementado pelo tamanho da inserção. Quando os bytes são removidos daquela região, o
O valor do campo é decrementado.

<a id="environment-variables"></a>
## Variáveis de ambiente

- **`AFL_FRAMESHIFT_DISABLE`** -- Definir para `1` para desativar o estágio de mudança de quadro e
todo o acompanhamento de relação inteiramente. Útil para alvos que não consomem
formatos binários estruturados, ou quando você quiser eliminar a sobrecarga de análise.

- **`AFL_FRAMESHIFT_MAX_OVERHEAD`** -- Uma flutuação entre `0.0` e `1.0` (padrão
`0.10`, ou seja, 10%) que cobre a fração do tempo total de fuzzing o deslocamento de quadro
análise é permitida para consumir. É aplicada como um balde de fichas: crédito
acumula como esta fração do tempo total de execução e cada fatia de análise gasta de
uma nova fatia é admitido apenas quando o crédito restante cobre pelo menos
`FRAMESHIFT_MIN_SLICE_MS`, e o prazo de corte é limitado ao restante
crédito, de modo que uma única fatia não pode ultrapassar a sobrecarga configurada por um
`FRAMESHIFT_TIME_BUDGET_MS` (que anteriormente permitia quase dois segundos
ultrapassada no início da campanha). Configure em `0.0` para desativar a análise, ou aumentar
para `1.0` para análise completa ao custo de menos execuções de destruição.

<a id="compile-time-constants"></a>
## Constantes de tempo de compilação

As seguintes constantes são definidas em `src/afl-fuzz-frameshift.c` e podem ser
ajustado pela edição da fonte:

|Constante|Predefinição|Significado|
|----------|---------|---------|
|`FRAMESHIFT_MAX_ITERS`|10|Iterações máximas de descoberta por entrada.|
|`FRAMESHIFT_LOSS_PCT`|5|Perda mínima de cobertura (%) para considerar um campo estrutural.|
|`FRAMESHIFT_RECOVER_PCT`|20|Recuperação mínima de cobertura (%) para aceitar uma âncora.|
|`FRAMESHIFT_TIME_BUDGET_MS`|2000|Difícil limite superior em uma única fatia de análise (ms); uma fatia admitida é tampado para o menor deste eo restante crédito de sobrecarga.|
|`FRAMESHIFT_MIN_SLICE_MS`|200|A menor fatia que vale a pena admitir (ms); abaixo disso a entrada é deixada sem análise até que mais crédito overhead adquira.|

<a id="when-to-use-frameshift"></a>
## Quando usar o FrameShift

FrameShift é **enabled por padrão** e é mais eficaz para:

- Formatos binários com comprimentos incorporados (TLV, codificações em blocos, contentor)
formatos).
- Protocolos de rede com mensagens prefixadas com comprimento.
- Qualquer alvo onde inserir ou excluir bytes faz com que o analisador salte para fora
cedo porque um campo de tamanho ou offset já não corresponde.

Overhead em alvos não estruturados é mínimo na prática, mas pode ser evitado completamente definindo `AFL_FRAMESHIFT_DISABLE=1`.

<a id="source-files"></a>
## arquivos de código

|arquivo|Sumário|
|------|----------|
|`src/afl-fuzz-frameshift.c`|Estágio de descoberta, rastreamento de relações, higienização.|
|`include/afl-fuzz.h`|`fs_relation_t`, `fs_meta_t`, `frameshift_stats` definições.|
|`src/afl-fuzz-one.c`|Integração com o loop de destruição/espelho.|


---

## Procedência desta tradução

Fonte: [https://github.com/AFLplusplus/AFLplusplus](https://github.com/AFLplusplus/AFLplusplus/blob/d0070729206a80a9af297b2341edd63f68fdac35/docs/FrameShift.md). Licença: [AGPL-3.0-or-later](../../99-Assets/upstream/aflplusplus/LICENSE.txt). Commit: d0070729206a80a9af297b2341edd63f68fdac35.

O original preservado, a lista de mudanças de apresentação e os hashes constam no manifesto do projeto. Nenhum exemplo desta documentação foi executado automaticamente.
