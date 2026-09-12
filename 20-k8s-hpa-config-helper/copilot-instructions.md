# Kubernetes HPA Config Helper (GitHub Copilot)

When generating or editing Kubernetes Horizontal Pod Autoscaler (HPA) manifests:

1. **API Version**: Use modern `autoscaling/v2`.
2. **Availability**: Enforce `minReplicas` $\ge 2$ for high availability across nodes.
3. **Flapping Prevention**: Always specify a `scaleDown` stabilization window (e.g. 300 seconds) in the `behavior` block.
4. **Metrics**: Target CPU `averageUtilization` (e.g. 70%) rather than memory alone for JVM applications.
