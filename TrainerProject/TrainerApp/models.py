from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

class Department(models.Model):
    department_name = models.CharField(max_length=100, unique=True)
    department_image = models.ImageField(upload_to='department_images/', blank=True, null=True)

    def __str__(self):
        return self.department_name


class CustomUser(AbstractUser):
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True, blank=True)
    phone_number = models.IntegerField(null=True, blank=True)
    def __str__(self):
        return f"{self.first_name} {self.last_name} {self.department}"


class Course(models.Model):
    class LevelChoices(models.TextChoices):
        LEVEL_6 = 'L6', 'Level 6'
        LEVEL_5 = 'L5', 'Level 5'
        LEVEL_3 = 'L3', 'Level 3'
        LEVEL_4 = 'L4', 'Level 4'
        
    class CycleChoices(models.TextChoices):
        CYCLE_1 = 'C1', 'Cycle 1'
        CYCLE_2 = 'C2', 'Cycle 2'
        CYCLE_3 = 'C3', 'Cycle 3'
        
    cycle = models.CharField(max_length=2, choices=CycleChoices.choices, default=CycleChoices.CYCLE_1)
    course_code = models.CharField(max_length=10)
    course_name = models.CharField(max_length=100, unique=True)
    course_image = models.ImageField(upload_to='course_images/', blank=True, null=True)
    course_level = models.CharField(max_length=2, choices=LevelChoices.choices, default=LevelChoices.LEVEL_6)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.course_name} {self.course_code}"


class Unit(models.Model):
    class ModuleChoices(models.TextChoices):
        MODULE_1 = 'M1', 'Module 1'
        MODULE_2 = 'M2', 'Module 2'
        MODULE_3 = 'M3', 'Module 3'
        MODULE_4 = 'M4', 'Module 4'
        MODULE_5 = 'M5', 'Module 5'
        MODULE_6 = 'M6', 'Module 6'
        
    class CompetencyChoices(models.TextChoices):
        BASIC = 'BC', 'Basic Competency'
        CORE = 'CR', 'Core Competency'
        COMMON = 'CC', 'Common Competency'

    module = models.CharField(max_length=2, choices=ModuleChoices.choices, default=ModuleChoices.MODULE_1, blank=True, null=True)
    unit_code = models.CharField(max_length=20)
    unit_name = models.CharField(max_length=100)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    competency = models.CharField(max_length=2, choices=CompetencyChoices.choices, default=CompetencyChoices.BASIC , blank=True, null=True)

    def __str__(self):
        return f"{self.unit_name} {self.unit_code}"


class Document(models.Model):
    class DocumentChoices(models.TextChoices):
        OCCUPATIONAL_STANDARDS = 'OS', 'Occupational Standards'
        CURRICULUM = 'CU', 'Curriculum'
        ASSESSMENT_TOOLS = 'AT', 'Assessment Tools'
        LEARNING_PLAN = 'LP', 'Learning Plan'
        WEIGHTING_TOOL = 'WT', 'Weighting Tool'
        OTHER_DOCUMENTS = 'OD', 'Other Documents'

    document_name = models.CharField(max_length=100, unique=True)
    document_file = models.FileField(upload_to='documents/')
    document_type = models.CharField(max_length=2, choices=DocumentChoices.choices,
                                     default=DocumentChoices.OCCUPATIONAL_STANDARDS)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    downloads = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.document_name

class Transactions(models.Model):
    merchant_request_id = models.CharField(max_length=50, null=True, blank=True)
    checkout_request_id = models.CharField(max_length=50, null=True, blank=True)
    result_code = models.IntegerField(null=True, blank=True)
    result_desc = models.CharField(max_length=255, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    transaction_id = models.CharField(max_length=50, null=True, blank=True)
    user_phone_number = models.CharField(max_length=15, null=True, blank=True)
    transaction_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Transaction {self.transaction_id} by {self.user_phone_number}"
    
class TrainingSession(models.Model):
    trainer_name = models.CharField(max_length=100)
    trainer_number = models.CharField(max_length=15)
    name_of_institution = models.CharField(max_length=200)
    date_of_preparation = models.DateField()
    number_of_learners = models.IntegerField()
    course_class = models.CharField(max_length=100)
    number_of_weeks = models.IntegerField(null=True, blank=True)
    number_of_sessions_per_week = models.IntegerField(null=True, blank=True)
    hours_per_session = models.IntegerField(null=True, blank=True)
    hours_per_session = models.IntegerField(null=True, blank=True)
    hours_per_session = models.IntegerField(null=True, blank=True)
    department = models.CharField(max_length=100, null=True, blank=True)
    course = models.CharField(max_length=100,null=True, blank=True)
    unit = models.CharField(max_length=100, null=True, blank=True)
    transaction = models.ForeignKey(Transactions, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.trainer_name} - {self.course}"