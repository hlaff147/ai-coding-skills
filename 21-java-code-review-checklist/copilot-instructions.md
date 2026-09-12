# Java & Micronaut Code Review Checklist (GitHub Copilot)

When performing code reviews on Java 21+ and Micronaut 4+ files:

1. **Check Non-Blocking Execution**: Ensure blocking database or network calls are dispatched off the Netty event loop via `@ExecuteOn(TaskExecutors.BLOCKING)`.
2. **Check Constructor Injection**: Disallow `@Inject` on private member fields. Require constructor injection with `final` fields.
3. **Prevent N+1 Queries**: Ensure Micronaut Data queries fetch required relationships using `@Join(..., type = Join.Type.FETCH)`.
4. **Data Integrity & Security**: Check that incoming request DTOs are Java Records annotated with `@Valid`, and logs do not expose sensitive customer PII.
