import json
import unittest
from urllib import error

from src.llm_client import LLMClientError, chat_local


class FakeResponse:
    def __init__(self, payload):
        self.payload = payload

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False

    def read(self):
        return json.dumps(self.payload).encode("utf-8")


class TestLLMClient(unittest.TestCase):

    def test_envia_um_unico_modo_ativo(self):
        capturado = {}

        def fake_urlopen(req, timeout):
            capturado["url"] = req.full_url
            capturado["timeout"] = timeout
            capturado["body"] = json.loads(req.data.decode("utf-8"))
            return FakeResponse({"message": {"content": "Resposta local"}})

        resposta = chat_local(
            "CLASSIFICACAO",
            "Recebi de um cliente por um serviço.",
            {"origem": "teste"},
            urlopen_func=fake_urlopen,
        )

        self.assertEqual(resposta, "Resposta local")
        self.assertEqual(capturado["url"], "http://127.0.0.1:11434/api/chat")
        self.assertEqual(capturado["body"]["model"], "llama3.2:3b")
        self.assertEqual(capturado["timeout"], 300)
        self.assertEqual(capturado["body"]["keep_alive"], "5m")
        self.assertEqual(capturado["body"]["options"]["temperature"], 0)
        self.assertEqual(capturado["body"]["options"]["num_ctx"], 4096)
        self.assertEqual(capturado["body"]["options"]["num_predict"], 512)
        mensagens = capturado["body"]["messages"]
        self.assertEqual(len(mensagens), 2)
        self.assertIn("MODO_ATIVO=CLASSIFICACAO", mensagens[0]["content"])
        self.assertNotIn("MODO_ATIVO=SEGURANCA", mensagens[0]["content"])
        self.assertEqual(mensagens[1]["content"], "Recebi de um cliente por um serviço.")

    def test_erro_de_conexao_e_controlado(self):
        def fake_urlopen(req, timeout):
            raise error.URLError("indisponível")

        with self.assertRaises(LLMClientError):
            chat_local(
                "CLASSIFICACAO",
                "Teste",
                urlopen_func=fake_urlopen,
            )

    def test_guardrail_rateio_calculado_preserva_valores(self):
        def fake_urlopen(req, timeout):
            return FakeResponse({"message": {"content": "Resposta inadequada"}})

        resposta = chat_local(
            "RATEIO",
            "Como ficou?",
            {"valor_pj": "R$108", "valor_pf": "R$72"},
            urlopen_func=fake_urlopen,
        )
        self.assertEqual(resposta, "Rateio gerencial: R$108 PJ e R$72 PF.")

    def test_guardrail_taxa_ausente_canoniza_contrato(self):
        def fake_urlopen(req, timeout):
            return FakeResponse({"message": {"content": "Recusa genérica"}})

        resposta = chat_local(
            "CREDITO_TAXA_AUSENTE",
            "Use uma taxa média",
            urlopen_func=fake_urlopen,
        )
        self.assertEqual(
            resposta,
            "Falta a taxa real/confirmada da proposta; não vou substituir esse dado por uma taxa média.\n"
            "Qual é a taxa real/confirmada da proposta?",
        )

    def test_guardrail_explicacao_caixa_remove_prescricao(self):
        def fake_urlopen(req, timeout):
            return FakeResponse({"message": {"content": "Resposta com recomendação indevida"}})

        resposta = chat_local(
            "EXPLICACAO_CAIXA",
            "O que isso significa?",
            {
                "saldo_projetado": "R$3.000",
                "reserva_minima": "R$3.500",
                "GAP_RESERVA": "R$500",
                "status_reserva": "ABAIXO_DA_RESERVA",
            },
            urlopen_func=fake_urlopen,
        )
        self.assertEqual(
            resposta,
            "Seu caixa projetado fica R$500 abaixo da reserva definida de R$3.500 neste cenário.",
        )

    def test_guardrail_seguranca_canoniza_contrato(self):
        def fake_urlopen(req, timeout):
            return FakeResponse({"message": {"content": "Não compartilhe senha."}})

        resposta = chat_local(
            "SEGURANCA",
            "Posso mandar minha senha?",
            urlopen_func=fake_urlopen,
        )
        self.assertEqual(
            resposta,
            "Não compartilhe senha, token ou código de acesso.\n"
            "A MILA não precisa de credenciais.",
        )

    def test_guardrail_fora_escopo_canoniza_contrato(self):
        def fake_urlopen(req, timeout):
            return FakeResponse({"message": {"content": "Não sei."}})

        resposta = chat_local(
            "FORA_ESCOPO",
            "Qual vai ser o tempo amanhã?",
            urlopen_func=fake_urlopen,
        )
        self.assertEqual(
            resposta,
            "Esse tema não faz parte da função da MILA.\n"
            "Vamos focar em caixa, gastos, PF/PJ ou decisões financeiras do MEI.",
        )
