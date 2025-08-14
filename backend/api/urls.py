from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ping,
    PersonViewSet,
    ResourceViewSet,
    AccountViewSet,
    PermissionViewSet,
    QueryAPIView
)

router = DefaultRouter()
router.register(r'persons', PersonViewSet)
router.register(r'resources', ResourceViewSet)
router.register(r'accounts', AccountViewSet)
router.register(r'permissions', PermissionViewSet)

urlpatterns = [
    path("ping/", ping, name="ping"),
    path("query/", QueryAPIView.as_view(), name="query"),
    path("", include(router.urls)),
]
