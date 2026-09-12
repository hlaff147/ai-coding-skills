---
name: mr-description-generator
description: >-
  Gera descrições estruturadas de Merge Request (MR) e Pull Request (PR) no GitLab a partir de diffs, commits ou notas. Acione ao pedir para criar, resumir, revisar ou formatar a descrição de um MR/PR.
---

# 🚀 GitLab Merge Request Description Generator

Gera descrições técnicas, estruturadas e completas para Merge Requests no GitLab (ou Pull Requests), reduzindo o tempo de code review e elevando o padrão de documentação técnica do time.

---

## 🚫 Restrições Negativas Críticas

- **NUNCA gere descrições genéricas**: Evite frases vagas como "ajustes no backend", "correções diversas" ou "update code".
- **NUNCA omita a seção de testes**: Todo MR de nível sênior deve conter passos reproduzíveis de teste ou evidências de testes unitários/integrados.
- **NUNCA assuma riscos como zero**: Se houver alteração de banco de dados, variáveis de ambiente, tópicos SQS/SNS ou manifesto K8s, declare o risco e o plano de rollback.
- **NUNCA alucine nomes de tabelas ou serviços**: Se faltar informação contextual (ex: número do ticket Jira ou nome exato da fila), inclua um placeholder explícito `[PREENCHER: ...]` em vez de inventar dados.

---

## 📋 Protocolo de Geração de MR

Quando o usuário solicitar uma descrição de MR fornecendo diffs, commits ou texto livre, siga estes passos:

### Passo 1: Analisar o Escopo das Mudanças
Identifique:
- Tipo de alteração (Feature, Bugfix, Refactor, Performance, Infra/CI).
- Camadas afetadas (Micronaut Controller, Service, Repository, Kafka/SQS Consumer, K8s manifests, DDL Flyway).
- Se há breaking changes ou dependências entre deploys.

### Passo 2: Estruturar a Saída
Preencha rigorosamente o **Template Padrão de MR**:

```markdown
## 🎯 Contexto e Motivação
<!-- Por que esta mudança é necessária? Qual problema resolve ou qual valor de negócio entrega? -->
- **Issue/Ticket:** `[PREENCHER ex: BACK-1234]`
- **Tipo:** `[Feature | Bugfix | Refactor | Performance | Infra]`
- **Resumo:** Breve descrição do objetivo da mudança.

---

## 🛠️ O que foi feito?
<!-- Detalhes técnicos organizados por responsabilidade -->
- **[Componente/Domínio]:** Descrição clara da alteração (ex: adicionado retry exponencial no consumer SQS).
- **[Config/Infra]:** Novas variáveis de ambiente, ajustes de memory limit ou tópicos criados.
- **[Database]:** Migration Flyway VXX__... criada (se aplicável).

---

## 🧪 Como Testar / Evidências
<!-- Passos claros e reproduzíveis para o revisor validar a mudança -->
1. Subir aplicação local ou apontar para ambiente de teste.
2. Executar o fluxo:
   ```bash
   curl -X POST http://localhost:8080/api/v1/... \
     -H "Content-Type: application/json" \
     -d '{"exemplo": "payload"}'
   ```
3. Verificar processamento na fila/banco/logs.
- [ ] Testes unitários executados (`./gradlew test` ou `mvn test`)
- [ ] Testes integrados com Testcontainers / LocalStack executados

---

## ⚠️ Avaliação de Risco & Rollback
- **Nível de Risco:** `[Baixo | Médio | Alto]`
- **Breaking Changes:** `[Sim | Não]`
- **Impacto em Produção:** Descrição do impacto se houver falha.
- **Plano de Rollback:** Reverter commit e aplicar deploy da versão anterior / Reverter migration Flyway.

---

## 🚢 Checklist Pré-Merge
- [ ] Código aderente aos padrões de arquitetura (Micronaut AOT / Java 21)
- [ ] Sem secrets ou chaves expostas
- [ ] Logs estruturados sem vazamento de dados sensíveis (PII/LGPD)
- [ ] Tags de deploy verificadas (`#deployuat #auto` se aplicável)
```

---

## 💡 Dicas de Ativação
- Se o usuário fornecer apenas `git log`, extraia a intenção e os arquivos tocados para estruturar a seção "O que foi feito".
- Mantenha o tom profissional, claro e objetivo.
