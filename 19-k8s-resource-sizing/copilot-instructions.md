# Kubernetes Resource Sizing (GitHub Copilot)

When sizing Kubernetes pod resources for Java/Micronaut applications:

1. **Memory Calculations**:
   - Always leave 25-30% buffer between JVM max heap (`-Xmx` or `MaxRAMPercentage`) and container `limits.memory` for Metaspace, thread stacks, and Netty direct memory.
   - Example: For 512Mi heap, set container memory limit to 768Mi.

2. **CPU Limits & Throttling**:
   - Do not constrain CPU limits too tightly; allow bursting during startup and request peaks to avoid Linux CFS throttling.

3. **Guaranteed QoS**:
   - Set `requests.memory` equal to `limits.memory` for production latency-sensitive pods to avoid node evictions.
