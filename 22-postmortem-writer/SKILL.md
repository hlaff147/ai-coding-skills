---
name: postmortem-writer
description: >-
  Estrutura relatórios de postmortem e análise de causa raiz (RCA) de incidentes de produção com linha do tempo, 5 Porquês e planos de ação. Acione ao pedir para redigir postmortem, relatório de incidente ou RCA.
---

# 📝 Incident Postmortem & Root Cause Analysis (RCA) Writer

Estrutura relatórios técnicos pós-incidente (*Blameless Postmortem*) com rigor metodológico, análise de causa raiz via 5 Porquês e plano de ação preventivo mensurável.

---

## 🚫 Restrições Negativas Críticas

- **NUNCA atribua culpa a indivíduos (*Blameless Culture*)**: Incidentes resultam de falhas em processos, salvaguardas ou monitoramento, nunca de erro individual de um desenvolvedor.
- **NUNCA deixe ações sem responsável e ticket**: Todo item de remediação deve conter Dono, Prioridade e ID de Ticket Jira/GitLab.
- **NUNCA aceite respostas superficiais no Porquê**: A causa raiz não é "o pod caiu"; é "por que o pod consumiu memória excessiva? Por que o limit não contemplava off-heap? Por que não havia alerta prévio aos 85%?".

---

## 📋 Template de Postmortem Padrão

```markdown
# 📄 Relatório de Incidente / Postmortem: [Título do Incidente]

- **Data do Incidente:** `[YYYY-MM-DD]`
- **Duração Total:** `[X horas / minutos]` (TTR: Time to Resolve)
- **Severidade:** `[SEV-1 | SEV-2 | SEV-3]`
- **Líder do Incidente:** `[@nome]`
- **Serviços Afetados:** `[Lista de microsserviços / clusters K8s / Bancos]`

---

## 💥 Impacto no Negócio & Usuários
- Quantidade de requisições falhas / pedidos afetados: `[X% de erro, Y usuários impactados]`
- Violação de SLO/SLA: `[Sim/Não - SLI afetado]`

---

## ⏱️ Linha do Tempo (Horário de Brasília / UTC)
- **HH:MM:** Introdução da mudança ou início da anomalia.
- **HH:MM:** Detecção do alerta via New Relic / PagerDuty.
- **HH:MM:** Convocação do war room e início do diagnóstico.
- **HH:MM:** Ação de mitigação aplicada (Rollback / Aumento de HPA / Failover).
- **HH:MM:** Estabilização dos serviços e encerramento do incidente.

---

## 🔍 Análise de Causa Raiz (5 Porquês)
1. **O que falhou?** Ex: As requisições de pagamento começaram a responder HTTP 500.
2. **Por quê?** Porque o banco Aurora PostgreSQL atingiu 100% de CPU.
3. **Por quê?** Porque uma consulta de conciliação executou sem índice, varrendo 15M de linhas em Seq Scan.
4. **Por quê?** Porque a query foi adicionada no último deploy sem review de DBA/análise com EXPLAIN.
5. **Por quê (Causa Raiz)?** Não havia guardrail no CI/CD nem alerta de slow query bloqueando migrações não-indexadas.

---

## 🛠️ Ações Corretivas & Prevenção (SMART)
| Ação Preventiva | Tipo | Prioridade | Responsável | Ticket |
|---|---|:---:|---|---|
| Adicionar índice concorrente na coluna `created_at` | Correção | P0 | @dev | JIRA-101 |
| Configurar alerta no New Relic para queries > 1000ms | Detecção | P1 | @sre | JIRA-102 |
| Revisar checklist de PR para exigir EXPLAIN ANALYZE | Processo | P2 | @time | JIRA-103 |
```
