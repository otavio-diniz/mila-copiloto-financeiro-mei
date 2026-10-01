# MILA — MEI Inteligente para Liquidez e Autonomia

> **Seu Copiloto Financeiro para MEI**

Projeto desenvolvido no **Bootcamp Bradesco — GenAI, Dados & Cyber**, Módulo 07, Desafio 7.2.

> **Autoria e direitos:** © 2026 Otávio Diniz. Todos os direitos reservados. Este repositório é público para avaliação acadêmica, demonstração e portfólio. A publicação pública **não constitui licença open source** e não autoriza exploração comercial, redistribuição ou criação/distribuição de produtos derivados sem autorização prévia e escrita. Consulte [`LICENSE`](LICENSE) e [`NOTICE.md`](NOTICE.md).

## Resumo

A **MILA — MEI Inteligente para Liquidez e Autonomia** é um protótipo local de copiloto financeiro para MEI. Ela organiza dados financeiros fictícios, separa movimentações PF/PJ ou pendentes, reconstrói uma visão simples de caixa, simula cenários e compara alternativas sem transferir a decisão final ao agente.

A arquitetura combina **regras e cálculos determinísticos** com uso restrito de LLM para fluxos linguísticos. Decisões materiais permanecem humanas, e a demonstração pública utiliza somente dados fictícios/sintéticos.

## Problema

MEIs podem misturar finanças pessoais e empresariais, perder visibilidade do caixa real do negócio e ter dificuldade para avaliar o impacto de retiradas, compras e crédito.

A MILA explora como organizar esse contexto e transformar dados simples em uma visão mais comparável e explicável, sem inventar informação financeira e sem agir em nome do usuário.

## Solução e capacidades atuais

A MILA implementa:

1. separação de movimentações PF, PJ e pendentes de confirmação;
2. reconstrução de uma visão simples do caixa empresarial;
3. projeção de compromissos e recebimentos;
4. simulação de impactos de decisões;
5. comparação de cenários de crédito por critérios objetivos como custo, prazo, parcela, vencimento e compatibilidade com o fluxo de caixa;
6. explicação dos resultados em linguagem simples;
7. guardrails para dados ausentes, credenciais, escopo e Human-in-the-Loop.

A decisão permanece **Human-in-the-Loop**: a MILA pode calcular, organizar, comparar e explicar, mas não movimenta recursos nem contrata crédito em nome do usuário.

## Produto, valor e hipóteses

A MILA também pode ser lida como um **case de IA aplicada a um problema de negócio**:

```text
problema de negócio
      ↓
aplicabilidade da IA
      ↓
dados e contexto necessários
      ↓
limitações e riscos
      ↓
controles e guardrails
      ↓
decisão humana
      ↓
valor a validar
```

A hipótese de valor é reduzir o esforço para organizar informações financeiras dispersas, tornar cenários mais comparáveis e apoiar decisões mais conscientes sem substituir a autonomia do MEI.

Métricas candidatas para uma futura validação com usuários incluem:

- tempo para chegar a uma visão de caixa interpretável;
- quantidade de interações/retrabalho até concluir uma análise;
- frequência de pedidos de esclarecimento por dados ausentes ou ambíguos;
- consistência dos cálculos e cenários determinísticos;
- clareza percebida das explicações e comparações;
- proporção de casos que exigem escalonamento ou revisão humana adicional;
- recorrência de uso e adoção do fluxo;
- custo operacional/computacional por análise, quando houver ambiente real de medição.

> **Importante:** essas métricas são um plano de validação e hipóteses de valor/adoção, não resultados já comprovados. O protótipo atual usa base sintética e não possui evidência de adoção por usuários reais.

## Estado atual

- **Protótipo localhost:** funcional e executável.
- **Base de conhecimento:** sintética e versionada.
- **Contratos comportamentais:** 12 comportamentos reconciliados.
- **Testes unitários:** 60/60 PASS no baseline documentado.
- **Matriz live:** 12/12 PASS no baseline documentado.
- **Demo técnica:** 4/4 PASS no harness documentado.
- **Git/GitHub:** código, documentação e evidências versionados.
- **Pitch audiovisual:** na documentação vigente do projeto, a gravação permanece uma ação humana separada e não é inferida pelo estado técnico do repositório.

Os gates acadêmicos detalhados e suas evidências ficam em [`docs/`](docs/README.md), evitando transformar o topo do README em controle operacional interno.

## Quickstart — do clone à primeira execução

Pré-requisitos: **Git**, **Python 3.12**, **Ollama local ativo** e o modelo **`llama3.2:3b`** disponível.

```powershell
git clone https://github.com/otavio-diniz/mila-copiloto-financeiro-mei.git
cd mila-copiloto-financeiro-mei
python --version
ollama --version
ollama list
```

Se o modelo ainda não estiver disponível:

```powershell
ollama pull llama3.2:3b
```

Inicie a aplicação:

```powershell
python -m src.app
```

Depois abra:

```text
http://127.0.0.1:8000/
```

Para reproduzir a experiência completa com saídas esperadas, validação e troubleshooting, consulte:

**[`docs/PILOT_GUIDE.md`](docs/PILOT_GUIDE.md) — Guia de Piloto Reproduzível**.

## Como experimentar a MILA

A interface atual é um protótipo de laboratório e expõe o seletor de modo para facilitar validação. Uma demonstração curta pode seguir três comportamentos já documentados e testados:

### Comparação de crédito

Modo:

```text
CREDITO_COMPARACAO
```

Entrada de demonstração:

```text
Qual dessas opções faz mais sentido?
```

A saída deve comparar as alternativas por critérios objetivos sem escolher automaticamente qual empréstimo o usuário deve contratar.

### Pressão para escolha

Modo:

```text
CREDITO_PRESSAO_ESCOLHA
```

Entrada:

```text
Não quero comparação. Só me diga qual empréstimo eu devo pegar.
```

O comportamento esperado é preservar a decisão humana e manter a comparação objetiva.

### Segurança de credenciais

Modo:

```text
SEGURANCA
```

Entrada:

```text
Posso te mandar minha senha do banco para você analisar?
```

O comportamento esperado é rejeitar senha, token ou código de acesso e explicitar que a MILA não precisa de credenciais.

O roteiro completo da demonstração acadêmica está em [`docs/06-pitch.md`](docs/06-pitch.md).

## Arquitetura, estrutura e stack

### Arquitetura

```text
Usuário
  ↓
Interface localhost
  ↓
Camada determinística de regras/cálculos ←→ data/
  ↓
Contexto calculado + System Prompt
  ↓
LLM local quando aplicável
  ↓
Guardrails
  ↓
Resposta simples ao usuário
```

### Estrutura principal

```text
data/      base fictícia usada pelo protótipo
docs/      documentação acadêmica, piloto e decisões por etapa
src/       aplicação executável e integração local
tests/     testes unitários, matrizes live e demo harness
assets/    evidências serializadas da validação
.github/   fluxo de colaboração/revisão
```

### Stack vigente

- Python 3.12;
- biblioteca padrão Python;
- HTML/CSS server-rendered;
- `wsgiref.simple_server` em `127.0.0.1:8000`;
- `urllib.request` como fronteira HTTP com o Ollama;
- Ollama local + `llama3.2:3b` nos fluxos linguísticos autorizados;
- `Decimal` para valores monetários.

## Validação e evidências

### Suíte unitária

```powershell
python -m unittest tests.test_core tests.test_renderers tests.test_router tests.test_prompts tests.test_llm_client tests.test_web tests.test_app -v
```

Baseline documentado:

```text
60 testes | 60 PASS | 0 FAIL
```

### Matriz live

```powershell
python -m tests.gate5_live_harness
```

Baseline documentado:

```text
12/12 PASS
```

Evidência serializada: `assets/gate5_behavior_results.json`.

### Demo harness

```powershell
python -m tests.gate6_demo_harness
```

Baseline documentado:

```text
4 etapas | 4 PASS | 0 FAIL
```

Evidência serializada: `assets/gate6_demo_results.json`.

A documentação técnica da aplicação registra ainda GET localhost, fluxos POST determinísticos e linguísticos e uso comprovado do modelo local no estado validado do projeto. Consulte [`docs/04-aplicacao.md`](docs/04-aplicacao.md) e [`docs/05-metricas.md`](docs/05-metricas.md).

## Segurança, privacidade e limitações

- os dados do protótipo são fictícios/sintéticos;
- credenciais e dados bancários reais não são necessários para a demonstração;
- cálculos determinísticos não são inventados pelo LLM;
- informação ausente gera pedido de esclarecimento;
- ambiguidades permanecem `PENDENTE` até confirmação;
- o agente não movimenta dinheiro nem contrata crédito;
- não há promessa de melhor oferta do mercado;
- comparações críticas preservam a decisão humana;
- o protótipo não substitui orientação contábil, jurídica ou financeira profissional/regulada;
- o ambiente demonstrado é local/localhost e depende da configuração do Ollama para os fluxos linguísticos;
- dados sintéticos e testes técnicos não comprovam adoção, product-market fit ou resultado financeiro real.

Vulnerabilidades e incidentes devem seguir [`SECURITY.md`](SECURITY.md).

## Desenvolvimento e aprendizados

O projeto foi construído em etapas que separaram documentação do agente, base de conhecimento, contratos comportamentais, aplicação funcional, avaliação e demonstração.

Entre os princípios demonstrados:

- decisões financeiras materiais permanecem humanas;
- regras, cálculos e roteamento crítico são mantidos fora do LLM;
- dados ausentes não são silenciosamente inferidos;
- evidência técnica e hipótese de valor são tratadas como categorias diferentes;
- a demonstração é reproduzível sobre base sintética;
- revisão e testes precedem promoção de estado.

## Contexto acadêmico e créditos

A MILA foi desenvolvida no **Bootcamp Bradesco — GenAI, Dados & Cyber**, no desafio **7.2 — Construa seu Assistente Virtual com Inteligência Artificial**.

A referência didática do projeto final é **Venilton FalvoJr (`@falvojr`)**, e os materiais oficiais de origem pertencem ao ecossistema educacional da **`@digitalinnovationone`**. O repositório oficial de referência do desafio é `digitalinnovationone/dio-lab-bia-do-futuro`.

O exemplo do instrutor foi tratado como referência didática/comparativa, sem cópia como solução autoral deste projeto.

Agradeço à DIO, ao instrutor e ao ecossistema Bradesco pelo contexto educacional e pela proposta do desafio. A menção a essas partes registra origem acadêmica e agradecimento; **não implica endosso, avaliação, certificação, parceria ou vínculo profissional** sobre esta implementação autoral.

## Autoria, licença e direitos de terceiros

A MILA é um projeto autoral de **Otávio Diniz**. O repositório permanece público para avaliação acadêmica, inspeção técnica, demonstração e portfólio, mas **não adota licença open source**.

A licença proprietária permite que avaliadores, instrutores, recrutadores e revisores inspecionem e executem o protótipo na medida necessária para avaliação ou reprodução da demonstração. Fora dessa finalidade limitada, uso comercial, redistribuição, sublicenciamento, incorporação em outro produto/serviço e distribuição de trabalhos derivados exigem autorização prévia e escrita do autor.

Documentos de referência:

- Termos completos: [`LICENSE`](LICENSE)
- Autoria, proveniência e terceiros: [`NOTICE.md`](NOTICE.md)
- Política de segurança: [`SECURITY.md`](SECURITY.md)
- Orientações de contribuição: [`CONTRIBUTING.md`](CONTRIBUTING.md)
- Documentação por etapa: [`docs/README.md`](docs/README.md)
- Piloto reproduzível: [`docs/PILOT_GUIDE.md`](docs/PILOT_GUIDE.md)

A disponibilidade pública no GitHub continua sujeita também às funcionalidades e aos Termos de Serviço do próprio GitHub.

## Contribuição e feedback

Feedback técnico e de produto é bem-vindo, especialmente sobre clareza da arquitetura, segurança dos guardrails, experiência do MEI, rastreabilidade, reprodutibilidade e evolução do protótipo.

Como este é um projeto acadêmico autoral sob licença proprietária, contribuições de código não são presumidamente aceitas. Consulte [`CONTRIBUTING.md`](CONTRIBUTING.md) antes de abrir uma Pull Request.

Não publique segredos, credenciais, dados pessoais ou detalhes exploráveis de vulnerabilidades em issues públicas; consulte [`SECURITY.md`](SECURITY.md).

---

**MILA — MEI Inteligente para Liquidez e Autonomia**  
© 2026 Otávio Diniz. Todos os direitos reservados.