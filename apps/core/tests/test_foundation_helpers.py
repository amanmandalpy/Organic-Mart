import logging

from apps.core.exceptions import ConflictError, PermissionPolicyError, ServiceError
from apps.core.logging import CorrelationIdFilter, safe_log_context
from apps.core.middleware import correlation_id_context
from apps.core.tasks import health_probe_task


def test_safe_log_context_removes_none_without_dropping_falsey_values():
    assert safe_log_context(user_id="u1", total=0, paid=False, secret=None) == {
        "user_id": "u1",
        "total": 0,
        "paid": False,
    }


def test_correlation_id_filter_adds_request_id_to_log_record():
    token = correlation_id_context.set("req-log-123")
    try:
        record = logging.LogRecord(
            name="organicmart.test",
            level=logging.INFO,
            pathname=__file__,
            lineno=1,
            msg="hello",
            args=(),
            exc_info=None,
        )

        assert CorrelationIdFilter().filter(record)
        assert record.correlation_id == "req-log-123"
    finally:
        correlation_id_context.reset(token)


def test_service_errors_expose_stable_codes():
    assert ServiceError.code == "service_error"
    assert ConflictError.code == "conflict"
    assert PermissionPolicyError.code == "permission_denied"


def test_health_probe_task_returns_serializable_payload():
    assert health_probe_task("probe-1") == {
        "probe_id": "probe-1",
        "status": "ok",
    }
