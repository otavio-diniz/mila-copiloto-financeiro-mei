# Etapa 3 — Prompts do Agente

> **Estado:** em desenvolvimento autoral.
>
> **Classificação:** material estrutural de apoio. Não é o system prompt final de submissão.

## Fonte oficial

A estrutura desta etapa segue o template oficial `docs/03-prompts.md` do repositório `digitalinnovationone/dio-lab-bia-do-futuro`, que solicita:

1. System Prompt;
2. exemplos de interação / Few-Shot Prompting;
3. Edge Cases;
4. observações e aprendizados.

## Contexto já aprovado e herdado

- Nome: **MILA — MEI Inteligente para Liquidez e Autonomia**.
- Persona atendida: MEI prestador de serviços com baixa maturidade financeira.
- Cenário do MVP: eletricista autônomo.
- Objetivo: separar PF/PJ, mostrar caixa real e explicar impactos de decisões.
- Tom: simples, direto, educativo, não julgador e com pouco jargão.
- Dados: somente a base sintética aprovada no Gate 2.
- Classes de movimentação: `PJ`, `PF`, `PENDENTE`.
- Caso ambíguo: não inferir com falsa certeza; pedir confirmação.
- Cálculos financeiros: determinísticos na aplicação; o LLM explica resultados.
- Crédito: comparar impactos e trade-offs; não ordenar contratação nem prometer melhor oferta de mercado.

## System Prompt

[PENDENTE DE REDAÇÃO AUTORAL]

### Decisões a validar antes da redação

- formato padrão das respostas;
- comportamento quando faltarem dados;
- ordem de apresentação de números, impactos e alternativas;
- forma de pedir esclarecimento em casos `PENDENTE`;
- limite de atuação para recomendações financeiras.

## Exemplos de Interação / Few-Shot

### Cenário 1 — Classificação ambígua

[PENDENTE DE AUTORIA]

### Cenário 2 — Comparação de crédito no fluxo de caixa

[PENDENTE DE AUTORIA]

## Edge Cases

### Pergunta fora do escopo

[PENDENTE DE AUTORIA]

### Tentativa de obter informação sensível

[PENDENTE DE AUTORIA]

### Decisão financeira sem contexto suficiente

[PENDENTE DE AUTORIA]

## Observações e Aprendizados

[PREENCHER APÓS TESTES E AJUSTES]

## Critério de passagem

O Gate 3 somente será promovido quando Otávio aprovar o conteúdo substantivo do prompt, os exemplos Few-Shot e os Edge Cases, e quando os testes demonstrarem que a MILA não inventa números nem ultrapassa os limites definidos.
