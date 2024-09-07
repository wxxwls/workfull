from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin
from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone  # 현재 시간 사용을 위한 임포트
class MyUserManager(BaseUserManager):
    def create_user(self, id, email, password=None, **extra_fields):
        """
        일반 유저 생성 메서드
        """
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(id=id, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, id, email, password=None, **extra_fields):
        """
        관리자 유저 생성 메서드
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(id, email, password, **extra_fields)


class MyUser(AbstractUser):
    GENDER_CHOICES = [
        ('M', '남자'),
        ('F', '여자'),
    ]
    
    # 사용자 정의 필드
    id = models.CharField(max_length=10, unique=True, primary_key=True)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=30)  # 사용자 이름
    birth_date = models.DateField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    phone_number = models.CharField(max_length=15)
    
    # 기본 AbstractUser 필드들
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='myuser_set',  # related_name 추가
        blank=True,
        help_text=('The groups this user belongs to. A user will get all permissions '
                   'granted to each of their groups.'),
        related_query_name='user',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='myuser_set', 
        blank=True,
        help_text='Specific permissions for this user.',
        related_query_name='user',
    )

    objects = MyUserManager()

    USERNAME_FIELD = 'id'  # 사용자 식별 필드
    REQUIRED_FIELDS = ['email', 'username', 'birth_date', 'gender', 'phone_number']  # 필수 필드 설정

    def __str__(self):
        return self.id
    


class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    like_count = models.IntegerField(default=0)  # 좋아요 수를 저장하는 필드
    created_at = models.DateTimeField(default=timezone.now)  # 게시물 생성 시각 필드 추가, 기본값은 현재 시간

class PostLike(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')

class qna(models.Model):
    title1 = models.CharField(max_length=100)
    content1 = models.TextField()
    title2 = models.CharField(max_length=100)
    content2 = models.TextField()
    title3 = models.CharField(max_length=100)
    content3 = models.TextField()
    title4 = models.CharField(max_length=100)
    content4 = models.TextField()
    title5 = models.CharField(max_length=100)
    content5 = models.TextField()

class InjuryApplication(models.Model):
    name = models.CharField(max_length=100)
    id_number = models.CharField(max_length=13)  # 주민등록번호 길이에 맞게 조정
    address = models.CharField(max_length=200)
    phone = models.CharField(max_length=15)
    start_time = models.TimeField()
    end_time = models.TimeField()
    job_type = models.CharField(max_length=100)
    
    relation_with_insured = models.CharField(max_length=50, choices=[
        ('none', '해당없음'),
        ('actual_employer', '실제사업주(동업자포함)'),
        ('sub_contractor', '하수급사업주')
    ])
    
    family_relation = models.CharField(max_length=50, choices=[
        ('none', '해당없음'),
        ('spouse', '배우자'),
        ('parent', '부모'),
        ('child', '자녀'),
        ('sibling', '형제자매'),
        ('other_relative', '기타친인척')
    ])
    
    application_type = models.CharField(max_length=50, choices=[
        ('work_accident', '업무상 사고'),
        ('work_disease', '업무상 질병'),
        ('commute_accident', '출퇴근 재해')
    ])
    
    business_name = models.CharField(max_length=100)
    business_owner_name = models.CharField(max_length=100)
    business_management_number = models.CharField(max_length=50)
    business_address = models.CharField(max_length=200)
    accident_description = models.TextField()

    # 체크박스 필드 추가
    checkbox_one = models.BooleanField(default=False)  # 체크박스 1
    checkbox_two = models.BooleanField(default=False)  # 체크박스 2
    checkbox_three = models.BooleanField(default=False)  # 체크박스 3

    # 목격자 정보
    witness_name = models.CharField(max_length=100, blank=True, null=True)
    witness_contact = models.CharField(max_length=15, blank=True, null=True)
    witness_relation = models.CharField(max_length=50, blank=True, null=True)

    # 수령 정보 여부 체크
    has_received_compensation = models.BooleanField(default=False, help_text="수령 여부")

    # 수령 정보
    receipt_date = models.DateField(blank=True, null=True)  # 수령일자
    receipt_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)  # 수령금액
    payment_source = models.CharField(max_length=100, blank=True, null=True)  # 지급처
    attached_documents = models.ImageField(upload_to='documents/', blank=True, null=True)  # 첨부서류 이미지

    



    def __str__(self):
        return f"{self.name} - {self.application_type}"