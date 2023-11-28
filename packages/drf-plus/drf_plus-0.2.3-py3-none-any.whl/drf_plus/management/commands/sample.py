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
        "conf": [
            "settings.py",
            "openapi.py",
            "router.py",
            "spectacular_hooks.py",
            "middleware.py",
            "backends.py",
        ],
        "app": [
            "apps.py",
            "admin.py",
            "models.py",
            "serializers.py",
            "views.py",
            "permissions.py",
            "filters.py",
            "signals.py",
            "migrations.py",
            "paginations.py",
            "tests.py",
        ],
    }

    def add_arguments(self, parser):
        parser.add_argument("name", type=str, help="생성할 키워드")

    def _copy_file(self, sample_file_path, new_file_path):
        """파일 복사를 위한 보조 함수"""
        if not os.path.exists(sample_file_path):
            raise CommandError(f"'{sample_file_path}' 파일을 찾을 수 없습니다.")
        with open(sample_file_path, "r") as sample_file:
            content = sample_file.read()
        with open(new_file_path, "w") as new_file:
            new_file.write(content)

    def _create_files(self, file_list, output_folder):
        """파일 또는 파일 리스트 생성"""
        os.makedirs(output_folder, exist_ok=True)
        for filename in file_list:
            sample_file_path = pkg_resources.resource_filename(
                "drf_plus", os.path.join("files/sample", filename)
            )
            new_file_path = os.path.join(output_folder, filename)
            self._copy_file(sample_file_path, new_file_path)
            self.stdout.write(
                self.style.SUCCESS(f"'{new_file_path}' 파일이 성공적으로 생성되었습니다.")
            )

    def handle(self, *args, **options):
        try:
            name = options["name"]
            if name in self.MAPPER:
                # 폴더와 해당 폴더에 속한 파일들 생성
                output_folder = os.path.join(os.getcwd(), "sample", name)
                self._create_files(self.MAPPER[name], output_folder)
            elif ".py" in name:
                # 단일 파일 생성
                self._create_files([name], os.path.join(os.getcwd(), "sample"))
            else:
                raise CommandError(f"'{name}'에 해당하는 파일이나 폴더가 없습니다.")
        except Exception as e:
            raise CommandError(e)
