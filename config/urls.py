"""
URL configuration for config project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import routers
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from auth.views import UserInfoView
from core import views

router =  routers.DefaultRouter()
router.register(r'veiculo', views.VeiculoViewSet, basename='veiculo')
router.register(r'marca', views.MarcaViewSet, basename='marca')

schema_view = get_schema_view(
    openapi.Info(
        title="Tinnova Veículos API",
        default_version='v1',
        description="API REST para gestão de veículos com funcionalidades de CRUD, relatórios e estatísticas",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contato@tinnova.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/user-info/', UserInfoView.as_view(), name='user-info'),
    path('api/', include(router.urls)),
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
