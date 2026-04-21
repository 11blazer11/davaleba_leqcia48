from django.urls import path
from . import views

urlpatterns = [
    #auth
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    #jobs
    path('', views.job_list, name='job_list'),

    path('job/create/', views.create_job, name='create_job'),
    path('job/<int:id>/update/', views.update_job, name='update_job'),
    path('job/<int:job_id>/delete/', views.delete_job, name='delete_job'),

    #aplications
    path('job/<int:job_id>/apply/', views.apply_to_job, name='apply_to_job'),

    path('job/<int:job_id>/applications/', views.job_applications, name='job_applications'),

    path('application/<int:app_id>/status/', views.update_application_status, name='update_application_status'),
]