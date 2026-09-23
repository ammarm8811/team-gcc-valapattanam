from django import forms
from .models import GCCDetails, HomeDetails, SkillsAndJobs


class GCCDetailsForm(forms.ModelForm):

    class Meta:
        model = GCCDetails

        fields = [
            'country',
            'city',
            'visa_type',
            'company_name',
            'job_title',
            'year_of_migration',
        ]


class HomeDetailsForm(forms.ModelForm):

    class Meta:
        model = HomeDetails

        fields = [
            'house_name',
            'ward_number',
            'family_location',
            'emergency_contact_name',
            'emergency_contact_number',
            'norka_id_status',
        ]


class SkillsAndJobsForm(forms.ModelForm):

    class Meta:
        model = SkillsAndJobs

        fields = [
            'education_qualification',
            'professional_skills',
            'looking_for_job',
            'resume_url',
        ]