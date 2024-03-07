from api.apps.classroom.views.classroom import (
    PeriodViewSet,
    RoomViewSet
)

from rest_framework.routers import DefaultRouter
from django.urls import (
    path,
    include
)

router = DefaultRouter()
router.register('periods', PeriodViewSet)
router.register('rooms', RoomViewSet)


urlpatterns = [
    path('', include(router.urls)),
]
