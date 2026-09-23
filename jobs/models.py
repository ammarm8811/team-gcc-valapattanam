from django.db import models
from accounts.models import User


class JobPosting(models.Model):

    STATUS_CHOICES = [
        ('Open', 'Open'),
        ('Closed', 'Closed'),
    ]

    posted_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='job_postings'
    )

    job_title = models.CharField(
        max_length=150
    )

    company = models.CharField(
        max_length=150
    )

    location = models.CharField(
        max_length=150
    )

    job_description = models.TextField()

    contact_email_phone = models.CharField(
        max_length=150
    )

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='Open'
    )

    posted_date = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.job_title} - {self.company}"



class JobApplication(models.Model):

    job = models.ForeignKey(
        JobPosting,
        on_delete=models.CASCADE,
        related_name='applications'
    )

    applicant = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='job_applications'
    )

    applied_date = models.DateTimeField(
        auto_now_add=True
    )

    status = models.CharField(
        max_length=20,
        choices=[
            ('Applied', 'Applied'),
            ('Accepted', 'Accepted'),
            ('Rejected', 'Rejected'),
        ],
        default='Applied'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['job', 'applicant'],
                name='unique_job_application'
            )
        ]

    def __str__(self):
        return f"{self.applicant.full_name} - {self.job.job_title}"