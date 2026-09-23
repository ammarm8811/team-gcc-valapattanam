from django.contrib import admin
from .models import JobPosting, JobApplication


@admin.register(JobPosting)
class JobPostingAdmin(admin.ModelAdmin):

    list_display = (
        'job_title',
        'company',
        'location',
        'status',
        'posted_by',
        'posted_date',
    )

    search_fields = (
        'job_title',
        'company',
        'location',
        'job_description',
    )

    list_filter = (
        'status',
        'location',
        'posted_date',
    )

    ordering = (
        '-posted_date',
    )


@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):

    list_display = (
        'applicant',
        'job',
        'applied_date',
        'status',
    )

    search_fields = (
        'applicant__full_name',
        'applicant__email',
        'job__job_title',
        'job__company',
    )

    list_filter = (
        'status',
        'applied_date',
    )

    ordering = (
        '-applied_date',
    )