from django.test import TestCase

from .models import Veiculo, VagaOcupada
from .servicos import registrar_saida
from .excecoes import VeiculoNaoEncontradoError


class RegistrarSaidaTests(TestCase):

    def criar_ocupacao(self, placa="ABC1234"):
        veiculo = Veiculo.objects.create(
            placa=placa,
            modelo="Fiat Uno"
        )

        ocupacao = VagaOcupada.objects.create(
            veiculo=veiculo
        )

        return veiculo, ocupacao

    def test_saida_valida(self):
        veiculo, ocupacao = self.criar_ocupacao()

        resultado = registrar_saida("ABC1234")

        self.assertEqual(resultado, "ABC1234")
        self.assertFalse(
            VagaOcupada.objects.filter(pk=ocupacao.pk).exists()
        )
        self.assertTrue(
            Veiculo.objects.filter(pk=veiculo.pk).exists()
        )

    def test_placa_formatada(self):
        veiculo, ocupacao = self.criar_ocupacao()

        resultado = registrar_saida("abc-1234")

        self.assertEqual(resultado, "ABC1234")
        self.assertFalse(
            VagaOcupada.objects.filter(pk=ocupacao.pk).exists()
        )
        self.assertTrue(
            Veiculo.objects.filter(pk=veiculo.pk).exists()
        )

    def test_saida_inexistente(self):
        veiculos_antes = Veiculo.objects.count()
        ocupacoes_antes = VagaOcupada.objects.count()

        with self.assertRaises(VeiculoNaoEncontradoError):
            registrar_saida("XYZ9000")

        self.assertEqual(Veiculo.objects.count(), veiculos_antes)
        self.assertEqual(VagaOcupada.objects.count(), ocupacoes_antes)

    def test_segunda_saida(self):
        self.criar_ocupacao()

        registrar_saida("ABC1234")

        veiculos_antes = Veiculo.objects.count()
        ocupacoes_antes = VagaOcupada.objects.count()

        with self.assertRaises(VeiculoNaoEncontradoError):
            registrar_saida("ABC1234")

        self.assertEqual(Veiculo.objects.count(), veiculos_antes)
        self.assertEqual(VagaOcupada.objects.count(), ocupacoes_antes)