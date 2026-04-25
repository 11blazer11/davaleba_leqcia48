from django.shortcuts import render, get_object_or_404, redirect
from .models import User, Job, Application
from .forms import CustomRegisterForm
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages


def register_view(request):
    if request.method == "POST":
        form = CustomRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)        # auto-login after register
            return redirect('job_list')
    else:
        form = CustomRegisterForm()

    return render(request, 'register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        user = authenticate(
            request,
            username=request.POST.get('username'),
            password=request.POST.get('password')
        )
        if user:
            login(request, user)
            return redirect('job_list')
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


def job_list(request):
    jobs = Job.objects.order_by('-created_at')
    return render(request, 'job_list.html', {'jobs': jobs})


@login_required
def create_job(request):
    if request.method == 'POST':
        job = Job(
            employer=request.user,
            title=request.POST.get('title'),
            description=request.POST.get('description'),
            location=request.POST.get('location'),
            salary=request.POST.get('salary') or None,
        )
        job.save()
        return redirect('job_list')

    return render(request, 'create_job.html')


@login_required
def update_job(request, id):
    job = get_object_or_404(Job, id=id)

    if job.employer != request.user:
        raise PermissionDenied("You are not this job's creator.")

    if request.method == 'POST':
        job.title = request.POST.get('title')
        job.description = request.POST.get('description')
        job.location = request.POST.get('location')
        job.salary = request.POST.get('salary') or None
        job.save()
        return redirect('job_list')

    return render(request, 'update_job.html', {'job': job})


@login_required
def delete_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)

    if job.employer != request.user:
        raise PermissionDenied("You don't have access to this job.")

    job.delete()
    return redirect('job_list')


@login_required
def apply_to_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)

    if request.method == 'POST':
        if Application.objects.filter(applicant=request.user, job=job).exists():
            return redirect('job_list')

        Application.objects.create(applicant=request.user, job=job)
        return redirect('job_list')

    return render(request, 'apply.html', {'job': job})


@login_required
def job_applications(request, job_id):
    job = get_object_or_404(Job, id=job_id)

    if job.employer != request.user:
        raise PermissionDenied("You aren't this job's employer.")

    applications = job.applications.all()
    return render(request, 'job_applications.html', {'job': job, 'applications': applications})


@login_required
def update_application_status(request, app_id):
    application = get_object_or_404(Application, id=app_id)

    if application.job.employer != request.user:
        raise PermissionDenied("You can't update this application's status.")

    status = request.POST.get('status')
    if status in ['pending', 'accepted', 'rejected']:
        application.status = status
        application.save()

    return redirect('job_applications', job_id=application.job.id)