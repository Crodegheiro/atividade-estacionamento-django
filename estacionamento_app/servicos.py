from .models import VagaOcupada
from .excecoes import VeiculoNaoEncontradoError


def registrar_saida(placa):
    placa_normalizada = placa.strip().upper().replace("-", "")

    ocupacao = (
        VagaOcupada.objects
        .filter(veiculo__placa=placa_normalizada)
        .order_by("data_entrada", "pk")
        .first()
    )

    if ocupacao is None:
        raise VeiculoNaoEncontradoError(
            f"Não existe ocupação ativa para a placa {placa_normalizada}."
        )

    ocupacao.delete()

    return placa_normalizada