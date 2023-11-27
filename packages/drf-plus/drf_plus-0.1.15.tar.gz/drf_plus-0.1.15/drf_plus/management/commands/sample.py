import os
import pkg_resources
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = (
        "새로운 앱을 생성합니다.\n"
        "사용법: python manage.py sample <파일명>\n"
        "예시: python manage.py startapp views"
    )
    missing_args_message = "원하시는 샘플 파일명을 입력해주세요."

    def add_arguments(self, parser):
        # 필요한 인자 추가
        parser.add_argument('filename', type=str, help='생성할 파일명')

    def handle(self, *args, **options):
        filename = options['filename']
        sample_folder = 'files/sample'  # 샘플 파일이 위치한 폴더명

        try:
            # pkg_resources를 이용하여 파일 경로 찾기
            sample_file_path = pkg_resources.resource_filename(__name__, os.path.join(sample_folder, filename))

            # 파일이 존재하는지 확인
            if not os.path.exists(sample_file_path):
                raise CommandError(f"'{filename}' 파일을 찾을 수 없습니다.")

            # 새 파일 생성
            with open(sample_file_path, 'r') as sample_file:
                content = sample_file.read()

            new_file_path = os.path.join(os.getcwd(), filename)
            with open(new_file_path, 'w') as new_file:
                new_file.write(content)

            self.stdout.write(self.style.SUCCESS(f"'{new_file_path}' 파일이 성공적으로 생성되었습니다."))

        except Exception as e:
            raise CommandError(f"파일 생성 중 오류가 발생했습니다: {e}")
