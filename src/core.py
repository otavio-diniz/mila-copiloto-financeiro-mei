from pathlib import Path
import json
import csv
from decimal import Decimal


CAMPOS_PERFIL_OBRIGATORIOS = {
    "classificacao",
    "nome_ficticio",
    "atividade",
    "regime",
    "faturamento_medio_mensal",
    "saldo_empresarial_inicial",
    "retirada_pessoal_habitual_mensal",
    "reserva_operacional_minima",
    "padrao_recebimentos",
    "aquisicao_simulada",
}

CAMPOS_TRANSACOES_OBRIGATORIOS = {
    "data",
    "descricao",
    "valor",
    "tipo_movimento",
    "classe_esperada",
    "observacao",
}

CAMPOS_COMPROMISSOS_OBRIGATORIOS = {
    "data_prevista",
    "descricao",
    "valor",
    "tipo_movimento",
    "classe_esperada",
    "observacao",
}


CAMPOS_PROPOSTAS_OBRIGATORIOS = {
    "proposta_id",
    "valor_financiado",
    "numero_parcelas",
    "valor_parcela",
    "total_pago",
    "custo_adicional",
    "dia_primeiro_vencimento",
    "caracteristica",
}


def carregar_perfil(caminho: Path) -> dict:
    """
    Carrega o arquivo JSON com o perfil sintético do MEI.
    """

    with caminho.open(mode="r", encoding="utf-8") as arquivo:
        try:
            perfil = json.load(arquivo)
        except json.JSONDecodeError as erro:
            raise ValueError(
                "JSON inválido no perfil."
            ) from erro

    if not isinstance(perfil, dict):
        raise ValueError("O perfil deve ser um objeto JSON.")

    erros = validar_perfil(perfil)

    if erros:
        raise ValueError(
            "Perfil inválido: " + "; ".join(erros)
        )

    perfil["faturamento_medio_mensal"] = normalizar_valor_monetario(
        str(perfil["faturamento_medio_mensal"])
    )

    perfil["saldo_empresarial_inicial"] = normalizar_valor_monetario(
        str(perfil["saldo_empresarial_inicial"])
    )

    perfil["retirada_pessoal_habitual_mensal"] = normalizar_valor_monetario(
        str(perfil["retirada_pessoal_habitual_mensal"])
    )

    perfil["reserva_operacional_minima"] = normalizar_valor_monetario(
        str(perfil["reserva_operacional_minima"])
    )

    aquisicao = perfil["aquisicao_simulada"]

    if not isinstance(aquisicao, dict):
        raise ValueError(
            "aquisicao_simulada deve ser um objeto."
        )

    if "valor" not in aquisicao:
        raise ValueError(
            "Campo obrigatório ausente: aquisicao_simulada.valor"
        )

    aquisicao["valor"] = normalizar_valor_monetario(
        str(aquisicao["valor"])
    )

    return perfil


def validar_perfil(perfil: dict) -> list[str]:
    """
    Verifica se todos os campos obrigatórios existem no perfil.
    """

    erros = []

    for campo in CAMPOS_PERFIL_OBRIGATORIOS:
        if campo not in perfil:
            erros.append(f"Campo obrigatório ausente: {campo}")

    return erros


def validar_cabecalhos(
    cabecalhos,
    campos_obrigatorios,
) -> list[str]:
    """
    Verifica se todos os cabeçalhos obrigatórios estão presentes.
    """

    cabecalhos_encontrados = set(cabecalhos or [])

    campos_ausentes = campos_obrigatorios - cabecalhos_encontrados

    return [
        f"Campo obrigatório ausente: {campo}"
        for campo in sorted(campos_ausentes)
    ]

def carregar_transacoes(caminho: Path) -> list[dict]:
    """
    Carrega as transações sintéticas do arquivo CSV.
    """

    with caminho.open(mode="r", encoding="utf-8", newline="") as arquivo:
        leitor = csv.DictReader(arquivo)

        erros = validar_cabecalhos(
            leitor.fieldnames,
            CAMPOS_TRANSACOES_OBRIGATORIOS,
        )

        if erros:
            raise ValueError(
                "Cabeçalho inválido em transações: " + "; ".join(erros)
            )

        transacoes = list(leitor)

    for transacao in transacoes:
        transacao["valor"] = normalizar_valor_monetario(transacao["valor"])

    return transacoes

def validar_transacoes(transacoes: list[dict]) -> list[str]:
    """
    Verifica se os registros possuem os campos obrigatórios.
    """

    erros = []

    for indice, transacao in enumerate(transacoes):
        for campo in CAMPOS_TRANSACOES_OBRIGATORIOS:
            if campo not in transacao:
                erros.append(
                    f"Transação {indice}: campo obrigatório ausente: {campo}"
                )

    return erros


def carregar_compromissos(caminho: Path) -> list[dict]:
    """
    Carrega os compromissos sintéticos do arquivo CSV.
    """

    with caminho.open(mode="r", encoding="utf-8", newline="") as arquivo:
        leitor = csv.DictReader(arquivo)
        erros = validar_cabecalhos(
            leitor.fieldnames,
            CAMPOS_COMPROMISSOS_OBRIGATORIOS,
        )

        if erros:
            raise ValueError(
                "Cabeçalho inválido em compromissos: " + "; ".join(erros)
            )
        compromissos = list(leitor)

    for compromisso in compromissos:
        compromisso["valor"] = normalizar_valor_monetario(compromisso["valor"])

    return compromissos

def validar_compromissos(compromissos: list[dict]) -> list[str]:
    """
    Verifica se os compromissos possuem os campos obrigatórios.
    """

    erros = []

    for indice, compromisso in enumerate(compromissos):
        for campo in CAMPOS_COMPROMISSOS_OBRIGATORIOS:
            if campo not in compromisso:
                erros.append(
                    f"Compromisso {indice}: campo obrigatório ausente: {campo}"
                )

    return erros


def carregar_propostas(caminho: Path) -> list[dict]:
    """
    Carrega as propostas sintéticas de crédito do arquivo CSV.
    """

    with caminho.open(mode="r", encoding="utf-8", newline="") as arquivo:
        leitor = csv.DictReader(arquivo)
        erros = validar_cabecalhos(
            leitor.fieldnames,
            CAMPOS_PROPOSTAS_OBRIGATORIOS,
        )

        if erros:
            raise ValueError(
                "Cabeçalho inválido em propostas: " + "; ".join(erros)
            )
        propostas = list(leitor)

    for proposta in propostas:
        proposta["valor_financiado"] = normalizar_valor_monetario(
            proposta["valor_financiado"]
        )
        proposta["valor_parcela"] = normalizar_valor_monetario(
            proposta["valor_parcela"]
        )
        proposta["total_pago"] = normalizar_valor_monetario(
            proposta["total_pago"]
        )
        proposta["custo_adicional"] = normalizar_valor_monetario(
            proposta["custo_adicional"]
        )
        proposta["numero_parcelas"] = int(proposta["numero_parcelas"])
        proposta["dia_primeiro_vencimento"] = int(proposta["dia_primeiro_vencimento"])

    return propostas


def validar_propostas(propostas: list[dict]) -> list[str]:
    """
    Verifica se as propostas possuem os campos obrigatórios.
    """

    erros = []

    for indice, proposta in enumerate(propostas):
        for campo in CAMPOS_PROPOSTAS_OBRIGATORIOS:
            if campo not in proposta:
                erros.append(
                    f"Proposta {indice}: campo obrigatório ausente: {campo}"
                )

    return erros


def normalizar_valor_monetario(valor_textual: str) -> Decimal:
    """
    Converte um valor monetário textual para Decimal.
    """

    return Decimal(valor_textual)


def somar_movimentos(movimentos: list[dict]) -> Decimal:
    """
    Soma efeitos monetários já assinados, sem inverter sinal novamente.
    """
    total = Decimal("0")

    for movimento in movimentos:
        total = total + movimento["valor"]

    return total


def avaliar_reserva(
    menor_caixa: Decimal,
    reserva_minima: Decimal,
) -> dict:
    """
    Deriva status e gap da reserva a partir de valores já calculados.
    """
    if menor_caixa < reserva_minima:
        status = "ABAIXO_DA_RESERVA"
        gap = reserva_minima - menor_caixa
    else:
        status = "RESERVA_PRESERVADA"
        gap = Decimal("0")

    return {
        "status": status,
        "gap": gap,
    }


def projetar_caixa(
    saldo_inicial: Decimal,
    compromissos: list[dict],
    reserva_minima: Decimal,
    proposta: dict | None = None,
) -> dict:
    """
    Projeta o caixa cronologicamente e acompanha o menor saldo observado.
    A proposta, quando fornecida, representa apenas a primeira parcela.
    A reserva mínima é recebida explicitamente para derivar status e gap.

    Retorno esperado:
    {
        "saldo_final": Decimal,
        "menor_caixa": Decimal,
        "status_reserva": str,
        "gap_reserva": Decimal,
    }
    """
    saldo = saldo_inicial
    menor_caixa = saldo_inicial
    eventos = []

    for compromisso in compromissos:
        dia = int(compromisso["data_prevista"].split("-")[-1])
        eventos.append(
            (
                dia,
                compromisso["valor"],
            )
        )

    if proposta is not None:
        eventos.append(
            (
                proposta["dia_primeiro_vencimento"],
                -proposta["valor_parcela"],
            )
        )

    eventos.sort(key=lambda evento: evento[0])

    for _, valor in eventos:
        saldo = saldo + valor

        if saldo < menor_caixa:
            menor_caixa = saldo

    reserva = avaliar_reserva(
        menor_caixa,
        reserva_minima,
    )

    return {
        "saldo_final": saldo,
        "menor_caixa": menor_caixa,
        "status_reserva": reserva["status"],
        "gap_reserva": reserva["gap"],
    }
