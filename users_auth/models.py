# Below are the list of classes that map data to the database
from django.db import models
from django.conf import settings
from django.templatetags.static import static

# Choices for gender field
GENDER_CHOICES = [
    ('Male', 'Male'),
    ('Female', 'Female'),
    ('unknown', 'Unknown'),
]

# Choices for race field
RACE = [
    ('Asian', 'Asian'),
    ('Black', 'Black'),
    ('White', 'White'),
    ('Hispanic', 'Hispanic'),
    ('Other', 'Other'),
]

# Choices for user type field
USER_TYPE_CHOICES = [
    ('student', 'Student'),
    ('educator', 'Educator'),
    ('parent', 'Parent'),
    ('staff', 'Staff'),
]

# Model representing a person
class Person(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    nickname = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='unknown')
    bio = models.TextField(max_length=250, blank=True)
    my_class = models.ForeignKey(
        'Classroom', on_delete=models.SET_NULL, null=True, blank=True)
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='Student')
    race = models.CharField(max_length=50, choices=RACE, default='Other')
    date_of_birth = models.DateField(blank=True, null=True)
    contact_number = models.CharField(max_length=25, blank=True, null=True)
    emergency_contact = models.CharField(max_length=25, blank=True, null=True)
    subjects = models.ManyToManyField('Subject', blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    profile_status = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'  # Makes the email field the default base field
    REQUIRED_FIELDS = []  # Fields required at user creation stage

    class Meta:
        ordering = ['-updated_at', '-created_at']  # Order by updated_at and created_at descending

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def avatar(self):
        try:
            avatar = self.profile_picture.url
        except:
            avatar = static('img/default_user.png')
        return avatar

# Model representing a classroom
class Classroom(models.Model):
    name = models.CharField(max_length=255, unique=True)
    teacher = models.ForeignKey(
        Person, null=True, blank=True, on_delete=models.CASCADE, related_name="class_teacher")
    participants = models.ManyToManyField(Person, blank=True)
    subjects = models.ManyToManyField('Subject', blank=True)
    description = models.TextField(max_length=500, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-name', '-created_at']  # Order by name and created_at descending

    def __str__(self):
        return str(self.name)

# Model representing a subject
class Subject(models.Model):
    class_room = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    participants = models.ManyToManyField(Person, related_name='participants', blank=True)
    teacher = models.ForeignKey(Person, null=True, blank=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']  # Order by created_at descending

    def __str__(self):
        return str(self.title)