from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from drf_yasg.utils import swagger_auto_schema
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.permissions import AllowAny



schema_view = get_schema_view(
    openapi.Info(
        title='Movie application Rest Api',
        default_version='v2',
        description='Swagger docs for Rest Api',
        contact=openapi.Contact("Samandar Shoyimov <samandar200527@gmail.com>"),
    ),
    public=True,
    permission_classes=(AllowAny, )
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('filmapp.urls')),
    path('auth/', obtain_auth_token),
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='swagger-docs'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='redoc-docs'),
]

