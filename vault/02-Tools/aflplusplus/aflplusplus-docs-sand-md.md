---
title: "aflplusplus — documentação oficial"
type: "official-documentation"
tool: "aflplusplus"
status: "translated-machine"
reviewed: "2026-10-26"
language: "pt-BR"
tags: ["documentation", "tool/aflplusplus"]
cssclasses: ["fieldbook"]
source_url: "https://github.com/AFLplusplus/AFLplusplus/blob/d0070729206a80a9af297b2341edd63f68fdac35/docs/SAND.md"
source_commit: "d0070729206a80a9af297b2341edd63f68fdac35"
source_sha256: "160b79c13dc735589666c56ecaae0a538e399d12a03b2c34d22fbcb99a107f52"
license_spdx: "AGPL-3.0-or-later"
human_review: "pending"
source_scope: "Repository root README and owned doc/docs/documentation Markdown or RST files; not a claim of full wiki/site coverage"
---

> Tradução automática local para português, ainda sem revisão humana integral. Estrutura e blocos de código preservados; referências externas não significam conteúdo espelhado.

# SAND: Decoupling Sanitization from Fuzzing for Low Overhead

- Autores: Ziqiao Kong, Shaohua Li, Heqing Huang, Zhendong Su
- Manutenção: [Ziqiao Kong](https://github.com/wtdcode)
- Preprint: [arXiv](https://arxiv.org/abs/2402.16497), aceito pelo ICSE 2025
- Repo principal (para papel, reprodução, referência ou citação): https://github.com/wtdcode/sand-aflpp

## Motivação

SAND introduz um novo fluxo de trabalho fuzzing que pode reduzir (ou mesmo eliminar) a sobrecarga do higienizador e combinar diferentes higienizadores em uma campanha fuzzing.

O ponto chave do SAND é que: higienizar todas as entradas está desperdiçando o poder do fuzzing, porque as entradas de desencadeamento de bugs são extremamente raras (~1%). Obviamente, nem todas as entradas valem a pena passar por higienizadores. Portanto, se pudermos de alguma forma "prever" se uma entrada pudesse acionar bugs (definidos como "padrão de execução"), poderíamos salvar muito o poder do fuzzing apenas por higienizar uma pequena proporção de todas as entradas. É exatamente assim que o SAND funciona.

## Uso

Para um fluxo de trabalho fuzzing normal, temos:

1. Compila o projeto alvo com AFL_USE_ASAN=1 para obter `target_asan`
2. Fuzz o alvo com `afl-fuzz -i seeds -o out -- ./target_asan`

Para o fluxo de trabalho SAND fuzzing, isso é ligeiramente diferente:

1. Construa o projeto alvo _sem_ quaisquer higienizadores para obter `target_native`, que nós definiremos como um "binário nativo". Geralmente é feito usando `afl-clang-fast/lto(++)` para compilar seu projeto _sem_ `AFL_USE_ASAN/UBSAN/MSAN`.
2. Build target project with AFL_USE_ASAN=1 AFL_LLVM_ONLY_FSRV=1 to get `target_asan`. Note que este passo pode ser repetido para vários higienizadores, como MSAN, UBSAN etc Também é possível ter ASAN e UBSAN para construir juntos.
3. Fuzz o alvo com `afl-fuzz -i seeds -o out -w ./target_asan -- ./target_native`. Nota `-w` pode ser especificado várias vezes.

Então você começa:

- quase o mesmo desempenho que `afl-fuzz -i seeds -o out -- ./target_native`
- e a mesma capacidade de encontrar erros que o `afl-fuzz -i seeds -o out -- ./target_asan`

## Exemplo de fluxo de trabalho

Tome [teste-instr.c](https://github.com/AFLplusplus/AFLplusplus/blob/d0070729206a80a9af297b2341edd63f68fdac35/test-instr.c) como um exemplo.

1. Compilar o binário nativo

```bash
afl-clang-fast test-instr.c -o ./native
```

Assim como o processo de construção normal, exceto usando `afl-clang-fast`

2. Construa os binários habilitados para higienizadores.

```bash
AFL_LLVM_ONLY_FSRV=1 AFL_USE_UBSAN=1 AFL_USE_ASAN=1 afl-clang-fast test-instr.c -o ./asanubsan
AFL_LLVM_ONLY_FSRV=1 AFL_USE_MSAN=1 afl-clang-fast test-instr.c -o ./msan
```

Fazer nota `AFL_LLVM_ONLY_FSRV=1` é crucial, isto permite que os servidores de fork, mas desactiva a instrumentação de pc. Você pode reutilizar binários habilitados para higienizadores, isto é, binários construídos _sem_ `AFL_LLVM_ONLY_FSRV=1`, a um custo de velocidade reduzida.

3. Iniciar o fuzzing

```bash
mkdir /tmp/test
echo "a" > /tmp/test/a
AFL_NO_UI=1 AFL_SKIP_CPUFREQ=1 afl-fuzz -i /tmp/test -o /tmp/out -w ./asanubsan -w ./msan -- ./native @@
```

É isso!

## Dicas

### Padrões de execução alternativos

Por padrão, o SAND usa o valor de hash do mapa de cobertura simplificado como padrão de execução, ou seja, se uma entrada tiver um mapa de cobertura único e simples, ele será enviado para higienizadores para inspeção. Isto irá funcionar para a maioria dos casos. Contudo, se você estiver fortemente preocupado com erros ausentes, tente o `AFL_SAN_ABSTRACTION=unique_trace afl-fuzz ...`, que filtra entradas com um mapa de cobertura _unique_. Lembre- se que isso aumenta significativamente o número de entradas em 4-10 vezes, levando a uma taxa de transferência muito menor. Alternativamente, o SAND também suporta o `AFL_SAN_ABSTRACTION=coverage_increase`, que é essencialmente igual a executar higienizadores no corpus e, portanto, ter quase zero sobrecarga, mas a um custo de faltando ~15% bugs na nossa avaliação.

SAND usa uma cache de de deduplicação limitada de 8 MB por padrão. Defina `AFL_SAN_DEDUP_SIZE` para o tamanho de cache desejado no MB. As colisões de índice de cache despejam o hash antigo e podem fazer com que uma entrada seja verificada novamente.

### Executar tantos higiénicos quanto possível

Embora tenhamos usado a ASAN como exemplo, a SAND funciona melhor se você fornecer mais higienizadores, por exemplo, UBSAN e MSAN.

Você pode fazê-lo via `afl-fuzz -i seeds -o out -w ./target_asan -w ./target_msan -w ./target_ubsan -- ./target_native`. Não se preocupe com os higienizadores lentos como MSAN, SAND ainda poderia executar muito rápido, porque apenas um pouco de entradas são higienizadas.

### Tipos de erros

O padrão de execução avaliado em nossos artigos está visando os bugs comuns, como captura ASAN/MSAN/UBSAN. Para outros tipos de bugs, você provavelmente precisa definir novos padrões de execução e reavaliar.

### Meu rendimento é muito impactado

Geralmente, isto é devido a muitas entradas passando por higienizadores, por exemplo, por causa de alvos instáveis. Você pode verificar estatísticas do `plot_file` para confirmar isso. Tente mudar os padrões de execução como indicado acima.


---

## Procedência desta tradução

Fonte: [https://github.com/AFLplusplus/AFLplusplus](https://github.com/AFLplusplus/AFLplusplus/blob/d0070729206a80a9af297b2341edd63f68fdac35/docs/SAND.md). Licença: [AGPL-3.0](../../99-Assets/upstream/aflplusplus/LICENSE.txt). Commit: d0070729206a80a9af297b2341edd63f68fdac35.

O original preservado, a lista de mudanças de apresentação e os hashes constam no manifesto do projeto. Nenhum exemplo desta documentação foi executado automaticamente.
