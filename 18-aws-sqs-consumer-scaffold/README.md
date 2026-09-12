# 📬 AWS SQS Consumer Scaffold (Micronaut)

> **Gera boilerplate resiliente e desacoplado para consumo de filas AWS SQS em microsserviços Java com Micronaut, com controle de idempotência, DLQ e offloading de threads.**

---

## 🎯 O Problema

- **Duplicidade de Mensagens**: O SQS garante entrega no modelo *at-least-once*. Sem validação de idempotência, pagamentos, faturamentos ou cadastros são duplicados sob instabilidade de rede.
- **Descarte Indevido de Mensagens**: Capturar exceções com blocos `try-catch` vazios faz o cliente SQS deletar a mensagem da fila sem que o retry ou a Dead Letter Queue (DLQ) sejam acionados.
- **Bloqueio da Thread do Framework**: Rodar processamentos pesados diretamente na thread de I/O do Netty derruba a vazão global do microsserviço.

---

## ✅ A Solução

Esta skill automatiza a implementação de consumers sênior em Micronaut:
1. **Padrão de Idempotência**: Checagem de evento antes do processamento e confirmação transacional após o sucesso.
2. **Ciclo de Vida Resiliente**: Propagação controlada de erros para permitir que a política de redrive do SQS direcione falhas persistentes para a DLQ.
3. **Isolamento de Threads**: Uso de `@ExecuteOn(TaskExecutors.BLOCKING)` ou Virtual Threads.

---

## 💬 Exemplo de Uso (Simulação)

### Entrada do Usuário:
```text
Crie um consumer SQS em Micronaut para a fila order-events-queue,
recebendo um OrderCreatedEvent e garantindo que pedidos duplicados não sejam processados.
```

### Saída da Skill:
- Gera a classe `@Singleton` com anotação `@Queue`.
- Injeta o serviço de idempotência.
- Trata logs com `messageId` para correlação com CloudWatch / New Relic.
- Guia a configuração do `application.yml`.

Consulte o código completo em [references/consumer-boilerplate.md](./references/consumer-boilerplate.md).
