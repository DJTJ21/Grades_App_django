from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdmin(BasePermission):
    def has_permission(self, request, view) -> bool:
        return bool(request.user and request.user.is_staff)


class IsTeacher(BasePermission):
    def has_permission(self, request, view) -> bool:
        return bool(request.user and request.user.groups.filter(name='enseignant').exists())


class IsStudent(BasePermission):
    def has_permission(self, request, view) -> bool:
        return bool(request.user and request.user.groups.filter(name='etudiant').exists())


class RoleBasedAccess(BasePermission):
    def has_permission(self, request, view) -> bool:
        if request.user and request.user.is_staff:
            return True
        if request.user and request.user.groups.filter(name='enseignant').exists():
            return True
        if request.user and request.user.groups.filter(name='etudiant').exists():
            return request.method in SAFE_METHODS
        return False

    def has_object_permission(self, request, view, obj) -> bool:
        if request.user and request.user.is_staff:
            return True
        if request.user and request.user.groups.filter(name='enseignant').exists():
            return True
        if request.user and request.user.groups.filter(name='etudiant').exists():
            if request.method not in SAFE_METHODS:
                return False
            if hasattr(obj, 'student'):
                return obj.student.email == request.user.email
            if hasattr(obj, 'email'):
                return obj.email == request.user.email
        return False
