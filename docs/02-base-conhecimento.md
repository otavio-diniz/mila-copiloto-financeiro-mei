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

## Transações aprovadas

| Data | Descrição | Valor | Classe esperada |
|---|---|---:|---|
| 02/10 | Serviço elétrico — Cliente A | +R$ 1.400 | PJ |
| 03/10 | Loja de materiais elétricos | -R$ 460 | PJ |
| 05/10 | Supermercado | -R$ 320 | PF |
| 07/10 | Serviço elétrico — Cliente B | +R$ 1.100 | PJ |
| 08/10 | Posto Avenida | -R$ 180 | PENDENTE |
| 10/10 | Conta de telefone | -R$ 120 | PENDENTE |
| 14/10 | Serviço comercial — Cliente C | +R$ 2.000 | PJ |
| 16/10 | Transferência para Carlos | -R$ 1.250 | PF |
| 20/10 | Serviço residencial — Cliente D | +R$ 1.650 | PJ |
| 22/10 | Ferramentas elétricas | -R$ 540 | PJ |
| 25/10 | Farmácia | -R$ 165 | PF |
| 27/10 | Serviço comercial — Cliente E | +R$ 2.350 | PJ |
| 28/10 | Transferência para Carlos | -R$ 1.250 | PF |
| 29/10 | Compra “Mercado Central” | -R$ 275 | PENDENTE |

Receitas do período: **R$ 8.500,00**.

## Compromissos aprovados

| Data prevista | Compromisso | Valor | Classe |
|---|---|---:|---|
| 05/11 | DAS MEI | -R$ 80 | PJ |
| 08/11 | Compra prevista de materiais | -R$ 650 | PJ |
| 12/11 | Cliente F — serviço agendado | +R$ 1.300 | PJ |
| 15/11 | Telefone/internet | -R$ 120 | PENDENTE |
| 22/11 | Cliente G — serviço comercial | +R$ 2.100 | PJ |
| 28/11 | Retirada pessoal planejada | -R$ 2.500 | PF |

## Regra de classificação aprovada

Quando a descrição ou o contexto forem insuficientes, a MILA não deve inferir PF/PJ com falsa certeza. A classificação deve permanecer `PENDENTE` e o agente deve pedir confirmação.

## Propostas de crédito aprovadas

| Proposta | Valor | Parcelamento | Total pago | Custo adicional | 1º vencimento | Característica |
|---|---:|---:|---:|---:|---|---|
| A | R$ 6.000 | 6 × R$ 1.070 | R$ 6.420 | R$ 420 | dia 05 | Menor custo total; maior pressão no início do mês |
| B | R$ 6.000 | 6 × R$ 1.110 | R$ 6.660 | R$ 660 | dia 25 | Melhor alinhamento com os principais recebimentos |
| C | R$ 6.000 | 12 × R$ 620 | R$ 7.440 | R$ 1.440 | dia 20 | Menor parcela; maior custo total e prazo |

Reserva operacional mínima aprovada: **R$ 3.500,00**.

## Validação da base sintética

- receitas de outubro: **R$ 8.500,00**;
- compromissos previstos de novembro, antes do crédito: efeito líquido de **+R$ 50,00**;
- proposta A: 6 × R$ 1.070 = **R$ 6.420**;
- proposta B: 6 × R$ 1.110 = **R$ 6.660**;
- proposta C: 12 × R$ 620 = **R$ 7.440**;
- custo adicional = total pago − R$ 6.000 em todas as propostas.

## Estado de integração

Os quatro arquivos sintéticos foram materializados em `develop` e conferidos por readback. Este documento permanece como **material de trabalho autoral**, não como declaração de submissão final.

## Estado do Gate 2

- cenário do MEI: **aprovado**;
- arquivos-base: **aprovados**;
- perfil e valores fictícios: **aprovados**;
- transações e compromissos: **aprovados**;
- regra PF/PJ/PENDENTE: **aprovada**;
- propostas de crédito e reserva operacional: **aprovadas**;
- arquivos sintéticos em `develop`: **materializados e conferidos**;
- promoção para `main`: **pendente de revisão autoral**.
