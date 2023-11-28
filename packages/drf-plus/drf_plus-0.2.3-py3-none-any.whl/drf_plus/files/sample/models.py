from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import UserManager as DjangoUserManager
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils import timezone
from encrypted_fields import fields


class UserManager(DjangoUserManager):
    """사용자 매니저"""

    def _create_user(self, email, password, **extra_fields):
        email = self.model.normalize_username(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        """사용자 생성"""
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser):
    """기본 사용자"""

    # 메인 필드
    email = models.EmailField(verbose_name="이메일", unique=True)
    # 기본 필드
    is_staff = models.BooleanField(verbose_name="스태프", default=False)
    is_superuser = models.BooleanField(verbose_name="슈퍼 유저 여부", default=False)
    is_active = models.BooleanField(verbose_name="활성화 여부", default=True)
    date_joined = models.DateTimeField(verbose_name="가입일", default=timezone.now)
    created_at = models.DateTimeField(verbose_name="생성일시", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="수정일시", auto_now=True)

    # 기본 설정
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    VERIFY_FIELDS = []
    REGISTER_FIELDS = ["password"]

    objects = UserManager()

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser

    class Meta:
        db_table = "users"
        verbose_name = "사용자"
        verbose_name_plural = verbose_name


class Profile(models.Model):
    """프로필"""

    user = models.OneToOneField(
        User, verbose_name="사용자", on_delete=models.CASCADE, related_name="profile"
    )
    name = fields.EncryptedCharField(verbose_name="이름", max_length=50)

    def __str__(self):
        return f"{self.user.email} - {self.name}"

    class Meta:
        db_table = "profiles"
        verbose_name = "프로필"
        verbose_name_plural = verbose_name


class SampleQuerySet(models.QuerySet):
    """샘플 쿼리셋"""

    def get_profile(self):
        return self.select_related("user__profile")


class SampleManager(models.Manager):
    """샘플 매니저"""

    def get_queryset(self):
        return SampleQuerySet(self.model, using=self._db)

    def get_profile(self):
        return self.get_queryset().get_profile()


class Sample(models.Model):
    """샘플 모델"""

    user = models.ForeignKey(
        User,
        verbose_name="사용자",
        on_delete=models.CASCADE,
        related_name="samples",
        db_column="user_id",
    )
    users = models.ManyToManyField(
        User,
        verbose_name="사용자 리스트",
        related_name="sample_list",
        db_table="sample_users",
    )

    class Meta:
        db_table = "sample"
        verbose_name = "샘플"
        verbose_name_plural = verbose_name


class AbstractSample(models.Model):
    """공통 필드 추상화 모델"""

    created_at = models.DateTimeField(auto_now_add=True, help_text="생성일시")
    updated_at = models.DateTimeField(auto_now=True, help_text="수정일시")

    class Meta:
        abstract = True


class ContentTypeSample(models.Model):
    """ContentType 모델"""

    help = """
    [ 문서 ]
    https://docs.djangoproject.com/en/4.2/ref/contrib/contenttypes/
    
    [ 예시 ]
    from django.contrib.contenttypes.models import ContentType
    user_type = ContentType.objects.get(app_label="auth", model="user")
    # <ContentType: user>
    user_type.model_class()
    # <class 'django.contrib.auth.models.User'>
    user_type.get_object_for_this_type(username="Guido")
    # <User: Guido>
    from django.contrib.auth.models import User
    ContentType.objects.get_for_model(User)
    # <ContentType: user>
    """

    tag = models.SlugField()
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    class Meta:
        indexes = [
            models.Index(fields=["content_type", "object_id"]),
        ]


def get_hash_key():
    # This must return a suitable string, eg from secrets.token_hex(32)
    return "f414ed6bd6fbc4aef5647abc15199da0f9badcc1d2127bde2087ae0d794a8a0a"


class EncryptSample(models.Model):
    """암호화 필드 모델"""

    help = """
    [ 설치 ]
    pip install django-searchable-encrypted-fields
    
    [ 설정 ]
    # in settings.py
    INSTALLED_APPS += ["encrypted_fields"]
    
    # A list of hex-encoded 32 byte keys
    # You only need one unless/until rotating keys
    FIELD_ENCRYPTION_KEYS = [
        "f164ec6bd6fbc4aef5647abc15199da0f9badcc1d2127bde2087ae0d794a9a0b"
    ]
    
    [ 예시 ]
    # "Jo" is hashed and stored in 'name' as well as symmetrically encrypted and stored in '_name_data'
    Person.objects.create(name="Jo", favorite_number=7, city="London")
    person = Person.objects.get(name="Jo")
    assert person.name == "Jo"
    assert person.favorite_number == 7
    
    person = Person.objects.get(city="London")
    assert person.name == "Jo" . # the data is taken from '_name_data', which decrypts it first.
    """

    _name_data = fields.EncryptedCharField(max_length=50, default="", null=True / False)
    name = fields.SearchField(hash_key=get_hash_key, encrypted_field_name="_name_data")
    favorite_number = fields.EncryptedIntegerField()
    city = models.CharField(max_length=255)
