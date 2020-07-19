from rest_framework.permissions import BasePermission, SAFE_METHODS

class GameStateOwnPermission(BasePermission):

  def has_permission(self, request, view):
    return True

  def has_object_permission(self, request, view, obj):
    owner = obj.user.id
    return owner == request.user.id