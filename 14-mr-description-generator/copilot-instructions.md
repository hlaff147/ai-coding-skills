# GitLab Merge Request Description Generator (GitHub Copilot)

Whenever asked to generate or write a Pull Request (PR) or GitLab Merge Request (MR) description:

1. **Structure the description into standard senior engineering sections**:
   - **🎯 Contexto e Motivação**: Business justification, ticket ID, and category (Feature, Bugfix, Refactor, Infra).
   - **🛠️ O que foi feito**: Bulleted list organized by layer/component describing technical modifications.
   - **🧪 Como Testar / Evidências**: Concrete testing steps (curl requests, unit test commands, test scenarios).
   - **⚠️ Avaliação de Risco & Rollback**: Risk level, breaking changes, and rollback instructions.
   - **🚢 Checklist Pré-Merge**: Quality checklist including deploy tags (#deployuat #auto) and secrets checking.

2. **Negative Constraints**:
   - Never generate vague summaries ("fixed bugs", "updated code").
   - Never omit test execution steps.
   - Never invent non-existent tickets, tables, or microservice names without flagging them as placeholders `[PREENCHER]`.
