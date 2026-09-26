import unittest
import tempfile
from pathlib import Path
from decimal import Decimal

from src.core import (
    carregar_perfil,
    validar_perfil,
    carregar_transacoes,
    carregar_compromissos,
    carregar_propostas,
    somar_movimentos,
    avaliar_reserva,
    projetar_caixa,
)


class TestCore(unittest.TestCase):

    def test_carregar_perfil_retorna_dict(self):
        perfil = carregar_perfil(Path("data/perfil_mei.json"))

        self.assertIsInstance(perfil, dict)

    def test_validar_perfil_completo_sem_erros(self):
        perfil = carregar_perfil(Path("data/perfil_mei.json"))

        erros = validar_perfil(perfil)

        self.assertEqual(erros, [])

    def test_validar_perfil_detecta_campo_ausente(self):
        perfil = carregar_perfil(Path("data/perfil_mei.json"))
        perfil.pop("regime")

        erros = validar_perfil(perfil)

        self.assertIn(
            "Campo obrigatório ausente: regime",
            erros,
        )

    def test_transacao_valor_e_decimal(self):
        transacoes = carregar_transacoes(Path("data/transacoes.csv"))

        self.assertIsInstance(
            transacoes[0]["valor"],
            Decimal,
        )

    def test_transacoes_preservam_pendente(self):
        transacoes = carregar_transacoes(Path("data/transacoes.csv"))

        pendentes = [
            transacao
            for transacao in transacoes
            if transacao["classe_esperada"] == "PENDENTE"
        ]

        self.assertEqual(len(pendentes), 3)
        self.assertTrue(
            all(
                transacao["classe_esperada"] == "PENDENTE"
                for transacao in pendentes
            )
        )

    def test_compromisso_valor_e_decimal(self):
        compromissos = carregar_compromissos(Path("data/compromissos.csv"))

        self.assertIsInstance(
            compromissos[0]["valor"],
            Decimal,
        )

    def test_proposta_tipos_convertidos(self):
        proposta = carregar_propostas(
            Path("data/propostas_credito.csv")
        )[0]

        self.assertIsInstance(proposta["valor_financiado"], Decimal)
        self.assertIsInstance(proposta["valor_parcela"], Decimal)
        self.assertIsInstance(proposta["total_pago"], Decimal)
        self.assertIsInstance(proposta["custo_adicional"], Decimal)
        self.assertIsInstance(proposta["numero_parcelas"], int)
        self.assertIsInstance(proposta["dia_primeiro_vencimento"], int)

    def test_transacoes_cabecalho_ausente_gera_value_error(self):
        conteudo = "data,descricao,tipo_movimento,classe_esperada,observacao\n"

        with tempfile.TemporaryDirectory() as pasta:
            caminho = Path(pasta) / "transacoes.csv"
            caminho.write_text(conteudo, encoding="utf-8")

            with self.assertRaises(ValueError) as contexto:
                carregar_transacoes(caminho)

            self.assertIn("valor", str(contexto.exception))

    def test_compromissos_cabecalho_ausente_gera_value_error(self):
        conteudo = "data_prevista,descricao,tipo_movimento,classe_esperada,observacao\n"

        with tempfile.TemporaryDirectory() as pasta:
            caminho = Path(pasta) / "compromissos.csv"
            caminho.write_text(conteudo, encoding="utf-8")

            with self.assertRaises(ValueError) as contexto:
                carregar_compromissos(caminho)

            self.assertIn("valor", str(contexto.exception))

    def test_propostas_cabecalho_ausente_gera_value_error(self):
        conteudo = (
            "proposta_id,valor_financiado,numero_parcelas,total_pago,"
            "custo_adicional,dia_primeiro_vencimento,caracteristica\n"
        )

        with tempfile.TemporaryDirectory() as pasta:
            caminho = Path(pasta) / "propostas_credito.csv"
            caminho.write_text(conteudo, encoding="utf-8")

            with self.assertRaises(ValueError) as contexto:
                carregar_propostas(caminho)

            self.assertIn("valor_parcela", str(contexto.exception))

    def test_json_invalido_gera_value_error(self):
        with tempfile.TemporaryDirectory() as pasta:
            caminho = Path(pasta) / "perfil.json"
            caminho.write_text('{"nome": ', encoding="utf-8")

            with self.assertRaises(ValueError):
                carregar_perfil(caminho)

    def test_perfil_campos_monetarios_sao_decimal(self):
        perfil = carregar_perfil(Path("data/perfil_mei.json"))

        campos = [
            "faturamento_medio_mensal",
            "saldo_empresarial_inicial",
            "retirada_pessoal_habitual_mensal",
            "reserva_operacional_minima",
        ]

        for campo in campos:
            self.assertIsInstance(perfil[campo], Decimal)

    def test_perfil_aquisicao_valor_e_decimal(self):
        perfil = carregar_perfil(Path("data/perfil_mei.json"))

        self.assertIsInstance(
            perfil["aquisicao_simulada"]["valor"],
            Decimal,
        )

    def test_somar_movimentos_compromissos_resulta_cinquenta(self):
        compromissos = carregar_compromissos(Path("data/compromissos.csv"))

        total = somar_movimentos(compromissos)

        self.assertEqual(total, Decimal("50.00"))

    def test_avaliar_reserva_detecta_gap(self):
        resultado = avaliar_reserva(
            Decimal("3000.00"),
            Decimal("3500.00"),
        )

        self.assertEqual(resultado["status"], "ABAIXO_DA_RESERVA")
        self.assertEqual(resultado["gap"], Decimal("500.00"))

    def test_avaliar_reserva_preservada_tem_gap_zero(self):
        resultado = avaliar_reserva(
            Decimal("4070.00"),
            Decimal("3500.00"),
        )

        self.assertEqual(resultado["status"], "RESERVA_PRESERVADA")
        self.assertEqual(resultado["gap"], Decimal("0"))

    def test_projetar_caixa_sem_credito(self):
        perfil = carregar_perfil(Path("data/perfil_mei.json"))
        compromissos = carregar_compromissos(Path("data/compromissos.csv"))

        resultado = projetar_caixa(
            perfil["saldo_empresarial_inicial"],
            compromissos,
            perfil["reserva_operacional_minima"],
        )

        self.assertEqual(resultado["saldo_final"], Decimal("4850.00"))
        self.assertEqual(resultado["menor_caixa"], Decimal("4070.00"))
        self.assertEqual(
            resultado["status_reserva"],
            "RESERVA_PRESERVADA",
        )
        self.assertEqual(resultado["gap_reserva"], Decimal("0"))

    def test_projetar_caixa_proposta_a(self):
        perfil = carregar_perfil(Path("data/perfil_mei.json"))
        compromissos = carregar_compromissos(Path("data/compromissos.csv"))
        proposta = carregar_propostas(Path("data/propostas_credito.csv"))[0]

        resultado = projetar_caixa(
            perfil["saldo_empresarial_inicial"],
            compromissos,
            perfil["reserva_operacional_minima"],
            proposta,
        )

        self.assertEqual(resultado["saldo_final"], Decimal("3780.00"))
        self.assertEqual(resultado["menor_caixa"], Decimal("3000.00"))
        self.assertEqual(resultado["status_reserva"], "ABAIXO_DA_RESERVA")
        self.assertEqual(resultado["gap_reserva"], Decimal("500.00"))

    def test_projetar_caixa_proposta_b(self):
        perfil = carregar_perfil(Path("data/perfil_mei.json"))
        compromissos = carregar_compromissos(Path("data/compromissos.csv"))
        proposta = carregar_propostas(Path("data/propostas_credito.csv"))[1]

        resultado = projetar_caixa(
            perfil["saldo_empresarial_inicial"],
            compromissos,
            perfil["reserva_operacional_minima"],
            proposta,
        )

        self.assertEqual(resultado["saldo_final"], Decimal("3740.00"))
        self.assertEqual(resultado["menor_caixa"], Decimal("3740.00"))
        self.assertEqual(
            resultado["status_reserva"],
            "RESERVA_PRESERVADA",
        )
        self.assertEqual(resultado["gap_reserva"], Decimal("0"))

    def test_projetar_caixa_proposta_c(self):
        perfil = carregar_perfil(Path("data/perfil_mei.json"))
        compromissos = carregar_compromissos(Path("data/compromissos.csv"))
        proposta = carregar_propostas(Path("data/propostas_credito.csv"))[2]

        resultado = projetar_caixa(
            perfil["saldo_empresarial_inicial"],
            compromissos,
            perfil["reserva_operacional_minima"],
            proposta,
        )

        self.assertEqual(resultado["saldo_final"], Decimal("4230.00"))
        self.assertEqual(resultado["menor_caixa"], Decimal("4070.00"))
        self.assertEqual(
            resultado["status_reserva"],
            "RESERVA_PRESERVADA",
        )
        self.assertEqual(resultado["gap_reserva"], Decimal("0"))

    def test_somar_movimentos_nao_inverte_saida_assinada(self):
        movimentos = [
            {
                "valor": Decimal("-80.00"),
                "tipo_movimento": "saida",
            }
        ]

        total = somar_movimentos(movimentos)

        self.assertEqual(total, Decimal("-80.00"))

    def test_projecao_preserva_classe_pendente(self):
        perfil = carregar_perfil(Path("data/perfil_mei.json"))
        compromissos = carregar_compromissos(Path("data/compromissos.csv"))

        pendente = next(
            item
            for item in compromissos
            if item["classe_esperada"] == "PENDENTE"
        )

        projetar_caixa(
            perfil["saldo_empresarial_inicial"],
            compromissos,
            perfil["reserva_operacional_minima"],
        )

        self.assertEqual(pendente["classe_esperada"], "PENDENTE")
        self.assertEqual(pendente["valor"], Decimal("-120.00"))

    def test_caracteristica_proposta_nao_altera_projecao(self):
        perfil = carregar_perfil(Path("data/perfil_mei.json"))
        compromissos = carregar_compromissos(Path("data/compromissos.csv"))
        proposta = carregar_propostas(Path("data/propostas_credito.csv"))[0]

        resultado_original = projetar_caixa(
            perfil["saldo_empresarial_inicial"],
            compromissos,
            perfil["reserva_operacional_minima"],
            proposta,
        )

        proposta["caracteristica"] = "TEXTO ALTERADO SEM EFEITO MATEMÁTICO"

        resultado_alterado = projetar_caixa(
            perfil["saldo_empresarial_inicial"],
            compromissos,
            perfil["reserva_operacional_minima"],
            proposta,
        )

        self.assertEqual(resultado_original, resultado_alterado)

if __name__ == "__main__":
    unittest.main()