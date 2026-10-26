# Plano do projeto

## Produto

Um fieldbook comunitário que continua útil quando a conexão cai: pesquisar uma ferramenta, entender
seu propósito, selecionar um comando, interpretar a saída e diagnosticar o erro sem abrir um site.
O vault não instala nem executa ferramentas automaticamente.

## Escopo e unidade editorial

Cada ferramenta real tem uma pasta com quatro notas de nomes únicos:
`ferramenta-guia.md`, `ferramenta-cheatsheet.md`, `ferramenta-troubleshooting.md` e `ferramenta-fontes.md`.
Bibliotecas, runtimes, aliases e coleções de dados entram como dependências/recursos ou apontam
para a nota principal; não viram quatro páginas vazias cada um.

O inventário anterior forneceu 178 pacotes associados a categorias Kali e 82 entradas extras.
São 260 registros candidatos antes da triagem, não 260 ferramentas independentes.

## Três camadas de documentação

1. **Essencial offline:** guia autoral e cheatsheet com comandos, parâmetros, pré-requisitos,
   interpretação, erros e limites do ambiente. Sempre incluída no release.
2. **Referência oficial:** URLs, versão/tag/commit, data de consulta e identificação da licença.
3. **Espelho autorizado:** cópia local de manuais/assets SOMENTE após verificar a licença específica,
   incluir avisos/atribuições e registrar arquivo, origem, data e SHA-256. Licença desconhecida bloqueia
   a redistribuição daquela cópia, não a escrita de uma explicação própria.

Salvar apenas links não resolve o problema de conexão. Redistribuir qualquer página encontrada
também não é um plano editorial sustentável.

## Organização

Ferramentas vivem em um único lugar. Mapas por categoria e workflows apontam para elas.
Conceitos reutilizáveis (TCP, filtros, HTTP, wordlists) têm notas pequenas próprias para evitar
explicar a mesma coisa de maneiras incompatíveis em vinte guias.
Não é necessário transformar uma referência técnica em um Zettelkasten de centenas de fragmentos.

## Fluxo de produção

inventário -> triagem -> fonte oficial -> síntese autoral -> exemplos -> teste local -> revisão -> release.

IA pode auxiliar pesquisa, rascunho e detecção de inconsistências. Não promove texto automaticamente
a conteúdo testado. Cada comando precisa de fonte, contexto de execução e resultado esperado.
Testes devem registrar entrada, stdout, stderr, exit status, versão e ambiente, sem material pessoal.

## Qualidade por módulo

- Uma frase explica para que serve e quando NÃO serve.
- Há pré-requisitos, instalação/referência e limitações de Kali/WSL quando relevantes.
- A cheatsheet inicial contém 5 a 10 receitas úteis, sem inflar com combinações redundantes.
- Cada receita informa objetivo, diretório de execução, variáveis, comando e interpretação.
- Guia, cheatsheet, troubleshooting e fontes estão ligados e sem links locais quebrados.
- Testes têm escopo explícito: um smoke test não valida todas as opções da ferramenta.
- Versão e data de revisão estão registradas; mudança incompatível abre revisão.
- Imagens e arquivos necessários estão presentes localmente; não há imagem remota indispensável.
- Conteúdo copiado tem licença/atribuição verificadas; exemplos usam dados sintéticos.

## Publicação comunitária

GitHub armazena a fonte. GitHub Releases distribui um ZIP completo do vault com manifesto SHA-256,
changelog e lista do que está efetivamente revisado. Não exigir Git LFS, submódulos, plugins ou
fontes remotas para ler o material já baixado.

Proposta de licenças: documentação autoral em CC BY-SA 4.0 e scripts em MIT, a confirmar pelo autor.
Material de terceiros mantém licença e avisos próprios. O protótipo não concede essas licenças por antecipação.

Antes do primeiro push: escolher licença, revisar diff, remover dados privados, habilitar proteções
de segredos e executar verificações. Não enviar o inventário bruto da máquina.
CI proposta: validação offline, lint Markdown, schema, checagem de links locais e detecção de segredos;
checagem de URLs externas é uma etapa separada quando houver conexão.

## Métricas

Medir módulos revisados/planejados, receitas testadas/receitas existentes, links locais quebrados,
fontes com procedência e notas com revisão vencida. Não usar número de arquivos como medida de qualidade.

## Aceite do MVP

Dez módulos priorizados, navegação por categoria, leitura sem internet, testes reproduzíveis,
licenciamento definido e ZIP verificado. Testar extração em pasta limpa e abertura no Obsidian.
O protótipo atual demonstra a estrutura com dois módulos e não equivale ao MVP concluído.
