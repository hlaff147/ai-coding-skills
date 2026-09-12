# 📝 Incident Postmortem & RCA Writer

> **Estrutura relatórios técnicos pós-incidente (*Blameless Postmortem*) com linha do tempo precisa, análise de 5 Porquês e matriz de ações preventivas mensuráveis.**

---

## 🎯 O Problema

- **Caça às Bruxas (Finger-Pointing)**: Relatórios que focam em "quem errou o commit" geram insegurança psicológica e não corrigem a causa estrutural que permitiu a falha.
- **Linha do Tempo Inconsistente**: Dificuldade em reconstruir a ordem exata dos acontecimentos, dificultando a medição de MTTA (Mean Time to Acknowledge) e MTTR (Mean Time to Resolve).
- **Ações Preventivas Esquecidas**: Planos de ação vagos como "melhorar testes", sem dono, sem prioridade e sem ticket no backlog, garantem que o mesmo incidente se repita no futuro.

---

## ✅ A Solução

Esta skill guia a criação de postmortems de nível sênior:
1. **Tom Construtivo e Sistêmico**: Foco em resiliência arquitetural e observabilidade.
2. **Método dos 5 Porquês**: Desce da falha superficial até o gap de processo ou salvaguarda.
3. **Plano SMART**: Tabela com Ação, Tipo, Prioridade, Responsável e Ticket.

---

## 🔧 Formatos Suportados
- **Antigravity / Gemini:** `SKILL.md`
- **Cursor:** `.cursorrules`
- **GitHub Copilot:** `copilot-instructions.md`
