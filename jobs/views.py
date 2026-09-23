from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from .models import JobPosting, JobApplication


def job_list(request):

    jobs = JobPosting.objects.filter(
        status='Open'
    ).order_by(
        '-posted_date'
    )

    applied_job_ids = []

    if request.user.is_authenticated:

        applications = JobApplication.objects.filter(
            applicant=request.user
        )

        for application in applications:

            applied_job_ids.append(
                application.job.id
            )

    return render(
        request,
        'jobs/job_list.html',
        {
            'jobs': jobs,
            'applied_job_ids': applied_job_ids,
        }
    )


@login_required
def apply_job(request, job_id):

    job = get_object_or_404(
        JobPosting,
        id=job_id
    )

    if request.method == 'POST':

        if job.status == 'Open':

            application, created = JobApplication.objects.get_or_create(
                job=job,
                applicant=request.user
            )

            if created:

                messages.success(
                    request,
                    'Job application submitted successfully.'
                )

            else:

                messages.info(
                    request,
                    'You have already applied for this job.'
                )

    return redirect('job_list')


@login_required
def my_applications(request):

    applications = JobApplication.objects.filter(
        applicant=request.user
    ).order_by(
        '-applied_date'
    )

    return render(
        request,
        'jobs/my_applications.html',
        {
            'applications': applications,
        }
    )


@staff_member_required
def add_job(request):

    if request.method == 'POST':

        job_title = request.POST.get('job_title')
        company = request.POST.get('company')
        location = request.POST.get('location')
        job_description = request.POST.get('job_description')
        contact_email_phone = request.POST.get(
            'contact_email_phone'
        )
        status = request.POST.get('status')

        JobPosting.objects.create(
            posted_by=request.user,
            job_title=job_title,
            company=company,
            location=location,
            job_description=job_description,
            contact_email_phone=contact_email_phone,
            status=status,
        )

        messages.success(
            request,
            'Job posted successfully.'
        )

        return redirect('job_list')

    return render(
        request,
        'jobs/add_job.html'
    )



@staff_member_required
def edit_job(request, job_id):

    job = get_object_or_404(
        JobPosting,
        id=job_id
    )

    if request.method == 'POST':

        job.job_title = request.POST.get('job_title')
        job.company = request.POST.get('company')
        job.location = request.POST.get('location')
        job.job_description = request.POST.get('job_description')
        job.contact_email_phone = request.POST.get(
            'contact_email_phone'
        )
        job.status = request.POST.get('status')

        job.save()

        messages.success(
            request,
            'Job updated successfully.'
        )

        return redirect('job_list')

    return render(
        request,
        'jobs/edit_job.html',
        {
            'job': job,
        }
    )



@staff_member_required
def delete_job(request, job_id):

    job = get_object_or_404(
        JobPosting,
        id=job_id
    )

    if request.method == 'POST':

        job.delete()

        messages.success(
            request,
            'Job deleted successfully.'
        )

        return redirect('job_list')

    return render(
        request,
        'jobs/delete_job.html',
        {
            'job': job,
        }
    )


@staff_member_required
def applications(request):

    applications = JobApplication.objects.select_related(
        'job',
        'applicant'
    ).order_by('-applied_date')

    return render(
        request,
        'jobs/applications.html',
        {
            'applications': applications,
        }
    )


@staff_member_required
def update_application_status(request, application_id):

    application = get_object_or_404(
        JobApplication,
        id=application_id
    )

    if request.method == 'POST':

        status = request.POST.get('status')

        if status in ['Applied', 'Accepted', 'Rejected']:

            application.status = status
            application.save()

            messages.success(
                request,
                'Application status updated successfully.'
            )

    return redirect('applications')