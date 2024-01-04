from django.db import models
from django.core.validators import (
    MinValueValidator,
    MinLengthValidator,
    MaxLengthValidator,
)

# Entidade Candidato


class Candidato(models.Model):
    nome = models.CharField(
        verbose_name="Nome", max_length=100, null=False, blank=False
    )

    numero = models.CharField(
        verbose_name="Número",
        unique=True,
        null=False,
        blank=False,
        max_length=2,
        validators=[MinLengthValidator(2)]
    )

    partido = models.CharField(
        verbose_name="Partido", max_length=50, null=False, blank=False
    )

    votos = models.IntegerField(
        validators=[MinValueValidator(0)], default=0, null=False
    )

    def adicionarVoto(self):
        self.votos += 1
        self.save()


# Entidade Eleitor


class Eleitor(models.Model):
    nome = models.CharField(
        verbose_name="Nome", max_length=100, null=False, blank=False
    )

    tituloEleitor = models.CharField(
        verbose_name="Titulo de Eleitor",
        unique=True,
        null=False,
        blank=False,
        max_length=14,
        validators=[MinLengthValidator(2)],
    )

    voto = models.CharField(max_length=100, null=False)

    def adicionarVoto(self, voto):
        self.voto = voto
        self.save()

