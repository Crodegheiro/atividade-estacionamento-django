from django.db import models


VAGAS_TOTAIS = 10


class Veiculo(models.Model):
    placa = models.CharField(max_length=10, unique=True)
    modelo = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.placa} - {self.modelo}"


class VagaOcupada(models.Model):
    veiculo = models.ForeignKey(
        Veiculo,
        on_delete=models.CASCADE
    )
    data_entrada = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            vagas_ocupadas = VagaOcupada.objects.count()

            if vagas_ocupadas >= VAGAS_TOTAIS:
                raise ValueError("Não há vagas disponíveis.")

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.veiculo} - Entrada: {self.data_entrada}"