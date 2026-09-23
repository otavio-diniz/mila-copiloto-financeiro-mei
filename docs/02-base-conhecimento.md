# Etapa 2 — Base de Conhecimento

> **Estado:** em desenvolvimento autoral.

## Cenário aprovado

**MEI eletricista autônomo.**

## Dados utilizados

Conjunto inicial **aprovado por Otávio**:

| Arquivo | Formato | Finalidade |
|---|---|---|
| `perfil_mei.json` | JSON | Contexto do negócio |
| `transacoes.csv` | CSV | Entradas, saídas e classificação PF/PJ/PENDENTE |
| `compromissos.csv` | CSV | Receitas previstas, despesas e vencimentos |
| `propostas_credito.csv` | CSV | Cenários fictícios de crédito |

`historico_interacoes.csv` ficou fora do escopo inicial.

## Adaptações

A base será específica para MEI e utilizará somente dados fictícios.

## Estratégia de integração

[PENDENTE DE DECISÃO/IMPLEMENTAÇÃO]

## Exemplo de contexto

[PENDENTE — depende da aprovação do perfil fictício, transações e propostas.]

## Perfil fictício aprovado

**Carlos**, eletricista autônomo e MEI.

| Parâmetro | Valor aprovado |
|---|---|
| Faturamento médio mensal | R$ 8.500,00 |
| Saldo empresarial inicial | R$ 4.800,00 |
| Retirada pessoal habitual | R$ 2.500,00/mês |
| Recebimentos | Irregulares, com maior concentração na segunda metade do mês |
| Despesas empresariais típicas | Materiais elétricos, combustível/deslocamento, telefone e ferramentas |
| Dor central | Mistura gastos pessoais e empresariais e perde visibilidade do caixa real |
| Aquisição simulada | Conjunto profissional de ferramentas/equipamentos de R$ 6.000,00 |

## Decisões ainda necessárias

- definir movimentações e compromissos;
- definir duas ou três propostas fictícias de crédito;
- validar as regras PF/PJ/PENDENTE.

## Estado do Gate 2

- cenário do MEI: **aprovado**;
- arquivos-base: **aprovados**;
- perfil e valores fictícios: **aprovados**.
