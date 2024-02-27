from rest_framework.permissions import BasePermission


class IsStudent(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_student and request.user.is_confirmed


class IsTeacher(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_teacher and request.user.is_confirmed


class IsSecretary(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_secretary and request.user.is_confirmed
