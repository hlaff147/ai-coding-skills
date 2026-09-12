# Kubernetes Pod Troubleshooting (GitHub Copilot)

When analyzing Kubernetes pod issues, CrashLoopBackOff, or deployment failures:

1. **Check Exit Codes First**:
   - Exit Code 137: Container killed by OOM (Out Of Memory). Check `limits.memory` vs JVM `-Xmx` / off-heap memory.
   - Exit Code 1: Unhandled application exception on startup. Ask for `kubectl logs <pod> --previous`.
   - Exit Code 143: Pod terminated via SIGTERM due to probe failure or node eviction.

2. **Provide Actionable Diagnosis**:
   - Identify the exact root cause from the provided `describe` or `logs`.
   - Supply CLI debugging commands (`kubectl describe pod`, `kubectl logs -p`).
   - Supply remediation patches for YAML manifests (`startupProbe`, `resources.requests`, `resources.limits`).
