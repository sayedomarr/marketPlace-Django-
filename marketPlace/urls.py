"""
URL configuration for marketPlace project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from products.views import home
from .views import signup

# TODO: Update URL configuration for MySQL and production readiness:

# 1. **Make products the home page** by adding: path('', include('products.urls'))

# 2. **Add media file serving for development**:
#    - Import settings and static from django.conf
#    - Add static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) for development
#    - Only serve media files when DEBUG = True

# 3. **MySQL-Specific Considerations**:
#    - Consider adding database health check URLs
#    - Handle MySQL connection error pages
#    - Add performance monitoring URLs if needed
#    - Consider adding database backup/restore endpoints (admin only)

# 4. **Production Considerations**:
#    - Use environment variables for sensitive settings
#    - Consider adding health check endpoints
#    - Handle static file serving in production
#    - Add proper error handling for database issues

# HINT: The order of URL patterns matters - more specific patterns should come first
# HINT: Media files need special handling in development vs production
# HINT: Use include() to include app-specific URLs
# HINT: MySQL provides better performance for complex URL routing
# HINT: Consider adding API endpoints for future mobile app development

urlpatterns = [
    path('admin/', admin.site.urls),
    # Make products the home page
    path('', home, name='home'),
    # Namespaced products URLs
    path('', include(('products.urls', 'products'), namespace='products')),
    path('categories/', include(('categories.urls', 'categories'), namespace='categories')),
    # Auth URLs
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/signup/', signup, name='signup'),
    path('aboutus/', include(('aboutus.urls', 'aboutus'), namespace='aboutus')),
    path('contactus/', include(('contactus.urls', 'contactus'), namespace='contactus')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
