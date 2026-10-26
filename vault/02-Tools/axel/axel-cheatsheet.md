---
title: "Axel — cheatsheet"
type: "cheatsheet"
tool: "axel"
status: "tested-local"
reviewed: "2026-10-26"
language: "pt-BR"
tags: ["cheatsheet", "tool/axel", "category/download"]
cssclasses: ["fieldbook"]
test_status: "partial-local"
tested_version: "2.17.14"
---

# Axel — cheatsheet

[Manual de referência em português](axel-doc-axel-txt.md) · [README upstream](axel-documentacao.md) · [Evidência dos testes](../../99-Assets/evidence/axel-local-tests.json).

## Versão e ajuda

```bash
# Bash · diretório atual · Kali Linux/WSL · Axel instalado
axel --version
axel --help
```

Observado: **Axel 2.17.14**. Ambos os comandos retornaram código 0.

## Download com limites explícitos

Receita parametrizada com as mesmas opções do download local verificado. Defina `URL` e `OUTPUT` antes de executá-la. A receita é uma adaptação; não substitui os exemplos literais do manual.

```bash
# Bash · diretório atual · Kali Linux/WSL · Axel instalado
axel -q -n 2 -s 131072 -T 5 \
  -H "X-Fieldbook: offline-fixture" -U "Fieldbook-Axel-Test" \
  -o "${OUTPUT:?Defina OUTPUT como o caminho de saída}" \
  "${URL:?Defina URL como a URL do arquivo}"
```

| Opção | Função |
|---|---|
| `-q` | Silenciar a saída normal |
| `-n 2` | Usar até duas conexões na versão testada |
| `-s 131072` | Limitar a velocidade a 131.072 bytes/s |
| `-T 5` | Definir o tempo limite de I/O e conexão |
| `-H` | Acrescentar um cabeçalho HTTP |
| `-U` | Definir o User-Agent |
| `-o` | Escolher o arquivo de saída |

No teste, o download de **65.536 bytes** retornou código 0; o hash coincidiu com a fixture, a saída normal ficou vazia e o servidor recebeu os cabeçalhos esperados.

## Não sobrescrever um download completo

```bash
# Bash · diretório atual · Kali Linux/WSL · Axel instalado
axel -c -q \
  -o "${OUTPUT:?Defina OUTPUT como um arquivo já existente}" \
  "${URL:?Defina URL como a URL do arquivo}"
```

**Comportamento observado:** com um arquivo completo já existente e sem arquivo de estado, o conteúdo permaneceu inalterado, mas o Axel 2.17.14 retornou **código 1** e a mensagem "No state file, cannot resume!". Isso não foi uma conclusão bem-sucedida de download nem prova de corrupção: foi uma recusa de retomada nessa instalação. A descrição upstream de `-c` e esse resultado local estão registrados separadamente, sem ocultar a divergência.

## Reproduzir o teste sem internet

Execute na raiz do repositório, dentro do Kali:

```bash
# Bash · raiz do repositório · Kali Linux/WSL · Python 3 e Axel instalados
python3 scripts/test_axel.py
```

O script abre uma fixture HTTP em `127.0.0.1` com porta temporária, oferece respostas a intervalos de bytes, verifica o download por SHA-256 e encerra o servidor ao terminar. O arquivo temporário também é removido. Ele não instala pacotes, não acessa URLs externas e, por padrão, não reescreve as evidências congeladas do repositório.

## Diferenças de versão que importam

- A ajuda local não lista `--location-trusted`, `--netrc`, `--no-netrc` ou `--progress`.
- Para a opção curta `-p`, a ajuda local apresenta `--percentage`; a fonte do manual apresenta `--progress`.
- O manual preserva as 22 opções da fonte fixada, sem apresentá-las como se todas tivessem sido testadas no pacote local.
- FTP, TLS, proxies, espelhos externos e as demais opções não foram exercitados.

## Procedência

As descrições foram conferidas com a ajuda instalada e com o [manual oficial fixado](https://github.com/axel-download-accelerator/axel/blob/dc10ba0c8f8d804c1568df5dba3cdd6fa89572b1/doc/axel.txt). O manual e sua tradução mantêm a licença GPL-2.0; esta folha autoral é complementar.
