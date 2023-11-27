import os

import pkg_resources
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = (
        "새로운 앱을 생성합니다.\n"
        "사용법: python manage.py sample <키워드>\n"
        "예시: python manage.py sample conf"
    )
    missing_args_message = "원하시는 키워드를 입력해주세요."

    # 파일 매퍼 정의
    MAPPER = {
        "conf": ["settings.py"],
        "app": ["apps.py", "models.py", "serializers.py", "views.py"],
    }

    def add_arguments(self, parser):
        parser.add_argument("name", type=str, help="생성할 키워드")

    def _create_file(self, name):
        """파일 생성"""
        sample_folder = "files/sample"
        try:
            # pkg_resources를 이용하여 파일 경로 찾기
            sample_file_path = pkg_resources.resource_filename(
                __name__, os.path.join(sample_folder, name)
            )
            # 파일이 존재하는지 확인
            if not os.path.exists(sample_file_path):
                raise CommandError(f"'{name}' 파일을 찾을 수 없습니다.")
            # 새 파일 생성
            with open(sample_file_path, "r") as sample_file:
                content = sample_file.read()
            new_file_path = os.path.join(os.getcwd(), name)
            with open(new_file_path, "w") as new_file:
                new_file.write(content)
            self.stdout.write(
                self.style.SUCCESS(f"'{new_file_path}' 파일이 성공적으로 생성되었습니다.")
            )
        except Exception as e:
            raise CommandError(f"파일 생성 중 오류가 발생했습니다: {e}")

    def _create_folder(self, name):
        """폴더 생성"""
        sample_folder = "files/sample"
        output_folder = os.path.join(os.getcwd(), "sample", name)
        if name not in self.MAPPER:
            raise CommandError(f"'{name}'에 해당하는 파일이 없습니다.")
        file_list = self.MAPPER[name]
        os.makedirs(output_folder, exist_ok=True)
        try:
            for filename in file_list:
                sample_file_path = pkg_resources.resource_filename(
                    "drf_plus", os.path.join(sample_folder, filename)
                )
                if not os.path.exists(sample_file_path):
                    raise CommandError(f"'{filename}' 파일을 찾을 수 없습니다.")
                with open(sample_file_path, "r") as sample_file:
                    content = sample_file.read()
                new_file_path = os.path.join(output_folder, filename)
                with open(new_file_path, "w") as new_file:
                    new_file.write(content)
            self.stdout.write(self.style.SUCCESS(f"'{name}' 폴더가 성공적으로 생성되었습니다."))
        except Exception as e:
            raise CommandError(f"파일 생성 중 오류가 발생했습니다: {e}")

    def handle(self, *args, **options):
        name = options["name"]
        if name in self.MAPPER:
            self._create_folder(name)
        if ".py" in name:
            self._create_file(name)
        raise CommandError(f"'{name}'에 해당하는 파일이 없습니다.")
