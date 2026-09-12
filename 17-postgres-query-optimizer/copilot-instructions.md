# PostgreSQL & Aurora Query Optimizer (GitHub Copilot)

When optimizing SQL queries or diagnosing slow queries in PostgreSQL / Amazon Aurora:

1. **Production Index Safety**:
   - Always suggest `CREATE INDEX CONCURRENTLY IF NOT EXISTS` to prevent table write locks.

2. **Query Sargability**:
   - Never use functions on indexed columns in `WHERE` clauses (e.g. replace `WHERE DATE(col) = '2026-09-12'` with range queries `col >= '...' AND col < '...'`).

3. **Plan Evaluation**:
   - When reviewing execution plans, prioritize eliminating expensive `Seq Scan` on large tables and resolving disk-based sorts (`Sort Method: external merge Disk`).
