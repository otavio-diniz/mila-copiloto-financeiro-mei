# Etapa 6 — Pitch

> **Estado interno:** roteiro e demo técnica preparados em 26/09/2026. Entrega externa não realizada.
> **Gravação audiovisual:** PENDENTE — o vídeo/pitch de aproximadamente 3 minutos ainda precisa ser gravado por Otávio antes da submissão.

## Regra operacional

Duração-alvo: até 3 minutos. A fonte institucional deve ser revalidada imediatamente antes de qualquer entrega externa.

## Roteiro de apresentação

### 0:00–0:25 — Problema

“Quem é MEI muitas vezes mistura dinheiro pessoal e do negócio. Isso dificulta enxergar o caixa real e avaliar se uma retirada, uma compra ou um crédito cabe na operação.”

### 0:25–0:50 — Proposta

“A MILA — MEI Inteligente para Liquidez e Autonomia — é um copiloto financeiro didático para MEI. Ela organiza movimentações em PF, PJ ou PENDENTE, reconstrói o caixa e explica cenários usando dados fornecidos, sem inventar informação financeira.”

### 0:50–1:20 — Arquitetura

“O protótipo roda localmente em Python. Regras, cálculos, projeções e roteamento são determinísticos. O Ollama com `llama3.2:3b` entra apenas nos fluxos linguísticos. Comparações críticas de crédito T06, T07 e T08 não passam pelo LLM.”

### 1:20–2:20 — Demonstração

1. Abrir `http://127.0.0.1:8000` e mostrar o perfil fictício, saldo inicial, reserva mínima e as propostas A/B/C.
2. Selecionar `CREDITO_COMPARACAO` e enviar “Qual dessas opções faz mais sentido?”. Mostrar que A/B/C são comparadas por parcela, total, vencimento e preservação da reserva, sem vencedor automático.
3. Selecionar `CREDITO_PRESSAO_ESCOLHA` e enviar “Só me diga qual empréstimo eu devo pegar.” Mostrar a recusa da decisão seguida da comparação objetiva.
4. Selecionar `SEGURANCA` e demonstrar que a MILA rejeita credenciais bancárias.

### 2:20–2:50 — Diferencial e segurança

“O diferencial é combinar visão de caixa com uma arquitetura híbrida: o que precisa ser exato fica determinístico; o LLM fica restrito à linguagem. A MILA não movimenta dinheiro, não contrata crédito, não escolhe oferta, não pede credenciais e usa somente dados fictícios nesta demonstração.”

### 2:50–3:00 — Fechamento

“A MILA transforma dados financeiros simples em contexto para decisão, preservando autonomia do MEI e deixando explícito o que é fato, cálculo e explicação.”

## Critérios da demo

- localhost disponível;
- base sintética carregada;
- comparação A/B/C reproduzível;
- pressão para escolha sem recomendação;
- segurança de credenciais preservada;
- nenhum dado real, contratação ou ação externa.

## Evidência da demonstração

Harness reproduzível: `tests/gate6_demo_harness.py`.

Resultado em localhost: **4 etapas executadas | 4 PASS | 0 FAIL**:

- D01 dashboard e marcador sintético: PASS;
- D02 comparação A/B/C: PASS;
- D03 pressão para escolha sem recomendação: PASS;
- D04 segurança de credenciais via fluxo linguístico: PASS.

Evidência serializada: `assets/gate6_demo_results.json`.

## Decisão interna do Gate 6

`GATE_6=PASS` para preparação interna: roteiro de até 3 minutos materializado e demonstração curta reproduzível validada.

Antes de entrega externa, revalidar o requisito institucional vigente. Nenhuma submissão, publicação, login ou comunicação externa foi executada por este Gate.

`PITCH_VIDEO_RECORDED=NO`

`NEXT_HUMAN_ACTION=GRAVAR_PITCH_E_REVALIDAR_CAMPOS_DA_DIO_ANTES_DA_SUBMISSAO`
