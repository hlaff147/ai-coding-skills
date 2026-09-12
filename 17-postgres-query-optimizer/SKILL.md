---
name: postgres-query-optimizer
description: >-
  Otimiza consultas SQL e analisa planos de execução (EXPLAIN ANALYZE) no PostgreSQL e Amazon Aurora RDS.
  Acione sempre que o usuário colar uma query lenta, plano de execução EXPLAIN, pedir recomendação de
  índices (B-Tree, Parcial, Composto), otimização de joins ou mitigação de locks em banco relacional.
---

# 🐘 PostgreSQL & Aurora RDS Query Optimizer

Otimizador especializado de consultas SQL para PostgreSQL e Amazon Aurora RDS. Identifica gargalos de I/O, sequential scans, buffer churn e sugere índices eficientes e reescritas sargables.

---

## 🚫 Restrições Negativas Críticas

- **NUNCA sugira `CREATE INDEX` sem `CONCURRENTLY` em tabelas de produção**: No PostgreSQL e Aurora, criar índice sem `CONCURRENTLY` adquire um lock exclusivo `SHARE` na tabela, bloqueando todos os `INSERT`, `UPDATE` e `DELETE`.
- **NUNCA ignore o cabeçalho `EXPLAIN (ANALYZE, BUFFERS)`**: Se o usuário fornecer apenas `EXPLAIN`, solicite sempre que execute com `EXPLAIN (ANALYZE, BUFFERS)` para analisar I/O real (`shared read/hit`) e desvios de linhas estimadas vs reais.
- **NUNCA indexe indiscriminadamente colunas com baixa cardinalidade**: Índices em colunas como `status` (booleano ou com poucos valores) são frequentemente ignorados pelo otimizador a menos que combinados em **índice parcial** (`WHERE status = 'PENDING'`).
- **NUNCA aplique funções em colunas indexadas no `WHERE`**: Proíba expressões como `WHERE DATE(created_at) = ...` ou `WHERE LOWER(email) = ...`. Recomende operadores de intervalo (`>= / <`) ou crie **Expression Indexes**.

---

## 🧭 Checklist de Análise de Plano de Execução

Ao analisar um plano `EXPLAIN (ANALYZE, BUFFERS)`, verifique sempre:

1. **Seq Scan em tabelas grandes**:
   - `Filter: (...)` com `Rows Removed by Filter` alto indica ausência de índice seletivo.
2. **Discrepância entre Linhas Estimadas e Reais**:
   - `rows=10` estimado vs `rows=500000` real indica que as estatísticas do planejador estão obsoletas (requer `ANALYZE nome_tabela`).
3. **I/O e Buffers (`shared hit` vs `shared read`)**:
   - Alto `shared read` indica leituras em disco (IOPS altos no Aurora RDS).
4. **Sort Method**:
   - `Sort Method: external merge Disk` indica que a ordenação estourou a memória de trabalho do banco (`work_mem`).

---

## 📋 Protocolo de Recomendação

Toda análise deve conter três seções claras:

### 1. 🔍 Diagnóstico do Gargalo
Explique sucintamente onde o plano está gastando tempo ou I/O:
*Exemplo: "O plano gasta 92% do tempo realizando um Seq Scan de 2.5 milhões de linhas na tabela `transactions`, removendo 2.49 milhões pelo filtro `status = 'WAITING_PAYMENT' AND created_at >= ...`."*

### 2. ⚡ DDL de Índice Recomendado (Safe for Production)
Forneça sempre o comando com `CONCURRENTLY`:

```sql
-- Criação de índice concorrente não-bloqueante para Aurora/Postgres
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_transactions_status_created_at
ON transactions (created_at DESC)
WHERE status = 'WAITING_PAYMENT';
```

*(Dica: use índice parcial sempre que o filtro buscar apenas um subset de dados frequentes).*

### 3. ✍️ Reescrita Sargable da Query (Se Aplicável)

#### ❌ Anti-padrão (Não Sargable):
```sql
SELECT id, customer_id, amount
FROM orders
WHERE DATE(created_at) = '2026-09-12';
```

#### ✅ Padrão Otimizado (Sargable):
```sql
SELECT id, customer_id, amount
FROM orders
WHERE created_at >= '2026-09-12 00:00:00'
  AND created_at < '2026-09-13 00:00:00';
```
*(Permite uso direto de índice B-tree comum em `created_at` sem scan de função).*
