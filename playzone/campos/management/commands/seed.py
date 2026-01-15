from __future__ import annotations

from decimal import Decimal

from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand
from django.db import transaction

from playzone.campos.models import Campo, Desporto


ADMIN_GROUP_NAME = "Admin"


DEFAULT_DESPORTOS = [
    "Futebol",
    "Ténis",
    "Padel",
    "Basquetebol",
    "Voleibol",
]

DEFAULT_CAMPOS = [
    # nome, preco_hora, estado, [desportos]
    ("Campo A", Decimal("25.00"), Campo.Estado.DISPONIVEL, ["Futebol"]),
    ("Campo B", Decimal("18.50"), Campo.Estado.DISPONIVEL, ["Ténis", "Padel"]),
    ("Campo C", Decimal("22.00"), Campo.Estado.MANUTENCAO, ["Basquetebol"]),
    ("Campo D", Decimal("15.00"), Campo.Estado.INATIVO, ["Voleibol"]),
]


class Command(BaseCommand):
    help = "Cria dados iniciais (desportos, campos) e grupo Admin. É idempotente."

    def add_arguments(self, parser):
        parser.add_argument(
            "--reset",
            action="store_true",
            help="Apaga campos e desportos antes de inserir novamente (CUIDADO).",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        reset = options["reset"]

        # 1) Grupo Admin
        group, created = Group.objects.get_or_create(name=ADMIN_GROUP_NAME)
        if created:
            self.stdout.write(self.style.SUCCESS(f"Grupo criado: {ADMIN_GROUP_NAME}"))
        else:
            self.stdout.write(f"Grupo já existe: {ADMIN_GROUP_NAME}")

        # 2) Reset opcional
        if reset:
            Campo.objects.all().delete()
            Desporto.objects.all().delete()
            self.stdout.write(self.style.WARNING("Reset efetuado: Campos e Desportos apagados."))

        # 3) Desportos
        desporto_objs = {}
        for nome in DEFAULT_DESPORTOS:
            obj, _ = Desporto.objects.get_or_create(nome=nome)
            desporto_objs[nome] = obj
        self.stdout.write(self.style.SUCCESS(f"Desportos garantidos: {len(desporto_objs)}"))

        # 4) Campos + M2M
        created_count = 0
        updated_count = 0

        for nome, preco, estado, desportos in DEFAULT_CAMPOS:
            campo, created = Campo.objects.get_or_create(
                nome=nome,
                defaults={"preco_hora": preco, "estado": estado},
            )
            if created:
                created_count += 1
            else:
                # mantém idempotência mas atualiza defaults caso tenham mudado
                changed = False
                if campo.preco_hora != preco:
                    campo.preco_hora = preco
                    changed = True
                if campo.estado != estado:
                    campo.estado = estado
                    changed = True
                if changed:
                    campo.save()
                    updated_count += 1

            campo.desportos.set([desporto_objs[d] for d in desportos])

        self.stdout.write(self.style.SUCCESS(f"Campos criados: {created_count} | atualizados: {updated_count}"))
        self.stdout.write(self.style.SUCCESS("Seed concluído com sucesso."))
