from .models import PageSEO


def seo_context(request):
    """
    Resolves current page's SEO record from URL name and
    injects it into the template context as `seo`.
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

    return {'seo': seo}
