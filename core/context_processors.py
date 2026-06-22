from .models import PageSEO, SiteSettings

def seo_context(request):
    """
    Resolves current page's SEO record from URL name and
    injects it into the template context as `seo`.
    Also injects global `site_settings`.
    """
    try:
        url_name = getattr(request.resolver_match, 'url_name', None)
        seo = None

        # Map Django URL names → PageSEO page_name choices
        url_to_seo_page = {
            'home': 'home',
            'about': 'about',
            'services': 'services',
            'team': 'team',
            'join_us': 'join_us',
        }

        target_page = url_to_seo_page.get(url_name)
        if target_page:
            seo = PageSEO.objects.filter(page_name=target_page).first()
    except Exception:
        seo = None

    import base64
    site_settings = SiteSettings.objects.first()
    email = site_settings.email if site_settings and site_settings.email else "info@oniontechs.com"
    
    try:
        u, d = email.split('@')
        email_u = base64.b64encode(u.encode('utf-8')).decode('utf-8')
        email_d = base64.b64encode(d.encode('utf-8')).decode('utf-8')
    except Exception:
        email_u = base64.b64encode(b"info").decode('utf-8')
        email_d = base64.b64encode(b"oniontechs.com").decode('utf-8')

    return {
        'seo': seo,
        'site_settings': site_settings,
        'email_u': email_u,
        'email_d': email_d,
    }
