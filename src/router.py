"""
Roteamento determinístico da MILA.

Não chama LLM/Ollama/HTTP e não executa cálculo financeiro.
"""


MODOS_LINGUISTICOS = {
    "CLASSIFICACAO",
    "RATEIO",
    "CREDITO_TAXA_AUSENTE",
    "SEGURANCA",
    "FORA_ESCOPO",
    "EXPLICACAO_CAIXA",
}

MODOS_RENDERER = {
    "CREDITO_COMPARACAO",
    "CREDITO_PRESSAO_ESCOLHA",
    "CREDITO_DADO_AUSENTE",
}


def selecionar_submodo_credito(contexto: dict) -> str:
    """Seleciona deterministicamente um submodo de crédito.

    Contexto esperado: abc_completo, exige_escolha, pede_comparacao,
    taxa_real_ausente e pede_taxa_media, todos booleanos.
    """
    if contexto["taxa_real_ausente"] and contexto["pede_taxa_media"]:
        return "CREDITO_TAXA_AUSENTE"
    elif contexto["abc_completo"] and contexto["exige_escolha"]:
        return "CREDITO_PRESSAO_ESCOLHA"
    elif contexto["abc_completo"] and contexto["pede_comparacao"]:
        return "CREDITO_COMPARACAO"
    elif not contexto["abc_completo"]:
        return "CREDITO_DADO_AUSENTE"
    else:
        raise ValueError("Estado de roteamento inválido.")


def selecionar_rota(
    modo_solicitado: str,
    contexto_estruturado: dict | None = None,
) -> dict:
    """Seleciona a rota determinística do modo informado.

    Modos de renderer devem indicar alvo e llm_call=False.
    Modos linguísticos devem indicar um único modo_ativo e llm_call=True.
    Modo desconhecido deve gerar ValueError.
    """
    rotas_renderer = {
        "CREDITO_COMPARACAO": "render_credito_comparacao",
        "CREDITO_PRESSAO_ESCOLHA": "render_credito_pressao_escolha",
        "CREDITO_DADO_AUSENTE": "render_credito_dado_ausente",
    }

    if modo_solicitado in rotas_renderer:
        return {
            "tipo": "renderer",
            "alvo": rotas_renderer[modo_solicitado],
            "llm_call": False,
        }

    if modo_solicitado in MODOS_LINGUISTICOS:
        return {
            "tipo": "llm",
            "modo_ativo": modo_solicitado,
            "llm_call": True,
        }

    raise ValueError("Modo desconhecido.")
