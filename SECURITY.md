# Política de Segurança — MILA

## Escopo

A MILA é um protótipo acadêmico de apoio financeiro para MEI. O repositório não deve conter dados bancários reais, credenciais, tokens, CPFs/CNPJs reais, senhas ou informações pessoais sensíveis.

## Regras obrigatórias

- Use somente dados fictícios/mockados no protótipo.
- Nunca versione arquivos `.env`, tokens de API ou credenciais.
- Cálculos financeiros devem ser executados por lógica determinística; o LLM apenas contextualiza e explica resultados.
- Dados insuficientes ou ambíguos devem ser sinalizados, não inventados.
- Cenários de crédito são simulações e não constituem contratação ou recomendação de instituição.
- O agente não movimenta dinheiro e não acessa contas bancárias reais.

## Incidente

Se um segredo ou dado real for adicionado por engano, interrompa o uso daquele dado, remova-o do repositório e rotacione imediatamente qualquer credencial exposta antes de continuar o desenvolvimento.
