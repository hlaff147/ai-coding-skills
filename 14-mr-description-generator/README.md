# 🚀 GitLab Merge Request Description Generator

> **Gera descrições técnicas, estruturadas e de alto impacto para Merge Requests no GitLab a partir de diffs, histórico de commits ou anotações rápidas.**

---

## 🎯 O Problema

- **Descrições vazias ou rasas**: Desenvolvedores frequentemente abrem MRs com descrições de uma linha ("fix bug", "nova feature"), forçando revisores a deduzir a intenção analisando linha por linha de diff.
- **Falta de evidência de teste**: Sem instruções claras de como testar, o code review fica lento e propenso a deixar passar regressões.
- **Riscos ocultos**: Alterações em banco de dados, variáveis de ambiente ou contratos de mensageria (SQS/SNS) sobem sem plano de rollback explícito.

---

## ✅ A Solução

Esta skill padroniza o formato de submissão de código através de um template estruturado para engenheiros seniores:
1. **Contexto e Motivação**: Vinculação a tickets e propósito de negócio.
2. **O Que Foi Feito**: Resumo técnico segmentado por arquitetura.
3. **Como Testar**: Instruções reproduzíveis (cURL, endpoints, logs).
4. **Avaliação de Risco & Rollback**: Análise de blast radius e contingência.
5. **Checklist Pré-Merge**: Validação de segurança, convenções e tags de deploy (`#deployuat #auto`).

---

## 💬 Exemplo de Uso (Simulação)

### Entrada do Usuário:
```text
Crie a descrição do MR para o ticket PAY-842.
Acabei de adicionar retry com backoff exponencial no consumer SQS de pagamentos
e criei a tabela de idempotência com migration Flyway V4__create_idempotency_table.sql.
```

### Resposta Gerada pela Skill:
````markdown
## 🎯 Contexto e Motivação
- **Issue/Ticket:** `PAY-842`
- **Tipo:** Refactor / Reliability
- **Resumo:** Implementação de processamento idempotente e política de retry com backoff exponencial no consumer SQS de eventos de pagamento, prevenindo duplicidade de cobranças e sobrecarga em instabilidades transitórias.

---

## 🛠️ O que foi feito?
- **[PaymentConsumer]:** Adicionada anotação `@Retryable` com backoff exponencial e Dead Letter Queue (DLQ) após 3 tentativas.
- **[Database / Flyway]:** Criada migration `V4__create_idempotency_table.sql` com chave primária em `idempotency_key` e índice único.
- **[IdempotencyService]:** Implementado lock otimista e verificação prévia de processamento antes de debitar.

---

## 🧪 Como Testar / Evidências
1. Subir a stack local com LocalStack e PostgreSQL via `docker-compose up -d`.
2. Publicar mensagem duplicada na fila de pagamentos:
   ```bash
   aws --endpoint-url=http://localhost:4566 sqs send-message \
     --queue-url http://localhost:4566/000000000000/payment-queue \
     --message-body '{"transactionId": "tx-123", "amount": 100.00}'
   ```
3. Conferir nos logs que a segunda mensagem foi ignorada por duplicidade (`Payment already processed`).
- [x] Testes unitários executados (`./gradlew test`)
- [x] Teste de idempotência validado com Testcontainers

---

## ⚠️ Avaliação de Risco & Rollback
- **Nível de Risco:** Médio (criação de nova tabela em banco relacional).
- **Breaking Changes:** Não.
- **Impacto em Produção:** Se a tabela falhar em ser criada, os consumers SQS pausarão o consumo até a correção.
- **Plano de Rollback:** Reverter imagem para a versão anterior (`git revert`) e aplicar migration compensatória se necessário.

---

## 🚢 Checklist Pré-Merge
- [x] Padrões Micronaut AOT e injeção por construtor validados
- [x] Sem credenciais ou secrets no código
- [x] Logs estruturados sem dados de cartão ou PII
- [ ] Confirmação de deploy UAT (`#deployuat #auto`)
````

---

## 🔧 Formatos Suportados
- **Antigravity / Gemini:** `SKILL.md`
- **Cursor:** `.cursorrules`
- **GitHub Copilot:** `copilot-instructions.md`
