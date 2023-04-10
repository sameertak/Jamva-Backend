from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import MyTokenObtainPairView, RegisterHere

urlpatterns = [
    path("admin/", admin.site.urls),
    path('register/', RegisterHere.as_view(), name='Register Manager'),
    path('userlogin/', include('userLogin.urls')),
    path('restaurant/', include('restaurant.urls')),
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('payment/', Payment.as_view())
]
if settings.DEBUG:
     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)