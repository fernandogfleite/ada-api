from api.apps.classroom.views.classroom import (
    PeriodViewSet,
)

from rest_framework.routers import DefaultRouter
from django.urls import (
    path,
    include
)

router = DefaultRouter()
router.register('periods', PeriodViewSet)


urlpatterns = [
    path('', include(router.urls)),
]
