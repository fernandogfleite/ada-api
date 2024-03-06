from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
)
from django.db import models

import uuid


class Base(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if email is None:
            raise TypeError('Users must have an email address.')

        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email, password):
        if password is None:
            raise TypeError('Superusers must have a password.')

        user = self.create_user(email, password)
        user.is_superuser = True
        user.is_staff = True
        user.is_confirmed = True
        user.save()

        return user


class StudentManager(models.Manager):
    def create_student(self, email, name, password, registration_id):
        user = User.objects.create_user(email, password)
        user.name = name
        user.is_confirmed = False
        user.save()

        student = self.model(user=user, registration_id=registration_id)
        student.save()

        UserConfirmation.objects.create(user=user, token=str(uuid.uuid4()))

        return student


class TeacherManager(models.Manager):
    def create_teacher(self, email, name, password):
        user = User.objects.create_user(email, password)
        user.name = name
        user.is_confirmed = False
        user.save()

        teacher = self.model(user=user)
        teacher.save()

        UserConfirmation.objects.create(user=user, token=str(uuid.uuid4()))

        return teacher


class SecreataryManager(models.Manager):
    def create_secretary(self, email, name, password):
        user = User.objects.create_user(email, password)
        user.name = name
        user.is_confirmed = False
        user.save()

        secretary = self.model(user=user)
        secretary.save()

        UserConfirmation.objects.create(user=user, token=str(uuid.uuid4()))

        return secretary


class User(Base, AbstractBaseUser, PermissionsMixin):
    username = None
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255, blank=True)
    is_confirmed = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email

    class Meta:
        db_table = 'users'
        ordering = ['created_at']
        verbose_name = 'user'
        verbose_name_plural = 'users'

    @property
    def is_student(self):
        return Student.objects.filter(user=self).exists()

    @property
    def is_teacher(self):
        return Teacher.objects.filter(user=self).exists()

    @property
    def is_secretary(self):
        return Secretary.objects.filter(user=self).exists()

    @property
    def student(self):
        if self.is_student:
            return Student.objects.get(user=self)
        return None

    @property
    def teacher(self):
        if self.is_teacher:
            return Teacher.objects.get(user=self)
        return None

    @property
    def secretary(self):
        if self.is_secretary:
            return Secretary.objects.get(user=self)
        return None

    @property
    def child(self):
        if self.is_student:
            return self.student

        if self.is_teacher:
            return self.teacher

        if self.is_secretary:
            return self.secretary

        return None


class Student(Base):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True)
    registration_id = models.CharField(max_length=255, unique=True)

    objects = StudentManager()

    def __str__(self):
        return f"Student - {self.user.name} - {self.registration_id}"

    class Meta:
        db_table = 'students'
        ordering = ['created_at']
        verbose_name = 'student'
        verbose_name_plural = 'students'


class Teacher(Base):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True)

    objects = TeacherManager()

    def __str__(self):
        return f"Teacher - {self.user.name}"

    class Meta:
        db_table = 'teachers'
        ordering = ['created_at']
        verbose_name = 'teacher'
        verbose_name_plural = 'teachers'


class Secretary(Base):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True)

    objects = SecreataryManager()

    def __str__(self):
        return f"Secretary - {self.user.name}"

    class Meta:
        db_table = 'secretaries'
        ordering = ['created_at']
        verbose_name = 'secretary'
        verbose_name_plural = 'secretaries'


class UserConfirmation(Base):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=255)

    class Meta:
        db_table = 'user_confirmations'
        ordering = ['created_at']
        verbose_name = 'user confirmation'
        verbose_name_plural = 'user confirmations'
