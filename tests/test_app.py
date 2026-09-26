import io
import unittest
from urllib.parse import urlencode

from src.app import application


class TestApp(unittest.TestCase):

    def chamar(self, metodo="GET", dados=None):
        corpo = urlencode(dados or {}).encode("utf-8")
        environ = {
            "REQUEST_METHOD": metodo,
            "CONTENT_LENGTH": str(len(corpo)),
            "wsgi.input": io.BytesIO(corpo),
        }
        capturado = {}

        def start_response(status, headers):
            capturado["status"] = status
            capturado["headers"] = headers

        resposta = b"".join(application(environ, start_response))
        return capturado, resposta.decode("utf-8")

    def test_get_retorna_html_200(self):
        meta, html = self.chamar()
        self.assertEqual(meta["status"], "200 OK")
        self.assertIn("MILA", html)
        self.assertIn("MATERIAL DIDÁTICO FICTÍCIO/SINTÉTICO", html)

    def test_post_renderer_retorna_saida_deterministica(self):
        meta, html = self.chamar(
            "POST",
            {
                "modo": "CREDITO_DADO_AUSENTE",
                "mensagem": "Posso pegar esse empréstimo?",
            },
        )
        self.assertEqual(meta["status"], "200 OK")
        self.assertIn("Falta o valor da parcela da proposta.", html)
        self.assertIn("Qual é o valor da parcela?", html)


if __name__ == "__main__":
    unittest.main()
