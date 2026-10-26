---
title: "arjun — documentação oficial"
type: "official-documentation"
tool: "arjun"
status: "translated-machine"
reviewed: "2026-10-26"
language: "pt-BR"
tags: ["documentation", "tool/arjun"]
cssclasses: ["fieldbook"]
source_url: "https://github.com/s0md3v/Arjun/blob/d1fb995cb1e064d4e171d83f19f6af79b0a3c5ce/README.md"
source_commit: "d1fb995cb1e064d4e171d83f19f6af79b0a3c5ce"
source_sha256: "85840661f4beed51722b507a267d390f6a2938eb0dafd13d6a7ff5687b8ebdd3"
license_spdx: "AGPL-3.0"
human_review: "pending"
source_scope: "Repository root README and owned doc/docs/documentation Markdown or RST files; not a claim of full wiki/site coverage"
---

> Tradução automática local para português, ainda sem revisão humana integral. Estrutura e blocos de código preservados; referências externas não significam conteúdo espelhado.

# arjun — documentação oficial


<h1 align="center">
  <br>
  <a href="https://github.com/s0md3v/Arjun"></a>
  <br>
Arjun
  <br>
</h1>

<h4 align="center">HTTP Parâmetro Discovery Suite</h4>

<p align="center">
  <a href="https://github.com/s0md3v/Arjun/releases">
    
  </a>
  <a href="https://pypi.python.org/pypi/arjun/">
    
  </a>
  <a href="https://github.com/s0md3v/Arjun/issues?q=is%3Aissue+is%3Aclosed">
      
  </a>
  <a href="https://travis-ci.com/s0md3v/Arjun">
      
  </a>
</p>

[Imagem/recurso externo: demo](https://i.ibb.co/p3VKSRJ/arjun-demo.png)

<a id="whats-arjun"></a>
### O que é Arjun?

Arjun pode encontrar parâmetros de consulta para os endpoints de URL. Se você não entender o que isso significa, está tudo bem, leia junto.

Aplicações Web usam parâmetros (ou consultas) para aceitar a entrada do usuário, tome o exemplo seguinte em consideração

`http://api.example.com/v1/userinfo?id=751634589`

Este URL parece carregar informações do usuário para um ID de usuário específico, mas e se existir um parâmetro chamado `admin` que quando definido para `True` faz com que o endpoint forneça mais informações sobre o usuário?\
Isto é o que Arjun faz, ele encontra parâmetros válidos HTTP com um enorme dicionário padrão de 25.890 nomes de parâmetros.

A melhor parte? Leva menos de 10 segundos para passar por esta lista enorme enquanto faz apenas 50-60 pedidos para o alvo. [Aqui está como...](https://github.com/s0md3v/Arjun/wiki/How-Arjun-works%3F).

<a id="why-arjun"></a>
### Porquê Arjun?

- Suporta pedidos `GET/POST/POST-JSON/POST-XML`
- Lida automaticamente com limites de taxa e tempo- limite
- Exportar resultados para: BurpSuite, texto ou arquivo JSON
- Importar os alvos de: BurpSuite, arquivo de texto ou um arquivo de solicitação bruto
- Pode extrair passivamente parâmetros de JS ou 3 fontes externas

<a id="installing-arjun"></a>
### Instalando o Arjun
A forma recomendada de instalar o `arjun` é a seguinte:
```text
pipx install arjun
```
> Nota: Se você estiver usando uma versão antiga do python, use pip em vez de pipx.

<a id="how-to-use-arjun"></a>
### Como utilizar Arjun?

Um guia de uso detalhado está disponível na seção [Uso](https://github.com/s0md3v/Arjun/wiki/Usage) da Wiki.

Links diretos para algumas opções básicas são dadas abaixo:

- [Digitalizar um único URL](https://github.com/s0md3v/Arjun/wiki/Usage#scan-a-single-url)
- [Objectivos de importação](https://github.com/s0md3v/Arjun/wiki/Usage#import-multiple-targets)
- [Resultados da exportação](https://github.com/s0md3v/Arjun/wiki/Usage#save-output-to-a-file)
- [Usar cabeçalhos HTTP personalizados](https://github.com/s0md3v/Arjun/wiki/Usage#use-custom-http-headers)

Opcionalmente, você pode usar o argumento `--help` para explorar Arjun sozinho.

<a id="credits"></a>
##### Créditos
A lista de palavras de nomes de parâmetros é criada extraindo nomes de parâmetros de topo do conjunto de dados [Rastejo Comum](http://commoncrawl.org) e fundindo as melhores palavras do [SecListas](https://github.com/danielmiessler/SecLists) e [param-miner](https://github.com/PortSwigger/param-miner) em que.\
A lista de palavras `db/special.json` é tirada do [carga de dados](https://github.com/yehgdotnet/data-payloads).


---

## Procedência desta tradução

Fonte: [https://github.com/s0md3v/Arjun](https://github.com/s0md3v/Arjun/blob/d1fb995cb1e064d4e171d83f19f6af79b0a3c5ce/README.md). Licença: [AGPL-3.0](../../99-Assets/upstream/arjun/LICENSE.txt). Commit: d1fb995cb1e064d4e171d83f19f6af79b0a3c5ce.

O original preservado, a lista de mudanças de apresentação e os hashes constam no manifesto do projeto. Nenhum exemplo desta documentação foi executado automaticamente.
