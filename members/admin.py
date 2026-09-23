from django.contrib import admin
from .models import GCCDetails, HomeDetails, SkillsAndJobs

@admin.register(GCCDetails)
class GCCDetailsAdmin(admin.ModelAdmin):

    list_display = (
        'user',
        'country',
        'city',
        'company_name',
        'job_title',
        'year_of_migration',
    )

    search_fields = (
        'user__full_name',
        'user__email',
        'company_name',
        'job_title',
    )

    list_filter = (
        'country',
        'year_of_migration',
    )


@admin.register(HomeDetails)
class HomeDetailsAdmin(admin.ModelAdmin):

    list_display = (
        'user',
        'house_name',
        'ward_number',
        'family_location',
        'emergency_contact_name',
        'emergency_contact_number',
        'norka_id_status',
    )

    search_fields = (
        'user__full_name',
        'user__email',
        'house_name',
        'emergency_contact_name',
    )

    list_filter = (
        'ward_number',
        'family_location',
        'norka_id_status',
    )

@admin.register(SkillsAndJobs)
class SkillsAndJobsAdmin(admin.ModelAdmin):

    list_display = (
        'user',
        'education_qualification',
        'looking_for_job',
        'resume_url',
    )

    search_fields = (
        'user__full_name',
        'user__email',
        'education_qualification',
        'professional_skills',
    )

    list_filter = (
        'looking_for_job',
    )