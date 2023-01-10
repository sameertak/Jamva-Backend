from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import MyTokenObtainPairView

urlpatterns = [
    path("admin/", admin.site.urls),
    path('userlogin/', include('userLogin.urls')),
    path('restaurant/', include('restaurant.urls')),
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair')
]
if settings.DEBUG:
     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)