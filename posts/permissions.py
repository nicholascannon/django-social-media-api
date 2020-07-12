from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Checks that the authorised user is the owner of the resource when making non
    safe http requests.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.author == request.user
