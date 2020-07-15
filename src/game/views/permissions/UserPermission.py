from rest_framework.permissions import BasePermission, SAFE_METHODS

class UserPermission(BasePermission):

  def has_permission(self, request, view):
    return True

  def has_object_permission(self, request, view, obj):
    owner = obj.created_by
    return int(owner) == request.auth.user.id