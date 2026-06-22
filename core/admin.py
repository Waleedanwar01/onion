from django.contrib import admin
from django.utils.html import format_html
from .models import PageSEO, TeamMember, JobOpening, Service


# ──────────────────────────────────────────────────────────────────
# Branding
# ──────────────────────────────────────────────────────────────────
admin.site.site_header = 'Onion Techs Admin'
admin.site.site_title  = 'Onion Techs'
admin.site.index_title = 'Onion Techs Control Panel'


# ══════════════════════════════════════════════════════════════════
# PAGE SEO
# ══════════════════════════════════════════════════════════════════
@admin.register(PageSEO)
class PageSEOAdmin(admin.ModelAdmin):

    def has_add_permission(self, request):
        return PageSEO.objects.count() < 5

    list_display       = ('page_badge', 'meta_title', 'robots_meta', 'og_type', 'og_image_preview', 'updated_at')
    list_display_links = ('page_badge', 'meta_title')
    search_fields      = ('meta_title', 'meta_description')
    readonly_fields    = ('updated_at', 'og_image_preview', 'twitter_image_preview')

    fieldsets = (
        ('Page', {
            'description': 'Select which page this SEO record controls.',
            'fields': ('page_name',),
        }),
        ('Basic SEO Meta Tags', {
            'description': 'Title: 50-70 chars | Description: 120-160 chars',
            'fields': ('meta_title', 'meta_description', 'meta_keywords', 'author', 'canonical_url', 'robots_meta'),
        }),
        ('Open Graph  (Facebook, LinkedIn, WhatsApp)', {
            'fields': ('og_title', 'og_description', 'og_type', 'og_image', 'og_image_preview'),
        }),
        ('Twitter / X Card', {
            'fields': ('twitter_card', 'twitter_title', 'twitter_description', 'twitter_image', 'twitter_image_preview'),
            'classes': ('collapse',),
        }),
        ('Schema / JSON-LD', {
            'fields': ('schema_json',),
            'classes': ('collapse',),
        }),
        ('Record Info', {
            'fields': ('updated_at',),
            'classes': ('collapse',),
        }),
    )

    @admin.display(description='Page', ordering='page_name')
    def page_badge(self, obj):
        colours = {
            'home': '#6366f1', 'about': '#0ea5e9',
            'services': '#10b981', 'team': '#f59e0b', 'join_us': '#ef4444',
        }
        c = colours.get(obj.page_name, '#64748b')
        return format_html(
            '<span style="background:{c};color:#fff;padding:3px 12px;border-radius:12px;'
            'font-size:12px;font-weight:600;">{l}</span>',
            c=c, l=obj.get_page_name_display(),
        )

    @admin.display(description='OG Image')
    def og_image_preview(self, obj):
        if obj.og_image:
            return format_html('<img src="{}" style="height:60px;border-radius:6px;"/>', obj.og_image.url)
        return format_html('<span style="color:#94a3b8;font-size:12px;">No image</span>')

    @admin.display(description='Twitter Image')
    def twitter_image_preview(self, obj):
        if obj.twitter_image:
            return format_html('<img src="{}" style="height:60px;border-radius:6px;"/>', obj.twitter_image.url)
        return format_html('<span style="color:#94a3b8;font-size:12px;">No image</span>')


# ══════════════════════════════════════════════════════════════════
# TEAM MEMBERS
# ══════════════════════════════════════════════════════════════════
@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display        = ('photo_thumb', 'name', 'role', 'category_badge', 'order', 'is_active')
    list_display_links  = ('photo_thumb', 'name')
    list_editable       = ('order', 'is_active')
    list_filter         = ('category', 'is_active')
    search_fields       = ('name', 'role', 'bio')
    readonly_fields     = ('photo_preview',)

    fieldsets = (
        ('Identity', {
            'fields': ('name', 'role', 'skills', 'category', 'order', 'is_active'),
        }),
        ('Photo', {
            'description': 'Upload a square profile photo (minimum 400×400 px).',
            'fields': ('photo', 'photo_preview'),
        }),
        ('Bio', {
            'fields': ('bio',),
        }),
        ('Social Links', {
            'fields': ('linkedin_url', 'portfolio_url'),
        }),
    )

    @admin.display(description='Photo')
    def photo_thumb(self, obj):
        if obj.photo:
            return format_html(
                '<img src="{}" style="width:40px;height:40px;border-radius:50%;object-fit:cover;"/>',
                obj.photo.url,
            )
        return format_html(
            '<div style="width:40px;height:40px;border-radius:50%;background:#6366f1;'
            'display:flex;align-items:center;justify-content:center;color:#fff;font-weight:700;">{}</div>',
            obj.name[0].upper() if obj.name else '?',
        )

    @admin.display(description='Category', ordering='category')
    def category_badge(self, obj):
        c = '#6366f1' if obj.category == 'leadership' else '#0ea5e9'
        return format_html(
            '<span style="background:{c};color:#fff;padding:2px 10px;border-radius:10px;font-size:12px;">{l}</span>',
            c=c, l=obj.get_category_display(),
        )

    @admin.display(description='Photo Preview')
    def photo_preview(self, obj):
        if obj.photo:
            return format_html(
                '<img src="{}" style="width:120px;height:120px;border-radius:50%;object-fit:cover;border:3px solid #6366f1;"/>',
                obj.photo.url,
            )
        return format_html('<span style="color:#94a3b8;">No photo uploaded yet.</span>')


# ══════════════════════════════════════════════════════════════════
# JOB OPENINGS
# ══════════════════════════════════════════════════════════════════
@admin.register(JobOpening)
class JobOpeningAdmin(admin.ModelAdmin):
    list_display       = ('title', 'location_badge', 'skills_preview', 'order', 'is_active', 'created_at')
    list_display_links = ('title',)
    list_editable      = ('order', 'is_active')
    list_filter        = ('location_type', 'is_active')
    search_fields      = ('title', 'description', 'skills')

    fieldsets = (
        ('Job Details', {
            'fields': ('title', 'description', 'skills', 'location_type'),
        }),
        ('Visibility', {
            'fields': ('is_active', 'order'),
        }),
    )

    @admin.display(description='Location', ordering='location_type')
    def location_badge(self, obj):
        colours = {'remote': '#10b981', 'hybrid': '#f59e0b', 'onsite': '#ef4444'}
        c = colours.get(obj.location_type, '#64748b')
        return format_html(
            '<span style="background:{c};color:#fff;padding:2px 10px;border-radius:10px;font-size:12px;">{l}</span>',
            c=c, l=obj.get_location_type_display(),
        )

    @admin.display(description='Skills')
    def skills_preview(self, obj):
        skills = obj.get_skills_list()[:3]
        badges = ''.join(
            f'<span style="background:#6366f1/15;border:1px solid #6366f1;color:#818cf8;'
            f'padding:2px 8px;border-radius:8px;font-size:11px;margin-right:4px;">{s}</span>'
            for s in skills
        )
        more = f'+{len(obj.get_skills_list()) - 3} more' if len(obj.get_skills_list()) > 3 else ''
        return format_html('{}{}', badges, more)


# ══════════════════════════════════════════════════════════════════
# SERVICES
# ══════════════════════════════════════════════════════════════════
@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display       = ('icon_col', 'title', 'slug', 'order', 'is_active', 'og_image_preview')
    list_display_links = ('icon_col', 'title')
    list_editable      = ('order', 'is_active')
    search_fields      = ('title', 'short_description', 'meta_title')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields    = ('og_image_preview',)

    fieldsets = (
        ('Service Info', {
            'description': 'Basic information shown on the Services listing page and detail page.',
            'fields': ('title', 'slug', 'icon', 'order', 'is_active'),
        }),
        ('Content', {
            'fields': ('short_description', 'full_description', 'features'),
        }),
        ('SEO — Basic Meta', {
            'description': 'These fields control how this service page ranks on Google.',
            'fields': ('meta_title', 'meta_description', 'meta_keywords', 'canonical_url'),
        }),
        ('SEO — Open Graph (Social Sharing)', {
            'fields': ('og_title', 'og_description', 'og_image', 'og_image_preview'),
            'classes': ('collapse',),
        }),
        ('SEO — Schema / JSON-LD', {
            'fields': ('schema_json',),
            'classes': ('collapse',),
        }),
    )

    @admin.display(description='Icon')
    def icon_col(self, obj):
        return format_html(
            '<span style="font-size:22px;" title="{}">{}</span>',
            obj.title, obj.icon,
        )

    @admin.display(description='OG Image')
    def og_image_preview(self, obj):
        if obj.og_image:
            return format_html('<img src="{}" style="height:60px;border-radius:6px;"/>', obj.og_image.url)
        return format_html('<span style="color:#94a3b8;font-size:12px;">No image</span>')
