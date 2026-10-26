---
title: "arsenal-ng — documentação oficial"
type: "official-documentation"
tool: "arsenal-ng"
status: "translated-machine"
reviewed: "2026-10-26"
language: "pt-BR"
tags: ["documentation", "tool/arsenal-ng"]
cssclasses: ["fieldbook"]
source_url: "https://github.com/halilkirazkaya/arsenal-ng/blob/58e18e015eddf4d379aa49454fd13194fd5546db/README.md"
source_commit: "58e18e015eddf4d379aa49454fd13194fd5546db"
source_sha256: "a7923931d363d28d4e69b27cbf96e9761d6afd55ff1d6fe68a39eded28e2c765"
license_spdx: "MIT"
human_review: "pending"
source_scope: "Repository root README and owned doc/docs/documentation Markdown or RST files; not a claim of full wiki/site coverage"
---

> Tradução automática local para português, ainda sem revisão humana integral. Estrutura e blocos de código preservados; referências externas não significam conteúdo espelhado.

# arsenal-ng — documentação oficial

<h1 align="center">arsenal-ng</h1>

<p align="center">
  
  
  
  <br>
  
  
</p>

<p align="center">
<b>🎯 Lançador de comando moderno pentest escrito em Go!</b>
</p>

<p align="center">
Inspirado em <a href="https://github.com/Orange-Cyberdefense/arsenal">arsenal</a>, reescrito do zero com foco na simplicidade, velocidade e experiência do desenvolvedor.
</p>

<p align="center">
  <img src="../../99-Assets/upstream/arsenal-ng/assets/basic-search.gif" alt="Basic Search Demo" width="800">
</p>

---

<a id="installation"></a>
## Instalação

<a id="option-1-go-install"></a>
### Opção 1: Instalação do Go

```bash
go install -v github.com/halilkirazkaya/arsenal-ng/cmd/arsenal-ng@latest
```
> Requer Go 1.24.0 Garanta que `$(go env GOPATH)/bin` está em seu `$PATH`.


<a id="option-2-kali-linux-apt"></a>
### Opção 2: Kali Linux (APT)

O Kali Linux envia o `arsenal-ng` nos seus repositórios oficiais. [Rastreador de pacotes](https://pkg.kali.org/pkg/arsenal-ng)

```bash
sudo apt install arsenal-ng
```

<a id="option-3-build-from-source-code"></a>
### Opção 3: Compilar a partir do código-fonte

```bash
git clone https://github.com/halilkirazkaya/arsenal-ng.git
cd arsenal-ng
make build
./bin/arsenal-ng
```

<a id="alias-optional"></a>
### Apelido (Opcional)

Você pode criar um alias para acesso rápido (por exemplo, `a`):

**Zsh:**
```bash
echo "alias a='arsenal-ng'" >> ~/.zshrc
source ~/.zshrc
```

**Bash:**
```bash
echo "alias a='arsenal-ng'" >> ~/.bashrc
source ~/.bashrc
```
---

<a id="platform-support"></a>
## Suporte à Plataforma

|Plataforma|Estado|Notas|
|----------|--------|-------|
|**Linux**|□ Totalmente Suportado|Requer configuração 6.2+ do kernel para pré- preenchimento do terminal (ver [Configuração do Linux](#configuração-do-linux))|
|**macOS**|□ Totalmente Suportado|Funciona fora da caixa, nenhuma configuração adicional necessária|
|**Windows**|Apenas WSL|Nativo (CMD/PowerShell) é **unsuportado**. Uso via **WSL**.|

---

<a id="linux-configuration"></a>
## Configuração do Linux

<a id="terminal-prefill-not-working-linux-kernel-62"></a>
### Prefil de Terminal Não Funciona ( kernel Linux 6.2+)

O `arsenal-ng` depende deste recurso para preencher o buffer de terminal. Você tem duas opções para habilitar esta funcionalidade, ambas com trade-offs de segurança.

<a id="option-1-enable-tiocsti-globally"></a>
#### Opção 1: Activar o TIOCSTI Globalmente
O ioctl TIOCsti está desativado por padrão em kernels Linux mais recentes por razões de segurança.

```bash
# Temporary (current session only)
sudo sysctl -w dev.tty.legacy_tiocsti=1

# Permanent (survives reboot)
echo "dev.tty.legacy_tiocsti=1" | sudo tee /etc/sysctl.d/99-tiocsti.conf
sudo sysctl --system
```

<a id="option-2-grant-cap_sys_admin-capability"></a>
#### Opção 2: Subvencionar a capacidade CAP_SYS_ADMIN
Em vez de modificar as configurações de todo o sistema, você pode conceder a capacidade `CAP_SYS_ADMIN` especificamente para o binário arsenal-ng.
CAP_SYS_ADMIN é poderoso e virtualmente equivalente ao acesso `root`. Use este método somente se você entender completamente os riscos.

```Bash
# Ensure 'setcap' is installed (Debian/Kali/Ubuntu)
sudo apt-get install libcap2-bin

# Grant the required capability to the binary
sudo setcap "cap_sys_admin+ep" $(which arsenal-ng)
```

---

<a id="features"></a>
## Características

|Característica|Designação das mercadorias|
|---------|-------------|
|**Instant Startup**|binário único, sem dependências, lança em milissegundos|
|🔍 **Smart Search**|Pesquisa multi-palavras fuzzy entre nomes de ferramentas, títulos, tags, descrições e comandos|
|🎨 **Syntax Highlighting**|Os comandos são codificados a cores com realce de sintaxe para melhor legibilidade|
|🏷® ** Etiquetas coloridas**|Cada tag tem uma cor consistente, distinta com base no hash para identificação visual rápida|
|📝 **Simple YAML Format**|Fácil de manter e estender as folhas de fraude|
|🔧 **Sistema de Argumento**|Suporte para `{{arg}}` e `{{arg\|default}}` placeholders com auto-completar|
|🌐 **Variáveis globais**|Definir uma vez, usar em qualquer lugar - as variáveis preenchem automaticamente todos os comandos|
|📊 **Tools View**|Navegue em todas as ferramentas disponíveis com contagens de comandos em uma tabela paginada|
|💡 **Dicas de Comando**|Dicas interativas para comandos especiais (`set`, `unset`, `variables`, `tools`)|
|• **Construído em Help**|Pressione `?` para uma tela de ajuda abrangente com todos os atalhos|
|🖥 o ** Integração Terminal**|Os comandos são gravados no buffer de entrada de terminal para edição fácil antes da execução|

---

<a id="usage"></a>
## Uso

<a id="quick-start"></a>
### Início Rápido

```bash
# Launch the application
arsenal-ng

# The TUI will open with all available commands
# Use arrow keys to navigate, type to search, Enter to select
```

O comando selecionado aparecerá em seu buffer de entrada de terminal, pronto para editar e executar.

<a id="basic-workflow"></a>
### Fluxo de Trabalho Básico

1. **Search for a command**: Digite palavras-chave (por exemplo, `nmap scan`, `ffuf`)
2. **Navigar resultados**: Use as teclas de seta para procurar comandos correspondentes
3. **Select command**: Pressione Enter no comando desejado
4. **Fill arguments**: Se o comando tiver `{{placeholders}}`, preencha-os
5. **Execute**: Pressione Enter para escrever o comando no seu terminal

<a id="example-session"></a>
### Sessão de Exemplo

```bash
# 1. Launch arsenal-ng
arsenal-ng

# 2. Set global variables (type in search box)
set target=10.10.10.10

# 3. Search for nmap commands
nmap

# 4. Select "nmap - syn stealth scan"
# The {{target}} placeholder is auto-filled with 10.10.10.10!

# 5. Command appears in terminal:
nmap -sS 10.10.10.10

# 6. Edit if needed, then press Enter to execute
```

<a id="keyboard-shortcuts"></a>
### Atalhos do Teclado

<a id="main-search-view"></a>
#### Área de Pesquisa Principal
|Chave|Acção|
|-----|--------|
|`↑` / `↓`|Navegar para cima/para baixo na lista|
|`Ctrl+P` / `Ctrl+N`|Navegar na lista (estilo de Vim)|
|`PgUp` / `PgDown`|Saltar uma página para cima/para baixo|
|`Enter`|Selecione o comando destacado ou execute o comando especial|
|`Esc` / `Ctrl+C`|Sair da aplicação|
|`?`|Mostrar o tela de ajuda|
|`q`|Sair (em algumas vistas)|

<a id="argument-input-view"></a>
#### Vista de Entrada de Argumentos
|Chave|Acção|
|-----|--------|
|`Tab` / `↓`|Mover para o campo de argumentos seguinte|
|`Shift+Tab` / `↑`|Mover para o campo de argumentos anterior|
|`Enter`|Executar o comando com argumentos preenchidos|
|`Esc`|Go voltar à área de pesquisa|

<a id="tools-view"></a>
#### Ver Ferramentas

<p align="center">
  <img src="../../99-Assets/upstream/arsenal-ng/assets/tools-view.gif" alt="Tools View Demo" width="800">
</p>

|Chave|Acção|
|-----|--------|
|`↑` / `↓`|Navegar pelas linhas da tabela|
|`←` / `→` ou `h` / `l`|Alterar página (anterior/próximo)|
|`Enter` / `Esc`|Go voltar à área de pesquisa|



<a id="help-views"></a>
#### Áreas de Ajuda

<p align="center">
  <img src="../../99-Assets/upstream/arsenal-ng/assets/help-screen.gif" alt="Help Screen Demo" width="800">
</p>

|Chave|Acção|
|-----|--------|
|`Enter` / `Esc`|Go voltar à área de pesquisa|

---

<a id="global-variables"></a>
## Variáveis globais

Define as variáveis uma vez e reutilize- as em todos os comandos na sua sessão. As variáveis preenchem automaticamente os campos de argumentos nos comandos.

<a id="special-commands"></a>
### Comandos Especiais

|Comando|Designação das mercadorias|
|---------|-------------|
|`set key=value`|Definir uma variável global (por exemplo, `set ip=10.10.10.10`)|
|`unset key`|Remover uma variável global|
|`variables`|Listar todas as variáveis atualmente definidas|
|`tools`|Mostrar todas as ferramentas disponíveis com contagens de comandos|
|`help`|Exibir tela de ajuda abrangente|

<a id="how-it-works"></a>
### Como funciona

<p align="center">
  <img src="../../99-Assets/upstream/arsenal-ng/assets/variables.gif" alt="Variables Demo" width="800">
</p>

1. Digite `set ip=10.10.10.10` e pressione Enter
2. Selecione qualquer comando com o placeholder `{{ip}}`
3. O campo `ip` será **pre-cheio** automaticamente com `10.10.10.10`
4. Você ainda pode editar o valor pré- preenchido, se necessário
5. As variáveis persistem durante toda a sua sessão até que você as saia ou desmarque

<a id="example-workflow"></a>
### Exemplo de fluxo de trabalho

```bash
# Set common variables at the start of your session
set ip=10.10.10.10
set domain=corp.local
set user=administrator

# Now select any command - arguments will auto-fill!
# Before: nmap -sV {{ip}}
# After:  nmap -sV 10.10.10.10  (auto-filled!)

# View all variables
variables

# Remove a variable when done
unset ip
```

<a id="common-variables"></a>
### Variáveis comuns

|Variável|Designação das mercadorias|
|----------|-------------|
|`ip`|Endereço IP do alvo|
|`domain`|Domínio do alvo|
|`user`|Nome de usuário|
|`pass`|Senha|
|`hash`|NTLM hash|
|`url`|URL do alvo|
|`port`|Número do porto|
|`lhost`|Máquina local (seu IP)|
|`lport`|Porto local|
|`wordlist`|Localização da lista de palavras|
|`output`|Nome do arquivo de saída|

---

<a id="cheat-file-format"></a>
## Formato de arquivo de fraude

Adicione seus próprios comandos criando arquivos YAML em `internal/loader/cheat-files/`:

```yaml
tool: mytool
tags: [recon, web, custom]

actions:
  - title: mytool - basic scan
    desc: Performs a basic scan against the target
    command: "mytool scan {{target}}"

  - title: mytool - scan with multiple arguments
    desc: Advanced scan with IP, port, and output file
    command: "mytool scan -t {{ip}} -p {{port|443}} -o {{output|scan.log}}"
```

<a id="argument-syntax"></a>
### Sintaxe do Argumento

|Sintaxe|Designação das mercadorias|Exemplo|
|--------|-------------|---------|
|`{{arg}}`|Argumento exigido (o usuário deve preencher)|`{{ip}}`|
|`{{arg\|default}}`|Argumento com valor padrão (pode ser editado)|`{{port\|8080}}`|

<a id="file-structure"></a>
### Estrutura do arquivo

- **tool**: Nome da ferramenta (por exemplo, `nmap`, `ffuf`, `gobuster`)
- **tags**: Array de tags para categorização (por exemplo, `[recon, scan, network]`)
- **actions**: Lista de entradas de comando
  - **title**: Mostrar o nome mostrado na lista
  - **desc**: Descrição opcional (mostrada na caixa de informações)
  - **command**: Modelo de comando com `{{placeholders}}`

<a id="tips"></a>
### Dicas

- Usar títulos descritivos que tornam mais fácil encontrar comandos
- Adicionar etiquetas relevantes para uma melhor buscabilidade
- Usar valores predefinidos para as opções comumente usadas
- Variáveis globais irão preencher automaticamente os nomes dos argumentos correspondentes

---

<a id="development"></a>
## Desenvolvimento

<a id="prerequisites"></a>
### Pré-requisitos

- Go 1.24.0 ou superior
- Marca (opcional, para usar Makefile)

<a id="building-from-source"></a>
### Compilando a partir do Código

```bash
git clone https://github.com/halilkirazkaya/arsenal-ng.git
cd arsenal-ng
make build
# Binary will be in ./bin/arsenal-ng
```

Ou construir diretamente com Go:

```bash
go build -o bin/arsenal-ng ./cmd/arsenal-ng
```

<a id="adding-new-tools"></a>
### Adicionando novas ferramentas

1. Criar um novo arquivo YAML no `internal/loader/cheat-files/`
2. Siga o formato acima (ver [Formato de arquivo de fraude](#formato-de-arquivo-de-fraude))
3. Reconstruir: `make build`

<a id="testing"></a>
### Teste

Após fazer alterações, reconstruir e testar:

```bash
make build
./bin/arsenal-ng
```

<a id="contributing-guidelines"></a>
### Orientações para a contribuição

- Siga as convenções de estilo de código Go
- Mantenha os arquivos YAML organizados e bem documentados
- Adicionar títulos descritivos e etiquetas aos comandos
- Teste suas alterações antes de enviar RPs

<a id="features-1"></a>
## Características

Este projeto é **open source** e contribuições são bem-vindas!

<a id="how-to-contribute"></a>
### Como contribuir

- 🔧 **Adicionar uma ferramenta**: Criar um arquivo YAML em `internal/loader/cheat-files/` e enviar uma PR
- 🐛 **Report bugs**: Abra um problema com detalhes sobre o problema
- 💡 **Suggest features**: Compartilhe suas ideias para melhorias
- 📝 **Improve documentation**: Ajude a melhorar o README e os comentários de código
- **Star o projeto**: Mostre seu suporte!

<a id="adding-cheat-sheets"></a>
### Adicionando folhas de fraude

A maneira mais fácil de contribuir é adicionando novos arquivos YAML folha de fraude:

1. Forque o repositório
2. Adicione o seu( s) arquivo( s) YAML( s) ao `internal/loader/cheat-files/`
3. Siga o formato e estilo existentes
4. Testar as suas alterações localmente
5. Enviar um pedido de pull

Veja [Formato de arquivo de fraude](#formato-de-arquivo-de-fraude) para mais detalhes.

---

<p align="center">
Feita com o <a href="https://github.com/charmbracelet/bubbletea">Bubble Tea</a>
</p>


---

## Procedência desta tradução

Fonte: [https://github.com/halilkirazkaya/arsenal-ng](https://github.com/halilkirazkaya/arsenal-ng/blob/58e18e015eddf4d379aa49454fd13194fd5546db/README.md). Licença: [MIT](../../99-Assets/upstream/arsenal-ng/LICENSE.txt). Commit: 58e18e015eddf4d379aa49454fd13194fd5546db.

O original preservado, a lista de mudanças de apresentação e os hashes constam no manifesto do projeto. Nenhum exemplo desta documentação foi executado automaticamente.
