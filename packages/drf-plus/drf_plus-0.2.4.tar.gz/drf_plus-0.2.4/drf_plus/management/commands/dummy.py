import random

from django.core.management.base import BaseCommand

from django.apps import apps
from django.db.models import ForeignKey
from django_seed import Seed


class Command(BaseCommand):
    help = f"이 명령은 입력 받은 모델의 더미 데이터를 만듭니다. ex) app_name.model_name"

    def get_seed_data(self, app_name, model_name, number):
        seeder = Seed.seeder()
        model = apps.get_model(app_label=app_name, model_name=model_name)
        fk_list = [
            (field.name, field.related_model)
            for field in model._meta.get_fields()
            if isinstance(field, ForeignKey)
        ]

        for _ in range(number):
            fk = {}
            for field_name, related_model in fk_list:
                fk[field_name] = random.choice(related_model.objects.all())
            seeder.add_entity(model, 1, fk)
        seeder.execute()

    def add_arguments(self, parser):
        parser.add_argument("model", type=str, help=f"모델을 입력하세요")
        parser.add_argument(
            "--number", "-n", default=10, type=int, help=f"몇개의 데이터를 생성 하시겠습니까?"
        )

    def handle(self, *args, **options):
        app_name, model_name = options["model"].split(".")
        number = options.get("number")

        self.get_seed_data(app_name, model_name, number)
        self.stdout.write(self.style.SUCCESS(f"{number} {model_name} 생성!"))
