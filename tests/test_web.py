import unittest
from pathlib import Path

from src.web import carregar_view_model, processar_mensagem, renderizar_pagina


BASE_DIR = Path(__file__).resolve().parents[1]


class TestWeb(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.vm = carregar_view_model(BASE_DIR)

    def test_view_model_credito_canonico(self):
        opcoes = self.vm["opcoes_credito"]
        self.assertEqual(opcoes["A"]["parcela"], "6x R$1.070")
        self.assertEqual(opcoes["A"]["status_reserva"], "ABAIXO_DA_RESERVA")
        self.assertEqual(opcoes["B"]["status_reserva"], "RESERVA_PRESERVADA")
        self.assertEqual(opcoes["C"]["status_reserva"], "RESERVA_PRESERVADA")

    def test_renderer_credito_comparacao(self):
        resposta = processar_mensagem(
            "CREDITO_COMPARACAO", "compare", self.vm
        )
        self.assertTrue(resposta.startswith("A: 6x R$1.070"))
        self.assertEqual(len(resposta.splitlines()), 4)

    def test_fluxo_linguistico_recebe_contexto(self):
        capturado = {}

        def fake_llm(modo, mensagem, contexto):
            capturado["modo"] = modo
            capturado["mensagem"] = mensagem
            capturado["contexto"] = contexto
            return "ok"

        resposta = processar_mensagem(
            "EXPLICACAO_CAIXA", "explique", self.vm, llm_func=fake_llm
        )
        self.assertEqual(resposta, "ok")
        self.assertEqual(capturado["modo"], "EXPLICACAO_CAIXA")
        self.assertIn("saldo_projetado", capturado["contexto"])
        self.assertIn("GAP_RESERVA", capturado["contexto"])

    def test_html_escapa_entrada_e_resposta(self):
        html = renderizar_pagina(
            self.vm,
            mensagem="<script>alert(1)</script>",
            resposta="<b>resposta</b>",
        )
        self.assertNotIn("<script>", html)
        self.assertIn("&lt;script&gt;alert(1)&lt;/script&gt;", html)
        self.assertIn("&lt;b&gt;resposta&lt;/b&gt;", html)
        self.assertIn("MATERIAL DIDÁTICO FICTÍCIO/SINTÉTICO", html)


if __name__ == "__main__":
    unittest.main()
