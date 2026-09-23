# MILA — MEI Inteligente para Liquidez e Autonomia

> **Seu Copiloto Financeiro para MEI**

Projeto em desenvolvimento no **Bootcamp Bradesco — GenAI, Dados & Cyber**, Módulo 07, Desafio 7.2.

## Estado do projeto

- **Gate 1 — Documentação do agente:** concluído por aprovação autoral; completude documental reconciliada.
- **Gate 2 — Base de conhecimento:** concluído com evidência, aprovação autoral e merge em `main`.
- **Gate 3 — Prompts do agente:** em desenvolvimento autoral; blocos substantivos aprovados e em consolidação para testes.
- **Gate 4 — Aplicação funcional:** ainda não iniciada; stack técnica não fixada.
- **Submissão:** não realizada.

## Onde cada parte é construída

```text
data/      base fictícia usada pelo protótipo
docs/      documentação acadêmica e decisões por etapa
src/       aplicação executável — será construída no Gate 4
tests/     testes de comportamento, segurança e métricas
assets/    diagramas, imagens e evidências visuais
.github/   fluxo de colaboração/revisão
```

Hoje a MILA existe como **especificação autoral + base sintética versionada**. O agente executável ainda não foi implementado.

## Problema

O projeto investiga como apoiar um MEI que mistura finanças pessoais e empresariais, perde visibilidade do caixa real do negócio e precisa avaliar o impacto de retiradas, compras e crédito.

## Direção funcional

A MILA deverá:

1. separar movimentações PF, PJ e pendentes de confirmação;
2. reconstruir uma visão simples do caixa empresarial;
3. projetar compromissos e recebimentos;
4. simular impactos de decisões;
5. comparar cenários de crédito considerando custo, prazo, parcela, vencimento e compatibilidade com o fluxo de caixa;
6. explicar resultados em linguagem simples.

## Arquitetura conceitual

```text
Usuário
  ↓
Interface
  ↓
Camada determinística de regras/cálculos ←→ data/
  ↓
Contexto calculado + System Prompt
  ↓
LLM
  ↓
Guardrails
  ↓
Resposta simples ao usuário
```

A tecnologia da interface e o modelo de linguagem serão definidos no **Gate 4**.

## Princípios de segurança

- dados do protótipo são fictícios/mockados;
- cálculos determinísticos não são inventados pelo LLM;
- informação ausente gera pedido de esclarecimento;
- ambiguidades permanecem `PENDENTE` até confirmação;
- o agente não movimenta dinheiro nem contrata crédito;
- não há promessa de melhor oferta do mercado;
- o protótipo não substitui orientação contábil, jurídica ou financeira profissional/regulada;
- senha, token e credenciais bancárias não são solicitados.

## Integridade acadêmica

Este repositório é um **workspace de desenvolvimento autoral**. Decisões substantivas, implementação e submissão pertencem a Otávio. Materiais de referência ou exemplos de terceiros não devem ser apresentados como produção autoral.

## Referências de origem

- Repositório oficial do desafio: `digitalinnovationone/dio-lab-bia-do-futuro`
- Exemplo do instrutor: referência didática/comparativa, sem cópia como solução do projeto.

---
**MILA** — MEI Inteligente para Liquidez e Autonomia.
