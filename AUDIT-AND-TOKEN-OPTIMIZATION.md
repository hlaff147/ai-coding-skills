# 📊 Framework de Auditoria, Conformidade & Otimização de Custo de Tokens

> **Framework e diretrizes para avaliar, auditar e otimizar AI Coding Skills em duas dimensões complementares: Conformidade Estrutural e Eficiência de Tokens (Progressive Disclosure).**

---

## 1. 🎯 Objetivo

As AI Coding Skills ensinam agentes (Cursor, Gemini/Antigravity, Claude Code, GitHub Copilot) a atuar como pares programadores especializados. No entanto, à medida que a biblioteca de skills cresce, dois riscos emergem:
1. **Divergência de Padrões:** Skills que perdem a estrutura consistente, têm gatilhos fracos ou carecem de regras negativas explícitas.
2. **Inchaço de Contexto e Custo de Tokens:** Inserção indiscriminada de boilerplate e documentação longa que consome a janela de contexto do LLM e encarece requisições desnecessariamente.

Este framework fornece um método objetivo e acionável para:
- Medir o custo de cada skill com base no modelo de **Progressive Disclosure** (Divulgação Progressiva).
- Diagnosticar os 8 problemas comuns de inchaço de tokens.
- Priorizar e validar refatorações sem perder a precisão do agente.

---

## 2. 🧱 As Duas Dimensões da Auditoria

### 2.1 Dimensão 1 — Conformidade com o Padrão
Toda skill deve atender à seguinte checklist de qualidade antes de ser considerada estável:

- [ ] **Frontmatter Completo:** Contém `name` (kebab-case) e `description` preenchidos.
- [ ] **Gatilho Robusto:** `description` cobre 2-3 sinônimos e formas distintas de pedir a tarefa (jargões reais do time).
- [ ] **Restrições Negativas Explícitas:** Seção `NEVER` / anti-padrões declarados no início.
- [ ] **Formato de Saída Fixo:** Template ou estrutura esperada definida para evitar que o modelo improvise formatos diferentes.
- [ ] **Zero Alucinação de Contexto:** Se faltar informação específica (tabela, fila, ticket), a skill instrui o agente a perguntar ou preencher com `[PREENCHER]`.
- [ ] **Portabilidade Multiformato:** Implementada nos 4 formatos (`SKILL.md`, `.cursorrules`, `copilot-instructions.md`, `README.md`).

---

### 2.2 Dimensão 2 — Otimização de Tokens (Progressive Disclosure)

O consumo de contexto de uma skill é dividido em **3 camadas funcionais**:

| Camada | O que contém | Quando é carregada | Impacto no Custo |
|---|---|---|---|
| **Camada 1: Metadata** | `name` + `description` | **Sempre**, em toda conversa | Custo fixo contínuo $\times$ quantidade total de skills |
| **Camada 2: Corpo da Skill** | Regras, restrições e passo a passo (`SKILL.md`) | Apenas quando a skill é **ativada** | Custo proporcional ao tamanho do arquivo por ativação |
| **Camada 3: Recursos Externos** | `references/`, `assets/`, `scripts/` | **Sob demanda**, apenas se referenciados | Custo zero até que o agente decida ler o arquivo |

#### 📏 Heurística Rápida de Medição
- **Palavras $\times$ 1,3 $\approx$ Tokens** (para mistura técnica português/inglês).
- **Metadata (`description`):** Ideal $\le$ **50 palavras** (~65 tokens). Acima de 80 palavras é considerado pesado.
- **Corpo (`SKILL.md`):**
  - **Até 100 linhas:** Custo baixo e ideal (~500 a 700 tokens).
  - **100 a 150 linhas:** Custo moderado; aceitável se indispensável no fluxo principal.
  - **Acima de 150 linhas:** Sinal de alerta; candidato imediato a extração de código para `references/`.

---

## 3. 🔍 Catálogo dos 8 Problemas Comuns de Custo & Soluções

| # | Problema | Sintoma | Causa / Efeito | Solução Recomendada |
|---|---|---|---|---|
| **1** | **Description Verbosa** | Description com mais de 70-100 palavras | Consome contexto em conversas que nem usam a skill | Reduzir para 2-3 frases objetivas com palavras-chave e sinônimos de ativação. |
| **2** | **SKILL.md Monolítico** | Arquivo único com >150 linhas cobrindo múltiplos fluxos | LLM lê todos os cenários mesmo usando apenas um | Dividir em subarquivos em `references/` e criar índice de decisão no `SKILL.md`. |
| **3** | **Boilerplate Extenso Embutido** | Classes Java inteiras ou YAMLs de 60+ linhas inlined | O modelo consome centenas de tokens lendo código estático | Mover exemplos longos para `references/code-examples.md` ou `assets/`. |
| **4** | **Conteúdo Duplicado** | Mesma convenção repetida em 5 skills diferentes | Desperdício de tokens e risco de divergência | Centralizar convenções compartilhadas em referências comuns. |
| **5** | **Exemplos Redundantes** | 4 ou mais exemplos quase idênticos no corpo | O agente aprende com 1 bom exemplo + 1 caso de borda | Limitar a 1-2 exemplos representativos (Happy Path + Edge Case). |
| **6** | **Over-triggering (Gatilho Amplo)** | Skill dispara em perguntas genéricas | Carregamento desnecessário do corpo | Especificar gatilhos no `description` para exigir menção explícita ao domínio. |
| **7** | **Skills Sobrepostas** | Duas skills resolvem tarefas quase idênticas | Duplicação de metadata e confusão de roteamento | Mesclar em uma única skill se o fluxo for contínuo. |
| **8** | **Ausência de Árvore de Decisão** | Agente lê tudo sem saber qual caminho seguir | Maior tempo de raciocínio e tokens de thinking | Incluir no topo do `SKILL.md`: *"Se cenário A $\rightarrow$ leia X; se cenário B $\rightarrow$ leia Y"*. |

---

## 4. 🗂️ Template Padrão de Auditoria por Skill

Para auditorias periódicas, utilize o seguinte template:

```markdown
### Auditoria: [nome-da-skill]

**1. Conformidade**
- [ ] Segue o padrão de 4 arquivos?
- [ ] Possui restrições negativas explícitas?
- [ ] Formato de saída fixo e padronizado?
- Pontos de melhoria: ...

**2. Métricas de Custo**
- Linhas do SKILL.md: ___ linhas
- Palavras da Description: ___ palavras
- Tokens Estimados: ~___ tokens
- Problemas Identificados: [#1, #2, #3...]

**3. Decisão de Ação**
- [ ] Manter como está (Custo baixo / Alta eficiência)
- [ ] Refatorar (Extrair exemplos para references/)
- [ ] Ajustar Description (Reduzir palavras de ativação)
- [ ] Arquivar / Mesclar
```

---

## 5. 🚦 Matriz de Priorização de Refatoração

```
                    ┌─────────────────────────┬─────────────────────────┐
                    │  Custo Alto             │  Custo Baixo            │
                    │  Uso Frequente          │  Uso Frequente          │
                    │                         │                         │
                    │  🔴 REFATORAR PRIMEIRO  │  🟢 NÃO MEXER           │
                    │  (Máxima economia real) │  (Já está eficiente)    │
                    ├─────────────────────────┼─────────────────────────┤
                    │  Custo Alto             │  Custo Baixo            │
                    │  Uso Raro               │  Uso Raro               │
                    │                         │                         │
                    │  🟡 ARQUIVAR OU DIVIDIR │  ⚪ BAIXA PRIORIDADE    │
                    │  (Esforço pode não valer│  (Revisar apenas se     │
                    │   a pena refatorar)     │   houver queixa)        │
                    └─────────────────────────┴─────────────────────────┘
```

> **Regra Prática de Retorno:** A refatoração só é vantajosa se:  
> `(Tokens economizados por chamada × Frequência semanal) > Esforço de manutenção e teste`.

---

## 6. 🔄 Checklist de Validação Pós-Refatoração

Após refatorar uma skill para reduzir tokens:
1. [ ] O número de linhas do `SKILL.md` caiu substancialmente?
2. [ ] A `description` continua disparando nos mesmos prompts reais de teste?
3. [ ] A qualidade e o rigor técnico das respostas continuam idênticos?
4. [ ] Todos os arquivos movidos para `references/` estão referenciados de forma navegável no `SKILL.md`?
5. [ ] Nenhuma regra negativa (`NEVER`) ou convenção crítica do time foi perdida?
