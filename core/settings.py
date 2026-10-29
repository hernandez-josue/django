# core/settings.py  (guardar como UTF-8)
import environ
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# ── Variables de entorno ──────────────────────────────────────────────────
env = environ.Env(DEBUG=(bool, False))
environ.Env.read_env(BASE_DIR / '.env')

SECRET_KEY = env(
    'SECRET_KEY',
    default='dev-clave-segura-para-desarrollo-w01'
)

DEBUG = env.bool('DEBUG', default=True)

ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    'testserver',
    'django-w4le.onrender.com',
]

# Necesario para login/formularios por HTTPS en Render
CSRF_TRUSTED_ORIGINS = ['https://django-w4le.onrender.com']

# ── Apps ──────────────────────────────────────────────────────────────────
INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    # Terceros
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'rest_framework',
    'rest_framework.authtoken',
    'whitenoise.runserver_nostatic',
    # Apps del ERP
    'core',
    'clientes',
    'proveedores',
    'productos',
    'ventas',
    'reportes',
    'configuracion',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]

ROOT_URLCONF = 'core.urls'

# ── Templates ─────────────────────────────────────────────────────────────
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# ── Base de datos ─────────────────────────────────────────────────────────
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# ── Internacionalización ──────────────────────────────────────────────────
LANGUAGE_CODE = 'es-mx'
TIME_ZONE     = 'America/Mexico_City'
USE_I18N      = True
USE_TZ        = True

# ── Archivos estáticos y media ────────────────────────────────────────────
STATIC_URL       = '/static/'
STATIC_ROOT      = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']

MEDIA_URL  = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedStaticFilesStorage",
    },
}

# ── Autenticación ─────────────────────────────────────────────────────────
LOGIN_URL           = '/accounts/login/'
LOGIN_REDIRECT_URL  = '/productos/'
LOGOUT_REDIRECT_URL = '/'

SITE_ID = 1

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

ACCOUNT_LOGIN_METHODS      = {'username'}
ACCOUNT_EMAIL_REQUIRED     = False
ACCOUNT_EMAIL_VERIFICATION = 'none'
ACCOUNT_LOGOUT_ON_GET      = True
ACCOUNT_SESSION_REMEMBER   = True

# ── DRF ───────────────────────────────────────────────────────────────────
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
}

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ── JAZZMIN — admin temático comida china ─────────────────────────────────
JAZZMIN_SETTINGS = {
    # Identidad
    'site_title':    'ERP Chinito',
    'site_header':   'ERP Chinito',
    'site_brand':    'ERP \u9f8d Chinito',
    'welcome_sign':  'Bienvenido al sistema de gestión · \u6b61\u8fce',
    'copyright':     'Chinos S.A. de C.V.',
    'site_icon':     None,
    'site_logo':     None,

    # Búsqueda global
    'search_model':  ['clientes.Cliente', 'productos.Producto'],

    # Menú superior
    'topmenu_links': [
        {'name': 'Inicio ERP', 'url': '/', 'new_window': False},
        {'name': 'Productos',  'url': '/productos/'},
        {'name': 'Clientes',   'url': '/clientes/'},
        {'name': 'Ventas',     'url': '/ventas/'},
    ],

    'usermenu_links': [
        {'name': 'Ver ERP', 'url': '/', 'new_window': False},
    ],

    # Orden del menú lateral
    'order_with_respect_to': [
        'clientes', 'proveedores', 'productos',
        'ventas', 'configuracion', 'auth',
    ],

    # Iconos Font Awesome
    'icons': {
        'auth':                           'fas fa-users-cog',
        'auth.user':                      'fas fa-user',
        'auth.Group':                     'fas fa-users',
        'clientes.Cliente':               'fas fa-users',
        'proveedores.Proveedor':          'fas fa-truck',
        'productos.Categoria':            'fas fa-tags',
        'productos.Producto':             'fas fa-utensils',
        'ventas.Venta':                   'fas fa-receipt',
        'ventas.DetalleVenta':            'fas fa-list',
        'ventas.Pedido':                  'fas fa-bell-concierge',
        'configuracion.ConfiguracionERP': 'fas fa-cogs',
    },
    'default_icon_parents':  'fas fa-folder',
    'default_icon_children': 'fas fa-circle',

    # Apariencia
    'related_modal_active': True,
    'custom_css':               'erp_custom.css',  
    'hide_apps':  [],
    'show_sidebar':         True,
    'navigation_expanded':  True,
    'show_ui_builder':      False,

    # Ocultar del menú lo que no se usa (siguen existiendo por URL)
    'hide_models': [],

    'changeform_format': 'horizontal_tabs',
    'language_chooser':  False,
}

JAZZMIN_UI_TWEAKS = {
    'navbar_small_text':         False,
    'footer_small_text':         False,
    'body_small_text':           False,
    'brand_small_text':          False,
    'brand_colour':              'navbar-danger',
    'accent':                    'accent-warning',
    'navbar':                    'navbar-danger',
    'no_navbar_border':          False,
    'navbar_fixed':              True,
    'layout_boxed':              False,
    'footer_fixed':              False,
    'sidebar_fixed':             True,
    'sidebar':                   'sidebar-dark-danger',
    'sidebar_nav_small_text':    False,
    'sidebar_disable_expand':    False,
    'sidebar_nav_child_indent':  True,
    'sidebar_nav_compact_style': False,
    'sidebar_nav_legacy_style':  False,
    'sidebar_nav_flat_style':    False,
    'theme':                     'flatly',
    'default_theme_mode':        'auto',
    'button_classes': {
        'primary':   'btn-primary',
        'secondary': 'btn-secondary',
        'info':      'btn-info',
        'warning':   'btn-warning',
        'danger':    'btn-danger',
        'success':   'btn-success',
    },
}

# ── Logging ───────────────────────────────────────────────────────────────
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {"class": "logging.StreamHandler"},
    },
    "loggers": {
        "django.request": {
            "handlers": ["console"],
            "level": "ERROR",
            "propagate": False,
        },
    },
}