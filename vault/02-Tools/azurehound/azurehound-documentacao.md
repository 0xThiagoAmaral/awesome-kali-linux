---
title: "azurehound — documentação oficial"
type: "official-documentation"
tool: "azurehound"
status: "translated-machine"
reviewed: "2026-10-26"
language: "pt-BR"
tags: ["documentation", "tool/azurehound"]
cssclasses: ["fieldbook"]
source_url: "https://github.com/SpecterOps/AzureHound/blob/b02d4577731f69c729a53055a09c44673689eefd/README.md"
source_commit: "b02d4577731f69c729a53055a09c44673689eefd"
source_sha256: "3d8e4489006823a8e6bef6ac0cf3ad5d9f51a4abfcfb0bcd7af65a3e56f954c4"
license_spdx: "GPL-3.0"
human_review: "pending"
source_scope: "Repository root README and owned doc/docs/documentation Markdown or RST files; not a claim of full wiki/site coverage"
---

> Tradução automática local para português, ainda sem revisão humana integral. Estrutura e blocos de código preservados; referências externas não significam conteúdo espelhado.

# AzureHound

O coletor de dados BloodHound para Microsoft Azure

[Imagem/recurso externo: GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/SpecterOps/AzureHound/build.yml)
[Imagem/recurso externo: GitHub release (latest SemVer)](https://img.shields.io/github/v/release/SpecterOps/AzureHound)
[Imagem/recurso externo: GitHub all releases](https://img.shields.io/github/downloads/SpecterOps/AzureHound/total)
[Documentation](https://pkg.go.dev/github.com/SpecterOps/AzureHound/v2)

<a id="get-azurehound"></a>
## Obter o AzureHound

<a id="release-binaries"></a>
### Binários de Lançamento

Baixe o binário apropriado para sua plataforma a partir de um dos nossos [Lançamentos](https://github.com/SpecterOps/AzureHound/releases).

<a id="rolling-release"></a>
#### Release de rolamento

A versão de rolamento contém binários pré-construídos que são automaticamente mantidos atualizados com o ramo `main` e podem ser baixados de
[Aqui.](https://github.com/SpecterOps/AzureHound/releases/tag/rolling).

> **Aviso:** A liberação de rolamento pode ser instável.

<a id="compiling"></a>
## Compilação

<a id="prerequisites"></a>
##### Pré-requisitos

- [Go  1.25](https://go.dev/dl/) ou posterior

Para compilar este projeto a partir do código-fonte execute o seguinte:

```sh
go build -o azurehound -ldflags="-s -w -X github.com/SpecterOps/AzureHound/v2/constants.Version=`git describe tags --exact-match 2> /dev/null || git rev-parse HEAD`"
```

<a id="documentation"></a>
## Documentação

Consulte o [Documentação da edição comunitária do BloodHound](https://bloodhound.specterops.io/home) para:
- [Edição da Comunidade de AzureHound](https://bloodhound.specterops.io/collect-data/ce-collection/azurehound)
- [Bandeiras da edição comunitária de AzureHound](https://bloodhound.specterops.io/collect-data/ce-collection/azurehound-flags)

<a id="usage"></a>
## Uso

<a id="quickstart"></a>
### Início rápido

**Imprimir todos os dados do Azure Tenant para o stdout**

```sh
❯ azurehound list -u "$USERNAME" -p "$PASSWORD" -t "$TENANT"
```

**Print todos os dados do Azure Tenant para o arquivo**

```sh
❯ azurehound list -u "$USERNAME" -p "$PASSWORD" -t "$TENANT" -o "mytenant.json"
```

**Print todos os dados Azure Tenant para arquivo, reutilizando sua autenticação existente do Azure CLI**

```text
❯ JWT=$(az account get-access-token --resource https://graph.microsoft.com | jq -r .accessToken)
❯ azurehound list --jwt "$JWT"
```

**Configure e inicie o serviço de coleta de dados para BloodHound Enterprise**

```sh
❯ azurehound configure
(follow prompts)

❯ azurehound start
```

### CLI

```text
❯ azurehound --help
AzureHound vx.x.x
Created by the BloodHound Enterprise team at SpecterOps - [https://bloodhoundenterprise.io](https://specterops.io/bloodhound-overview/)

The official tool for collecting Azure data for BloodHound Community Edition and BloodHound Enterprise

Usage:
  azurehound [command]

Available Commands:
  completion  Generate the autocompletion script for the specified shell
  configure   Configure AzureHound
  help        Help about any command
  list        Lists Azure Objects
  start       Start Azure data collection service for BloodHound Enterprise

Flags:
  -c, --config string          AzureHound configuration file (default: /Users/dlees/.config/azurehound/config.json)
  -h, --help                   help for azurehound
      --json                   Output logs as json
  -j, --jwt string             Use an acquired JWT to authenticate into Azure
      --log-compress           Compress rotated logs with gzip (default: true)
      --log-file string        Output logs to this file
      --log-max-age int        Maximum age in days for rotated logs (default: 14; 0 disables age pruning)
      --log-max-backups int    Maximum number of rotated logs to retain (default: 20; 0 disables count pruning)
      --log-max-size int       Maximum active log size in MiB before rotation (default: 100)
      --proxy string           Sets the proxy URL for the AzureHound service
  -r, --refresh-token string   Use an acquired refresh token to authenticate into Azure
  -v, --verbosity int          AzureHound verbosity level (defaults to 0) [Min: -1, Max: 2]
      --version                version for azurehound

Use "azurehound [command] --help" for more information about a command.
```

<a id="log-file-management"></a>
### Gestão de arquivos de registo

Quando o `--log-file` está configurado, o AzureHound roda o log ativo quando atinge o `--log-max-size`. Os logs rotacionados são cronometrados, armazenados ao lado do log ativo e compactados com gzip por padrão.

Os arquivos são retidos no máximo por dias `--log-max-age` e também são limitados pelo `--log-max-backups`. Definir uma das opções de retenção para `0` desabilita esse limite individual. Os padrões não retêm mais de 20 arquivos ou 14 dias de história. Apenas um processo AzureHound deve escrever para um determinado arquivo de registro.


---

## Procedência desta tradução

Fonte: [https://github.com/SpecterOps/AzureHound](https://github.com/SpecterOps/AzureHound/blob/b02d4577731f69c729a53055a09c44673689eefd/README.md). Licença: [GPL-3.0](../../99-Assets/upstream/azurehound/LICENSE.txt). Commit: b02d4577731f69c729a53055a09c44673689eefd.

O original preservado, a lista de mudanças de apresentação e os hashes constam no manifesto do projeto. Nenhum exemplo desta documentação foi executado automaticamente.
