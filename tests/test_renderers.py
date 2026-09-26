import copy
import hashlib
import unittest
from pathlib import Path

from src.renderers import (
    render_credito_comparacao,
    render_credito_pressao_escolha,
    render_credito_dado_ausente,
)


OPCOES = {
    "A": {
        "parcela": "6x R$1.070",
        "total": "R$6.420",
        "vencimento": "dia 05",
        "status_reserva": "ABAIXO_DA_RESERVA",
    },
    "B": {
        "parcela": "6x R$1.110",
        "total": "R$6.660",
        "vencimento": "dia 25",
        "status_reserva": "RESERVA_PRESERVADA",
    },
    "C": {
        "parcela": "12x R$620",
        "total": "R$7.440",
        "vencimento": "dia 20",
        "status_reserva": "RESERVA_PRESERVADA",
    },
}

EXPECTED_T06 = "\n".join(
    [
        "A: 6x R$1.070; total R$6.420; vencimento dia 05; reserva ABAIXO_DA_RESERVA.",
        "B: 6x R$1.110; total R$6.660; vencimento dia 25; reserva RESERVA_PRESERVADA.",
        "C: 12x R$620; total R$7.440; vencimento dia 20; reserva RESERVA_PRESERVADA.",
        (
            "O que é mais importante para você: menor custo total, "
            "menor parcela, vencimento ou preservar a reserva?"
        ),
    ]
)

EXPECTED_T07 = "\n".join(
    [
        "A MILA não decide qual empréstimo você deve pegar.",
        "A: 6x R$1.070; total R$6.420; vencimento dia 05; reserva ABAIXO_DA_RESERVA.",
        "B: 6x R$1.110; total R$6.660; vencimento dia 25; reserva RESERVA_PRESERVADA.",
        "C: 12x R$620; total R$7.440; vencimento dia 20; reserva RESERVA_PRESERVADA.",
        (
            "O que é mais importante para você: menor custo total, "
            "menor parcela, vencimento ou preservar a reserva?"
        ),
    ]
)

EXPECTED_T08 = "\n".join(
    [
        "Falta o valor da parcela da proposta.",
        "Qual é o valor da parcela?",
    ]
)


def sha256_texto(texto: str) -> str:
    return hashlib.sha256(texto.encode("utf-8")).hexdigest().upper()


class TestRenderers(unittest.TestCase):

    def test_t06_output_exato_e_hash(self):
        saida = render_credito_comparacao(copy.deepcopy(OPCOES))
        self.assertEqual(saida, EXPECTED_T06)
        self.assertEqual(len(saida.encode("utf-8")), 334)
        self.assertEqual(
            sha256_texto(saida),
            "CAE94B2390341A94E2229D18E326011128E62F2D15B7EA3E11CAF2AF72A4AB26",
        )

    def test_t07_output_exato_e_hash(self):
        saida = render_credito_pressao_escolha(copy.deepcopy(OPCOES))
        self.assertEqual(saida, EXPECTED_T07)
        self.assertEqual(len(saida.encode("utf-8")), 388)
        self.assertEqual(
            sha256_texto(saida),
            "03947E4F3C244B7DF909901E8ADEBB221B62D9A5AA6E8781899AD31CD3227047",
        )

    def test_t08_output_exato_e_hash(self):
        saida = render_credito_dado_ausente()
        self.assertEqual(saida, EXPECTED_T08)
        self.assertEqual(len(saida.encode("utf-8")), 65)
        self.assertEqual(
            sha256_texto(saida),
            "FB9405EC9EB66B4BE26A682ED2EF72B1D942A93EE38B1FD57CBC128FFFAC7A0A",
        )

    def test_sem_trailing_newline_ou_linha_em_branco(self):
        saidas = [
            render_credito_comparacao(copy.deepcopy(OPCOES)),
            render_credito_pressao_escolha(copy.deepcopy(OPCOES)),
            render_credito_dado_ausente(),
        ]

        for saida in saidas:
            self.assertFalse(saida.endswith("\n"))
            self.assertNotIn("\n\n", saida)
            for linha in saida.split("\n"):
                self.assertEqual(linha, linha.rstrip())

    def test_t06_t07_ignoram_campos_extras(self):
        opcoes = copy.deepcopy(OPCOES)
        for opcao in opcoes.values():
            opcao["menor_caixa_projetado"] = "R$999.999"
            opcao["reserva_minima"] = "R$999.999"

        self.assertEqual(
            render_credito_comparacao(opcoes),
            EXPECTED_T06,
        )
        self.assertEqual(
            render_credito_pressao_escolha(opcoes),
            EXPECTED_T07,
        )

    def test_dado_obrigatorio_ausente_gera_value_error(self):
        opcoes = copy.deepcopy(OPCOES)
        del opcoes["A"]["parcela"]

        with self.assertRaises(ValueError):
            render_credito_comparacao(opcoes)

    def test_renderers_sem_llm_ou_http(self):
        conteudo = Path("src/renderers.py").read_text(encoding="utf-8").lower()

        termos_proibidos = [
            "import ollama",
            "import requests",
            "import urllib",
            "from urllib",
            "openai",
            "http://",
            "https://",
        ]

        for termo in termos_proibidos:
            self.assertNotIn(termo, conteudo)


if __name__ == "__main__":
    unittest.main()
