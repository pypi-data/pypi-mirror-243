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

    FILE_MAPPER = {
        "conf": {
            "settings.py",
        },
        "app": {
            "apps.py",
            "models.py",
            {
                "v1": {
                    "serializers.py",
                    "views.py",
                }
            }
        }
    }

    def add_arguments(self, parser):
        parser.add_argument("name", type=str, help="생성할 키워드")

    def handle(self, *args, **options):
        name = options["name"]
        sample_folder = "files/sample"
        output_folder = os.path.join(os.getcwd(), "sample", name)

        if name not in self.FILE_MAPPER:
            raise CommandError(f"'{name}'에 해당하는 파일이나 폴더가 없습니다.")

        try:
            self.create_files(name, self.FILE_MAPPER[name], sample_folder, output_folder)
            self.stdout.write(self.style.SUCCESS(f"'{name}'에 대한 파일 생성이 완료되었습니다."))
        except Exception as e:
            raise CommandError(f"파일 생성 중 오류가 발생했습니다: {e}")

    def create_files(self, name, file_list, sample_folder, output_folder):
        for item in file_list:
            if isinstance(item, set):
                for sub_name, sub_files in item.items():
                    sub_sample_folder = os.path.join(sample_folder, name, sub_name)
                    sub_output_folder = os.path.join(output_folder, sub_name)
                    os.makedirs(sub_output_folder, exist_ok=True)
                    self.create_files(sub_name, sub_files, sub_sample_folder, sub_output_folder)
            else:
                filename = item
                sample_file_path = pkg_resources.resource_filename("drf_plus", os.path.join(sample_folder, name, filename))
                if not os.path.exists(sample_file_path):
                    raise CommandError(f"'{filename}' 파일을 찾을 수 없습니다.")

                with open(sample_file_path, "r") as sample_file:
                    content = sample_file.read()
                new_file_path = os.path.join(output_folder, filename)
                with open(new_file_path, "w") as new_file:
                    new_file.write(content)
