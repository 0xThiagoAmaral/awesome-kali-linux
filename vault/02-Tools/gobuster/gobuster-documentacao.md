---
title: "gobuster — documentação oficial"
type: "official-documentation"
tool: "gobuster"
status: "translated-machine"
reviewed: "2026-10-26"
language: "pt-BR"
tags: ["documentation", "tool/gobuster"]
cssclasses: ["fieldbook"]
source_url: "https://github.com/OJ/gobuster/blob/c77583fbb8824058d74d38240896eff610683c8e/README.md"
source_commit: "c77583fbb8824058d74d38240896eff610683c8e"
source_sha256: "9c5b67cdd42cd59eb9d4c3c0ed9c90aae05fce56803ff92d81e8fd097a6fff0d"
license_spdx: "Apache-2.0"
human_review: "pending"
source_scope: "Official English repository README/docs and available upstream Portuguese README; external manuals/wiki coverage tracked separately"
---

> Tradução automática local para português, ainda sem revisão humana integral. Estrutura e blocos de código preservados; referências externas não significam conteúdo espelhado.

# Gobuster

[Go Report Card](https://goreportcard.com/report/github.com/OJ/gobuster/v3) [License](https://github.com/OJ/gobuster/blob/master/LICENSE) [Backers on Open Collective](https://opencollective.com/gobuster) [Sponsors on Open Collective](https://opencollective.com/gobuster)

<a id="-introduction"></a>
## Introdução ao 💻

> Uma ferramenta rápida e flexível de força bruta escrita em Go

**Gobuster** é um diretório/arquivo de alto desempenho, DNS e ferramenta de força bruta de host virtual escrito em Go. Ele é projetado para ser rápido, confiável e fácil de usar para profissionais de segurança e testadores de penetração.

<a id="-features"></a>
## □ Características

- 🚀 **High Performance**: Digitalização multi-threadada com concurrência configurável
- 🔍 **Multiple Modes**: Directory, DNS, máquina virtual, S3, GCS, TFTP e modos fuzzing
- 🛡® **Security Focused**: Construído para testes de penetração e avaliações de segurança
- 🐳 **Docker Support**: Disponível como um recipiente Docker
- 🔧 **Extensible**: Digitalização baseada em padrões e listas de palavras personalizadas

<a id="-what-can-gobuster-do"></a>
## 🎯 O que pode Gobuster fazer?

- **Web Directory/File Enumeration**: Descubra diretórios e arquivos ocultos em servidores web
- **DNS Subdomínio Discovery**: Encontrar subdomínios com suporte a caracteres especiais
- **Detecção Virtual de Host**: Identificar hosts virtuais em servidores web de destino
- **Cloud Armazenamento Enumeração**: Descubra os baldes de armazenamento Amazon S3 e Google Cloud abertos
- Arquivo **TFTP Discovery**: Encontre arquivos em servidores TFTP
- **Custom Fuzzing**: Flexível fuzzing com parâmetros personalizáveis

<a id="-quick-start"></a>
## Início Rápido do 🚀

```bash
# Install gobuster
go install github.com/OJ/gobuster/v3@latest

# Basic directory enumeration
gobuster dir -u https://example.com -w /path/to/wordlist.txt

# DNS subdomain enumeration
gobuster dns -do example.com -w /path/to/wordlist.txt

# Virtual host discovery
gobuster vhost -u https://example.com -w /path/to/wordlist.txt

# S3 bucket enumeration
gobuster s3 -w /path/to/bucket-names.txt
```

<a id="-installation"></a>
## Instalação do 📦

<a id="quick-install-recommended"></a>
### Instalação Rápida (Recomendada)

```bash
go install github.com/OJ/gobuster/v3@latest
```

**Requirements**: Go 1.24 ou superior

<a id="alternative-installation-methods"></a>
### Métodos de instalação alternativos

<a id="using-binary-releases"></a>
#### Usando versões binárias

Baixe binários pré-compilados do [página de lançamentos](https://github.com/OJ/gobuster/releases).

<a id="using-docker"></a>
#### Usar o Docker

```bash
# Pull the latest image
docker pull ghcr.io/oj/gobuster:latest

# Run gobuster in Docker
docker run --rm -it ghcr.io/oj/gobuster:latest dir -u https://example.com -w /usr/share/wordlists/dirb/common.txt
```

<a id="building-from-source"></a>
#### Compilando a partir do Código

```bash
git clone https://github.com/OJ/gobuster.git
cd gobuster
go mod tidy
go build
```

<a id="troubleshooting-installation"></a>
### Solução de problemas de instalação

Se você encontrar problemas:

- Garantir Go versão 1.24+ está instalado: `go version`
- Verifique suas variáveis de ambiente `$GOPATH` e `$GOBIN`
- Verifique se o `$GOPATH/bin` está no seu `$PATH`

<a id="-usage"></a>
## Uso do 🎯

O Gobuster usa uma abordagem baseada no modo. Cada modo é projetado para tarefas específicas de enumeração:

```bash
gobuster [mode] [options]
```

<a id="getting-help"></a>
### Obter Ajuda

```bash
gobuster help                   # Show general help
gobuster help [mode]            # Show help for specific mode
gobuster [mode] --help          # Alternative help syntax
```

<a id="-available-modes"></a>
### Modos disponíveis do 📊

<a id="-directory-mode-dir"></a>
#### Modo de diretório 🌐 (`dir`)

Enumere diretórios e arquivos em servidores web.

Uso básico do **:**

```bash
gobuster dir -u https://example.com -w wordlist.txt
```

**Opções avançadas:**

```bash
# With file extensions
gobuster dir -u https://example.com -w wordlist.txt -x php,html,js,txt

# With custom headers and cookies
gobuster dir -u https://example.com -w wordlist.txt -H "Authorization: Bearer token" -c "session=value"

# Show response length
gobuster dir -u https://example.com -w wordlist.txt -l

# Filter by status codes
gobuster dir -u https://example.com -w wordlist.txt -s 200,301,302
```

<a id="-dns-mode-dns"></a>
#### Modo 🔍 DNS (`dns`)

Descubra subdomínios através da resolução DNS.

Uso básico do **:**

```bash
gobuster dns -do example.com -w wordlist.txt
```

**Opções avançadas:**

```bash
# Use custom DNS server
gobuster dns -do example.com -w wordlist.txt -r 8.8.8.8:53

# Increase threads for faster scanning
gobuster dns -do example.com -w wordlist.txt -t 50
```

<a id="-virtual-host-mode-vhost"></a>
#### Modo de máquina virtual 🏠 (`vhost`)

Descubra hosts virtuais em servidores web.

Uso básico do **:**

```bash
gobuster vhost -u https://example.com --append-domain -w wordlist.txt
```

<a id="-s3-mode-s3"></a>
#### Modo S3 (`s3`)

Enumerar os baldes Amazon S3.

Uso básico do **:**

```bash
gobuster s3 -w bucket-names.txt
```

**Com saída de depuração:**

```bash
gobuster s3 -w bucket-names.txt --debug
```

<a id="-tftp-mode-tftp"></a>
#### Modo 🖥 o TFTP (`tftp`)

Enumere os arquivos nos servidores tftp.

Uso básico do **:**

```bash
gobuster tftp -s 10.0.0.1 -w wordlist.txt
```

<a id="-gcs-mode-gcs"></a>
#### Modo GCS (`gcs`)

Enumere os Baldes de Armazenamento da Google Cloud.

Uso básico do **:**

```bash
gobuster gcs -w bucket-names.txt
```

**Com saída de depuração:**

```bash
gobuster gcs -w bucket-names.txt --debug
```

#### 🔧 Fuzz Mode (`fuzz`)

fuzzing personalizado com a palavra-chave `FUZZ`.

Uso básico do **:**

```bash
gobuster fuzz -u https://example.com?FUZZ=test -w wordlist.txt
```

**Exemplos avançados:**

```bash
# Fuzz URL parameters
gobuster fuzz -u https://example.com?param=FUZZ -w wordlist.txt

# Fuzz headers
gobuster fuzz -u https://example.com -H "X-Custom-Header: FUZZ" -w wordlist.txt

# Fuzz POST data
gobuster fuzz -u https://example.com -d "username=admin&password=FUZZ" -w passwords.txt
```

<a id="-support"></a>
## Suporte ao 💰

[Backers on Open Collective](https://opencollective.com/gobuster) [Sponsors on Open Collective](https://opencollective.com/gobuster)

<a id="love-this-tool-back-it"></a>
### Adoras esta ferramenta?

Se você já está nos apoiando, você rock. Se você não é, isso é legal também! Quer nos apoiar? [Tornar-se um financiador](https://opencollective.com/gobuster#backer)!

[Backers](https://opencollective.com/gobuster#backers)

Todos os fundos que são doados para este projeto serão doados para caridade. Um diário completo de doações de caridade estará disponível neste repositório à medida que forem processados.

<a id="-common-use-cases"></a>
## 💡 Casos de Uso Comum

<a id="web-application-security-testing"></a>
### Testes de segurança de aplicativos Web

```bash
# Comprehensive directory enumeration
gobuster dir -u https://target.com -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -x php,html,js,txt,asp,aspx,jsp

# API endpoint discovery
gobuster dir -u https://api.target.com -w /usr/share/wordlists/dirb/common.txt -x json

# Admin panel discovery
gobuster dir -u https://target.com -w admin-panels.txt -s 200,301,302,403
```

<a id="dns-reconnaissance"></a>
### Reconhecimento DNS

```bash
# Comprehensive subdomain enumeration
gobuster dns -do target.com -w /usr/share/wordlists/dnsrecon/subdomains-top1mil-5000.txt -t 50
```

<a id="cloud-storage-assessment"></a>
### Avaliação do armazenamento em nuvem

```bash
# S3 bucket enumeration with patterns
gobuster s3 -w company-names.txt -v

# GCS bucket enumeration
gobuster gcs -w company-names.txt -v
```

<a id="-troubleshooting"></a>
## Resolução de Problemas do 🔧

<a id="common-issues"></a>
### Questões Comuns

<a id="permission-denied-or-access-denied"></a>
#### "Permissão negada" ou "Acesso negado"

- Tente reduzir a contagem de fios com a bandeira `-t`
- Adicionar atrasos entre as solicitações com o `--delay`
- Usar agente de usuário diferente com a bandeira `-a`

<a id="connection-timeout"></a>
#### Tempo limite de ligação

- Aumentar o tempo- limite com a bandeira `--timeout`
- Reduza a contagem de threads para alvos mais lentos
- Verifique a sua ligação à Internet

<a id="no-results-found"></a>
#### "Nenhum resultado encontrado"

- Verificar se o URL de destino está acessível
- Tente diferentes listas de palavras
- Verificar a filtragem do código de estado com a bandeira `-s`

<a id="performance-issues"></a>
### Questões de desempenho

<a id="slow-scanning"></a>
#### Escaneamento lento

- Aumentar a contagem de threads com a bandeira `-t` (mas tenha cuidado para não sobrecarregar o alvo)
- Usar listas de palavras menores e mais direcionadas

<a id="-best-practices"></a>
## Melhores práticas do 🎯

<a id="security-testing-guidelines"></a>
### Orientações relativas aos testes de segurança

1. **Sempre obter a autorização adequada** antes de testar qualquer alvo
2. **Iniciar com baixas contagens de thread** para evitar servidores esmagadores
3. **Use listas de palavras apropriadas** para a tecnologia alvo
4. **Respect rate limits** e implementar atrasos se necessário
5. **Monitor seu tráfego de rede** para evitar detecção

<a id="wordlist-selection"></a>
### Selecção da Lista de Palavras

- **Para aplicações web**: Use wordlists específicos para tecnologia (PHP, ASP.NET, etc.)
- **For APIs**: Foco em endpoints comuns do API e padrões de versão
- **For DNS**: Usar listas de palavras específicas para subdomínios com padrões comuns
- **For cloud storage**: Use padrões específicos da empresa/marca

<a id="output-management"></a>
### Gestão de Saídas

```bash
# Save results to file
gobuster dir -u https://example.com -w wordlist.txt -o results.txt

# Use quiet mode for clean output
gobuster dir -u https://example.com -w wordlist.txt -q
```

<a id="-additional-resources"></a>
## 📚 Recursos adicionais

<a id="recommended-wordlists"></a>
### Listas de palavras recomendadas

- **SecLists**: [https://github.com/danielmiessler/SecLists](https://github.com/danielmiessler/SecLists)
- **FuzzDB**: [https://github.com/fuzzdb-project/fuzzdb](https://github.com/fuzzdb-project/fuzzdb)
- **Seclistas DNS**: [https://github.com/danielmiessler/SecLists/tree/master/Discovery/DNS](https://github.com/danielmiessler/SecLists/tree/master/Discovery/DNS)

---

**Happy hacking! 🚀**

_Lembre-se: teste sempre responsável e com a devida autorização._

# Changes

<details>

<summary>3.8.2</summary>

## 3.8.2

- Corrigir o modo expandido para mostrar o URL completo novamente

</details>

<details>

<summary>3.8.1</summary>

## 3.8.1

- Corrigir o modo expandido que mostra os itens duas vezes

</details>

<details>

<summary>3.8</summary>

## 3.8

- Adicionar uma bandeira com o nome da máquina para ajustar dinamicamente o comprimento da exclusão por @ 0xyy66
- Corrigir os parâmetros da consulta do Fuzzing
- Adicionar a bandeira `--force` no modo `dir` para continuar a execução se ocorrerem erros de verificação prévia

</details>

<details>

<summary>3.7</summary>

## 3.7

- usar nova biblioteca cli
- muito mais opções curtas devido à nova biblioteca cli
- mensagens de erro mais amigável do usuário
- limpar o modo DNS
- renomeado `show-cname` para `check-cname` no modo dns
- se livrou da bandeira `verbose` e introduziu `debug` em vez
- o comando versão agora também mostra algumas variáveis de compilação para mais informações
- mudou para outra biblioteca pkcs12 para suportar p12s gerados com openssl3 que usam SHA256 HMAC
- comentários em listas de palavras (textos que começam com #) não são mais ignorados
- alertar no modo vhost se o interruptor -- append- domain pôde ter sido esquecido
- permite excluir o código de estado e o comprimento no modo vhost
- adicionar automaxprocs para uso em docker com limites de cpu
- registrar pedidos em http com a depuração habilitada
- permitir o fuzzing do cabeçalho Host no modo fuzz
- desactivar automaticamente a saída de progresso quando a saída é redireccionada
- corrigir caracteres extra especiais quando executado com `--no-progress`
- alertar ao usar o modo vhost com um proxy e URLs baseadas em http, pois isto pode não funcionar como esperado
- adicionar parâmetros `interface` e `local-ip` para especificar a interface de saída para pedidos http
- adicionar suporte para renegociação de tls
- corrigir o progresso com padrões por @ acamack
- corrigir a descoberta de backup por @ acamack
- suporta protocolo tcp em servidores dns
- adicionar suporte para parâmetros de pesquisa de URL

</details>

<details>
<summary>3.6</summary>

## 3.6

- Parâmetro de deslocamento da lista de palavras para pular x linhas da lista de palavras
- evitar cortes duplos ao criar um url em modo dir
- permitir múltiplos valores e intervalos no `--exclude-length`
- O parâmetro `no-fqdn` no dns bruteforce para desactivar a utilização dos domínios de pesquisa dos sistemas. Isto deverá acelerar a execução se tiver configurado alguns domínios de pesquisa. [https://github.com/OJ/gobuster/pull/418](https://github.com/OJ/gobuster/pull/418)

</details>

<details>
<summary>3.5</summary>

## 3.5

- Permitir intervalos na lista negra do código de estado e do código de estado. Exemplo: 200.300-305.404

</details>

<details>
<summary>3.4</summary>

## 3.4

- Habilitar suporte TLS1.0 e TLS1.1
- Adicionar o modo TFTP à procura de arquivos nos servidores tftp

</details>

<details>
<summary>3.3</summary>

## 3.3

- Suporte aos certificados do cliente TLS / mtls
- suportar o carregamento de extensões do arquivo
- apoio fuzzing POST corpo, cabeçalhos HTTP e autenticação básica
- nova opção para não canonicalizar nomes de cabeçalho

</details>

<details>
<summary>3.2</summary>

## 3.2

- Usar o 1.19
- usar contextos da maneira correta
- livrar-se da bandeira wildcard (exceto no modo DNS)
- saída de cor
- tentar novamente no tempo- limite
- enumeração do balde de nuvem do Google
- corrigir erros de referência nulos

</details>

<details>
<summary>3.1</summary>

## 3.1

- enumerar os baldes públicos AWS S3
- Modo fuzzing
- especificar o método HTTP
- suporte adicionado para padrões. Agora você pode especificar um arquivo que contém padrões que são aplicados a cada palavra, um por linha. Cada ocorrência do termo `{GOBUSTER}` nele será substituído pelo item da lista de palavras atual. Por favor, use com cautela, pois isso pode causar o aumento do número de solicitações emitidas muito.
- A faixa de taquigrafia `p` que foi atribuída ao proxy agora é usada pela bandeira padrão

</details>

<details>
<summary>3.0</summary>

## 3.0

- Novas opções CLI para que os modos são estritamente separados (`-m` agora desapareceu!)
- Otimizações de desempenho e melhor manuseio de conexão
- Capacidade de enumerar nomes de vhost
- Opção para fornecer cabeçalhos HTTP personalizados

</details>


---

## Procedência desta tradução

Fonte: [https://github.com/OJ/gobuster](https://github.com/OJ/gobuster/blob/c77583fbb8824058d74d38240896eff610683c8e/README.md). Licença: [Apache-2.0](../../99-Assets/upstream/gobuster/LICENSE.txt). Commit: c77583fbb8824058d74d38240896eff610683c8e.

O original preservado, a lista de mudanças de apresentação e os hashes constam no manifesto do projeto. Nenhum exemplo desta documentação foi executado automaticamente.
