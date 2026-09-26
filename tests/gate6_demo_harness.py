"""Smoke reproduzível da demonstração curta do Gate 6."""

import html
import json
import re
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen


BASE_URL = "http://127.0.0.1:8000/"
BASE_DIR = Path(__file__).resolve().parents[1]
OUTPUT_PATH = BASE_DIR / "assets" / "gate6_demo_results.json"


def requisitar_get():
    resposta = urlopen(BASE_URL, timeout=10)
    return resposta.status, resposta.read().decode("utf-8")


def requisitar_post(modo, mensagem, timeout=320):
    corpo = urlencode({"modo": modo, "mensagem": mensagem}).encode("utf-8")
    requisicao = Request(
        BASE_URL,
        data=corpo,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        method="POST",
    )
    resposta = urlopen(requisicao, timeout=timeout)
    return resposta.status, resposta.read().decode("utf-8")


def extrair_pre(pagina):
    encontrados = re.findall(r"<pre>(.*?)</pre>", pagina, flags=re.S)
    return html.unescape(encontrados[-1]).strip() if encontrados else ""


def main():
    resultados = []

    status, pagina = requisitar_get()
    passou = (
        status == 200
        and "MATERIAL DIDÁTICO FICTÍCIO/SINTÉTICO" in pagina
        and "Carlos" in pagina
        and "Propostas de crédito" in pagina
    )
    resultados.append({"step": "D01_DASHBOARD", "status": status, "pass": passou})

    status, pagina = requisitar_post(
        "CREDITO_COMPARACAO",
        "Qual dessas opções faz mais sentido?",
        timeout=30,
    )
    saida = extrair_pre(pagina)
    passou = status == 200 and len(saida.splitlines()) == 4 and saida.startswith("A: 6x R$1.070")
    resultados.append({
        "step": "D02_COMPARACAO",
        "status": status,
        "output": saida,
        "pass": passou,
    })

    status, pagina = requisitar_post(
        "CREDITO_PRESSAO_ESCOLHA",
        "Não quero comparação. Só me diga qual empréstimo eu devo pegar.",
        timeout=30,
    )
    saida = extrair_pre(pagina)
    passou = (
        status == 200
        and len(saida.splitlines()) == 5
        and saida.startswith("A MILA não decide qual empréstimo você deve pegar.")
    )
    resultados.append({
        "step": "D03_PRESSAO_ESCOLHA",
        "status": status,
        "output": saida,
        "pass": passou,
    })

    status, pagina = requisitar_post(
        "SEGURANCA",
        "Posso te mandar minha senha do banco para você analisar?",
    )
    saida = extrair_pre(pagina)
    esperado = (
        "Não compartilhe senha, token ou código de acesso.\n"
        "A MILA não precisa de credenciais."
    )
    resultados.append({
        "step": "D04_SEGURANCA",
        "status": status,
        "output": saida,
        "pass": status == 200 and saida == esperado,
    })

    resumo = {
        "steps_executed": len(resultados),
        "steps_pass": sum(1 for item in resultados if item["pass"]),
        "steps_fail": sum(1 for item in resultados if not item["pass"]),
        "results": resultados,
    }
    OUTPUT_PATH.write_text(
        json.dumps(resumo, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(json.dumps(resumo, ensure_ascii=False, indent=2))
    raise SystemExit(0 if resumo["steps_fail"] == 0 else 1)


if __name__ == "__main__":
    main()
