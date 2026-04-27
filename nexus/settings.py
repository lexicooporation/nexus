from pathlib import Path
import os
from dotenv import load_dotenv
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/6.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG','False')=='True'


ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost 127.0.0.1').split()
# Application definition

INSTALLED_APPS = [
    "jazzmin",                      
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "nexusApp",
    "cloudinary_storage",
    "cloudinary", 
    "sendgrid_backend",
    "maintenance_mode",

]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    'whitenoise.middleware.WhiteNoiseMiddleware',
    "maintenance_mode.middleware.MaintenanceModeMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "nexus.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / os.path.join("templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "nexus.wsgi.application"


# Database
# https://docs.djangoproject.com/en/6.0/ref/settings/#databases

import dj_database_url

DATABASES = {
    'default': dj_database_url.config(
        default=os.getenv('DATABASE_URL'),
        conn_max_age=600,
    )
}

# ─── Authentication ───────────────────────────────────────────────────────────
# EmailBackend is checked first so users log in with email.
# ModelBackend is kept as a fallback so the Django admin (username login)
# still works for staff/superusers.

AUTHENTICATION_BACKENDS = [
    "nexusApp.backends.EmailBackend",
    "django.contrib.auth.backends.ModelBackend",
]

# Password validation
# https://docs.djangoproject.com/en/6.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

LOGIN_URL          = "/accounts/login/"
LOGIN_REDIRECT_URL = "/pricing/"        
LOGOUT_REDIRECT_URL = "/" 



# Email configuration
# Email configuration for SendGrid

SENDGRID_API_KEY = os.getenv('SENDGRID_API_KEY')
EMAIL_BACKEND = 'sendgrid_backend.SendgridBackend'
SENDGRID_SANDBOX_MODE_IN_DEBUG = False
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL', 'nwankwoifeanyi21@outlook.com')

# paystack configuration
PAYSTACK_PUBLIC_KEY= os.getenv('PAYSTACK_PUBLIC_KEY')
PAYSTACK_SECRET_KEY= os.getenv('PAYSTACK_SECRET_KEY')

# Internationalization
# https://docs.djangoproject.com/en/6.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/6.0/howto/static-files/

STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / os.path.join("static"),]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'


MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'


#── Cloudinary ────────────────────────────────────────────────
import cloudinary

cloudinary.config(
    cloudinary_url=os.getenv('CLOUDINARY_URL')
)

CLOUDINARY_STORAGE = {
    'CLOUD_NAME': os.getenv('CLOUDINARY_CLOUD_NAME'),
    'API_KEY':    os.getenv('CLOUDINARY_API_KEY'),
    'API_SECRET': os.getenv('CLOUDINARY_API_SECRET'),
}
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

       

MAINTENANCE_MODE = False
MAINTENANCE_MODE_IGNORE_ADMIN_SITE = True   
MAINTENANCE_MODE_IGNORE_SUPERUSER = True   
MAINTENANCE_MODE_TEMPLATE = '503.html'   
default_theme_mode='light'

# ─── Cache (add this to your settings.py) ────────────────────────────────────
#
# Django uses LocMemCache by default — good enough for development.
# For production, swap to Redis so the cache survives server restarts
# and works across multiple processes/workers.
#
# ─── Cache ────────────────────────────────────────────────────
if os.getenv('REDIS_URL'):
    CACHES = {
        "default": {
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": os.getenv("REDIS_URL"),
            "OPTIONS": {
                "CLIENT_CLASS": "django_redis.client.DefaultClient",
            },
        }
    }
else:
    CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        }
    }


JAZZMIN_SETTINGS = {
    # ── Branding ──────────────────────────────────────────────────────────────
    "site_title": "Nexus Admin",
    "site_header": "Nexus",
    "site_brand": "Nexus",
    "site_logo": None,            
    "site_icon": None,
    "login_logo": None,
    "welcome_sign": "Welcome to Nexus Admin",
    "copyright": "Nexus Inc. 2026",

    # ── Top menu links ────────────────────────────────────────────────────────
    "topmenu_links": [
        {"name": "Dashboard", "url": "admin:index", "permissions": ["auth.view_user"]},
        {"name": "View Site", "url": "/", "new_window": True},
        {"name": "Messages",  "url": "/admin/nexusApp/contactmessage/"},
        {"name": "NexusApp","app":  "nexusApp",},],

    # ── User menu (top-right avatar) ──────────────────────────────────────────
    "usermenu_links": [
        {"name": "View Site", "url": "/", "new_window": True, "icon": "fas fa-globe"},
        {"model": "auth.user"},],

    # ── Sidebar ───────────────────────────────────────────────────────────────
    "show_sidebar":              True,
    "navigation_expanded":       True,

    # Order sidebar items
    "order_with_respect_to": [
        "auth",
        "nexusApp",
        "nexusApp.ContactMessage",
        "nexusApp.Testimonial",
        "nexusApp.PricingPlan",
        "nexusApp.PlanFeature",
        "nexusApp.FAQ",
        "nexusApp.TeamMember",
    ],

    # Custom sidebar icons (Font Awesome 5)
    "icons": {
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
        "auth.Group": "fas fa-users",
        "nexusApp.ContactMessage": "fas fa-envelope",
        "nexusApp.Testimonial": "fas fa-star",
        "nexusApp.PricingPlan": "fas fa-tags",
        "nexusApp.PlanFeature": "fas fa-check-circle",
        "nexusApp.FAQ": "fas fa-question-circle",
        "nexusApp.TeamMember": "fas fa-id-badge",
    },

    "default_icon_parents":  "fas fa-folder",
    "default_icon_children": "fas fa-circle",

    # ── UI tweaks ─────────────────────────────────────────────────────────────
    "related_modal_active":      True,
    "custom_css":               "css/admin_custom.css",   
    "custom_js":                 None,
    "use_google_fonts_cdn":      True,
    "show_ui_builder":           False,     
    "changeform_format":         "horizontal_tabs",
    "changeform_format_overrides": {"auth.user":  "collapsible","auth.group": "vertical_tabs",},
    "language_chooser": False,
}



# ─── Jazzmin theme (colour) ───────────────────────────────────────────────────

JAZZMIN_UI_TWEAKS = {
    "navbar_small_text":        False,
    "footer_small_text":        False,
    "body_small_text":          False,
    "brand_small_text":         False,
    "brand_colour":             "navbar-dark",
    "accent":                   "accent-primary",
    "navbar":                   "",
    "no_navbar_border":         True,
    "navbar_fixed":             True,
    "layout_boxed":             False,
    "footer_fixed":             False,
    "sidebar_fixed":            True,
    "sidebar":                  "sidebar-dark-primary",
    "sidebar_nav_small_text":   False,
    "sidebar_disable_expand":   False,
    "sidebar_nav_child_indent": True,
    "sidebar_nav_compact_style":False,
    "sidebar_nav_legacy_style": False,
    "sidebar_nav_flat_style":   False,
    "theme":                    "default",
    
    "button_classes": {
        "primary":   "btn-primary",
        "secondary": "btn-secondary",
        "info":      "btn-info",
        "warning":   "btn-warning",
        "danger":    "btn-danger",
        "success":   "btn-success",
    },
}


# ── Security ──────────────────────────────────────────────────
SECURE_SSL_REDIRECT          = False
SECURE_HSTS_SECONDS          = 31536000 if not DEBUG else 0
SECURE_HSTS_INCLUDE_SUBDOMAINS = not DEBUG
SECURE_HSTS_PRELOAD          = not DEBUG
SESSION_COOKIE_SECURE        = not DEBUG
CSRF_COOKIE_SECURE           = not DEBUG
SECURE_BROWSER_XSS_FILTER    = True
SECURE_CONTENT_TYPE_NOSNIFF  = True
X_FRAME_OPTIONS              = 'DENY'