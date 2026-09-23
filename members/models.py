from django.db import models
from accounts.models import User


class GCCDetails(models.Model):

    COUNTRY_CHOICES = [
        ('UAE', 'United Arab Emirates'),
        ('KSA', 'Saudi Arabia'),
        ('Qatar', 'Qatar'),
        ('Oman', 'Oman'),
        ('Bahrain', 'Bahrain'),
        ('Kuwait', 'Kuwait'),
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='gcc_details'
    )

    country = models.CharField(
        max_length=20,
        choices=COUNTRY_CHOICES
    )

    city = models.CharField(
        max_length=100
    )

    visa_type = models.CharField(
        max_length=100
    )

    company_name = models.CharField(
        max_length=150
    )

    job_title = models.CharField(
        max_length=150
    )

    year_of_migration = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.user.full_name} - {self.country}"

class HomeDetails(models.Model):

    FAMILY_LOCATION_CHOICES = [
        ('Home Country', 'Home Country'),
        ('With Member in GCC', 'With Member in GCC'),
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='home_details'
    )

    house_name = models.CharField(
        max_length=150
    )

    ward_number = models.CharField(
        max_length=20
    )

    family_location = models.CharField(
        max_length=30,
        choices=FAMILY_LOCATION_CHOICES
    )

    emergency_contact_name = models.CharField(
        max_length=150
    )

    emergency_contact_number = models.CharField(
        max_length=20
    )

    norka_id_status = models.CharField(
        max_length=20,
        choices=[
            ('Yes', 'Yes'),
            ('No', 'No'),
            ('Need Help', 'Need Help'),
        ]
    )

    def __str__(self):
        return f"{self.user.full_name} - Home Details"

class SkillsAndJobs(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='skills_and_jobs'
    )

    education_qualification = models.TextField()

    professional_skills = models.TextField()

    looking_for_job = models.BooleanField(
        default=False
    )

    resume_url = models.URLField(
        blank=True,
        null=True
    )

    def __str__(self):
        return f"{self.user.full_name} - Skills & Jobs"