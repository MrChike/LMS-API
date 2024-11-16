from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.hashers import make_password, check_password
from django.db import models
import uuid

class MemberRole(models.TextChoices):
    ADMIN = 'ADMIN'
    TEACHER = 'TEACHER'
    STUDENT = 'STUDENT'


class ProfileManager(BaseUserManager):
    def create_user(self, user_id, first_name, last_name, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(user_id=user_id, first_name=first_name, last_name=last_name, email=email, **extra_fields)
        
        if password:
            user.set_password(password)  # Ensures password is hashed

        user.save(using=self._db)
        return user

    def create_superuser(self, user_id, first_name, last_name, email, password=None, **extra_fields):
        extra_fields.setdefault('role', MemberRole.ADMIN)
        return self.create_user(user_id, first_name, last_name, email, password, **extra_fields)


class Profile(AbstractBaseUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.CharField(max_length=255, unique=True, db_column='userId')
    first_name = models.CharField(max_length=255, db_column='firstName')
    last_name = models.CharField(max_length=255, db_column='lastName')
    phone = models.CharField(max_length=20)
    image_url = models.URLField(blank=True, null=True, db_column='imageUrl')
    email = models.EmailField(unique=True)

    role = models.CharField(
        max_length=20,
        choices=MemberRole.choices,
        default=MemberRole.STUDENT
    )
    created_at = models.DateTimeField(auto_now_add=True, db_column='createdAt')
    updated_at = models.DateTimeField(auto_now=True, db_column='updatedAt')
    last_login = models.DateTimeField(auto_now=True, null=True, db_column='lastLogin')
    is_staff = models.BooleanField(default=True, db_column='isStaff')

    objects = ProfileManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['user_id', 'first_name', 'last_name']

    class Meta:
        managed = False
        db_table = 'Profile'

    def set_password(self, raw_password):
        """Override to hash the password before saving"""
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        """Override to check password hash"""
        return check_password(raw_password, self.password)

    def has_module_perms(self, app_label):
        # Custom implementation if needed
        return True  # For example purposes

    def has_perm(self, perm, obj=None):
        # Custom permission check
        return True
        

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Course(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.CharField(max_length=255, db_column='userId')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    image_url = models.URLField(blank=True, null=True, db_column='imageUrl')
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    is_published = models.BooleanField(default=False, db_column='isPublished')

    category = models.ForeignKey('Category', related_name='courses', on_delete=models.SET_NULL, null=True, blank=True, db_column='categoryId')
    attachments = models.ManyToManyField('Attachment', related_name='courses')
    chapters = models.ManyToManyField('Chapter', related_name='courses')
    purchases = models.ManyToManyField('Purchase', related_name='courses')

    created_at = models.DateTimeField(auto_now_add=True, db_column='createdAt')
    updated_at = models.DateTimeField(auto_now=True, db_column='updatedAt')

    class Meta:
        managed = False
        db_table = 'Course'

    def __str__(self):
        return self.title

class Attachment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    url = models.URLField()
    course = models.ForeignKey(Course, related_name='CourseId', on_delete=models.CASCADE, db_column='courseId')
    created_at = models.DateTimeField(auto_now_add=True, db_column='createdAt')
    updated_at = models.DateTimeField(auto_now=True, db_column='updatedAt')

    class Meta:
        managed = False
        db_table = 'Attachment'

    def __str__(self):
        return self.name

class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True, db_column='createdAt')
    updated_at = models.DateTimeField(auto_now=True, db_column='updatedAt')

    class Meta:
        managed = False
        db_table = 'Category'

    def __str__(self):
        return self.name

class Chapter(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    video_url = models.URLField(blank=True, null=True, db_column='videoUrl')
    position = models.IntegerField()
    is_published = models.BooleanField(default=False, db_column='isPublished')
    is_free = models.BooleanField(default=False, db_column='isFree')
    course = models.ForeignKey(Course, related_name='course_chapters', on_delete=models.CASCADE, db_column='courseId')
    user_progress = models.ManyToManyField('UserProgress', related_name='user_progress_chapter', db_column='userProgress')

    created_at = models.DateTimeField(auto_now_add=True, db_column='createdAt')
    updated_at = models.DateTimeField(auto_now=True, db_column='updatedAt')

    class Meta:
        managed = False
        db_table = 'Chapter'

    def __str__(self):
        return self.title

class MuxData(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    asset_id = models.CharField(max_length=255, db_column='assetId')
    playback_id = models.CharField(max_length=255, blank=True, null=True, db_column='playbackId')

    chapter = models.OneToOneField(Chapter, related_name='mux_data_chapter', on_delete=models.CASCADE, db_column='chapterId')

    class Meta:
        managed = False
        db_table = 'MuxData'

    def __str__(self):
        return self.asset_id

class UserProgress(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.CharField(max_length=255, db_column='userId')
    chapter = models.ForeignKey(Chapter, related_name='user_progress_chapter', on_delete=models.CASCADE, db_column='chapterId')
    is_completed = models.BooleanField(default=False, db_column='isCompleted')

    created_at = models.DateTimeField(auto_now_add=True, db_column='createdAt')
    updated_at = models.DateTimeField(auto_now=True, db_column='updatedAt')

    class Meta:
        unique_together = ('user_id', 'chapter')
        managed = False    
        db_table = 'UserProgress'

    def __str__(self):
        return f"Progress of {self.user_id} in {self.chapter.title}"

class Purchase(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.CharField(max_length=255, db_column='userId')
    course = models.ForeignKey(Course, related_name='course_purchases', on_delete=models.CASCADE, db_column='courseId')

    created_at = models.DateTimeField(auto_now_add=True, db_column='createdAt')
    updated_at = models.DateTimeField(auto_now=True, db_column='updatedAt')

    class Meta:
        unique_together = ('user_id', 'course')
        managed = False    
        db_table = 'Purchase'

    def __str__(self):
        return f"{self.user_id} purchased {self.course.title}"

class StripeCustomer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.CharField(max_length=255, unique=True, db_column='userId')
    stripe_customer_id = models.CharField(max_length=255, unique=True, db_column='stripeCustomerId')

    created_at = models.DateTimeField(auto_now_add=True, db_column='createdAt')
    updated_at = models.DateTimeField(auto_now=True, db_column='updatedAt')

    class Meta:
        managed = False
        db_table = 'StripeCustomer'

    def __str__(self):
        return f"Stripe Customer: {self.stripe_customer_id}"

class Logging(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    url = models.URLField()
    method = models.CharField(max_length=10)
    body = models.TextField(blank=True, null=True)
    response = models.TextField(blank=True, null=True)
    status_code = models.IntegerField(blank=True, null=True, db_column='statusCode')
    error_message = models.TextField(blank=True, null=True, db_column='errorMessage')
    created_at = models.DateTimeField(auto_now_add=True, db_column='createdAt')

    class Meta:
        managed = False
        db_table = 'Logging'

    def __str__(self):
        return f"Log {self.id} for {self.url}"

