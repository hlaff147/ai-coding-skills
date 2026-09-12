---
name: aws-sqs-consumer-scaffold
description: >-
  Gera listeners e consumers de filas AWS SQS no Micronaut com controle de idempotência, tratamento de DLQ, retry exponencial e execução não-bloqueante. Acione ao pedir para criar, configurar ou revisar consumers de mensageria SQS.
---

# 📬 AWS SQS Consumer Scaffold (Micronaut)

Gera boilerplate robusto para processamento de mensagens de filas AWS SQS em microsserviços Java com Micronaut, garantindo resiliência, idempotência e tratamento adequado de Dead Letter Queue (DLQ).

---

## 🚫 Restrições Negativas Críticas

- **NUNCA consuma mensagens sem verificação de idempotência**: Filas SQS padrão garantem entrega *at-least-once*, podendo reenviar mensagens idênticas.
- **NUNCA capture exceções silenciosamente sem rethrow**: Engolir exceções confirma o recebimento indevido para a AWS (`delete-message`), descartando mensagens com erro sem acionar retry ou DLQ.
- **NUNCA execute I/O de consumer na thread de polling do Netty**: Sempre anote métodos com `@ExecuteOn(TaskExecutors.BLOCKING)` ou configure Virtual Threads.
- **NUNCA faça hardcode de nomes de filas**: Utilize injeção de propriedades (`${aws.sqs.queue-name}`) configuradas no `application.yml`.

---

## 📋 Arquitetura do Consumer SQS

1. **Injeção e Configuração:**
   - Use `@Singleton` e `@Queue(value = "${aws.sqs.queue-name}")`.
   - Injection por construtor com campos `final`.
2. **Ciclo de Vida da Mensagem:**
   - Validar chave única de idempotência (`payload.eventId()` ou `messageId`).
   - Se já processado: registrar log e retornar imediatamente.
   - Se novo: executar regra de negócio, marcar como concluído no banco/cache e concluir transação.
   - Em caso de falha: relançar exceção para que o SQS mantenha a mensagem no Visibility Timeout e acione a Redrive Policy para a DLQ após o número de tentativas (`maxReceiveCount`).
3. 📖 *Implementação de Referência Completa:* [references/consumer-boilerplate.md](./references/consumer-boilerplate.md)

---

## ⚙️ Configuração no `application.yml`
```yaml
aws:
  sqs:
    orders-queue: "https://sqs.us-east-1.amazonaws.com/123456789012/order-events-queue"
    orders-dlq: "https://sqs.us-east-1.amazonaws.com/123456789012/order-events-dlq"
```
