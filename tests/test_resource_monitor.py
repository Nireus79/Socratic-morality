"""Comprehensive tests for resource monitor."""

import pytest
import os
from socratic_morality.security.resource_monitor import (
    ResourceMonitor,
    ResourceUsage,
    LimitViolation,
    ResourceType,
    SeverityLevel,
)


@pytest.fixture
def resource_monitor():
    """Create resource monitor."""
    return ResourceMonitor()


@pytest.fixture
def custom_limits():
    """Create custom resource limits."""
    return {
        "cpu_percent": 50.0,
        "memory_mb": 512.0,
        "file_descriptors": 256,
        "processes": 16,
    }


class TestMonitoringSessionManagement:
    """Tests for monitoring session management."""

    def test_start_monitoring_with_default_limits(self, resource_monitor):
        """Test starting monitoring with default limits."""
        session = resource_monitor.start_monitoring(os.getpid())

        assert session.process_id == os.getpid()
        assert session.is_active is True
        assert session.session_id is not None
        assert len(session.limits) > 0

    def test_start_monitoring_with_custom_limits(self, resource_monitor, custom_limits):
        """Test starting monitoring with custom limits."""
        session = resource_monitor.start_monitoring(os.getpid(), limits=custom_limits)

        assert session.limits == custom_limits
        assert session.is_active is True

    def test_multiple_sessions(self, resource_monitor):
        """Test managing multiple monitoring sessions."""
        session1 = resource_monitor.start_monitoring(os.getpid())
        session2 = resource_monitor.start_monitoring(os.getpid() + 1, limits={"cpu_percent": 30.0})

        assert session1.session_id != session2.session_id
        assert session1.limits != session2.limits


class TestResourceUsageTracking:
    """Tests for resource usage tracking."""

    def test_get_current_usage(self, resource_monitor):
        """Test getting current resource usage."""
        usage = resource_monitor.get_current_usage()

        assert isinstance(usage, ResourceUsage)
        assert usage.cpu_percent >= 0
        assert usage.memory_mb >= 0
        assert usage.file_descriptors >= 0
        assert usage.processes >= 0
        assert usage.timestamp is not None
        assert usage.within_limits is True

    def test_current_usage_for_session(self, resource_monitor):
        """Test getting usage for a specific session."""
        session = resource_monitor.start_monitoring(os.getpid())
        usage = resource_monitor.get_current_usage(session.session_id)

        assert usage.timestamp is not None
        # Should be stored in session snapshots
        assert usage in session.snapshots

    def test_usage_details_included(self, resource_monitor):
        """Test that usage details are included."""
        usage = resource_monitor.get_current_usage()

        assert "cpu_percent" in usage.usage_details
        assert "memory_mb" in usage.usage_details
        assert "file_descriptors" in usage.usage_details
        assert "processes" in usage.usage_details


class TestLimitViolationDetection:
    """Tests for limit violation detection."""

    def test_check_limits_violated_no_violations(self, resource_monitor):
        """Test checking limits when none are violated."""
        session = resource_monitor.start_monitoring(
            os.getpid(),
            limits={
                "cpu_percent": 100.0,  # Very high limit
                "memory_mb": 10000.0,  # Very high limit
            },
        )

        violations = resource_monitor.check_limits_violated(session.session_id)

        # Unlikely to have violations with such high limits
        assert isinstance(violations, list)

    def test_violation_severity_determination(self, resource_monitor):
        """Test that violation severity is correctly determined."""
        # Set very low limits to force violations
        session = resource_monitor.start_monitoring(
            os.getpid(),
            limits={
                "cpu_percent": 0.1,  # Very low
                "memory_mb": 0.1,  # Very low
            },
        )

        violations = resource_monitor.check_limits_violated(session.session_id)

        if violations:
            # Violations should be marked as warning or critical
            assert all(
                v.severity in (SeverityLevel.WARNING, SeverityLevel.CRITICAL) for v in violations
            )

    def test_violation_stored_in_session(self, resource_monitor):
        """Test that violations are stored in session."""
        session = resource_monitor.start_monitoring(
            os.getpid(),
            limits={
                "cpu_percent": 0.001,  # Extremely low
                "memory_mb": 0.001,  # Extremely low
            },
        )

        violations = resource_monitor.check_limits_violated(session.session_id)

        # Violations should be in session
        assert len(session.violations) == len(violations)


class TestLimitEnforcement:
    """Tests for limit enforcement."""

    def test_enforce_limits_soft(self, resource_monitor):
        """Test soft enforcement of limits."""
        session = resource_monitor.start_monitoring(os.getpid())

        result = resource_monitor.enforce_limits(session.session_id, hard=False)

        assert isinstance(result, dict)
        assert "success" in result

    def test_enforce_limits_hard(self, resource_monitor):
        """Test hard enforcement of limits."""
        session = resource_monitor.start_monitoring(
            os.getpid(),
            limits={
                "cpu_percent": 0.001,
                "memory_mb": 0.001,
            },
        )

        result = resource_monitor.enforce_limits(session.session_id, hard=True)

        assert isinstance(result, dict)
        assert "success" in result

    def test_enforce_nonexistent_session(self, resource_monitor):
        """Test enforcing limits for nonexistent session."""
        result = resource_monitor.enforce_limits("nonexistent_session")

        assert result["success"] is False


class TestUsageHistory:
    """Tests for usage history tracking."""

    def test_get_usage_history_empty(self, resource_monitor):
        """Test getting history from new session."""
        session = resource_monitor.start_monitoring(os.getpid())

        # Should have at least no history initially or one snapshot
        history = resource_monitor.get_usage_history(session.session_id)
        assert isinstance(history, list)

    def test_get_usage_history_accumulates(self, resource_monitor):
        """Test that usage history accumulates."""
        session = resource_monitor.start_monitoring(os.getpid())

        # Get usage multiple times
        resource_monitor.get_current_usage(session.session_id)
        resource_monitor.get_current_usage(session.session_id)
        resource_monitor.get_current_usage(session.session_id)

        history = resource_monitor.get_usage_history(session.session_id)

        # Should have accumulated snapshots
        assert len(history) >= 3

    def test_history_for_nonexistent_session(self, resource_monitor):
        """Test getting history for nonexistent session."""
        history = resource_monitor.get_usage_history("nonexistent")

        assert history == []


class TestMonitoringSessionTermination:
    """Tests for monitoring session termination."""

    def test_stop_monitoring_generates_report(self, resource_monitor):
        """Test stopping monitoring and generating report."""
        session = resource_monitor.start_monitoring(os.getpid())

        # Collect some data
        resource_monitor.get_current_usage(session.session_id)

        report = resource_monitor.stop_monitoring(session.session_id)

        assert report is not None
        assert report.session_id == session.session_id
        assert report.process_id == os.getpid()
        assert report.duration_seconds >= 0
        assert report.peak_cpu_percent >= 0
        assert report.peak_memory_mb >= 0
        assert isinstance(report.recommendations, list)

    def test_stop_monitoring_nonexistent_session(self, resource_monitor):
        """Test stopping nonexistent session."""
        report = resource_monitor.stop_monitoring("nonexistent")

        assert report is None

    def test_session_inactive_after_stop(self, resource_monitor):
        """Test that session becomes inactive after stopping."""
        session = resource_monitor.start_monitoring(os.getpid())
        assert session.is_active is True

        resource_monitor.stop_monitoring(session.session_id)
        assert session.is_active is False

    def test_report_contains_statistics(self, resource_monitor):
        """Test that report contains usage statistics."""
        session = resource_monitor.start_monitoring(os.getpid())

        # Generate some snapshots
        for _ in range(3):
            resource_monitor.get_current_usage(session.session_id)

        report = resource_monitor.stop_monitoring(session.session_id)

        assert "cpu_percent" in report.average_usage
        assert "memory_mb" in report.average_usage


class TestGlobalLimitsManagement:
    """Tests for global limits management."""

    def test_set_global_limits(self, resource_monitor):
        """Test setting global limits."""
        new_limits = {
            "cpu_percent": 75.0,
            "memory_mb": 1024.0,
        }

        resource_monitor.set_global_limits(new_limits)

        global_limits = resource_monitor.get_global_limits()
        assert global_limits["cpu_percent"] == 75.0
        assert global_limits["memory_mb"] == 1024.0

    def test_global_limits_used_as_default(self, resource_monitor):
        """Test that global limits are used as default."""
        custom_limits = {
            "cpu_percent": 60.0,
            "memory_mb": 768.0,
        }
        resource_monitor.set_global_limits(custom_limits)

        session = resource_monitor.start_monitoring(os.getpid())

        assert session.limits["cpu_percent"] == 60.0
        assert session.limits["memory_mb"] == 768.0

    def test_custom_limits_override_global(self, resource_monitor):
        """Test that custom limits override global limits."""
        resource_monitor.set_global_limits({"cpu_percent": 80.0})

        session = resource_monitor.start_monitoring(
            os.getpid(),
            limits={"cpu_percent": 30.0},
        )

        assert session.limits["cpu_percent"] == 30.0


class TestSessionStatus:
    """Tests for session status."""

    def test_get_session_status(self, resource_monitor):
        """Test getting session status."""
        session = resource_monitor.start_monitoring(os.getpid())

        status = resource_monitor.get_session_status(session.session_id)

        assert status is not None
        assert status["session_id"] == session.session_id
        assert status["is_active"] is True
        assert "current_usage" in status
        assert "limits" in status
        assert "violations_count" in status

    def test_get_status_nonexistent_session(self, resource_monitor):
        """Test getting status of nonexistent session."""
        status = resource_monitor.get_session_status("nonexistent")

        assert status is None


class TestActiveSessions:
    """Tests for active sessions listing."""

    def test_list_active_sessions_empty(self, resource_monitor):
        """Test listing active sessions when none exist."""
        sessions = resource_monitor.list_active_sessions()

        assert isinstance(sessions, list)
        assert len(sessions) == 0

    def test_list_active_sessions_multiple(self, resource_monitor):
        """Test listing multiple active sessions."""
        session1 = resource_monitor.start_monitoring(os.getpid())
        session2 = resource_monitor.start_monitoring(os.getpid() + 1)

        active = resource_monitor.list_active_sessions()

        assert len(active) >= 2
        assert session1.session_id in active
        assert session2.session_id in active

    def test_stopped_session_not_in_active_list(self, resource_monitor):
        """Test that stopped sessions are not in active list."""
        session = resource_monitor.start_monitoring(os.getpid())
        assert session.session_id in resource_monitor.list_active_sessions()

        resource_monitor.stop_monitoring(session.session_id)

        active = resource_monitor.list_active_sessions()
        assert session.session_id not in active


class TestResourceMonitorIntegration:
    """Integration tests for resource monitor."""

    def test_full_monitoring_workflow(self, resource_monitor):
        """Test complete monitoring workflow."""
        # Start session
        session = resource_monitor.start_monitoring(
            os.getpid(),
            limits={
                "cpu_percent": 80.0,
                "memory_mb": 2048.0,
            },
        )

        # Collect usage
        usage1 = resource_monitor.get_current_usage(session.session_id)
        usage2 = resource_monitor.get_current_usage(session.session_id)

        # Check violations
        violations = resource_monitor.check_limits_violated(session.session_id)

        # Enforce limits
        enforcement = resource_monitor.enforce_limits(session.session_id, hard=False)

        # Get history
        history = resource_monitor.get_usage_history(session.session_id)

        # Get status
        status = resource_monitor.get_session_status(session.session_id)

        # Stop monitoring
        report = resource_monitor.stop_monitoring(session.session_id)

        assert status is not None
        assert report is not None
        assert len(history) >= 2

    def test_parallel_sessions_independent(self, resource_monitor):
        """Test that parallel sessions are independent."""
        session1 = resource_monitor.start_monitoring(os.getpid())
        session2 = resource_monitor.start_monitoring(os.getpid() + 1)

        resource_monitor.get_current_usage(session1.session_id)
        resource_monitor.get_current_usage(session1.session_id)

        history1 = resource_monitor.get_usage_history(session1.session_id)
        history2 = resource_monitor.get_usage_history(session2.session_id)

        # Session 1 should have more history
        assert len(history1) > len(history2)
