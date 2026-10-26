---
title: "altdns — documentação oficial"
type: "official-documentation"
tool: "altdns"
status: "translated-machine"
reviewed: "2026-10-26"
language: "pt-BR"
tags: ["documentation", "tool/altdns"]
cssclasses: ["fieldbook"]
source_url: "https://github.com/infosec-au/altdns/blob/6728272cbda8b8ceca4d59f4398e81df921853f2/README.md"
source_commit: "6728272cbda8b8ceca4d59f4398e81df921853f2"
source_sha256: "7ffd79d4fa13dc984e937af9e4b65698c0b4e34e5db87951b07b8c0e49dd10c7"
license_spdx: "Apache-2.0"
human_review: "pending"
source_scope: "Repository root README and owned doc/docs/documentation Markdown or RST files; not a claim of full wiki/site coverage"
---

> Tradução automática local para português, ainda sem revisão humana integral. Estrutura e blocos de código preservados; referências externas não significam conteúdo espelhado.

# Altdns - Subdomain discovery through alterations and permutations

Altdns é uma ferramenta de reconhecimento DNS que permite a descoberta de subdomínios que estejam de acordo com os padrões. Altdns leva em palavras que poderiam estar presentes em subdomínios sob um domínio (como teste, dev, encenação), bem como leva em uma lista de subdomínios que você conhece.

A partir destas duas listas que são fornecidas como entrada para altdns, a ferramenta então gera um _massive_ saída de subdomínios potenciais "alterados" ou "mutados" que poderia estar presente. Ele salva esta saída para que ele possa então ser usado pela sua ferramenta favorita de força bruta DNS.

Alternativamente, a bandeira `-r` pode ser passada para altdns para que uma vez que esta saída é gerada, a ferramenta pode então resolver estes subdomínios (multi-threaded) e salvar os resultados em um arquivo.

Altdns funciona melhor com grandes conjuntos de dados. Ter um conjunto de dados inicial de 200 ou mais subdomínios deve gerar alguns subdomínios válidos através das alterações geradas.

Mais informações sobre a metodologia de ataque e esta versão da ferramenta podem ser encontradas aqui: https://docs.google.com/presentation/d/1PCnjzCeklOeGMoWiE2IUzlRGOBxNp8K5hLQuvBNzrFY/

# Installation

Python 2:

`pip install py-altdns==1.0.0`

Python 3:

`pip3 install py-altdns==1.0.2`

# Usage

`# altdns -i subdomains.txt -o data_output -w words.txt -r -s results_output.txt`

- `subdomains.txt` contém os subdomínios conhecidos para uma organização
- `data_output` é um arquivo que irá conter a lista _massive_ de subdomínios alterados e permutados
- `words.txt` é a sua lista de palavras com as quais gostaria de permutar os seus subdomínios actuais (ou seja, `admin`, `staging`, `dev`, `qa`) - uma palavra por linha
- o comando `-r` resolve cada subdomínio gerado e permutado
- o comando `-s` diz altdns onde salvar os resultados dos subdomínios permutados resolvidos. `results_output.txt` conterá a lista final de subdomínios permutados encontrados que são válidos e têm um registro DNS.
- o comando `-t` limita quantos threads o resolvedor usará simultaneamente
- `-d 1.2.3.4` substitui o resolvedor padrão do sistema DNS e usará o endereço IP especificado como servidor de resolução. Configurando isso para o servidor DNS autorizado do domínio alvo *may* aumenta o desempenho de resolução

# Screenshots





# Show some love

Se esta ferramenta foi útil para você durante as etapas de reconhecimento DNS - gostaríamos de saber. Quaisquer sugestões ou ideias para esta ferramenta são bem-vindas - basta tweetar [@ infosec_au](https://twitter.com/infosec_au) ou [@nnwakelam](https://twitter.com/nnwakelam) e vamos trabalhar nele.


---

## Procedência desta tradução

Fonte: [https://github.com/infosec-au/altdns](https://github.com/infosec-au/altdns/blob/6728272cbda8b8ceca4d59f4398e81df921853f2/README.md). Licença: [Apache-2.0](../../99-Assets/upstream/altdns/LICENSE.txt). Commit: 6728272cbda8b8ceca4d59f4398e81df921853f2.

O original preservado, a lista de mudanças de apresentação e os hashes constam no manifesto do projeto. Nenhum exemplo desta documentação foi executado automaticamente.
