"""Fronteira única da MILA com o Ollama local."""

import json
from urllib import error, request

from src.prompts import montar_system_prompt


DEFAULT_ENDPOINT = "http://127.0.0.1:11434/api/chat"
DEFAULT_MODEL = "llama3.2:3b"
DEFAULT_TIMEOUT = 300


class LLMClientError(RuntimeError):
    """Erro controlado da integração local com o modelo."""


def chat_local(
    modo_ativo: str,
    mensagem: str,
    contexto: dict | None = None,
    *,
    endpoint: str = DEFAULT_ENDPOINT,
    model: str = DEFAULT_MODEL,
    timeout: int = DEFAULT_TIMEOUT,
    urlopen_func=request.urlopen,
) -> str:
    system_prompt = montar_system_prompt(modo_ativo, contexto)
    payload = {
        "model": model,
        "stream": False,
        "keep_alive": "5m",
        "options": {
            "temperature": 0,
            "num_ctx": 4096,
            "num_predict": 512,
        },
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": mensagem},
        ],
    }
    corpo = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    requisicao = request.Request(
        endpoint,
        data=corpo,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        resposta = urlopen_func(requisicao, timeout=timeout)
        with resposta:
            dados = json.loads(resposta.read().decode("utf-8"))
    except (error.URLError, error.HTTPError, TimeoutError, OSError) as erro:
        raise LLMClientError("O Ollama local não respondeu corretamente.") from erro
    except (UnicodeDecodeError, json.JSONDecodeError) as erro:
        raise LLMClientError("Resposta inválida recebida do Ollama local.") from erro
    try:
        conteudo = dados["message"]["content"]
    except (KeyError, TypeError) as erro:
        raise LLMClientError("Resposta do Ollama sem conteúdo esperado.") from erro

    if not isinstance(conteudo, str) or not conteudo.strip():
        raise LLMClientError("Resposta vazia recebida do Ollama local.")

    linhas = [linha.strip() for linha in conteudo.strip().splitlines() if linha.strip()]
    normalizada = "\n".join(linhas)

    if modo_ativo == "RATEIO" and contexto:
        valor_pj = contexto.get("valor_pj")
        valor_pf = contexto.get("valor_pf")
        if valor_pj is not None and valor_pf is not None:
            return f"Rateio gerencial: {valor_pj} PJ e {valor_pf} PF."

    if modo_ativo == "CREDITO_TAXA_AUSENTE":
        return (
            "Falta a taxa real/confirmada da proposta; "
            "não vou substituir esse dado por uma taxa média.\n"
            "Qual é a taxa real/confirmada da proposta?"
        )

    if modo_ativo == "SEGURANCA":
        return (
            "Não compartilhe senha, token ou código de acesso.\n"
            "A MILA não precisa de credenciais."
        )

    if modo_ativo == "FORA_ESCOPO":
        return (
            "Esse tema não faz parte da função da MILA.\n"
            "Vamos focar em caixa, gastos, PF/PJ ou decisões financeiras do MEI."
        )

    if modo_ativo == "EXPLICACAO_CAIXA" and contexto:
        gap = contexto.get("GAP_RESERVA")
        reserva = contexto.get("reserva_minima")
        status = contexto.get("status_reserva")
        if gap is not None and reserva is not None and status == "ABAIXO_DA_RESERVA":
            return (
                f"Seu caixa projetado fica {gap} abaixo da reserva definida "
                f"de {reserva} neste cenário."
            )

    return normalizada
