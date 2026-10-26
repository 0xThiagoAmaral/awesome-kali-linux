---
title: "aflplusplus — documentação oficial"
type: "official-documentation"
tool: "aflplusplus"
status: "translated-machine"
reviewed: "2026-10-26"
language: "pt-BR"
tags: ["documentation", "tool/aflplusplus"]
cssclasses: ["fieldbook"]
source_url: "https://github.com/AFLplusplus/AFLplusplus/blob/d0070729206a80a9af297b2341edd63f68fdac35/docs/IJON.md"
source_commit: "d0070729206a80a9af297b2341edd63f68fdac35"
source_sha256: "7f7fa00f996c32b0e3be6bdeb7d5a4506aac29fe334201e0bd4bd13aa1c3ab3e"
license_spdx: "AGPL-3.0-or-later"
human_review: "pending"
source_scope: "Repository root README and owned doc/docs/documentation Markdown or RST files; not a claim of full wiki/site coverage"
---

> Tradução automática local para português, ainda sem revisão humana integral. Estrutura e blocos de código preservados; referências externas não significam conteúdo espelhado.

# IJON – Guided Fuzzing with Annotations

IJON é um mecanismo de notação **annotation** para fuzzers AFL++ que permite aos analistas guiar fuzzing expondo informações *state* ou *indicadores de progresso* diretamente para o fuzzer.
Com pequenas anotações de código (muitas vezes uma única linha), você pode ajudar AFL++ a explorar estados de programa profundos que são inalcançáveis.

O IJON permite:
- Guia furadores através de máquinas de estado complexas.
- Explore espaços de estado grandes (por exemplo, jogos, manipuladores de protocolo).
- Resolva desafios fuzzing "insolvíveis", tais como:
  - Completando os níveis Super Mario Bros. automaticamente.
  - Manipulação de formatos de entrada estruturados (PNG, WAV, mensagens TPM).
  - Resolvendo as buscas complexas de mapas de hash.

Esta é uma implementação completa de todas as funcionalidades do IJON para instrumentação de código fonte em AFL++.
Baseado no trabalho de pesquisa: [IJON: Explorando Espaços Estaduais Profundos via Fuzzing](https://nyx-fuzz.com/papers/ijon.pdf)
Dados de teste e benchmarks disponíveis em: [Repositório de Dados IJON](https://github.com/RUB-SysSec/ijon-data/tree/master/ijon-data)

**NOTE** Existe também uma implementação IJON para o modo qemu_, ver [qemu_mode/README.md](https://github.com/AFLplusplus/AFLplusplus/blob/d0070729206a80a9af297b2341edd63f68fdac35/qemu_mode/README.md)

<a id="important-linker-parameters"></a>
## IMPORTANTE: Parâmetros do linker

Se seu compilador não usar ld.bfd ou lld ou o linker é chamado diretamente pelo seu ambiente de compilação, então vincular o binário alvo falhará:

```text
/usr/bin/ld: b.o:(.data+0x0): multiple definition of `__afl_ijon_enabled'; a.o:(.data+0x0): first defined here
```

Para lld e ld.bfd isso pode ser resolvido geralmente com a definição do parâmetro de ligação necessário:
```text
export LD_FLAGS=--allow-multiple-definition
```

Se você usar um linker diferente do que descobrir qual é a bandeira de linker necessária para permitir múltiplas definições fortes, por exemplo.
`-z muldefs` para o ouro, e então definir o ambiente de compilação em conformidade, por exemplo:
```text
export C_FLAGS="-Wl,-z,muldefs"
export CXX_FLAGS="-Wl,-z,muldefs"
export CPP_FLAGS="-Wl,-z,muldefs"
export LD_FLAGS="-z muldefs"
```

<a id="ijon-api-reference"></a>
## Referência IJON API

<a id="core-value-tracking-macros"></a>
### Macros de Rastreamento do Valor Principal

#### `IJON_MAX(x)`
Diga ao fuzzer para **maximize** o valor `x`.
Útil quando o espaço de estado é muito grande para enumerar e você quer guiar a exploração para o progresso.
Exemplo: em Super Mario Bros., `IJON_MAX(player_x)` faz com que o fuzzer tente empurrar Mario o mais longe possível.

#### `IJON_MIN(x)`
Diga ao fuzzer para **minimize** o valor `x`.
Implementado pela maximização do valor negado.
Exemplo: `IJON_MIN(latency)` recompensa entradas que reduzem a latência.

#### `IJON_SET(x)`
Marque o valor `x` como um novo evento de cobertura.
Cada valor distinto de `x` será tratado como um novo ramo pela AFL.
Exemplo: `IJON_SET(hash_int(x, y))` recompensa visitar novas posições (x,y) em um labirinto.

#### `IJON_INC(x)`
Incrementar a entrada do mapa de cobertura para o valor `x`.
Ao contrário de `IJON_SET`, isso recompensa **como frequentemente** diferentes valores ocorrem.
Exemplo: `IJON_INC(packet_type)` faz AFL explorar muitos tipos de pacotes diferentes.

<a id="state-management-macros"></a>
### Macros de Gestão do Estado

#### `IJON_STATE(n)`
Estenda a cobertura de borda da AFL com um **virtual state component**.
Os mesmos caminhos de código irão contar como cobertura diferente dependendo do valor do `n`.
Use com moderação – muitos estados podem causar explosão de estado.
Exemplo: `IJON_STATE(has_hello + has_login)` distingue estados de protocolo.

#### `IJON_CTX(x)`
Hashing de estado escopo: incorpora temporariamente a variável `x` no hash de estado.
Útil para distinguir comportamentos baseados no contexto de execução.
Exemplo: `IJON_CTX(function_id)` faz AFL rastrear o mesmo código de forma diferente, dependendo da função ativa.

<a id="distance-and-comparison-macros"></a>
### Distância e Comparação Macros

#### `IJON_STRDIST(x, y)`
Recompensa inputs que aumentam o **comprimento comum do prefixo** de duas cordas.  
Exemplo: `IJON_STRDIST(input, "bootloader")` ajuda AFL a resolver comparações de strings dentro de mapas de hash.

#### `IJON_DIST(x, y)`
Recompensa fuzzing entradas que compartilham os bytes mais iniciais.
(note que isso mudou para o comportamento original do IJON, não é mais a distância absoluta.)
O comprimento máximo é definido em instrumentação/afl-compiler-rt.o.c e é definido em 1024.
Exemplo: `IJON_DIST(buf, expected)` guia o fuzzer em direção aos valores esperados do byte.

#### `IJON_CMP(x, y)`
Recompensa proximidade de dois inteiros, contando diferentes bits.
Exemplo: `IJON_CMP(input_val, magic_val)` ajuda o fuzzer a resolver verificações de igualdade inteiras.

#### `IJON_BITS(x)`
Retorna o número de zero bits principais no `x`.
Pode ser usado para medir como “fechar” um valor é zero ou um poder de dois.
Exemplo: `IJON_BITS(mask)` para entradas onde o alinhamento importa.

<a id="stack-aware-macros"></a>
### Macros de Aware de Pilha

#### `IJON_STACK_MAX(x)`
Como `IJON_MAX(x)`, mas a maximização é **scoped para a pilha de chamadas atual**.
Isso permite maximizar o mesmo valor de forma diferente em diferentes contextos de chamada.
Exemplo: `IJON_STACK_MAX(buffer_len)` recompensa o progresso em diferentes funções de análise independentemente.

#### `IJON_STACK_MIN(x)`
Como `IJON_MIN(x)`, mas scoped para a pilha de chamadas atual.
Exemplo: A `IJON_STACK_MIN(depth)` recompensa atingir uma recursão mais rasa em um contexto, mais profunda em outro.

<a id="example-usage"></a>
## Uso do Exemplo

<a id="maze-example"></a>
### Exemplo de labirinto

Em um labirinto que queremos ativar cobertura em novos locais no labirinto, podemos simplesmente usar `IJON_SET`:

```c
while (true) {
    ox = x; oy = y;
    switch (input[i]) {
        case 'w': y--; break;
        case 's': y++; break;
        case 'a': x--; break;
        case 'd': x++; break;
    }
    IJON_SET(hash_int(x, y)); // new position = new coverage
}
```

<a id="protocol-example"></a>
### Exemplo de protocolo

Quando nós fuzz um protocolo, nós queremos recompensar diferentes tipos de mensagem e estados:

```c
msg = parse_msg();
state_log = (state_log << 8) + msg.type;
IJON_STATE(state_log); // reward new message sequences
```

<a id="retiring-completed-max-targets"></a>
### Aposentar metas máximas concluídas

Usar `IJON_MAX_UNTIL(x, limit)` quando um objectivo IJON max tem um superior conhecido
Ligar e continuar a programar as suas sementes após esse ponto deixa de ser útil:

```c
IJON_MAX_UNTIL(depth, 100);
IJON_MAX_UNTIL_AT(0x1234, score, target_score);
```

O fuzzer continua guiando `x` para cima enquanto `x < limit`. Quando `x >= limit`, o
o slot escreve o valor do terminal `UINT64_MAX`. Se o `AFL_IJON_RETIRE_MAX` estiver definido
durante o fuzzing, o AFL++ remove a entrada máxima do IJON do pool de agendamento do IJON.

Entradas de alcance máximo armazenadas são validadas e carregadas novamente quando o AFL++ começa.
O programador repete-os round-robin depois de cada 15 turnos normal programador,
assim, IJON replay ocupa no máximo uma de cada 16 oportunidades de agendamento.
a cobertura encontrada durante o replay entra na fila como uma entrada root independente.

<a id="usage-instructions"></a>
## Instruções de utilização

<a id="building-afl-with-ijon"></a>
### Construindo AFL++ com IJON

```bash
make clean
make LLVM_CONFIG=llvm-config-18 source-only
```

<a id="ijon-mode-debug-build-for-afl-fuzz"></a>
### Compilação de depuração do modo IJON para o afl-fuzz

Note que isso não afeta qualquer funcionalidade ijon, ele apenas cria um arquivo extra.

```bash
make clean
CFLAGS="-DDUMP_IJON_STATE" make afl-fuzz
```

Isto irá produzir valores não-zero para o arquivo padrão/ijon_max/cur_state sempre que
o bitmap do ijon max é atualizado. Ao olhar para este arquivo, você pode ver os valores máximos
de suas anotações max/min até agora, o que pode ajudá-lo a entender o progresso atual do fuzzing.

Por exemplo, você pode verificar a posição do eixo y atual do Mario.

<a id="compiling-target-programs"></a>
### Compilando Programas- Alvo

Ao usar a instrumentação IJON em AFL++, é necessário invocar `__AFL_INIT()` no início da função `main()` do seu programa alvo:
```c
int main(int argc, char **argv) {
    __AFL_INIT();
    // Your code here
}
```
Adicionando `__AFL_INIT()` garante:
- Inicialização adequada do ambiente de execução AFL++
- Configuração correta do mapa de bits de cobertura e regiões de feedback IJON
- Melhoria da compatibilidade entre os objetivos

Definir as variáveis de ambiente durante a compilação:
```bash
AFL_LLVM_IJON=1 CC=afl-clang-fast CXX=afl-clang-fast++ make
```

<a id="fuzzing-configuration"></a>
### Configuração do Fuzzing

<a id="basic-fuzzing"></a>
#### Fuzzing básico
```bash
AFL_IJON_HISTORY_LIMIT=1000 afl-fuzz -i input_dir -o output_dir -- ./target
```

<a id="for-large-targets-bitmap--65k"></a>
#### Para alvos grandes (bitmap > 65k)
```bash
echo test > test_input.txt && AFL_DUMP_MAP_SIZE=1 ./target

AFL_IJON_HISTORY_LIMIT=1000 afl-fuzz -S worker -i input_dir -o output_dir -- ./target
```

<a id="environment-variables"></a>
### Variáveis de Ambiente

- **`AFL_LLVM_IJON=1`**: Activa a instrumentação IJON durante a compilação
- **`AFL_IJON_HISTORY_LIMIT=N`**: Define o número máximo de entradas de valor máximo de IJON armazenadas na máquina (por omissão: 20)
- **`AFL_IJON_RETIRE_MAX=1`**: Trata os valores máximos de `UINT64_MAX` IJON como alvos completados e pára de agendar a entrada de IJON armazenada

<a id="performance-super-mario-bros-level-11-ijon_maxpos_y16-world_pos"></a>
## Desempenho (Super Mario Bros. Nível 1.1, ijon_max(pos_y/16, world_pos))

Ambiente de teste: Ubuntu 20.04, 16 GB de RAM, 8 núcleos

|Executar|IJON AFL|IJON AFL++|
| ---- | -------- | ---------- |
|1|1 h 19 min|30 min|
|2|50 min|34 min|
|3|31 min|36 min|
|4|1 h 22 min|28 min|
|5|2 h 14 min|28 min|
|AVG|1 h 16 min|31.2 min|

No geral, o IJON AFL++ é ~2.4x mais rápido em média (76.0 min -> 31.2 min).

<a id="performance-maze-ijon_setijon_hashintx-y"></a>
## Desempenho (Maze, IJON_SET(ijon_hashint(x, y))))

Ambiente de teste: Ubuntu 20.04, 16 GB de RAM, 8 núcleos

|Executar|Fácil Pequeno (ijon AFL)|Fácil Pequeno (ijon AFL++)|Grande Fácil (ijon AFL)|Grande Fácil (ijon AFL++)|Duro Pequeno (Ijon AFL)|Hard Small (AFL++ ijon)|Grande Difícil (Ijon AFL)|Grande (ijon AFL++)|
| --- | ------------------------ | -------------------------- | ---------------------- | ------------------------ | ----------------------- | ------------------------- | --------------------- | ----------------------- |
|1|1 min 56 s|2 min 24 s|15 min 32 s|5 min 30 s|40 s|16 s|22 s|1 min 40 s|
|2|1 min 21 s|1 min 30 s|10 min 56 s|6 min 40 s|25 s|18 s|11 min 6 s|1 min 30 s|
|3|1 min 53 s|2 min 10 s|18 min 18 s|9 min 44 s|5 min 8 s|40 s|10 min 33 s|59 s|
|4|3 min 25 s|1 min 1 s|29 min 32 s|6 min 3 s|1 min 12 s|23 s|2 min 11 s|1 min 5 s|
|5|2 min 28 s|1 min 3 s|10 min 34 s|11 min 6 s|19 s|15 s|4 min 29 s|2 min 23 s|
|6|2 min 30 s|1 min 51 s|11 min 49 s|5 min 27 s|2 min 37 s|22 s|11 min 16 s|1 min 32 s|
|7|1 min 5 s|1 min 49 s|12 min 18 s|6 min 10 s|38 s|17 s|10 min 9 s|1 min 12 s|
|8|42 s|1 min 12 s|11 min 41 s|6 min 30 s|52 s|24 s|5 min 47 s|2 min 28 s|
|9|12 min 18 s|1 min 49 s|9 min 36 s|8 min 36 s|56 s|20 s|5 min 24 s|1 min 57 s|
|10|1 min 32 s|2 min 32 s|12 min 7 s|11 min 50 s|1 min 5 s|24 s|17 min 10 s|1 min 42 s|
|AVG|2 min 55 s|1 min 44 s (1,68x)|14 min 14 s|7 min 46 s (1,83x)|1 min 23 s|21.9 s (3. 8x)|7 min 51 s|1 min 39 s (4,75x)|

<a id="implementation-details"></a>
## Detalhes da Implementação

<a id="memory-layout"></a>
### Disposição da Memória

Esta implementação usa um layout de memória compartilhada dinâmica unificada que funciona para todos os tamanhos de mapa:

```text
Dynamic Shared Memory Layout (All Map Sizes):

Base Address    ┌─────────────────────────────────────┐
                │ AFL++ Shared Memory Region          │
                │ (Total: variable size)              │
                │                                     │
+0              ├─────────────────────────────────────┤ <- __afl_area_ptr
                │ Coverage Bitmap                     │   (fuzzer: trace_bits)
                │ Size: coverage_size bytes           │   (target: __afl_area_ptr)
                │ Type: u8[coverage_size]             │   (variable: 65536, 262144, etc.)
                │                                     │
                │ [0x0000] = edge_hits[0]             │
                │ [0x0001] = edge_hits[1]             │
                │ ...                                 │
                │ [coverage_size-1] = edge_hits[N]    │
                │                                     │
+coverage_size  ├─────────────────────────────────────┤
                │ IJON Set/Inc/State Area             │
                │ Size: 65,536 bytes                  │
                │ Type: u8[65536]                     │
                │                                     │
                │                                     │
+coverage_size  ├─────────────────────────────────────┤ <- __afl_ijon_bits
+65536          │ IJON Max Values                     │   (fuzzer: ijon_bits)
                │ Size: 4,096 bytes (512 × 8)         │   (target: __afl_ijon_bits)
                │ Type: u64[512]                      │   Dynamic Offset: calculated
                │                                     │
                │ [0] = max_value_slot_0              │
                │ [1] = max_value_slot_1              │
                │ ...                                 │
                │ [25] = 15240170669                  │ <- Tracked value
                │ ...                                 │
                │ [351] = 520011065792645             │ <- Tracked value  
                │ ...                                 │
                │ [458] = 964077327750                │ <- Tracked value
                │ ...                                 │
                │ [511] = max_value_slot_511          │
                │                                     │
+coverage_size  └─────────────────────────────────────┘
+69632
```

**Key Características:**
- **Unified Design**: Funciona para todos os tamanhos de mapas (65k, 256k, 1M+)
- **Offsets dinâmicos**: Offset IJON calculado em tempo de execução com base no tamanho real da cobertura
- **Disposição Consistente**: Mesma organização de memória, independentemente do tamanho do alvo
- **Suporte rápido**: Offsets IJON preservados em sessões fuzzing

<a id="the-other-tools"></a>
### As outras ferramentas

`afl-showmap`, `afl-cmin`, `afl-tmin` e `afl-analyze` ver o mesmo mapa
Afl-fuzz faz: cobertura mais 64 KB `IJON_SET`/`IJON_INC` área, com o
4 KB de slots `IJON_MAX` (e um mapa de passagem de bugs, se o alvo tiver um) excluídos,
porque aqueles têm valores largos em vez de contagens de hit e de outra forma seria
reportado como tuplas, minimizado contra, ou balde-classificado no local.
`afl-showmap` descarte de um alvo IJON lista tuplas acima do tamanho da cobertura, e
duas entradas que diferem apenas em um valor `IJON_SET` são dois traços diferentes —
que é o que faz `afl-cmin` manter ambos, exatamente como afl-fuzz faria.

Os canais IJON precisam de um mapa para escrever: uma execução `./target` nua deixa-os
sozinho, enquanto uma corrida sob qualquer uma destas ferramentas tem uma. Nada tem de ser passado
por isso.


---

## Procedência desta tradução

Fonte: [https://github.com/AFLplusplus/AFLplusplus](https://github.com/AFLplusplus/AFLplusplus/blob/d0070729206a80a9af297b2341edd63f68fdac35/docs/IJON.md). Licença: [AGPL-3.0-or-later](../../99-Assets/upstream/aflplusplus/LICENSE.txt). Commit: d0070729206a80a9af297b2341edd63f68fdac35.

O original preservado, a lista de mudanças de apresentação e os hashes constam no manifesto do projeto. Nenhum exemplo desta documentação foi executado automaticamente.
