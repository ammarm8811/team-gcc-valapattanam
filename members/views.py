from django.shortcuts import render, redirect,  get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from accounts.models import User
from django.db import models
from jobs.models import JobPosting
from .forms import GCCDetailsForm, HomeDetailsForm, SkillsAndJobsForm
from .models import GCCDetails, HomeDetails, SkillsAndJobs
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse
from openpyxl import Workbook
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from django.core.paginator import Paginator


def home(request):

    total_members = User.objects.filter(role='Member').count()

    total_jobs = JobPosting.objects.filter(status='Open').count()

    total_countries = User.objects.filter(
        role='Member',
        gcc_details__isnull=False
    ).values(
        'gcc_details__country'
    ).distinct().count()

    context = {
        'total_members': total_members,
        'total_jobs': total_jobs,
        'total_countries': total_countries,
    }

    return render(request, 'home.html', context)




@login_required
def gcc_details(request):

    try:
        gcc_details = request.user.gcc_details
    except GCCDetails.DoesNotExist:
        gcc_details = None

    if request.method == 'POST':

        form = GCCDetailsForm(
            request.POST,
            instance=gcc_details
        )

        if form.is_valid():

            gcc_details = form.save(commit=False)
            gcc_details.user = request.user
            gcc_details.save()
            messages.success(
                request,
                'GCC Details updated successfully.'
            )
            return redirect('dashboard')

    else:

        form = GCCDetailsForm(
            instance=gcc_details
        )

    return render(
        request,
        'members/gcc_details.html',
        {'form': form}
    )



@login_required
def home_details(request):

    try:
        home_details = request.user.home_details
    except HomeDetails.DoesNotExist:
        home_details = None


    if request.method == 'POST':

        form = HomeDetailsForm(
            request.POST,
            instance=home_details
        )

        if form.is_valid():

            home_details = form.save(commit=False)
            home_details.user = request.user
            home_details.save()
            messages.success(
                request,
                'Home Details updated successfully.'
            )

            return redirect('dashboard')

    else:

        form = HomeDetailsForm(
            instance=home_details
        )

    return render(
        request,
        'members/home_details.html',
        {'form': form}
    )




@login_required
def skills_and_jobs(request):

    try:
        skills_and_jobs = request.user.skills_and_jobs
    except SkillsAndJobs.DoesNotExist:
        skills_and_jobs = None


    if request.method == 'POST':

        form = SkillsAndJobsForm(
            request.POST,
            instance=skills_and_jobs
        )

        if form.is_valid():
            skills_and_jobs = form.save(commit=False)
            skills_and_jobs.user = request.user
            skills_and_jobs.save()
            messages.success(
                request,
                'Skills & Jobs details updated successfully.'
            )
            
            return redirect('dashboard')

    else:

        form = SkillsAndJobsForm(
            instance=skills_and_jobs
        )

    return render(
        request,
        'members/skills_and_jobs.html',
        {'form': form}
    )




@login_required
def dashboard(request):

    try:
        gcc_details = request.user.gcc_details
    except Exception:
        gcc_details = None

    try:
        home_details = request.user.home_details
    except Exception:
        home_details = None

    try:
        skills_and_jobs = request.user.skills_and_jobs
    except Exception:
        skills_and_jobs = None


    # Profile completion

    completed_sections = 1

    if gcc_details:
        completed_sections += 1

    if home_details:
        completed_sections += 1

    if skills_and_jobs:
        completed_sections += 1

    profile_completion = completed_sections * 25


    return render(
        request,
        'members/dashboard.html',
        {
            'gcc_details': gcc_details,
            'home_details': home_details,
            'skills_and_jobs': skills_and_jobs,
            'profile_completion': profile_completion,
        }
    )




@staff_member_required
def admin_dashboard(request):

    total_members = User.objects.filter(
        role='Member'
    ).count()

    total_job_seekers = SkillsAndJobs.objects.filter(
        looking_for_job=True
    ).count()

    total_jobs = JobPosting.objects.count()
    open_jobs = JobPosting.objects.filter(
        status='Open'
    ).count()

    jobs = JobPosting.objects.all().order_by('-posted_date')

    total_countries = GCCDetails.objects.values(
        'country'
    ).distinct().count()

    country_stats = {}
    for country, name in GCCDetails.COUNTRY_CHOICES:
        country_stats[name] = GCCDetails.objects.filter(
            country=country
        ).count()

    members = User.objects.filter(
        role='Member'
    ).order_by(
        'full_name'
    )

    search = request.GET.get('search')
    country = request.GET.get('country')
    blood_group = request.GET.get('blood_group')
    ward = request.GET.get('ward')
    job_status = request.GET.get('job_status')

    if search:

        members = members.filter(
            models.Q(full_name__icontains=search)
            | models.Q(email__icontains=search)
            | models.Q(phone_whatsapp__icontains=search)
            | models.Q(gcc_details__country__icontains=search)
            | models.Q(gcc_details__city__icontains=search)
            | models.Q(gcc_details__company_name__icontains=search)
            | models.Q(gcc_details__job_title__icontains=search)
        )

    if country:
        members = members.filter(
            gcc_details__country=country
        )


    if blood_group:
        members = members.filter(
            blood_group=blood_group
        )


    if ward:
        members = members.filter(
            home_details__ward_number=ward
        )


    if job_status == 'looking':

        members = members.filter(
            skills_and_jobs__looking_for_job=True
        )

    elif job_status == 'not_looking':

        members = members.filter(
            skills_and_jobs__looking_for_job=False
        )

    paginator = Paginator(
        members,
        10
    )

    page_number = request.GET.get('page')

    members = paginator.get_page(
        page_number
    )


    job_seekers = SkillsAndJobs.objects.filter(
        looking_for_job=True
    ).count()

    not_job_seekers = SkillsAndJobs.objects.filter(
        looking_for_job=False
    ).count()



    blood_group_stats = {}
    for blood_group, name in User.BLOOD_GROUPS:

        blood_group_stats[name] = User.objects.filter(
            role='Member',
            blood_group=blood_group
        ).count()


    return render(
        request,
        'members/admin_dashboard.html',
        {
            'total_members': total_members,
            'country_stats': country_stats,
            'total_job_seekers': total_job_seekers,
            'total_jobs': total_jobs,
            'open_jobs': open_jobs,
            'jobs': jobs,
            'total_countries': total_countries,
            'members': members,
            'search': search,
            'country': country,
            'blood_group': blood_group,
            'ward': ward,
            'job_status': job_status,
            'job_seekers': job_seekers,
            'not_job_seekers': not_job_seekers,
            'blood_group_stats': blood_group_stats,
        }
    )




@staff_member_required
def export_members_excel(request):

    members = User.objects.filter(
        role='Member'
    ).select_related(
        'gcc_details',
        'home_details',
        'skills_and_jobs'
    )

    workbook = Workbook()

    worksheet = workbook.active

    worksheet.title = 'Members'

    headers = [
        'Full Name',
        'Email',
        'WhatsApp',
        'Date of Birth',
        'Blood Group',
        'GCC Country',
        'GCC City',
        'Visa Type',
        'Company',
        'Job Title',
        'Year of Migration',
        'House Name',
        'Ward Number',
        'Family Location',
        'Emergency Contact Name',
        'Emergency Contact Number',
        'NORKA ID Status',
        'Education',
        'Professional Skills',
        'Looking for Job',
        'Resume URL',
    ]

    worksheet.append(headers)

    for member in members:

        if hasattr(member, 'gcc_details'):
            gcc = member.gcc_details
        else:
            gcc = None

        if hasattr(member, 'home_details'):
            home = member.home_details
        else:
            home = None

        if hasattr(member, 'skills_and_jobs'):
            skills = member.skills_and_jobs
        else:
            skills = None

        worksheet.append([
            member.full_name,
            member.email,
            member.phone_whatsapp,
            member.dob,
            member.blood_group,
            gcc.get_country_display() if gcc else '',
            gcc.city if gcc else '',
            gcc.visa_type if gcc else '',
            gcc.company_name if gcc else '',
            gcc.job_title if gcc else '',
            gcc.year_of_migration if gcc else '',
            home.house_name if home else '',
            home.ward_number if home else '',
            home.family_location if home else '',
            home.emergency_contact_name if home else '',
            home.emergency_contact_number if home else '',
            home.norka_id_status if home else '',
            skills.education_qualification if skills else '',
            skills.professional_skills if skills else '',
            'Yes' if skills and skills.looking_for_job else 'No',
            skills.resume_url if skills else '',
        ])

    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )

    response['Content-Disposition'] = (
        'attachment; filename="team_gcc_members.xlsx"'
    )

    workbook.save(response)

    return response




@staff_member_required
def export_members_pdf(request):

    members = User.objects.filter(
        role='Member'
    ).select_related(
        'gcc_details',
        'home_details',
        'skills_and_jobs'
    )

    response = HttpResponse(
        content_type='application/pdf'
    )

    response['Content-Disposition'] = (
        'attachment; filename="team_gcc_members.pdf"'
    )

    document = SimpleDocTemplate(
        response,
        pagesize=landscape(A4),
        rightMargin=20,
        leftMargin=20,
        topMargin=20,
        bottomMargin=20,
    )

    styles = getSampleStyleSheet()

    data = [
        [
            'Name',
            'Email',
            'WhatsApp',
            'Blood',
            'Country',
            'City',
            'Company',
            'Job Title',
            'Ward',
            'Job Seeker',
        ]
    ]

    for member in members:

        if hasattr(member, 'gcc_details'):
            gcc = member.gcc_details
        else:
            gcc = None

        if hasattr(member, 'home_details'):
            home = member.home_details
        else:
            home = None

        if hasattr(member, 'skills_and_jobs'):
            skills = member.skills_and_jobs
        else:
            skills = None

        data.append([
            member.full_name,
            member.email,
            member.phone_whatsapp,
            member.blood_group or '',
            gcc.get_country_display() if gcc else '',
            gcc.city if gcc else '',
            gcc.company_name if gcc else '',
            gcc.job_title if gcc else '',
            home.ward_number if home else '',
            'Yes' if skills and skills.looking_for_job else 'No',
        ])

    table = Table(
        data,
        repeatRows=1
    )

    table.setStyle(
        TableStyle([
            (
                'BACKGROUND',
                (0, 0),
                (-1, 0),
                colors.darkgreen
            ),
            (
                'TEXTCOLOR',
                (0, 0),
                (-1, 0),
                colors.white
            ),
            (
                'GRID',
                (0, 0),
                (-1, -1),
                0.5,
                colors.grey
            ),
            (
                'FONTNAME',
                (0, 0),
                (-1, 0),
                'Helvetica-Bold'
            ),
            (
                'FONTSIZE',
                (0, 0),
                (-1, -1),
                7
            ),
            (
                'VALIGN',
                (0, 0),
                (-1, -1),
                'MIDDLE'
            ),
        ])
    )

    document.build([table])

    return response



@staff_member_required
def member_details(request, user_id):

    member = get_object_or_404(
        User,
        id=user_id,
        role='Member'
    )

    try:
        gcc_details = member.gcc_details
    except GCCDetails.DoesNotExist:
        gcc_details = None

    try:
        home_details = member.home_details
    except HomeDetails.DoesNotExist:
        home_details = None

    try:
        skills_and_jobs = member.skills_and_jobs
    except SkillsAndJobs.DoesNotExist:
        skills_and_jobs = None

    return render(
        request,
        'members/member_details.html',
        {
            'member': member,
            'gcc_details': gcc_details,
            'home_details': home_details,
            'skills_and_jobs': skills_and_jobs,
        }
    )


@staff_member_required
def edit_member(request, user_id):

    member = get_object_or_404(
        User,
        id=user_id,
        role='Member'
    )

    try:
        gcc_details = member.gcc_details
    except GCCDetails.DoesNotExist:
        gcc_details = None

    try:
        home_details = member.home_details
    except HomeDetails.DoesNotExist:
        home_details = None

    try:
        skills_and_jobs = member.skills_and_jobs
    except SkillsAndJobs.DoesNotExist:
        skills_and_jobs = None

    if request.method == 'POST':

        member.full_name = request.POST.get('full_name')
        member.email = request.POST.get('email')
        member.phone_whatsapp = request.POST.get('phone_whatsapp')
        member.dob = request.POST.get('dob') or None
        member.blood_group = request.POST.get('blood_group') or None

        gcc_form = GCCDetailsForm(
            request.POST,
            instance=gcc_details
        )

        home_form = HomeDetailsForm(
            request.POST,
            instance=home_details
        )

        skills_form = SkillsAndJobsForm(
            request.POST,
            instance=skills_and_jobs
        )

        if (
            gcc_form.is_valid()
            and home_form.is_valid()
            and skills_form.is_valid()
        ):

            member.save()

            gcc = gcc_form.save(commit=False)
            gcc.user = member
            gcc.save()

            home = home_form.save(commit=False)
            home.user = member
            home.save()

            skills = skills_form.save(commit=False)
            skills.user = member
            skills.save()

            messages.success(
                request,
                'Member details updated successfully.'
            )

            return redirect(
                'member_details',
                user_id=member.id
            )

    else:

        gcc_form = GCCDetailsForm(
            instance=gcc_details
        )

        home_form = HomeDetailsForm(
            instance=home_details
        )

        skills_form = SkillsAndJobsForm(
            instance=skills_and_jobs
        )

    return render(
        request,
        'members/edit_member.html',
        {
            'member': member,
            'gcc_form': gcc_form,
            'home_form': home_form,
            'skills_form': skills_form,
        }
    )


@staff_member_required
def delete_member(request, user_id):

    member = get_object_or_404(
        User,
        id=user_id,
        role='Member'
    )

    if request.method == 'POST':

        member_name = member.full_name

        member.delete()

        messages.success(
            request,
            f'Member "{member_name}" deleted successfully.'
        )

        return redirect('admin_dashboard')

    return render(
        request,
        'members/delete_member.html',
        {
            'member': member,
        }
    )



@login_required
def emergency(request):

    blood_group = request.GET.get('blood_group', '')

    donors = None
    searched = False

    country_codes = {
        'UAE': '971',
        'KSA': '966',
        'Qatar': '974',
        'Oman': '968',
        'Bahrain': '973',
        'Kuwait': '965',
    }

    if blood_group:

        donors = User.objects.filter(
            role='Member',
            blood_group=blood_group
        ).select_related('gcc_details').order_by('full_name')

        for donor in donors:

            if hasattr(donor, 'gcc_details'):

                country = donor.gcc_details.country
                country_code = country_codes.get(country, '')

                donor.whatsapp_link = (
                    country_code + donor.phone_whatsapp
                )

            else:

                donor.whatsapp_link = donor.phone_whatsapp

        searched = True

    return render(
        request,
        'members/emergency.html',
        {
            'donors': donors,
            'searched': searched,
            'selected_blood_group': blood_group,
        }
    )



