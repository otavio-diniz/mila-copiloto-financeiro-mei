# Contribuição e Fluxo Autoral

## Princípio

Este repositório acompanha um desafio acadêmico formal. O conteúdo deve preservar autoria, proveniência e separação entre referência e produção própria.

## Fluxo

1. Decisão autoral aprovada.
2. Materialização na etapa correspondente.
3. Implementação pelo autor.
4. Revisão e testes.
5. Evidência de funcionamento.
6. Promoção ao próximo gate.

## Branches

- `main`: estado integrado e revisado.
- `develop`: trabalho em andamento.
- branches de tarefa: `feat/<tema>`, `docs/<tema>`, `fix/<tema>`.

## Commits

Preferir mensagens curtas e descritivas, por exemplo:

- `docs: registra decisao autoral da etapa 2`
- `feat: adiciona classificador de transacoes`
- `test: cobre movimentacoes ambiguas`
- `fix: corrige calculo de fluxo projetado`

## Documentação pública

Mudanças no README ou em documentação voltada a avaliadores/visitantes devem preservar:

- **hierarquia de informação:** o leitor deve entender primeiro o que é o projeto, por que existe e o que faz antes de entrar em detalhes operacionais;
- **cronologia de leitura:** visão/problema → solução/capacidades → estado → execução/uso → arquitetura → validação → segurança/limitações → contexto/licença;
- **responsabilidade única por seção:** cada bloco deve ter uma função predominante;
- **local canônico:** instruções como instalação, execução e validação devem ter um ponto principal, com links quando houver aprofundamento;
- **não redundância:** repetir somente quando houver relação clara de resumo → detalhe; evitar blocos paralelos com a mesma função;
- **reprodutibilidade:** quando a execução for material, manter Quickstart desde clone limpo e documentação suficiente para um terceiro reproduzir o piloto sem conhecimento tácito do autor;
- **verdade factual:** distinguir funcionalidade implementada, evidência observada, hipótese, roadmap e ação institucional/humana ainda não realizada.

Quando o detalhamento operacional tornar o README excessivo, manter um Quickstart curto no README e mover o roteiro completo para `docs/`, apontando para o arquivo canônico.

## Integridade

- Não copiar a solução do instrutor como produção autoral.
- Referências externas devem ser identificadas como referência.
- Dados fictícios devem ser reconhecíveis como sintéticos.
- Não promover etapa por inferência; exigir evidência e revisão.
- Não transformar hipótese de valor ou adoção em resultado comprovado.
- Não publicar segredos, credenciais ou dados reais desnecessários.