# 📬 Micronaut AWS SQS Consumer Reference Boilerplate

Exemplo completo e canônico de Listener SQS em Micronaut com verificação de idempotência, DLQ, backoff exponencial e execução em thread pool dedicada.

```java
package com.portfolio.messaging.consumer;

import com.portfolio.messaging.dto.OrderEventPayload;
import com.portfolio.messaging.service.IdempotencyService;
import com.portfolio.messaging.service.OrderProcessingService;
import io.micronaut.jms.sqs.annotation.Queue;
import io.micronaut.messaging.annotation.MessageBody;
import io.micronaut.messaging.annotation.MessageHeader;
import io.micronaut.scheduling.TaskExecutors;
import io.micronaut.scheduling.annotation.ExecuteOn;
import jakarta.inject.Singleton;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

@Singleton
public class OrderSqsConsumer {

    private static final Logger LOG = LoggerFactory.getLogger(OrderSqsConsumer.class);

    private final IdempotencyService idempotencyService;
    private final OrderProcessingService processingService;

    public OrderSqsConsumer(IdempotencyService idempotencyService, OrderProcessingService processingService) {
        this.idempotencyService = idempotencyService;
        this.processingService = processingService;
    }

    @Queue(value = "${aws.sqs.orders-queue}")
    @ExecuteOn(TaskExecutors.BLOCKING)
    public void receiveOrderEvent(
            @MessageBody OrderEventPayload payload,
            @MessageHeader("MessageId") String messageId) {

        LOG.info("Consumindo mensagem SQS. messageId={}, eventId={}", messageId, payload.eventId());

        // 1. Verificação de Idempotência
        if (idempotencyService.isAlreadyProcessed(payload.eventId())) {
            LOG.warn("Mensagem duplicada ignorada. eventId={}", payload.eventId());
            return;
        }

        try {
            // 2. Processamento de Negócio
            processingService.process(payload);

            // 3. Marcação de Conclusão com Sucesso
            idempotencyService.markAsProcessed(payload.eventId());
            LOG.info("Mensagem processada com sucesso. eventId={}", payload.eventId());

        } catch (Exception ex) {
            LOG.error("Falha ao processar mensagem SQS. messageId={}, eventId={}. Encaminhando para retry/DLQ.", 
                messageId, payload.eventId(), ex);
            // Relançar para acionar Visibility Timeout / Redrive Policy para DLQ
            throw ex;
        }
    }
}
```
