from django.db import models
from django.contrib.auth.models import  AbstractUser , BaseUserManager, PermissionsMixin


class CustomUserManager(BaseUserManager):
    def create_user(self,username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('El correo electrónico es obligatorio')
        email = self.normalize_email(email)
        user = self.model( username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Los superusuarios deben tener is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Los superusuarios deben tener is_superuser=True.')

        return self.create_user(username=username, email=email, password=password, **extra_fields)


class Skill(models.Model):
    name = models.CharField(max_length=100)


    def __str__(self):
        return self.name

class Badge(models.Model):
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class CustomUser(AbstractUser, PermissionsMixin):
    ROLE_CHOICESD = [ 
        ('ADMIN', 'Administrador'),
        ('GERENTE', 'Gerente'),
        ('EMPLEADO', 'Empleado'),
    ]

    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    role = models.CharField(max_length=10, choices=ROLE_CHOICESD, default='EMPLEADO')
   
    skill = models.ManyToManyField(Skill , blank=True) 
    badges = models.ManyToManyField(Badge, blank=True)

    assigned_banca = models.CharField(max_length=255, blank=True, null=True)
    access_level = models.CharField(max_length=50, blank=True, null=True)    
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return f"{self.email} ({self.get_role_display()})"
    

    def get_initials(self):
        first_name = self.first_name or ""
        last_name = self.last_name or ""
        initials = (first_name[:1] + last_name[:1]).upper()

        return initials




class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    biography = models.TextField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    linkedin_profile = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"Profile of {self.user.username}"