# 🚀 Hoppscotch Collection & Test Generator

> **Gera coleções JSON e scripts de teste automatizados (`pw.expect`) prontos para importação no Hoppscotch (alternativa open-source ao Postman/Insomnia) a partir de controllers Micronaut, endpoints REST ou comandos cURL.**

---

## 🎯 O Problema

- **Migração e Suporte Open-Source**: Muitos times estão migrando do Postman para o [Hoppscotch](https://hoppscotch.io) por ser open-source, leve e auto-hospedável, mas sofrem para recriar coleções manualmente endpoint por endpoint.
- **Incompatibilidade de Sintaxe**: Desenvolvedores e IAs habituados ao Postman erram ao gerar variáveis no formato `{{variavel}}` (quando o Hoppscotch exige `<<variavel>>`) e testes no objeto `pm.*` (quando o Hoppscotch utiliza `pw.*`).
- **Falta de Automação de Testes**: Endpoints são cadastrados sem scripts de validação de status HTTP ou encadeamento automático de tokens JWT.

---

## ✅ A Solução

Esta skill transforma código de controllers Java/Micronaut ou comandos `curl` diretamente no JSON nativo do Hoppscotch:
1. **Sintaxe Nativa**: Gera automaticamente variáveis `<<baseUrl>>` e `<<authToken>>`.
2. **Scripts de Teste `pw.*`**: Insere asserções automáticas (`pw.expect(pw.response.status).toBe(...)`) e encadeia IDs e tokens com `pw.env.set()`.
3. **Importação em 1 Clique**: Gera o arquivo JSON pronto para importar no menu *Collections > Import > From JSON* do Hoppscotch.

---

## 🔄 Tabela Comparativa: Postman vs Hoppscotch

| Recurso | Postman | Hoppscotch |
|---|---|---|
| **Interpolação de Variáveis** | `{{baseUrl}}/api/v1` | `<<baseUrl>>/api/v1` |
| **Namespace de Testes** | `pm.expect(...)` | `pw.expect(...)` |
| **Definir Variável de Ambiente** | `pm.environment.set("k", "v")` | `pw.env.set("k", "v")` |
| **Ler Variável de Ambiente** | `pm.environment.get("k")` | `pw.env.get("k")` |
| **Status HTTP** | `pm.response.to.have.status(200)` | `pw.expect(pw.response.status).toBe(200)` |
| **Licenciamento** | Proprietário / Freemium | Open Source (MIT) / Self-hostable |

---

## 💬 Exemplo de Uso (Simulação)

### Entrada do Usuário:
```text
Crie uma collection do Hoppscotch para o endpoint de autenticação e consulta de usuários:
POST /api/v1/auth/login -> retorna { "token": "jwt..." }
GET /api/v1/users/{id} -> requer Bearer token
```

### Saída Gerada:
Gera o bloco JSON no padrão v2 com a pasta `Auth` e `Users`, populando os headers de `Authorization: Bearer <<authToken>>`, o body da requisição e os scripts `pw.env.set("authToken", data.token)`.

Consulte o template de referência em [references/hoppscotch-template.json](./references/hoppscotch-template.json).

---

## 🔧 Formatos Suportados
- **Antigravity / Gemini:** `SKILL.md`
- **Cursor:** `.cursorrules`
- **GitHub Copilot:** `copilot-instructions.md`
