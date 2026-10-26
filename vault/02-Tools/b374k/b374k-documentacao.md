---
title: "b374k — documentação oficial"
type: "official-documentation"
tool: "b374k"
status: "translated-machine"
reviewed: "2026-10-26"
language: "pt-BR"
tags: ["documentation", "tool/b374k"]
cssclasses: ["fieldbook"]
source_url: "https://github.com/b374k/b374k/blob/3e456486c94582e2403f047c80500da3261694ab/README.md"
source_commit: "3e456486c94582e2403f047c80500da3261694ab"
source_sha256: "ee9b184309c7d53f7b7cefff185e28be30470362ede3ffb79c8d4c21280d20e6"
license_spdx: "MIT"
human_review: "pending"
source_scope: "Repository root README and owned doc/docs/documentation Markdown or RST files; not a claim of full wiki/site coverage"
---

> Tradução automática local para português, ainda sem revisão humana integral. Estrutura e blocos de código preservados; referências externas não significam conteúdo espelhado.

# b374k shell 3.2
Este PHP Shell é uma ferramenta útil para o administrador de sistema ou web para fazer gerenciamento remoto sem usar cpanel, conectando-se usando ssh, ftp etc Todas as ações ocorrem dentro de um navegador web

Características :
 * Gerenciador de arquivos (ver, editar, renomear, excluir, carregar, baixar, arquivar, etc.)
 * Procurar arquivo, conteúdo de arquivo, pasta (também usando regex)
 * Execução de comandos
 * Execução do programa (php, perl, python, ruby, java, node.js, c)
 * Dar-lhe shell através de ligação de linha de ligação/ inversão
 * crafter de pacotes simples
 * Conecte-se ao DBMS (mysql, mssql, oráculo, sqlite, postgresql e muitos mais usando ODBC ou PDO)
 * SQL Explorer
 * Lista de processos/gerenciador de tarefas
 * Enviar e- mail com anexo (você pode anexar o arquivo local no servidor)
 * Conversão de texto
 * Tudo isso apenas em 1 arquivo, nenhuma instalação necessária
 * Suporte PHP > 4.3.3 e PHP 5

<a id="requirements-"></a>
## Requisitos:
 * Versão PHP > 4.3.3 e PHP 5
 * Como ele usa zepto.js v1.1.2, você precisa de navegador moderno para usar b374k shell. Veja o suporte do navegador no site zepto.js http://zeptojs.com/
 * Responsabilidade do que você faz com esta concha
 
<a id="installation-"></a>
## Instalação:
Baixar b374k.php (senha padrão : b374k), editar e alterar senha e carregar b374k.php para seu servidor, senha está no formato sha1(md5(). Ou criar seu próprio b374k.php, explicado abaixo

<a id="customize-"></a>
## Personalizar :
Depois de terminar de editar com arquivos, upload index.php, base, módulo, tema e todos os arquivos dentro dele para um servidor

Usando o Navegador Web :

Abra index.php em seu navegador, a execução rápida só executará a shell. Use o empacotador para embalar todos os arquivos em um único arquivo PHP. Defina todas as opções disponíveis e o arquivo de saída estará no mesmo diretório que index.php

Usando Console :
```text
$ php -f index.php
b374k shell packer 0.4

options :
        -o filename                             save as filename
        -p password                             protect with password
        -t theme                                theme to use
        -m modules                              modules to pack separated by comma
        -s                                      strip comments and whitespaces
        -b                                      encode with base64
        -z [no|gzdeflate|gzencode|gzcompress]   compression (use only with -b)
        -c [0-9]                                level of compression
        -l                                      list available modules
        -k                                      list available themes
```
exemplo :
```text
$ php -f index.php -- -o myShell.php -p myPassword -s -b -z gzcompress -c 9
```
Não se esqueça de excluir index.php, base, módulo, tema e todos os arquivos dentro dele depois que você terminou. Porque ele não está protegido com senha para que possa ser uma ameaça de segurança para o seu servidor

<a id="documentation-"></a>
## Documentação:
Em breve.

<a id="old-version-"></a>
## Versão antiga:
Se o seu navegador não for suportado, ou qualquer outra razão, você pode ver a versão antiga aqui
https://code.google.com/p/b374k-shell/


---

## Procedência desta tradução

Fonte: [https://github.com/b374k/b374k](https://github.com/b374k/b374k/blob/3e456486c94582e2403f047c80500da3261694ab/README.md). Licença: [MIT](../../99-Assets/upstream/b374k/LICENSE.txt). Commit: 3e456486c94582e2403f047c80500da3261694ab.

O original preservado, a lista de mudanças de apresentação e os hashes constam no manifesto do projeto. Nenhum exemplo desta documentação foi executado automaticamente.
