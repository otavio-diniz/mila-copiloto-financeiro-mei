import unittest

from src.prompts import BASE_PROMPT, MODE_PROMPTS, montar_system_prompt


class TestPrompts(unittest.TestCase):

    def test_apenas_seis_modos_linguisticos(self):
        self.assertEqual(
            set(MODE_PROMPTS),
            {
                "CLASSIFICACAO",
                "RATEIO",
                "CREDITO_TAXA_AUSENTE",
                "SEGURANCA",
                "FORA_ESCOPO",
                "EXPLICACAO_CAIXA",
            },
        )

    def test_renderers_nao_possuem_mode_prompt(self):
        for modo in (
            "CREDITO_COMPARACAO",
            "CREDITO_PRESSAO_ESCOLHA",
            "CREDITO_DADO_AUSENTE",
        ):
            self.assertNotIn(modo, MODE_PROMPTS)

    def test_prompt_contem_base_um_modo_e_contexto(self):
        prompt = montar_system_prompt("SEGURANCA", {"origem": "teste"})
        self.assertIn(BASE_PROMPT, prompt)
        self.assertIn("MODO_ATIVO=SEGURANCA", prompt)
        self.assertIn("origem=teste", prompt)
        self.assertNotIn("MODO_ATIVO=CLASSIFICACAO", prompt)
        self.assertNotIn("MODO_ATIVO=RATEIO", prompt)

    def test_contexto_decimal_usa_serializacao_textual(self):
        prompt = montar_system_prompt(
            "EXPLICACAO_CAIXA",
            {"saldo": "4800.00"},
        )
        self.assertIn("saldo=4800.00", prompt)

    def test_modo_desconhecido_gera_erro(self):
        with self.assertRaises(ValueError):
            montar_system_prompt("CREDITO_COMPARACAO", {})


if __name__ == "__main__":
    unittest.main()
