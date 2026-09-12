---
name: java-code-review-checklist
description: >-
  Revisa código Java 21+ e Micronaut 4+ com base em critérios de engenharia sênior: concorrência, não-bloqueio de Netty, imutabilidade, N+1 queries e segurança. Acione ao pedir code review ou checklist de revisão Java.
---

# 🔍 Java & Micronaut Senior Code Review Checklist

Checklist de revisão de código para times Java 21+ e Micronaut 4+, assegurando performance, resiliência e segurança de produção.

---

## 🚫 Restrições Negativas Críticas

- **NUNCA aprove I/O bloqueante na thread do Netty**: Chamadas JDBC, HTTP síncronas ou leitura em disco sem `@ExecuteOn(TaskExecutors.BLOCKING)` ou Virtual Threads congelam o throughput global.
- **NUNCA tolere injeção por campo (`@Inject` em variáveis privadas)**: Exija sempre injeção exclusiva por construtor com atributos `final`.
- **NUNCA aprove consultas relacionais com risco de N+1**: Exija `@Join(value = "...", type = Join.Type.FETCH)` explícito em repositórios Micronaut Data.
- **NUNCA aprove logs com dados sensíveis (PII/LGPD)**: Bloqueie logs que exponham tokens, CPF, cartões de crédito ou senhas.

---

## 📋 Checklist de 6 Dimensões

### 1. 🧵 Concorrência & Threading
- [ ] Operações de banco ou chamadas HTTP externas estão offloaded da thread principal de eventos?
- [ ] O código é thread-safe? Classes `@Singleton` não possuem estado mutável compartilhado em campos de instância?

### 2. 🛡️ Imutabilidade & Design de Dados
- [ ] DTOs são modelados com Java Records?
- [ ] Coleções expostas retornam cópias imutáveis (`List.copyOf()`, `Collections.unmodifiableList()`)?

### 3. ⚡ Compilação AOT & GraalVM Readiness
- [ ] Há ausência total de reflexão dinâmica não declarada (`Class.forName()`, `Method.invoke()`)?
- [ ] Classes DTO possuem `@Serdeable` ou `@Introspected` para serialização reflection-free?

### 4. 🗄️ Camada de Persistência & Transações
- [ ] Métodos de consulta somente leitura utilizam `@Transactional(readOnly = true)`?
- [ ] Não há `EAGER fetch` implícito em entidades JPA que possa disparar dezenas de queries desnecessárias?

### 5. 🛑 Tratamento de Exceções
- [ ] Exceções capturadas são relançadas com a causa raiz preservada (`throw new BusinessException("msg", ex)`)?
- [ ] Respostas de erro HTTP mapeadas ocultam stack traces internos do usuário final?

### 6. 📝 Observabilidade & Validação
- [ ] Payloads recebidos nos controllers são validados com `@Valid`?
- [ ] Logs contêm identificadores de rastreabilidade (Correlation ID / Trace ID)?
