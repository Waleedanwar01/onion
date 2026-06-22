from django.shortcuts import render, get_object_or_404
from .models import PageSEO, TeamMember, JobOpening, Service


def _get_seo(page_name):
    return PageSEO.objects.filter(page_name=page_name).first()


def home(request):
    return render(request, 'index.html', {'seo': _get_seo('home')})


def about(request):
    return render(request, 'about.html', {'seo': _get_seo('about')})


def services(request):
    services_qs = Service.objects.filter(is_active=True).order_by('order')
    return render(request, 'services.html', {
        'seo': _get_seo('services'),
        'services': services_qs,
    })


def service_detail(request, slug):
    service = get_object_or_404(Service, slug=slug, is_active=True)
    related  = Service.objects.filter(is_active=True).exclude(slug=slug).order_by('order')[:3]
    return render(request, 'service-detail.html', {
        'service': service,
        'related_services': related,
        # Pass seo=None so base.html falls back to service block overrides
        'seo': None,
    })


def team(request):
    leadership = TeamMember.objects.filter(category='leadership', is_active=True).order_by('order')
    core       = TeamMember.objects.filter(category='core',       is_active=True).order_by('order')
    interns    = TeamMember.objects.filter(category='internship', is_active=True).order_by('order')
    return render(request, 'team.html', {
        'seo': _get_seo('team'),
        'leadership_members': leadership,
        'core_members': core,
        'intern_members': interns,
    })


def join_us(request):
    jobs = JobOpening.objects.filter(is_active=True).order_by('order')
    return render(request, 'join-us.html', {
        'seo': _get_seo('join_us'),
        'jobs': jobs,
    })