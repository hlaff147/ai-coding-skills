---
name: java-micronaut-standards
description: >-
  Enforces modern Java 21+ and Micronaut 4+ idiomatic standards, Ahead-of-Time (AOT) compilation,
  reflection-free dependency injection, compile-time Micronaut Data repositories, GraalVM native
  readiness, and @MicronautTest patterns. Activate when writing, reviewing, or generating Micronaut code.
---

# 🚀 Java & Micronaut 4+ Standards

Enforces Ahead-of-Time (AOT) compilation idioms, reflection-free dependency injection, compile-time Micronaut Data JPA practices, and GraalVM native image compatibility.

---

## 🚫 Critical Negative Constraints (Anti-Patterns)

- **NEVER import Spring Framework classes**: Ban `org.springframework.*` (`@Service`, `@Autowired`, `@Component`, `@RestController`).
- **NEVER use field injection**: Ban `@Inject` or `@Autowired` on private instance variables. Use constructor injection exclusively.
- **NEVER use legacy Java EE namespaces**: Ban `javax.*` imports — use `jakarta.*` (`jakarta.inject.*`, `jakarta.persistence.*`, `jakarta.validation.*`).
- **NEVER block the Netty event loop**: Offload blocking I/O (JDBC, HTTP calls) with `@ExecuteOn(TaskExecutors.BLOCKING)` or Java 21+ Virtual Threads.
- **NEVER use dynamic reflection or runtime bytecode generation**: Ban runtime reflection, `java.lang.reflect.Proxy`, or CGLIB proxies. Everything must be discoverable at compile-time for GraalVM Native Image compatibility.
- **NEVER return `null` for query results**: Return `Optional<T>` for single entities or immutable collections (`List.of()`, `Set.of()`).

---

## 🧩 1. Dependency Injection & AOT Architecture

- **Constructor Injection**: Inject dependencies exclusively via explicit constructors with `final` fields.
- **Jakarta Scopes**: Use `jakarta.inject.Singleton` as default bean scope. Use `@Prototype` or `@RequestScope` only when state dictates.
- **Factory Beans**: Use `@Factory` classes with `@Singleton` producer methods for external library beans.
- **Conditional Wiring**: Use `@Requires(property = "feature.enabled", value = "true")` or `@Requires(env = "dev")`.

---

## 🌐 2. HTTP Controllers & Routing

- **Controller Definition**: Use `@Controller("/api/v1/resource")` from `io.micronaut.http.annotation.Controller`.
- **HTTP Responses**: Return `io.micronaut.http.HttpResponse<T>` with explicit status codes (`HttpResponse.ok()`, `HttpResponse.created()`, `HttpResponse.noContent()`).
- **DTOs & Serialization**: Use Java Records for DTOs. For POJOs, annotate with `@Introspected` or `@Serdeable` for compile-time reflection-free serializers.
- **Input Validation**: Annotate request payloads with `@Valid` and Jakarta validation annotations (`@NotNull`, `@Size`, `@NotBlank`, `@Positive`).
- 📖 *Full Controller reference implementation:* [references/code-examples.md#1-controller-reference](./references/code-examples.md#1-controller-reference)

---

## 🗄️ 3. Micronaut Data JPA & Repository Layer

- **Declarative Interfaces**: Extend `JpaRepository<Entity, ID>` or `CrudRepository<Entity, ID>` annotated with `@Repository`.
- **Compile-Time Queries**: Leverage method name conventions (`findByStatusAndCreatedAtAfter`) validated during `javac` compilation.
- **N+1 Prevention with Declarative Fetching**: Use `@Join(value = "relation", type = Join.Type.FETCH)` instead of runtime entity graphs.
- **Projections**: Use constructor-expression projections with Java text blocks (`SELECT new ... FROM ...`).
- **Transactions**: Annotate methods with `jakarta.transaction.Transactional`. Use `@Transactional(readOnly = true)` for queries.
- 📖 *Full Repository reference implementation:* [references/code-examples.md#2-repository-reference](./references/code-examples.md#2-repository-reference)

---

## ⚡ 4. Virtual Threads & Concurrency (Java 21+)

- **Virtual Thread Offloading**: Configure virtual threads in `application.yml` (`micronaut.server.thread-selection: AUTO`) or annotate blocking controllers/services with `@ExecuteOn(TaskExecutors.BLOCKING)`.

---

## 🧪 5. Testing with `@MicronautTest`

- **Test Harness**: Use `@MicronautTest` from `io.micronaut.test.extensions.junit5.annotation.MicronautTest`.
- **Injection in Tests**: Inject beans directly into test constructors or test fields with `@Inject`.
- **Assertion Standards**: Use AssertJ (`assertThat(...)`).
- 📖 *Full Test suite reference implementation:* [references/code-examples.md#3-testing-reference](./references/code-examples.md#3-testing-reference)

---

## 🔄 Verification Commands

Before completing tasks on a Micronaut project, verify:
- **Compile & AOT check**: `./gradlew compileJava` or `mvn compile` (verifies annotation processors pass)
- **Unit & Integration tests**: `./gradlew test` or `mvn test`
- **Check for banned imports**:
  ```bash
  ! grep -rn "org.springframework" src/
  ! grep -rn "javax.persistence" src/
  ```
