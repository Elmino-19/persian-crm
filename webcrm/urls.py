from django.contrib import admin
from django.contrib.admin.views.decorators import staff_member_required
from django.urls import include
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.shortcuts import redirect

from common.views.favicon import FaviconRedirect
from crm.views.contact_form import contact_form
from massmail.views.get_oauth2_tokens import get_refresh_token


def home_redirect(request):
    """
    Redirect users from the root URL to the main CRM page.
    
    This function handles the root URL ('/') and redirects users to the 
    main CRM interface with the appropriate language prefix and secret prefix.
    
    Args:
        request: The HTTP request object
        
    Returns:
        HttpResponseRedirect: Redirect to the main CRM page
    """
    return redirect(f'/{settings.LANGUAGE_CODE}/{settings.SECRET_CRM_PREFIX}')


urlpatterns = [
    path('', home_redirect, name='home'),
    path('favicon.ico', FaviconRedirect.as_view()),
    path('voip/', include('voip.urls')),
    path(
        'OAuth-2/authorize/',
        staff_member_required(get_refresh_token), 
        name='get_refresh_token'
    ),   
]

urlpatterns += static(
    settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
)

if 'rosetta' in settings.INSTALLED_APPS:
    urlpatterns += [
        path('rosetta/', include('rosetta.urls'))
    ]

urlpatterns += i18n_patterns(
    path(settings.SECRET_CRM_PREFIX, include('common.urls')),
    path(settings.SECRET_CRM_PREFIX, include('crm.urls')),
    path(settings.SECRET_CRM_PREFIX, include('massmail.urls')),
    path(settings.SECRET_CRM_PREFIX, include('tasks.urls')),
    path(settings.SECRET_ADMIN_PREFIX, admin.site.urls),
    path('contact-form/<uuid:uuid>/', contact_form, name='contact_form'),
)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
