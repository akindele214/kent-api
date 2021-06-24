from django.urls import include, path
from django.urls.conf import include, re_path

from account.views import UserListView

# DRF YASG
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from rest_framework_simplejwt import views

urlpatterns = [
    re_path(r"^jwt/create/?", views.TokenObtainPairView.as_view(), name="jwt-create"),
]
schema_view = get_schema_view(
    openapi.Info(
        title="API End Points",
        default_version="v1",
        description="REST implementation of Django authentication system. djoser library provides a set of Django Rest Framework views to handle basic actions such as registration, login, logout, password reset and account activation. It works with custom user model.",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

account_urlpatterns = [
    path('api/', include('djoser.urls')),
    # path('api/', include('djoser.urls.jwt')),
    re_path("login/", views.TokenObtainPairView.as_view(), name="jwt-create"),
    path('api/get-users', UserListView.as_view()),
    re_path(
        r"^api/docs/$",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
]