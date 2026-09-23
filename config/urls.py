from django.contrib import admin
from django.urls import path
from members.views import home, gcc_details, home_details
from accounts.views import register, user_login, user_logout
from members.views import home, gcc_details, home_details, skills_and_jobs
from members.views import home, gcc_details, home_details, skills_and_jobs, dashboard, admin_dashboard, export_members_excel, export_members_pdf, member_details, edit_member, emergency, delete_member
from jobs.views import job_list, apply_job, my_applications, add_job, edit_job, delete_job, applications, update_application_status


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('register/', register, name='register'),
    path('gcc-details/', gcc_details, name='gcc_details'),
    path('login/', user_login, name='login'),
    path('home-details/', home_details, name='home_details'),
    path('skills-and-jobs/', skills_and_jobs, name='skills_and_jobs'),
    path('dashboard/', dashboard, name='dashboard'),
    path('logout/', user_logout, name='logout'),
    path('jobs/', job_list, name='job_list'),
    path('jobs/<int:job_id>/apply/', apply_job, name='apply_job'),
    path('my-applications/', my_applications, name='my_applications'),
    path('admin-dashboard/', admin_dashboard, name='admin_dashboard'),
    path('admin-dashboard/export-excel/', export_members_excel, name='export_members_excel'),
    path('admin-dashboard/export-pdf/', export_members_pdf, name='export_members_pdf'),
    path('admin-dashboard/member/<int:user_id>/', member_details, name='member_details'),
    path('admin-dashboard/member/<int:user_id>/edit/', edit_member, name='edit_member'),
    path('emergency/', emergency, name='emergency'),
    path('admin-dashboard/member/<int:user_id>/delete/', delete_member, name='delete_member'),
    path('admin-dashboard/add-job/', add_job, name='add_job'),
    path('admin-dashboard/job/<int:job_id>/edit/', edit_job, name='edit_job'),
    path('admin-dashboard/job/<int:job_id>/delete/', delete_job, name='delete_job'),
    path('admin-dashboard/applications/', applications, name='applications'),
    path('admin-dashboard/application/<int:application_id>/update/', update_application_status, name='update_application_status'),
]
