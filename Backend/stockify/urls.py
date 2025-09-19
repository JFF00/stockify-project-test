from django.contrib import admin
from django.urls import include, path
from stock.views import CategoryViewSet, ProductViewSet
from users.views import UserViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'category', CategoryViewSet)
router.register(r'products', ProductViewSet)


urlpatterns = [
    path("admin/", admin.site.urls),
    path('api/', include(router.urls)),
    path('', include(router.urls))
]