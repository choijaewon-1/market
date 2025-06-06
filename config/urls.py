from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from django.conf import settings
from django.conf.urls.static import static
from market.views import post_list

def root_redirect(request):
    if request.user.is_authenticated:
        return post_list(request)
    else:
        return redirect('login')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', root_redirect, name='home'),
    path('market/', include('market.urls')),
    path('accounts/', include('accounts.urls')),
    path('chat/', include('chat.urls')),
]

# ✅ media 파일 URL 설정 추가
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
