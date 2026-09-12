# AWS SQS Consumer Scaffold (GitHub Copilot)

When generating or refactoring AWS SQS consumers in Java/Micronaut:

1. **Idempotency & Retries**:
   - Enforce an idempotency check using a unique message/event key before applying business logic.
   - Do not catch and suppress exceptions; let them bubble up to allow SQS visibility timeout and Dead Letter Queue (DLQ) redrive.

2. **Concurrency & Threading**:
   - Always offload listener execution using `@ExecuteOn(TaskExecutors.BLOCKING)` or virtual threads to avoid blocking Netty threads.

3. **External Configuration**:
   - Bind queue URLs to application configuration properties (`@Queue("${aws.sqs.queue-name}")`).
