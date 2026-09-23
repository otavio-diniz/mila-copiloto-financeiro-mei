# MILA — MEI Inteligente para Liquidez e Autonomia

> **Seu Copiloto Financeiro para MEI**

Projeto em desenvolvimento no **Bootcamp Bradesco — GenAI, Dados & Cyber**, Módulo 07, Desafio 7.2.

## Estado do projeto

- **Gate 1 — Documentação do agente:** concluído por aprovação autoral.
- **Gate 2 — Base de conhecimento:** em desenvolvimento autoral.
- **Cenário do MVP:** MEI eletricista autônomo.
- **Aplicação funcional:** ainda não implementada.
- **Submissão:** não realizada.

## Problema

O projeto investiga como apoiar um MEI que mistura finanças pessoais e empresariais, perde visibilidade do caixa real do negócio e precisa avaliar o impacto de retiradas, compras e crédito.

## Direção funcional

A MILA deverá, progressivamente:

1. separar movimentações PF, PJ e pendentes de confirmação;
2. reconstruir uma visão simples do caixa empresarial;
3. projetar compromissos e recebimentos;
4. simular impactos de decisões;
5. comparar cenários de crédito considerando custo, prazo, parcela, vencimento e compatibilidade com o fluxo de caixa;
6. explicar resultados em linguagem simples.

## Princípios de segurança

- dados do protótipo serão fictícios/mockados;
- cálculos determinísticos não devem ser inventados pelo LLM;
- informação ausente deve gerar pedido de esclarecimento;
- o agente não movimenta dinheiro nem contrata crédito;
- não há promessa de melhor oferta do mercado;
- o protótipo não substitui aconselhamento contábil, jurídico ou financeiro regulado.

## Estrutura

```text
data/      dados fictícios e documentação da base
docs/      artefatos acadêmicos por etapa do desafio
src/       implementação do protótipo
tests/     casos de teste e métricas
assets/    diagramas, imagens e evidências visuais
.github/   templates de colaboração e controle do fluxo
```

## Integridade acadêmica

Este repositório é um **workspace de desenvolvimento autoral**. Decisões substantivas, implementação e submissão pertencem a Otávio. Materiais de referência ou exemplos de terceiros não devem ser apresentados como produção autoral.

## Referências de origem

- Repositório oficial do desafio: `digitalinnovationone/dio-lab-bia-do-futuro`
- Exemplo do instrutor: usado somente como referência didática/comparativa, sem cópia como solução do projeto.

---
**MILA** — MEI Inteligente para Liquidez e Autonomia.
