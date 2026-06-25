"""Typed service errors that delivery layers can translate consistently."""


class ServiceError(Exception):
    """Base class for expected, safe-to-present application failures."""

    code = "service_error"


class ConflictError(ServiceError):
    """The requested mutation conflicts with current persisted state."""

    code = "conflict"


class PermissionPolicyError(ServiceError):
    """The actor is not allowed to perform the requested domain action."""

    code = "permission_denied"
