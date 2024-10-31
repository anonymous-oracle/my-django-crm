"""
URL configuration for djcrm project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from leads.views import landing_page, LandingPageView, SignupView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('leads/', include('leads.urls', namespace='leads')),
    path('agents/', include('agents.urls', namespace='agents')),
    # path('', landing_page, name='landing-page')
    path('', LandingPageView.as_view(), name='landing-page'),
    path('login/', LoginView.as_view(), name='login'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('reset-password/', PasswordResetView.as_view(), name='reset-password'),
    path('password-reset-done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    # 1. PasswordResetForm is a class in forms.py in django forms; the context parameters required to pass in the email template is present in the save method of the form class
    # 2. <uidb64> and <token> parameters will be checked for their presence in the kwargs of the password reset confirm view's dispatch method
    # 3. password-reset-confirm is needed in the token url because the HTTP routes start with the endpoint; if there is no endpoint then the relative path will start from the uid
    path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password-reset-complete/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('logout/', LogoutView.as_view(template_name='registration/logout.html'), name='logout')
]

if settings.DEBUG:
    # adds the static file directory only in the debug mode
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)