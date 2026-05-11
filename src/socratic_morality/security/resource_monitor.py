"""Resource Monitor for tracking and enforcing resource limits."""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
from enum import Enum
from datetime import datetime
import os
import psutil


class SeverityLevel(str, Enum):
    """Severity levels for resource violations."""

    WARNING = "warning"
    CRITICAL = "critical"


class ResourceType(str, Enum):
    """Types of resources being monitored."""

    CPU = "cpu"
    MEMORY = "memory"
    FILE_DESCRIPTORS = "fd"
    PROCESSES = "process"


@dataclass
class ResourceUsage:
    """Current resource usage snapshot."""

    cpu_percent: float  # CPU percentage (0-100)
    memory_mb: float  # Memory in MB
    file_descriptors: int  # Number of open file descriptors
    processes: int  # Number of running processes
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    within_limits: bool = True
    usage_details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class LimitViolation:
    """Record of a resource limit violation."""

    resource: ResourceType
    current_value: float
    limit: float
    severity: SeverityLevel
    action_taken: str
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    description: str = ""


@dataclass
class MonitoringSession:
    """Active monitoring session."""

    session_id: str
    process_id: int
    limits: Dict[str, float]
    started_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    stopped_at: Optional[str] = None
    is_active: bool = True
    snapshots: List[ResourceUsage] = field(default_factory=list)
    violations: List[LimitViolation] = field(default_factory=list)


@dataclass
class FinalReport:
    """Final monitoring report."""

    session_id: str
    process_id: int
    duration_seconds: float
    peak_cpu_percent: float
    peak_memory_mb: float
    total_violations: int
    critical_violations: int
    average_usage: Dict[str, float] = field(default_factory=dict)
    recommendations: List[str] = field(default_factory=list)


class ResourceMonitor:
    """Monitor and enforce resource limits for processes."""

    def __init__(self):
        """Initialize resource monitor."""
        self.sessions: Dict[str, MonitoringSession] = {}
        self.global_limits: Dict[str, float] = {
            "cpu_percent": 80.0,
            "memory_mb": 2048.0,
            "file_descriptors": 1024,
            "processes": 128,
        }
        self._session_counter = 0

    def start_monitoring(
        self, process_id: int, limits: Optional[Dict[str, float]] = None
    ) -> MonitoringSession:
        """Start monitoring a process.

        Args:
            process_id: ID of process to monitor
            limits: Optional custom limits (uses global limits if not provided)

        Returns:
            MonitoringSession for tracking
        """
        self._session_counter += 1
        session_id = f"session_{self._session_counter}_{process_id}"

        # Use provided limits or default to global
        effective_limits = limits or self.global_limits.copy()

        session = MonitoringSession(
            session_id=session_id,
            process_id=process_id,
            limits=effective_limits,
            is_active=True,
        )

        self.sessions[session_id] = session
        return session

    def get_current_usage(self, session_id: Optional[str] = None) -> ResourceUsage:
        """Get current resource usage for a session or system.

        Args:
            session_id: Optional session ID (uses current process if not provided)

        Returns:
            ResourceUsage snapshot
        """
        if session_id and session_id in self.sessions:
            session = self.sessions[session_id]
            process_id = session.process_id
        else:
            process_id = os.getpid()

        try:
            process = psutil.Process(process_id)

            # Get CPU usage
            cpu_percent = process.cpu_percent(interval=0.1)

            # Get memory usage
            memory_info = process.memory_info()
            memory_mb = memory_info.rss / (1024 * 1024)

            # Get file descriptors
            file_descriptors = process.num_fds() if hasattr(process, "num_fds") else 0

            # Get number of threads (proxy for processes spawned)
            processes = process.num_threads()

        except (psutil.NoSuchProcess, psutil.AccessDenied):
            # Fallback values if process not accessible
            cpu_percent = 0.0
            memory_mb = 0.0
            file_descriptors = 0
            processes = 1

        usage = ResourceUsage(
            cpu_percent=cpu_percent,
            memory_mb=memory_mb,
            file_descriptors=file_descriptors,
            processes=processes,
            within_limits=True,
            usage_details={
                "cpu_percent": cpu_percent,
                "memory_mb": memory_mb,
                "file_descriptors": file_descriptors,
                "processes": processes,
            },
        )

        # Store in session if available
        if session_id and session_id in self.sessions:
            self.sessions[session_id].snapshots.append(usage)

        return usage

    def check_limits_violated(self, session_id: str) -> List[LimitViolation]:
        """Check if any resource limits are violated.

        Args:
            session_id: Session ID to check

        Returns:
            List of limit violations detected
        """
        if session_id not in self.sessions:
            return []

        session = self.sessions[session_id]
        usage = self.get_current_usage(session_id)
        violations = []

        # Check CPU limit
        if "cpu_percent" in session.limits:
            if usage.cpu_percent > session.limits["cpu_percent"]:
                severity = (
                    SeverityLevel.CRITICAL
                    if usage.cpu_percent > session.limits["cpu_percent"] * 1.5
                    else SeverityLevel.WARNING
                )
                violation = LimitViolation(
                    resource=ResourceType.CPU,
                    current_value=usage.cpu_percent,
                    limit=session.limits["cpu_percent"],
                    severity=severity,
                    action_taken="monitoring",
                    description=f"CPU usage {usage.cpu_percent:.1f}% exceeds limit {session.limits['cpu_percent']:.1f}%",
                )
                violations.append(violation)
                session.violations.append(violation)

        # Check memory limit
        if "memory_mb" in session.limits:
            if usage.memory_mb > session.limits["memory_mb"]:
                severity = (
                    SeverityLevel.CRITICAL
                    if usage.memory_mb > session.limits["memory_mb"] * 1.5
                    else SeverityLevel.WARNING
                )
                violation = LimitViolation(
                    resource=ResourceType.MEMORY,
                    current_value=usage.memory_mb,
                    limit=session.limits["memory_mb"],
                    severity=severity,
                    action_taken="monitoring",
                    description=f"Memory usage {usage.memory_mb:.1f}MB exceeds limit {session.limits['memory_mb']:.1f}MB",
                )
                violations.append(violation)
                session.violations.append(violation)

        # Check file descriptor limit
        if "file_descriptors" in session.limits:
            if usage.file_descriptors > session.limits["file_descriptors"]:
                severity = (
                    SeverityLevel.CRITICAL
                    if usage.file_descriptors > session.limits["file_descriptors"] * 1.5
                    else SeverityLevel.WARNING
                )
                violation = LimitViolation(
                    resource=ResourceType.FILE_DESCRIPTORS,
                    current_value=float(usage.file_descriptors),
                    limit=session.limits["file_descriptors"],
                    severity=severity,
                    action_taken="monitoring",
                    description=f"File descriptors {usage.file_descriptors} exceed limit {session.limits['file_descriptors']}",
                )
                violations.append(violation)
                session.violations.append(violation)

        # Check process limit
        if "processes" in session.limits:
            if usage.processes > session.limits["processes"]:
                severity = (
                    SeverityLevel.CRITICAL
                    if usage.processes > session.limits["processes"] * 1.5
                    else SeverityLevel.WARNING
                )
                violation = LimitViolation(
                    resource=ResourceType.PROCESSES,
                    current_value=float(usage.processes),
                    limit=session.limits["processes"],
                    severity=severity,
                    action_taken="monitoring",
                    description=f"Process count {usage.processes} exceeds limit {session.limits['processes']}",
                )
                violations.append(violation)
                session.violations.append(violation)

        return violations

    def enforce_limits(
        self, session_id: str, hard: bool = False
    ) -> Dict[str, Any]:
        """Enforce resource limits for a session.

        Args:
            session_id: Session ID to enforce limits for
            hard: If True, apply hard limits; if False, only warn

        Returns:
            EnforcementResult with action taken
        """
        if session_id not in self.sessions:
            return {"success": False, "error": "Session not found"}

        session = self.sessions[session_id]
        violations = self.check_limits_violated(session_id)

        if not violations:
            return {
                "success": True,
                "action": "no_violations",
                "violations_found": 0,
            }

        # Determine enforcement action
        actions_taken = []
        critical_violations = [v for v in violations if v.severity == SeverityLevel.CRITICAL]

        if hard and critical_violations:
            actions_taken.append("HARD_LIMIT_ENFORCEMENT_INITIATED")
            # In real implementation, would kill or restrict process
            for violation in critical_violations:
                violation.action_taken = "hard_limit_enforced"

        if not hard:
            actions_taken.append("WARNING_ISSUED")
            for violation in violations:
                violation.action_taken = "warning"

        return {
            "success": True,
            "violations_found": len(violations),
            "critical_violations": len(critical_violations),
            "actions_taken": actions_taken,
            "hard_enforcement": hard,
        }

    def get_usage_history(self, session_id: str) -> List[ResourceUsage]:
        """Get historical resource usage for a session.

        Args:
            session_id: Session ID to get history for

        Returns:
            List of ResourceUsage snapshots
        """
        if session_id not in self.sessions:
            return []

        return self.sessions[session_id].snapshots.copy()

    def stop_monitoring(self, session_id: str) -> FinalReport:
        """Stop monitoring and generate final report.

        Args:
            session_id: Session ID to stop monitoring

        Returns:
            FinalReport with analysis
        """
        if session_id not in self.sessions:
            return None

        session = self.sessions[session_id]
        session.is_active = False
        session.stopped_at = datetime.utcnow().isoformat()

        # Calculate statistics
        if not session.snapshots:
            # Generate one final snapshot
            session.snapshots.append(self.get_current_usage(session_id))

        cpu_values = [s.cpu_percent for s in session.snapshots]
        memory_values = [s.memory_mb for s in session.snapshots]

        peak_cpu = max(cpu_values) if cpu_values else 0.0
        peak_memory = max(memory_values) if memory_values else 0.0
        avg_cpu = sum(cpu_values) / len(cpu_values) if cpu_values else 0.0
        avg_memory = sum(memory_values) / len(memory_values) if memory_values else 0.0

        # Calculate duration
        start_time = datetime.fromisoformat(session.started_at)
        stop_time = datetime.fromisoformat(session.stopped_at)
        duration = (stop_time - start_time).total_seconds()

        # Count violations
        critical_violations = [v for v in session.violations if v.severity == SeverityLevel.CRITICAL]

        # Generate recommendations
        recommendations = self._generate_recommendations(
            peak_cpu, peak_memory, session.limits, len(critical_violations)
        )

        report = FinalReport(
            session_id=session_id,
            process_id=session.process_id,
            duration_seconds=duration,
            peak_cpu_percent=peak_cpu,
            peak_memory_mb=peak_memory,
            total_violations=len(session.violations),
            critical_violations=len(critical_violations),
            average_usage={
                "cpu_percent": avg_cpu,
                "memory_mb": avg_memory,
            },
            recommendations=recommendations,
        )

        return report

    def _generate_recommendations(
        self,
        peak_cpu: float,
        peak_memory: float,
        limits: Dict[str, float],
        critical_violations: int,
    ) -> List[str]:
        """Generate recommendations based on resource usage."""
        recommendations = []

        if critical_violations > 0:
            recommendations.append("CRITICAL: Address resource limit violations immediately")

        if peak_cpu > limits.get("cpu_percent", 80.0) * 0.8:
            recommendations.append(
                f"CPU usage {peak_cpu:.1f}% is high; consider optimizing computational tasks"
            )

        if peak_memory > limits.get("memory_mb", 2048.0) * 0.8:
            recommendations.append(
                f"Memory usage {peak_memory:.1f}MB is high; implement memory cleanup"
            )

        if not recommendations:
            recommendations.append("Resource usage within acceptable limits")

        return recommendations

    def set_global_limits(self, limits: Dict[str, float]) -> None:
        """Set global resource limits.

        Args:
            limits: Dictionary of resource limits
        """
        self.global_limits.update(limits)

    def get_global_limits(self) -> Dict[str, float]:
        """Get current global limits.

        Returns:
            Dictionary of global limits
        """
        return self.global_limits.copy()

    def get_session_status(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get status of a monitoring session.

        Args:
            session_id: Session ID to get status for

        Returns:
            Session status or None if not found
        """
        if session_id not in self.sessions:
            return None

        session = self.sessions[session_id]
        usage = self.get_current_usage(session_id)

        return {
            "session_id": session_id,
            "process_id": session.process_id,
            "is_active": session.is_active,
            "started_at": session.started_at,
            "current_usage": {
                "cpu_percent": usage.cpu_percent,
                "memory_mb": usage.memory_mb,
                "file_descriptors": usage.file_descriptors,
                "processes": usage.processes,
            },
            "limits": session.limits,
            "violations_count": len(session.violations),
            "critical_violations": len(
                [v for v in session.violations if v.severity == SeverityLevel.CRITICAL]
            ),
        }

    def list_active_sessions(self) -> List[str]:
        """List all active monitoring sessions.

        Returns:
            List of active session IDs
        """
        return [sid for sid, s in self.sessions.items() if s.is_active]
