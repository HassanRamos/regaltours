from django.contrib import admin
from django.urls import include, re_path,path
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from django.conf import settings
from django.conf.urls.static import static


schema_view = get_schema_view(
    openapi.Info(
        title="Regal Tours Website",
        default_version='v1',
        description="",
        terms_of_service="Internal use only !!!",
        contact=openapi.Contact(email="emkiarie0@gmail.com"),
        license=openapi.License(name="Docs only for internal use only !!!"),
    ),
    public=False,
    permission_classes=(permissions.AllowAny,)

)

urlpatterns = [
   path('admin/', admin.site.urls),
   path('', include('website.urls'), name='website'),
   path('documentation/', include([
        path('', schema_view.with_ui('swagger', cache_timeout=0), name="schema-swagger-ui"),
        path('api/api.json/', schema_view.without_ui(cache_timeout=0), name="schema-swagger-ui"),
        path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name="schema-redoc")
        ]))

]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
