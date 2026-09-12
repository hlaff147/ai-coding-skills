# 🐘 PostgreSQL & Aurora RDS Query Optimizer

> **Otimizador especializado de consultas SQL para PostgreSQL e Amazon Aurora RDS. Analisa planos EXPLAIN, elimina Sequential Scans e sugere índices concorrentes seguros para produção.**

---

## 🎯 O Problema

- **Downtime e Locks por criação ingênua de índices**: Executar `CREATE INDEX` em tabelas com milhões de registros sem `CONCURRENTLY` adquire lock de exclusividade de escrita (`SHARE lock`), enfileirando requisições e derrubando a aplicação.
- **Sequential Scans silenciosos**: Queries que parecem rápidas em dev degradam drasticamente em produção no Aurora quando o volume de linhas e IOPS dispara.
- **Consultas não-sargables**: O uso de funções como `WHERE LOWER(email) = ...` ou `WHERE DATE(created_at) = ...` invalida índices existentes, forçando o PostgreSQL a varrer a tabela inteira.

---

## ✅ A Solução

Esta skill atua como um DBA sênior automatizado:
1. **Analisa o plano de execução**: Identifica operações que mais consom tempo e I/O (`Buffers: shared read`).
2. **Gera DDLs seguros**: Fornece sempre comandos com `CONCURRENTLY` e avalia o benefício de índices parciais.
3. **Sugere reescritas de SQL**: Transforma predicados não-sargables em condições indexáveis.

---

## 💬 Exemplo de Uso (Simulação)

### Entrada do Usuário:
```text
Minha query de listagem de pedidos pendentes está demorando 4 segundos no Aurora.
Query:
SELECT id, customer_id, total_amount, created_at 
FROM orders 
WHERE status = 'PENDING' 
  AND created_at >= NOW() - INTERVAL '7 days'
ORDER BY created_at DESC;

No EXPLAIN ANALYZE apareceu Seq Scan em 1.800.000 rows.
```

### Resposta Gerada pela Skill:
````markdown
### 🔍 Diagnóstico do Plano
- **Gargalo:** O PostgreSQL está realizando um `Seq Scan` em 1.8M de linhas na tabela `orders`.
- **Filtro de Baixa Seletividade Global:** Apenas uma pequena fração dos pedidos possui status `'PENDING'`, mas como não há índice cobrindo `status` + `created_at`, o planejador precisa ler o heap inteiro do disco.

---

### ⚡ Solução: Índice Parcial Concorrente
Como a busca filtra apenas pedidos pendentes recentes, a melhor abordagem com menor impacto de armazenamento e escrita é um **Índice Parcial**:

```sql
-- Executar em produção com CONCURRENTLY (não bloqueia INSERT/UPDATE)
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_orders_pending_created_at
ON orders (created_at DESC)
WHERE status = 'PENDING';
```

**Por que este índice?**
1. **Tamanho minúsculo:** Indexa apenas as linhas com `status = 'PENDING'`, economizando buffer cache do Aurora.
2. **Index Scan direto:** Atende simultaneamente o filtro `WHERE created_at >= ...` e a cláusula `ORDER BY created_at DESC` sem necessidade de etapa de `Sort` em memória/disco.
````

---

## 🔧 Formatos Suportados
- **Antigravity / Gemini:** `SKILL.md`
- **Cursor:** `.cursorrules`
- **GitHub Copilot:** `copilot-instructions.md`
