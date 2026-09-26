"""
Renderers determinísticos da MILA para os contratos T06/T07/T08.

Este arquivo não calcula valores financeiros e não chama LLM/Ollama.
"""


def _linha_opcao(rotulo: str, opcao: dict) -> str:
    campos_obrigatorios = (
        "parcela",
        "total",
        "vencimento",
        "status_reserva",
    )

    for campo in campos_obrigatorios:
        if campo not in opcao:
            raise ValueError(
                f"Campo obrigatório ausente: {campo}"
            )

    return f"{rotulo}: {opcao['parcela']}; total {opcao['total']}; vencimento {opcao['vencimento']}; reserva {opcao['status_reserva']}."


def render_credito_comparacao(opcoes: dict) -> str:
    linhas = [
        _linha_opcao("A", opcoes["A"]),
        _linha_opcao("B", opcoes["B"]),
        _linha_opcao("C", opcoes["C"]),
        "O que é mais importante para você: menor custo total, menor parcela, vencimento ou preservar a reserva?",
    ]

    return "\n".join(linhas)


def render_credito_pressao_escolha(opcoes: dict) -> str:
    linhas = [
        "A MILA não decide qual empréstimo você deve pegar.",
        _linha_opcao("A", opcoes["A"]),
        _linha_opcao("B", opcoes["B"]),
        _linha_opcao("C", opcoes["C"]),
        "O que é mais importante para você: menor custo total, menor parcela, vencimento ou preservar a reserva?",
    ]

    return "\n".join(linhas)


def render_credito_dado_ausente() -> str:
    linhas = [
        "Falta o valor da parcela da proposta.",
        "Qual é o valor da parcela?",
    ]

    return "\n".join(linhas)