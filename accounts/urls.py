from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('signup/email/', views.signup_email, name='signup_email'),
    path('signup/verify/', views.signup_verify, name='signup_verify'),
    path('signup/complete/', views.signup_complete, name='signup_complete'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
]
