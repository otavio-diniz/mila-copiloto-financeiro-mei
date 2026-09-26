# Etapa 4 — Aplicação Funcional

> **Estado interno:** PASS técnico/acadêmico em 26/09/2026. Submissão externa não realizada.

## Stack técnica vigente

- Python 3.12 + biblioteca padrão;
- interface web local server-rendered em HTML/CSS;
- servidor `wsgiref.simple_server` em `127.0.0.1:8000`;
- `urllib.request` como única fronteira HTTP com o Ollama;
- Ollama local + `llama3.2:3b` nos fluxos linguísticos autorizados;
- `Decimal` para valores monetários.

## Componentes materializados

- `src/core.py`: loaders, validação, caixa, projeção e reserva;
- `src/renderers.py`: T06/T07/T08 determinísticos;
- `src/router.py`: seleção de rota/modo antes do LLM;
- `src/prompts.py`: BASE_PROMPT + um único MODE_PROMPT ativo;
- `src/llm_client.py`: integração local e guardrails;
- `src/web.py`: view-model e HTML escapado;
- `src/app.py`: composition root e servidor localhost.

## Contratos preservados

- cálculos, status e roteamento não são delegados ao LLM;
- T06/T07/T08 usam exclusivamente renderers determinísticos e zero HTTP/LLM;
- modo desconhecido gera erro controlado, sem fallback silencioso;
- crédito não é escolhido/recomendado pela MILA;
- dados financeiros ausentes não são inferidos;
- `data/` permanece sem mutação pela aplicação;
- entradas e respostas exibidas em HTML são escapadas.

## Evidência de funcionamento

- `py_compile` dos módulos e testes: PASS;
- regressão unitária final: 60 testes, 60 PASS, 0 FAIL;
- GET localhost: HTTP 200 e marcador `MATERIAL DIDÁTICO FICTÍCIO/SINTÉTICO` presente;
- POST determinístico T08: HTTP 200 e saída contratual presente;
- POST linguístico `SEGURANCA`: HTTP 200 e contrato completo de duas frases;
- integração local Ollama: `llama3.2:3b` comprovado e utilizado;
- implementação, testes, documentação e evidências versionados no GitHub; a publicação terminal preserva a cadeia por commits e PR controlado.

O status histórico anterior de “não iniciada” fica superado por esta evidência de 26/09/2026.
