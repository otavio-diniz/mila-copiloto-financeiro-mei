"""Composição de dados e HTML server-rendered da MILA."""

from decimal import Decimal
from html import escape
from pathlib import Path

from src.core import carregar_compromissos, carregar_perfil
from src.core import carregar_propostas, carregar_transacoes, projetar_caixa
from src.llm_client import chat_local
from src.renderers import render_credito_comparacao
from src.renderers import render_credito_dado_ausente
from src.renderers import render_credito_pressao_escolha
from src.router import selecionar_rota


MODOS_UI = (
    "CLASSIFICACAO", "RATEIO", "CREDITO_COMPARACAO",
    "CREDITO_PRESSAO_ESCOLHA", "CREDITO_DADO_AUSENTE",
    "CREDITO_TAXA_AUSENTE", "SEGURANCA", "FORA_ESCOPO",
    "EXPLICACAO_CAIXA",
)


def formatar_brl(valor: Decimal) -> str:
    texto = f"{valor:,.2f}"
    texto = texto.replace(",", "_").replace(".", ",").replace("_", ".")
    if texto.endswith(",00"):
        texto = texto[:-3]
    return f"R${texto}"


def carregar_view_model(base_dir: Path) -> dict:
    data_dir = base_dir / "data"
    perfil = carregar_perfil(data_dir / "perfil_mei.json")
    transacoes = carregar_transacoes(data_dir / "transacoes.csv")
    compromissos = carregar_compromissos(data_dir / "compromissos.csv")
    propostas = carregar_propostas(data_dir / "propostas_credito.csv")
    reserva = perfil["reserva_operacional_minima"]
    saldo = perfil["saldo_empresarial_inicial"]
    projecao_base = projetar_caixa(saldo, compromissos, reserva)

    projecoes = {}
    opcoes_credito = {}
    for proposta in propostas:
        identificador = proposta["proposta_id"]
        projecao = projetar_caixa(saldo, compromissos, reserva, proposta)
        projecoes[identificador] = projecao
        opcoes_credito[identificador] = {
            "parcela": f"{proposta['numero_parcelas']}x {formatar_brl(proposta['valor_parcela'])}",
            "total": formatar_brl(proposta["total_pago"]),
            "vencimento": f"dia {proposta['dia_primeiro_vencimento']:02d}",
            "status_reserva": projecao["status_reserva"],
        }

    return {
        "perfil": perfil,
        "transacoes": transacoes,
        "compromissos": compromissos,
        "propostas": propostas,
        "projecao_base": projecao_base,
        "projecoes_credito": projecoes,
        "opcoes_credito": opcoes_credito,
    }


def contexto_llm(modo: str, view_model: dict) -> dict:
    if modo != "EXPLICACAO_CAIXA":
        return {}
    projecao = view_model["projecao_base"]
    perfil = view_model["perfil"]
    return {
        "saldo_projetado": formatar_brl(projecao["saldo_final"]),
        "reserva_minima": formatar_brl(perfil["reserva_operacional_minima"]),
        "GAP_RESERVA": formatar_brl(projecao["gap_reserva"]),
        "status_reserva": projecao["status_reserva"],
    }


def processar_mensagem(modo, mensagem, view_model, *, llm_func=chat_local):
    rota = selecionar_rota(modo)
    if rota["tipo"] == "renderer":
        if modo == "CREDITO_COMPARACAO":
            return render_credito_comparacao(view_model["opcoes_credito"])
        if modo == "CREDITO_PRESSAO_ESCOLHA":
            return render_credito_pressao_escolha(view_model["opcoes_credito"])
        if modo == "CREDITO_DADO_AUSENTE":
            return render_credito_dado_ausente()
        raise ValueError("Renderer não mapeado.")

    contexto = contexto_llm(rota["modo_ativo"], view_model)
    return llm_func(rota["modo_ativo"], mensagem, contexto)


def renderizar_pagina(view_model, *, resposta="", erro="", mensagem="", modo="CLASSIFICACAO"):
    perfil = view_model["perfil"]
    projecao = view_model["projecao_base"]
    opcoes = []
    for item in MODOS_UI:
        selecionado = " selected" if item == modo else ""
        opcoes.append(
            '<option value="{}"{}>{}</option>'.format(
                escape(item), selecionado, escape(item)
            )
        )
    linhas = []
    for identificador in ("A", "B", "C"):
        opcao = view_model["opcoes_credito"][identificador]
        linhas.append(
            "<tr><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr>".format(
                identificador,
                escape(opcao["parcela"]),
                escape(opcao["total"]),
                escape(opcao["vencimento"]),
                escape(opcao["status_reserva"]),
            )
        )
    partes = [
        '<!doctype html><html lang="pt-BR"><head><meta charset="utf-8">',
        '<meta name="viewport" content="width=device-width,initial-scale=1">',
        '<title>MILA — Copiloto Financeiro para MEI</title>',
        '<style>body{font-family:Arial,sans-serif;max-width:1050px;margin:auto;padding:24px;background:#f4f6f8;color:#1f2933}',
        'header,section{background:white;border:1px solid #d9e2ec;border-radius:12px;padding:20px;margin-bottom:16px}',
        'table{width:100%;border-collapse:collapse}th,td{padding:8px;border-bottom:1px solid #e5e7eb;text-align:left}',
        'select,textarea,button{width:100%;box-sizing:border-box;padding:10px;margin-top:6px}pre{white-space:pre-wrap}</style>',
        '</head><body><header><h1>MILA</h1>',
        '<p>MEI Inteligente para Liquidez e Autonomia</p>',
        '<p><strong>MATERIAL DIDÁTICO FICTÍCIO/SINTÉTICO</strong></p></header>',
    ]
    partes.extend([
        '<section><h2>Perfil demonstrativo</h2>',
        '<p><strong>{}</strong> — {} — {}</p>'.format(
            escape(perfil["nome_ficticio"]),
            escape(perfil["atividade"]),
            escape(perfil["regime"]),
        ),
        '<p>Saldo empresarial inicial: <strong>{}</strong> | Reserva mínima: <strong>{}</strong></p>'.format(
            formatar_brl(perfil["saldo_empresarial_inicial"]),
            formatar_brl(perfil["reserva_operacional_minima"]),
        ),
        '<p>Projeção sem crédito: saldo final <strong>{}</strong>; menor caixa <strong>{}</strong>; status <strong>{}</strong>.</p>'.format(
            formatar_brl(projecao["saldo_final"]),
            formatar_brl(projecao["menor_caixa"]),
            escape(projecao["status_reserva"]),
        ),
        '</section>',
    ])
    partes.extend([
        '<section><h2>Propostas de crédito</h2><table>',
        '<thead><tr><th>Opção</th><th>Parcela</th><th>Total</th><th>Vencimento</th><th>Reserva</th></tr></thead><tbody>',
        ''.join(linhas),
        '</tbody></table></section>',
        '<section><h2>Interagir com a MILA</h2><form method="post">',
        '<label for="modo">Modo</label><select id="modo" name="modo">',
        ''.join(opcoes),
        '</select><label for="mensagem">Mensagem</label>',
        '<textarea id="mensagem" name="mensagem" rows="4">{}</textarea>'.format(escape(mensagem)),
        '<button type="submit">Enviar</button></form>',
    ])
    if erro:
        partes.append('<p><strong>{}</strong></p>'.format(escape(erro)))
    partes.append('</section>')
    if resposta:
        partes.append(
            '<section><h2>Resposta da MILA</h2><pre>{}</pre></section>'.format(
                escape(resposta)
            )
        )
    partes.append('</body></html>')
    return ''.join(partes)
