---
name: daily-standup-summary
description: >-
  Gera resumos concisos e profissionais para Daily Standup (ontem, hoje, bloqueios) a partir de commits,
  MRs abertos, cards de Kanban ou notas rápidas. Acione quando o usuário pedir para montar, gerar,
  resumir ou redigir o status diário para a reunião de daily, Slack ou Microsoft Teams.
---

# 📅 Daily Standup Summary Generator

Transforma anotações soltas, histórico recente de commits e status de cards em um resumo de Daily Standup profissional, conciso e orientado a resultados (Ontem, Hoje, Impedimentos).

---

## 🚫 Restrições Negativas Críticas

- **NUNCA crie listas prolixas**: Daily standup não é relatório de horas; limite cada seção a 2-4 itens de impacto real.
- **NUNCA liste tarefas triviais**: Evite mencionar "li e-mails", "participei de reuniões rotineiras" ou "configurei ambiente" a menos que seja um bloqueador crítico.
- **NUNCA oculte bloqueios**: Se houver dependência de terceiros (revisão de PR atrasada, permissão AWS pendente, ambiente instável), destaque explicitamente na seção de impedimentos com menção clara ao responsável/time.
- **NUNCA use linguagem passiva ou confusa**: Use verbos de ação no passado para ontem ("Concluí", "Ajustei", "Abri MR") e no futuro imediato para hoje ("Finalizo", "Valido", "Inicio").

---

## 📋 Protocolo de Síntese da Daily

Ao receber comandos rápidos como `"me ajuda com a daily"`, lista de commits ou prints de tarefas, siga esta estrutura:

### Formato Padrão para Slack / Teams

```markdown
*📌 Daily Standup — [Data ou Dia]*

*⏪ Ontem:*
• Concluí [tarefa/ticket] com [resultado ou MR aberto/aprovado].
• Avancei no desenvolvimento de [feature/investigação].

*⏩ Hoje:*
• Foco em [tarefa prioritária/finalização de MR].
• Validação em ambiente de UAT / homologação.

*🚧 Bloqueios & Dependências:*
• Nenhum impedimento técnico no momento.
_OU_
• ⚠️ Aguardando aprovação no MR `[ID-MR]` (revisores: @time) para merge e deploy.
• ⚠️ Bloqueado aguardando criação da fila SQS no ambiente de teste pelo time de Cloud/SRE.
```

---

## 💡 Adaptação por Canal de Comunicação

1. **Slack / Mattermost**: Use formatação compacta com bullet points (`•`) e negrito no padrão `*texto*`.
2. **Microsoft Teams**: Use markdown limpo ou formato em tópicos de fácil leitura mobile.
3. **Reunião Falada (Síncrona)**: Forneça também uma versão em 20 segundos para fala direta, sem jargões desnecessários.
