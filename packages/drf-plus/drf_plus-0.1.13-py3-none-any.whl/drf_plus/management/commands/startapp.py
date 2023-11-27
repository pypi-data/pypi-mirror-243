import os
import pkg_resources

from django.core.management import CommandError
from django.core.management.templates import TemplateCommand


class Command(TemplateCommand):
    help = (
        "새로운 앱을 생성합니다.\n"
        "사용법: python manage.py startapp <앱이름>\n"
        "예시: python manage.py startapp abcd"
    )
    missing_args_message = "앱 이름을 입력해주세요."

    def handle(self, **options):
        app_name = options.pop("name")
        self._create_app(app_name=app_name, template_name="app_template", **options)

    def _create_app(self, app_name, template_name, **options):
        target = f"app/{app_name}" if os.path.exists("app") else app_name
        top_dir = os.path.abspath(os.path.expanduser(target))
        try:
            self._make_dirs(top_dir)
            template_path = pkg_resources.resource_filename(
                "drf_plus", os.path.join("management", template_name)
            )
            options["template"] = "file://" + str(template_path)
            super().handle("app", app_name, target, **options)
        except CommandError as e:
            self.stderr.write(f'"{app_name}" 생성간 오류가 발생했습니다.\n=> {e}')

    @staticmethod
    def _make_dirs(top_dir):
        try:
            os.makedirs(top_dir)
        except FileExistsError:
            raise CommandError("'%s' 앱이 이미 존재합니다." % top_dir)
        except OSError as e:
            raise CommandError(f"'{top_dir}' 디렉토리를 생성할 수 없습니다.\n=> {e}")
