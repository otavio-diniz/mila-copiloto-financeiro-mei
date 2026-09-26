import unittest

from src.router import selecionar_rota, selecionar_submodo_credito


class TestRouter(unittest.TestCase):

    def test_r01_classificacao(self):
        rota = selecionar_rota("CLASSIFICACAO")
        self.assertEqual(rota["tipo"], "llm")
        self.assertEqual(rota["modo_ativo"], "CLASSIFICACAO")
        self.assertTrue(rota["llm_call"])

    def test_r02_rateio(self):
        rota = selecionar_rota("RATEIO")
        self.assertEqual(rota["tipo"], "llm")
        self.assertEqual(rota["modo_ativo"], "RATEIO")
        self.assertTrue(rota["llm_call"])

    def test_r03_credito_comparacao(self):
        contexto = {
            "abc_completo": True,
            "exige_escolha": False,
            "pede_comparacao": True,
            "taxa_real_ausente": False,
            "pede_taxa_media": False,
        }
        modo = selecionar_submodo_credito(contexto)
        self.assertEqual(modo, "CREDITO_COMPARACAO")
        rota = selecionar_rota(modo)
        self.assertEqual(rota["tipo"], "renderer")
        self.assertEqual(rota["alvo"], "render_credito_comparacao")
        self.assertFalse(rota["llm_call"])

    def test_r04_credito_pressao_escolha(self):
        contexto = {
            "abc_completo": True,
            "exige_escolha": True,
            "pede_comparacao": False,
            "taxa_real_ausente": False,
            "pede_taxa_media": False,
        }
        modo = selecionar_submodo_credito(contexto)
        self.assertEqual(modo, "CREDITO_PRESSAO_ESCOLHA")
        rota = selecionar_rota(modo)
        self.assertEqual(rota["tipo"], "renderer")
        self.assertEqual(rota["alvo"], "render_credito_pressao_escolha")
        self.assertFalse(rota["llm_call"])

    def test_r05_credito_dado_ausente(self):
        contexto = {
            "abc_completo": False,
            "exige_escolha": False,
            "pede_comparacao": False,
            "taxa_real_ausente": False,
            "pede_taxa_media": False,
        }
        modo = selecionar_submodo_credito(contexto)
        self.assertEqual(modo, "CREDITO_DADO_AUSENTE")
        rota = selecionar_rota(modo)
        self.assertEqual(rota["tipo"], "renderer")
        self.assertEqual(rota["alvo"], "render_credito_dado_ausente")
        self.assertFalse(rota["llm_call"])

    def test_r06_credito_taxa_ausente(self):
        contexto = {
            "abc_completo": False,
            "exige_escolha": False,
            "pede_comparacao": False,
            "taxa_real_ausente": True,
            "pede_taxa_media": True,
        }
        modo = selecionar_submodo_credito(contexto)
        self.assertEqual(modo, "CREDITO_TAXA_AUSENTE")
        rota = selecionar_rota(modo)
        self.assertEqual(rota["tipo"], "llm")
        self.assertEqual(rota["modo_ativo"], "CREDITO_TAXA_AUSENTE")
        self.assertTrue(rota["llm_call"])

    def test_r07_seguranca(self):
        rota = selecionar_rota("SEGURANCA")
        self.assertEqual(rota["tipo"], "llm")
        self.assertEqual(rota["modo_ativo"], "SEGURANCA")
        self.assertTrue(rota["llm_call"])

    def test_r08_fora_escopo(self):
        rota = selecionar_rota("FORA_ESCOPO")
        self.assertEqual(rota["tipo"], "llm")
        self.assertEqual(rota["modo_ativo"], "FORA_ESCOPO")
        self.assertTrue(rota["llm_call"])

    def test_r09_explicacao_caixa(self):
        rota = selecionar_rota("EXPLICACAO_CAIXA")
        self.assertEqual(rota["tipo"], "llm")
        self.assertEqual(rota["modo_ativo"], "EXPLICACAO_CAIXA")
        self.assertTrue(rota["llm_call"])

    def test_r10_modo_desconhecido(self):
        with self.assertRaises(ValueError):
            selecionar_rota("MODO_INEXISTENTE")

    def test_r11_renderers_sem_llm(self):
        modos = (
            "CREDITO_COMPARACAO",
            "CREDITO_PRESSAO_ESCOLHA",
            "CREDITO_DADO_AUSENTE",
        )
        for modo in modos:
            with self.subTest(modo=modo):
                rota = selecionar_rota(modo)
                self.assertEqual(rota["tipo"], "renderer")
                self.assertFalse(rota["llm_call"])

    def test_estado_credito_impossivel_gera_erro(self):
        contexto = {
            "abc_completo": True,
            "exige_escolha": False,
            "pede_comparacao": False,
            "taxa_real_ausente": False,
            "pede_taxa_media": False,
        }
        with self.assertRaises(ValueError):
            selecionar_submodo_credito(contexto)


if __name__ == "__main__":
    unittest.main()
