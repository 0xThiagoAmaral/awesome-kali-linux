# Catálogo de triagem

O inventário existente forneceu 178 pacotes ligados a categorias Kali e 82 entradas extras fora do dpkg.
O catálogo sanitizado mantém nomes e versões conhecidas, não caminhos pessoais, usuários, hostnames,
configurações, listas de serviços nem inventário bruto.

260 registros não equivalem a 260 ferramentas independentes. Bibliotecas, dados, runtimes e aliases
precisam de triagem. Apenas Nmap e ffuf têm módulo-piloto aqui; o restante é backlog, não documentação pronta.

- `candidates.json`: registros factuais e estado de triagem.
- `backlog.csv`: lista editável para priorização.
- `sources.json`: referências e decisões de redistribuição ainda pendentes.
- `provenance.json`: hash do inventário utilizado, sem caminho de origem pessoal.
