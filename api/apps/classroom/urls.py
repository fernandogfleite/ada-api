from api.apps.classroom.views.classroom import (
    PeriodViewSet,
    RoomViewSet,
    SubjectViewSet,
    SubjectPeriodViewSet,
    SubjectPeriodStudentViewSet,
    ClassroomViewSet,
    ListLoggedUserClassrooms,
    ListLoggedUserSubjectPeriods,
    ListStudentInSubjectPeriod
)

from rest_framework.routers import DefaultRouter
from django.urls import (
    path,
    include
)

router = DefaultRouter()
router.register('periods', PeriodViewSet)
router.register('rooms', RoomViewSet)
router.register('subjects', SubjectViewSet)
router.register('subject-periods', SubjectPeriodViewSet)
router.register('subject-period-students', SubjectPeriodStudentViewSet)
router.register('classrooms', ClassroomViewSet)
router.register('user-classrooms', ListLoggedUserClassrooms)
router.register('user-subject-periods', ListLoggedUserSubjectPeriods)


urlpatterns = [
    path(
        'subject-period-students/<int:subject_period_id>/students/',
        ListStudentInSubjectPeriod.as_view(
            {
                'get': 'list'
            }
        ),
        name='list-student-in-subject-period'
    ),
    path('', include(router.urls)),
]
