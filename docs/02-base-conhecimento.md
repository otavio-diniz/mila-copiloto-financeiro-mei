# Etapa 2 — Base de Conhecimento

> **Estado:** Gate 2 concluído com evidência e aprovação autoral.  
> **Natureza:** material de trabalho acadêmico; não representa submissão final.  
> **Backfill documental:** 23/09/2026 — Estratégia de Integração e Exemplo de Contexto foram consolidados tardiamente a partir de decisões já aprovadas e registrados sem reescrever a cronologia.

## Dados Utilizados

| Arquivo | Formato | Utilização no Agente |
|---|---|---|
| `perfil_mei.json` | JSON | Contextualizar o MEI, saldo, retirada, reserva e aquisição simulada |
| `transacoes.csv` | CSV | Registrar entradas, saídas e classificação PF/PJ/PENDENTE |
| `compromissos.csv` | CSV | Projetar recebimentos, despesas e vencimentos |
| `propostas_credito.csv` | CSV | Comparar cenários fictícios de crédito |

`historico_interacoes.csv` ficou fora do escopo inicial.

## Adaptações nos Dados

A base foi adaptada para um cenário de microempreendedor individual. Todos os dados são **MATERIAL DIDÁTICO FICTÍCIO/SINTÉTICO**. Não são usados CPF/CNPJ reais, credenciais bancárias ou dados financeiros reais.

### Perfil fictício aprovado

- Nome: **Carlos**
- Atividade: **eletricista autônomo / MEI**
- Faturamento médio mensal: **R$ 8.500**
- Saldo empresarial inicial: **R$ 4.800**
- Retirada pessoal habitual: **R$ 2.500/mês**
- Reserva operacional mínima: **R$ 3.500**
- Recebimentos: irregulares, concentrados principalmente na segunda metade do mês
- Aquisição simulada: conjunto profissional de ferramentas/equipamentos de **R$ 6.000**

### Classificação

- `PJ`: movimentação claramente ligada ao negócio;
- `PF`: movimentação claramente pessoal;
- `PENDENTE`: contexto insuficiente ou ambíguo; a MILA pede confirmação.

A classificação não deve ser forçada quando a descrição não for suficiente.

## Estratégia de Integração

### Como os dados são carregados?

A aplicação deverá carregar os quatro arquivos JSON/CSV da pasta `data/`. A tecnologia de implementação será decidida no Gate 4.

A camada de regras e cálculos usa esses arquivos para montar saldo, projeções, compromissos, parcelas e demais resultados numéricos. Esses cálculos são **determinísticos** e ficam fora do LLM.

### Como os dados são usados no prompt?

O **System Prompt** contém identidade, escopo, linguagem e guardrails. Os dados do MEI não ficam fixados nele.

A cada análise, a aplicação monta um **contexto dinâmico** apenas com os dados e resultados necessários para aquela pergunta. O LLM recebe esse contexto para explicar os resultados em linguagem simples, mas não pode alterar valores calculados nem inventar dados ausentes.

Quando faltar informação indispensável, a resposta deve pedir uma informação objetiva por vez.

## Exemplo de Contexto Montado

```text
MATERIAL DIDÁTICO FICTÍCIO/SINTÉTICO

MEI:
- Nome: Carlos
- Atividade: eletricista autônomo / MEI
- Saldo empresarial inicial: R$ 4.800
- Reserva operacional mínima: R$ 3.500
- Retirada pessoal habitual: R$ 2.500/mês

Aquisição em simulação:
- Ferramentas/equipamentos: R$ 6.000

Compromissos e recebimentos relevantes:
- 05/11: DAS MEI - R$ 80
- 08/11: materiais - R$ 650
- 12/11: Cliente F + R$ 1.300
- 22/11: Cliente G + R$ 2.100
- 28/11: retirada pessoal - R$ 2.500

Propostas de crédito:
- A: 6 x R$ 1.070 | total R$ 6.420 | vencimento dia 05
- B: 6 x R$ 1.110 | total R$ 6.660 | vencimento dia 25
- C: 12 x R$ 620 | total R$ 7.440 | vencimento dia 20

Itens ambíguos:
- despesas classificadas como PENDENTE devem ser confirmadas antes de uma classificação PF/PJ definitiva.

Objetivo da resposta:
- explicar o efeito de cada cenário sobre o caixa e a reserva;
- mostrar os trade-offs em linguagem simples;
- não escolher a proposta pelo usuário.
```

## Transações Aprovadas

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
| 29/10 | Compra Mercado Central | -R$ 275 | PENDENTE |

Receitas do período: **R$ 8.500**.

## Compromissos Aprovados

| Data prevista | Compromisso | Valor | Classe |
|---|---|---:|---|
| 05/11 | DAS MEI | -R$ 80 | PJ |
| 08/11 | Compra prevista de materiais | -R$ 650 | PJ |
| 12/11 | Cliente F — serviço agendado | +R$ 1.300 | PJ |
| 15/11 | Telefone/internet | -R$ 120 | PENDENTE |
| 22/11 | Cliente G — serviço comercial | +R$ 2.100 | PJ |
| 28/11 | Retirada pessoal planejada | -R$ 2.500 | PF |

## Propostas de Crédito Aprovadas

| Proposta | Valor | Parcelamento | Total pago | Custo adicional | 1º vencimento | Característica |
|---|---:|---:|---:|---:|---|---|
| A | R$ 6.000 | 6 × R$ 1.070 | R$ 6.420 | R$ 420 | dia 05 | Menor custo total; maior pressão no início do mês |
| B | R$ 6.000 | 6 × R$ 1.110 | R$ 6.660 | R$ 660 | dia 25 | Melhor alinhamento com os principais recebimentos |
| C | R$ 6.000 | 12 × R$ 620 | R$ 7.440 | R$ 1.440 | dia 20 | Menor parcela; maior custo total e prazo |

## Validação da Base Sintética

- receitas de outubro: **R$ 8.500**;
- compromissos previstos de novembro antes do crédito: efeito líquido de **+R$ 50**;
- A: 6 × R$ 1.070 = **R$ 6.420**;
- B: 6 × R$ 1.110 = **R$ 6.660**;
- C: 12 × R$ 620 = **R$ 7.440**.

Os quatro arquivos foram materializados, lidos de volta e promovidos para `main` após aprovação explícita de Otávio.

## Estado do Gate 2

- aprovação autoral: **confirmada**;
- PR de integração: **#2**;
- merge commit: `fba1bc97d66982927e272c5435b6dc1ec4c8f716`;
- submissão final: **não realizada**;
- backfill documental de completude: **registrado em 23/09/2026**.

`GATE_2=CONCLUIDO_COM_EVIDENCIA_E_BACKFILL_DOCUMENTAL`
