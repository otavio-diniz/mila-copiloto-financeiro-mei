# MILA — MEI Inteligente para Liquidez e Autonomia

> **Seu Copiloto Financeiro para MEI**

Projeto desenvolvido no **Bootcamp Bradesco — GenAI, Dados & Cyber**, Módulo 07, Desafio 7.2.

## Estado do projeto

- **Gate 1 — Documentação do agente:** PASS.
- **Gate 2 — Base de conhecimento:** PASS.
- **Gate 3 — Prompts/contratos comportamentais:** PASS, 12 comportamentos reconciliados.
- **Gate 4 — Aplicação funcional:** PASS interno; protótipo localhost executável conectado à base sintética.
- **Gate 5 — Avaliação e métricas:** PASS interno; 60 testes unitários + matriz live 12/12.
- **Gate 6 — Pitch/demo:** PASS interno; roteiro de até 3 minutos + demo reproduzível 4/4.
- **Git/GitHub:** código, documentação e evidências versionados; publicação terminal rastreada por commits e PR.
- **Submissão DIO:** pendente exclusivamente de Otávio.

## Onde cada parte é construída

```text
data/      base fictícia usada pelo protótipo
docs/      documentação acadêmica e decisões por etapa
src/       aplicação executável e integração local
tests/     testes unitários, matrizes live e demo harness
assets/    evidências serializadas da validação
.github/   fluxo de colaboração/revisão
```

Hoje a MILA existe como **protótipo funcional local + base sintética + testes e evidências reproduzíveis**.

## Problema

O projeto investiga como apoiar um MEI que mistura finanças pessoais e empresariais, perde visibilidade do caixa real do negócio e precisa avaliar o impacto de retiradas, compras e crédito.

## Direção funcional

A MILA implementa:

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

Implementação vigente: **Python 3.12 + biblioteca padrão + HTML/CSS server-rendered + `urllib.request` + Ollama local `llama3.2:3b`**, com execução em browser localhost.

## Princípios de segurança

- dados do protótipo são fictícios/mockados;
- cálculos determinísticos não são inventados pelo LLM;
- informação ausente gera pedido de esclarecimento;
- ambiguidades permanecem `PENDENTE` até confirmação;
- o agente não movimenta dinheiro nem contrata crédito;
- não há promessa de melhor oferta do mercado;
- o protótipo não substitui orientação contábil, jurídica ou financeira profissional/regulada;
- senha, token e credenciais bancárias não são solicitados.

## Integridade e autoridade vigente

Em 26/09/2026, Otávio reclassificou esta execução como **projeto prático formativo sem nota** e autorizou assistência técnica direta para conclusão interna da MILA e conclusão controlada do processo no GitHub. A submissão à DIO permanece exclusiva de Otávio. O histórico anterior permanece preservado nas fontes acadêmicas.

## Referências de origem

- Repositório oficial do desafio: `digitalinnovationone/dio-lab-bia-do-futuro`
- Exemplo do instrutor: referência didática/comparativa, sem cópia como solução do projeto.

---
**MILA** — MEI Inteligente para Liquidez e Autonomia.
