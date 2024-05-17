# bellow are the list of classes that map data to teh database
from django.db import models
# Create your models here.
from django.contrib.auth.models import User
from django.conf import settings
from django.templatetags.static import static
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import AbstractBaseUser

GENDER_CHOICES = [
    ('Male', 'Male'),
    ('Female', 'Female'),
]
Race = [
    ('Asian', 'Asian'),
    ('Black', 'Black'),
    ('White', 'White'),
    ('Hispanic', 'Hispanic'),
    ('Other', 'Other'),
]

USER_TYPE_CHOICES = [
    ('student', 'Student'),
    ('educator', 'Educator'),
    ('parent', 'Parent'),
    ('staff', 'Staff'),
]

class Person(AbstractBaseUser):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='profile')
    first_name = models.CharField(max_length=50, blank=False, null= False)
    last_name = models.CharField(max_length=50, blank=False, null= False)
    nickname = models.CharField(max_length=50, blank=False, null= False)
    email = models.EmailField(blank=False, null=False)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    bio = models.TextField(max_length=250, blank=True)
    my_class = models.ForeignKey(
        'Classroom', on_delete=models.SET_NULL, null=True)
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES,
                                 default='Student')
    race = models.CharField(
        max_length=50, choices=Race, default='Other')
    date_of_birth = models.DateField()
    contact_number = PhoneNumberField()
    emergency_contact = PhoneNumberField()
    subjects = models.ManyToManyField('Subject', blank=True)
    profile_picture = models.ImageField(
        upload_to='profile_pics/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # makes the email field teh default base field
    USERNAME_FIELD = 'email'
    # created the fields tha are required at user creation stage
    REQUIRED_FIELDS = []

    class Meta:
        ordering = ['-updated_at', '-created_at']

    def __str__(self):
        return str(self.first_name)

    @property
    def avatar(self):
        try:
            avatar = self.profile_picture.url
        except:
            avatar = static('img/default_user.png')
        return avatar

    
class Classroom(models.Model):
    name = models.CharField(max_length=255, unique=True)
    teacher =  models.CharField(max_length=50, default="teacher")
    participants =models.ManyToManyField(
        Person, blank=True)
    subjects = models.ManyToManyField('Subject',  blank=True)
    description = models.TextField(max_length=500, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering  = ['-updated_at', '-created_at']

    def __str__(self):
        return str(self.name)

    
class Subject(models.Model):
    class_room = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    participants = models.ManyToManyField(
        Person, related_name='participants', blank=True)
    teacher = models.ForeignKey(
        Person, null=True, blank=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-updated_at', '-created_at']

    def __str__(self):
        return str(self.title)