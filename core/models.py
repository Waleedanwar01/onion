from django.db import models
from django.utils.text import slugify


# ══════════════════════════════════════════════════════════════════
# PAGE-LEVEL SEO
# ══════════════════════════════════════════════════════════════════
class PageSEO(models.Model):
    PAGE_CHOICES = [
        ('home',     'Home'),
        ('about',    'About'),
        ('services', 'Services'),
        ('team',     'Team'),
        ('join_us',  'Join Us'),
    ]
    OG_TYPE_CHOICES = [
        ('website', 'Website'), ('article', 'Article'),
        ('profile', 'Profile'), ('product', 'Product'),
    ]
    ROBOTS_CHOICES = [
        ('index, follow',     'Index, Follow (default)'),
        ('noindex, follow',   'No-Index, Follow'),
        ('index, nofollow',   'Index, No-Follow'),
        ('noindex, nofollow', 'No-Index, No-Follow'),
    ]
    TWITTER_CARD_CHOICES = [
        ('summary',             'Summary'),
        ('summary_large_image', 'Summary Large Image (recommended)'),
        ('app',                 'App'),
        ('player',              'Player'),
    ]

    page_name        = models.CharField(max_length=50, choices=PAGE_CHOICES, unique=True, verbose_name='Page')
    meta_title       = models.CharField(max_length=70,  verbose_name='Meta Title',       help_text='50–70 chars')
    meta_description = models.TextField(max_length=160, verbose_name='Meta Description', help_text='120–160 chars')
    meta_keywords    = models.TextField(blank=True, verbose_name='Meta Keywords')
    author           = models.CharField(max_length=100, blank=True, default='Onion Techs', verbose_name='Author')
    canonical_url    = models.URLField(blank=True, verbose_name='Canonical URL')
    robots_meta      = models.CharField(max_length=50, choices=ROBOTS_CHOICES, default='index, follow', verbose_name='Robots Meta')

    og_title       = models.CharField(max_length=95,  blank=True, verbose_name='OG Title')
    og_description = models.TextField(max_length=200, blank=True, verbose_name='OG Description')
    og_type        = models.CharField(max_length=20, choices=OG_TYPE_CHOICES, default='website', verbose_name='OG Type')
    og_image       = models.ImageField(upload_to='seo/og_images/', blank=True, null=True, verbose_name='OG Image', help_text='1200×630 px')

    twitter_card        = models.CharField(max_length=30, choices=TWITTER_CARD_CHOICES, default='summary_large_image', verbose_name='Twitter Card Type')
    twitter_title       = models.CharField(max_length=70,  blank=True, verbose_name='Twitter Title')
    twitter_description = models.TextField(max_length=200, blank=True, verbose_name='Twitter Description')
    twitter_image       = models.ImageField(upload_to='seo/twitter_images/', blank=True, null=True, verbose_name='Twitter Image')

    schema_json = models.TextField(blank=True, verbose_name='Schema / JSON-LD')
    updated_at  = models.DateTimeField(auto_now=True, verbose_name='Last Updated')

    class Meta:
        verbose_name        = 'Page SEO'
        verbose_name_plural = 'Pages SEO'
        ordering            = ['page_name']

    def __str__(self):
        return f'{self.get_page_name_display()} — SEO'


# ══════════════════════════════════════════════════════════════════
# TEAM MEMBERS
# ══════════════════════════════════════════════════════════════════
class TeamMember(models.Model):
    CATEGORY_CHOICES = [
        ('leadership', 'Leadership Team'),
        ('core',       'Core Team'),
        ('internship', 'Interns / Trainees'),
    ]

    name          = models.CharField(max_length=100, verbose_name='Full Name')
    role          = models.CharField(max_length=150, verbose_name='Role / Title')
    bio           = models.TextField(verbose_name='Bio', help_text='Short biography shown on the team card.')
    skills        = models.CharField(
        max_length=255, 
        blank=True, 
        verbose_name='Skills', 
        help_text='Comma-separated skills, e.g. Python, React, AWS'
    )
    photo         = models.ImageField(
        upload_to='team/photos/',
        blank=True, null=True,
        verbose_name='Profile Photo',
        help_text='Square image, at least 400×400 px recommended.',
    )
    category      = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='leadership', verbose_name='Category')
    linkedin_url  = models.URLField(blank=True, verbose_name='LinkedIn URL')
    portfolio_url = models.URLField(blank=True, verbose_name='Portfolio URL')
    order         = models.PositiveIntegerField(default=0, verbose_name='Display Order', help_text='Lower = shown first.')
    is_active     = models.BooleanField(default=True, verbose_name='Active', help_text='Uncheck to hide from website.')

    class Meta:
        verbose_name        = 'Team Member'
        verbose_name_plural = 'Team Members'
        ordering            = ['order', 'name']

    def __str__(self):
        return f'{self.name} — {self.role}'

    def get_skills_list(self):
        if self.skills:
            return [s.strip() for s in self.skills.split(',') if s.strip()]
        return []


# ══════════════════════════════════════════════════════════════════
# JOB OPENINGS
# ══════════════════════════════════════════════════════════════════
class JobOpening(models.Model):
    LOCATION_CHOICES = [
        ('remote', 'Remote'),
        ('hybrid', 'Hybrid'),
        ('onsite', 'On-site'),
    ]

    title         = models.CharField(max_length=150, verbose_name='Job Title')
    description   = models.TextField(verbose_name='Description', help_text='Brief role description shown on the listing.')
    skills        = models.CharField(
        max_length=500,
        verbose_name='Required Skills',
        help_text='Comma-separated, e.g. React, TypeScript, Next.js',
    )
    location_type = models.CharField(max_length=20, choices=LOCATION_CHOICES, default='remote', verbose_name='Location Type')
    is_active     = models.BooleanField(default=True, verbose_name='Active', help_text='Uncheck to hide from website.')
    order         = models.PositiveIntegerField(default=0, verbose_name='Display Order')
    created_at    = models.DateTimeField(auto_now_add=True, verbose_name='Created At')

    class Meta:
        verbose_name        = 'Job Opening'
        verbose_name_plural = 'Job Openings'
        ordering            = ['order', '-created_at']

    def __str__(self):
        return self.title

    def get_skills_list(self):
        return [s.strip() for s in self.skills.split(',') if s.strip()]


# ══════════════════════════════════════════════════════════════════
# SERVICES  (with per-service SEO)
# ══════════════════════════════════════════════════════════════════
class Service(models.Model):
    # ── Core ──────────────────────────────────────────────────────
    title             = models.CharField(max_length=150, verbose_name='Service Title')
    slug              = models.SlugField(
        unique=True,
        verbose_name='URL Slug',
        help_text='Auto-generated from title. Used in URL: /services/your-slug/',
    )
    icon              = models.CharField(
        max_length=10, default='💻',
        verbose_name='Icon (Emoji)',
        help_text='Single emoji used as the service icon.',
    )
    cover_image       = models.ImageField(
        upload_to='services/covers/',
        blank=True, null=True,
        verbose_name='Cover Image',
        help_text='High quality image for the service card.',
    )
    short_description = models.TextField(
        max_length=250,
        verbose_name='Short Description',
        help_text='Shown on the Services listing page card (max 250 chars).',
    )
    full_description  = models.TextField(
        verbose_name='Full Description',
        help_text='Detailed content for the individual service page.',
    )
    features          = models.TextField(
        blank=True,
        verbose_name='Key Features',
        help_text='One feature per line. Shown as bullet points on the detail page.',
    )
    order             = models.PositiveIntegerField(default=0, verbose_name='Display Order')
    is_active         = models.BooleanField(default=True, verbose_name='Active')

    # ── SEO ───────────────────────────────────────────────────────
    meta_title        = models.CharField(
        max_length=70, verbose_name='Meta Title',
        help_text='50–70 characters. Shown in Google search results.',
    )
    meta_description  = models.TextField(
        max_length=160, verbose_name='Meta Description',
        help_text='120–160 characters. Shown below title in Google.',
    )
    meta_keywords     = models.TextField(blank=True, verbose_name='Meta Keywords')
    canonical_url     = models.URLField(blank=True, verbose_name='Canonical URL', help_text='e.g. https://oniontechs.com/services/web-applications/')
    og_title          = models.CharField(max_length=95, blank=True, verbose_name='OG Title', help_text='Blank = use Meta Title')
    og_description    = models.TextField(max_length=200, blank=True, verbose_name='OG Description', help_text='Blank = use Meta Description')
    og_image          = models.ImageField(
        upload_to='seo/services/', blank=True, null=True,
        verbose_name='OG Image', help_text='1200×630 px recommended.',
    )
    schema_json       = models.TextField(blank=True, verbose_name='Schema / JSON-LD')

    class Meta:
        verbose_name        = 'Service'
        verbose_name_plural = 'Services'
        ordering            = ['order', 'title']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_features_list(self):
        return [f.strip() for f in self.features.split('\n') if f.strip()]
