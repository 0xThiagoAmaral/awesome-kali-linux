---
title: "aflplusplus — documentação oficial"
type: "official-documentation"
tool: "aflplusplus"
status: "translated-machine"
reviewed: "2026-10-26"
language: "pt-BR"
tags: ["documentation", "tool/aflplusplus"]
cssclasses: ["fieldbook"]
source_url: "https://github.com/AFLplusplus/AFLplusplus/blob/d0070729206a80a9af297b2341edd63f68fdac35/docs/rpc_statsd.md"
source_commit: "d0070729206a80a9af297b2341edd63f68fdac35"
source_sha256: "2728f461a25974b04ee1840ebb646575132184fcf6f43926554c22079aec8738"
license_spdx: "AGPL-3.0-or-later"
human_review: "pending"
source_scope: "Repository root README and owned doc/docs/documentation Markdown or RST files; not a claim of full wiki/site coverage"
---

> Tradução automática local para português, ainda sem revisão humana integral. Estrutura e blocos de código preservados; referências externas não significam conteúdo espelhado.

# Remote monitoring and metrics visualization

O AFL++ pode enviar métricas como mensagens StatsD.
visualização das métricas, você pode configurar uma cadeia de ferramentas.
Prometheus e Grafana. Todas as ferramentas são livres e de código aberto.

Isso permite que você crie painéis agradáveis e legíveis contendo todos os
informações que você precisa em suas instâncias fuzzer. Não há necessidade de escrever seu
sistema próprio de análise de estatísticas, implantação e manutenção para todas as suas instâncias, e
sincronizar com o seu sistema de renderização de gráficos.

Comparado com a interface integrada padrão de AFL++, isso pode ajudá-lo a visualizar
tendências e o estado fuzzing ao longo do tempo.
fuzzing processo atingiu um estado de nenhum progresso e visualizar o que são os
"melhores estratégias" para os seus alvos (de acordo com os seus próprios critérios).
Então, sem entrar em cada instância individualmente.

[Imagem/recurso externo: example visualization with Grafana](https://github.com/AFLplusplus/AFLplusplus/blob/d0070729206a80a9af297b2341edd63f68fdac35/docs/resources/statsd-grafana.png)

Esta é uma visualização de exemplo com Grafana. O painel pode ser importado
com [Este modelo JSON](https://github.com/AFLplusplus/AFLplusplus/blob/d0070729206a80a9af297b2341edd63f68fdac35/docs/resources/grafana-afl++.json).

## métricas AFL++ e EstatísticasD

StatsD permite que você receba e agregue métricas de uma ampla gama de
aplicações e retransmiti-los para uma infra- estrutura de sua escolha.

A partir de AFL++, o StatsD pode receber as seguintes métricas:
- cur_item
- cycle_ done
- ciclos_wo_ finds
- arestas_encontradas
- execucs_ done
- execs_per_sec
- caos_ expansão
- max_ profundidade
- Corpus_favored
- corpus_encontrado
- corpus_importado
- corpus_contagem
- _favs pendentes
- _Total pendente
- mais lento_exec_ms
- total_crashes
- _crashes gravados
- _Atalhos gravados
- var_byte_count
- corpus_variável

Dependendo de seu servidor StatsD, você será capaz de monitorar, ativar alertas, ou
executar ações baseadas nessas métricas (por exemplo: alerta em exec/s lentos para
nova compilação, limiar de falhas, tempo desde o último acidente > X, e assim por diante).

## Definir variáveis de ambiente em AFL++

1. Para habilitar a coleção de métricas StatsD em suas instâncias fuzzer, defina o
variável de ambiente `AFL_STATSD=1`. Por padrão, o AFL++ enviará as métricas
sobre UDP para 127.0.0.1:8125.

2. Para ativar tags para cada métrica com base em seu formato (banner e
afl_ version), definir a variável de ambiente `AFL_STATSD_TAGS_FLAVOR`. By
padrão, nenhuma tag será adicionada às métricas.

    The available values are the following:
    -  `dogstatsd`
    -  `influxdb`
    -  `librato`
    -  `signalfx`

    For more information on environment variables, see
    [env_variables.md](aflplusplus-docs-env-variables-md.md).

    Note: When using multiple fuzzer instances with StatsD it is *strongly*
    recommended to set up `AFL_STATSD_TAGS_FLAVOR` to match your StatsD server.
    This will allow you to see individual fuzzer performance, detect bad ones,
    and see the progress of each strategy.

3. Opcional: Para definir a máquina e o porto do seu servidor StatsD, defina
`AFL_STATSD_HOST` e `AFL_STATSD_PORT`. Os valores padrão são `localhost`
e `8125`.

## Instalando e configurando StatsD, Prometeu e Grafana

A maneira mais fácil de instalar e configurar a infra-estrutura é com Docker e
Docker Compose.

Dependendo da sua configuração e infraestrutura fuzzing, você pode não querer executar
estas aplicações nas suas instâncias fuzzer. Esta configuração pode ser modificada antes
usar em um ambiente de produção; por exemplo, adicionar senhas, criar volumes
para armazenamento, ajustar a coleta de métricas para obter métricas de host (CPU, RAM, e
e assim por diante).

Para todas as suas instâncias fuzzing, apenas uma instância de Prometeu e Grafana é
necessário.
[exportador de estatísticas](https://registry.hub.docker.com/r/prom/statsd-exporter)
converte as métricas StatsD para Prometeu. Se você estiver usando um provedor que
suporta StatsD diretamente, você pode pular esta parte da configuração."

Você pode criar e mover os arquivos de infraestrutura para um diretório do seu
escolha. A pasta irá guardar todos os arquivos de configuração necessários.

Para instalar e configurar Prometeu e Grafana:

1. Instalar a Acoplagem e a Acoplagem:

    ```sh
    curl -fsSL https://get.docker.com -o get-docker.sh
    sh get-docker.sh
    ```

2. Criar um `docker-compose.yml` contendo o seguinte:

    ```yml
    version: '3'

    networks:
      statsd-net:
        driver: bridge

    services:
      prometheus:
        image: prom/prometheus
        container_name: prometheus
        volumes:
          - ./prometheus.yml:/prometheus.yml
        command:
          - '--config.file=/prometheus.yml'
        restart: unless-stopped
        ports:
          - "9090:9090"
        networks:
          - statsd-net

      statsd_exporter:
        image: prom/statsd-exporter
        container_name: statsd_exporter
        volumes:
          - ./statsd_mapping.yml:/statsd_mapping.yml
        command:
          - "--statsd.mapping-config=/statsd_mapping.yml"
        ports:
          - "9102:9102/tcp"
          - "8125:9125/udp"
        networks:
          - statsd-net

      grafana:
        image: grafana/grafana
        container_name: grafana
        restart: unless-stopped
        ports:
            - "3000:3000"
        networks:
          - statsd-net
    ```

3. Criar um `prometheus.yml` contendo o seguinte:

    ```yml
    global:
      scrape_interval:      15s
      evaluation_interval:  15s

    scrape_configs:
      - job_name: 'fuzzing_metrics'
        static_configs:
          - targets: ['statsd_exporter:9102']
    ```

4. Criar um `statsd_mapping.yml` contendo o seguinte:

    ```yml
    mappings:
    - match: "fuzzing.*"
      name: "fuzzing"
      labels:
          type: "$1"
    ```

5. Executar `docker-compose up -d`.

## Executar AFL++ com StatsD

Para executar suas instâncias fuzzing:

```text
AFL_STATSD_TAGS_FLAVOR=dogstatsd AFL_STATSD=1 afl-fuzz -M test-fuzzer-1 -i i -o o [./bin/my-application] @@
AFL_STATSD_TAGS_FLAVOR=dogstatsd AFL_STATSD=1 afl-fuzz -S test-fuzzer-2 -i i -o o [./bin/my-application] @@
...
```

---

## Procedência desta tradução

Fonte: [https://github.com/AFLplusplus/AFLplusplus](https://github.com/AFLplusplus/AFLplusplus/blob/d0070729206a80a9af297b2341edd63f68fdac35/docs/rpc_statsd.md). Licença: [AGPL-3.0](../../99-Assets/upstream/aflplusplus/LICENSE.txt). Commit: d0070729206a80a9af297b2341edd63f68fdac35.

O original preservado, a lista de mudanças de apresentação e os hashes constam no manifesto do projeto. Nenhum exemplo desta documentação foi executado automaticamente.
