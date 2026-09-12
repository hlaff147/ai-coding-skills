# 📅 Daily Standup Summary Generator

> **Sintetiza commits recentes, status do git e cards do Kanban em um resumo de Daily Standup limpo, conciso e profissional para Slack, Teams ou reuniões síncronas.**

---

## 🎯 O Problema

- **Esquecimento na hora da reunião**: No calor da rotina de engenharia sênior, é comum esquecer exatamente o que foi finalizado no dia anterior ou falar sobre detalhes operacionais desnecessários.
- **Standups longas e cansativas**: Relatos prolixos dispersam o time e tiram o foco dos objetivos de entrega.
- **Impedimentos não verbalizados**: Dificuldade em explicitar bloqueios técnicos ou dependências de code review de forma clara e acionável.

---

## ✅ A Solução

Esta skill analisa rapidamente as últimas ações (commits, MRs ou notas fornecidas) e gera uma mensagem no formato padrão da indústria:
1. **Ontem**: Entregas reais e avanços palpáveis.
2. **Hoje**: Prioridade #1 do dia.
3. **Bloqueios**: Dependências externas ou aprovações necessárias.

---

## 💬 Exemplo de Uso (Simulação)

### Entrada do Usuário:
```text
Gera minha daily. Ontem terminei a migration do Aurora e subi o MR 142 do consumer SQS.
Hoje vou ajustar o HPA no K8s e esperar aprovação do MR. Sem bloqueios graves, só preciso de review.
```

### Resposta Gerada pela Skill:
```markdown
*📌 Daily Standup — Quarta-feira*

*⏪ Ontem:*
• Finalizei a migration Flyway para o cluster Aurora PostgreSQL.
• Abri o MR !142 com a implementação do retry e dead-letter queue no consumer SQS.

*⏩ Hoje:*
• Ajustar manifestos de HPA e requests/limits no Kubernetes para o serviço de mensageria.
• Acompanhar homologação em UAT assim que o MR !142 for integrado.

*🚧 Bloqueios & Dependências:*
• ⚠️ Aguardando aprovação no MR !142 para merge e deploy automatizado.
```

---

## 🔧 Formatos Suportados
- **Antigravity / Gemini:** `SKILL.md`
- **Cursor:** `.cursorrules`
- **GitHub Copilot:** `copilot-instructions.md`
