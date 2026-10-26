# Política editorial e estilo

## Notas

- Um H1 por nota. H2 para seções e H3 para receitas. Não pular níveis.
- Título informativo, resumo curto, listas para passos e tabelas somente para comparar campos curtos.
- Identificadores e comandos em inglês; explicações em PT-BR nesta primeira coleção.
- Cada arquivo tem nome único e previsível. Pastas usam o slug da ferramenta.
- Propriedades YAML simples e de tipos consistentes. Não usar objetos aninhados em propriedades Obsidian.
- `status`: draft, source-checked, tested-local ou community-reviewed. Estado de teste é separado.
- `tags` têm vocabulário curto; `tool`, `type` e `status` são propriedades, não centenas de tags redundantes.
- Use links Markdown relativos. Wikilinks não são requisito para backlinks no Obsidian.
- Uma nota de conceito por assunto reutilizável; mapas são curadorias, não cópias de guias.

## Receitas

Cada comando deve ter objetivo, pré-requisitos, shell/OS, diretório de execução, comando completo,
saída esperada e interpretação. Diferencie saída esperada de saída realmente observada.
Use variáveis claras e defaults locais quando o exemplo for um laboratório reproduzível.
Não chame qualquer endereço indisponível de erro da ferramenta: conferir serviço, DNS, rota e VPN separadamente.

## Apresentação

Tema padrão funciona. Snippet CSS opcional melhora largura e tabelas sem fontes externas.
Use callouts nativos com moderação; nenhuma informação deve depender da cor.
Blocos de código sempre declaram linguagem. Não usar imagens de terminal no lugar de comandos copiáveis.
Não depender de Dataview, Templater ou Obsidian Git para leitura/navegação do release.

## Comunidade

Uma contribuição pequena por ferramenta ou correção. Exigir fontes primárias, versão e evidência
quando o autor disser que executou um comando. Sem publicação automática de rascunhos gerados por IA.
Separar revisão textual, teste técnico e permissão de redistribuição.
