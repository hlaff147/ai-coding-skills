---
name: hoppscotch-collection-generator
description: >-
  Gera coleções, environments e scripts de teste (pw.expect) para Hoppscotch a partir de controllers Micronaut, endpoints REST ou comandos curl. Acione ao pedir para criar collections ou testes no Hoppscotch.
---

# 🚀 Hoppscotch Collection & Test Generator

Gera coleções JSON prontas para importação no **Hoppscotch** (ferramenta open-source para desenvolvimento e teste de APIs) a partir de controllers Java/Micronaut, especificações OpenAPI ou comandos `curl`.

---

## 🚫 Restrições Negativas Críticas

- **NUNCA use a sintaxe de variáveis do Postman (`{{var}}`)**: No Hoppscotch, a sintaxe mandatória de variáveis de ambiente é com delimitadores duplos angulares `<<variavel>>`.
- **NUNCA use o objeto global `pm.*` em scripts**: O Hoppscotch utiliza exclusivamente o namespace **`pw.*`** (`pw.expect()`, `pw.env.set()`, `pw.env.get()`, `pw.response.status`, `pw.response.body`).
- **NUNCA faça hardcode de URLs de host**: Sempre utilize `<<baseUrl>>` no prefixo do endpoint (ex: `<<baseUrl>>/api/v1/vehicles`).
- **NUNCA gere JSON com trailing commas ou sintaxe inválida**: O payload gerado deve ser 100% compatível com a funcionalidade *Import Collection > From JSON* do Hoppscotch.

---

## 🧭 Mapeamento de Micronaut para Hoppscotch

| Anotação Micronaut | Mapeamento no Hoppscotch |
|---|---|
| `@Controller("/api/v1/orders")` | Prefixo da URL: `<<baseUrl>>/api/v1/orders` |
| `@Get("/{id}")` | `method: "GET"`, endpoint: `<<baseUrl>>/api/v1/orders/<<id>>` |
| `@Post` / `@Put` com `@Body` | `method: "POST"`, `body.contentType: "application/json"`, payload no body |
| `@QueryValue("status")` | Item no array `params: [{"key": "status", "value": "PENDING", "active": true}]` |
| `@Header("Authorization")` | Item no array `headers: [{"key": "Authorization", "value": "Bearer <<token>>"}]` |

---

## 🧪 Padrão de Scripts de Teste (`pw.*`)

Toda requisição gerada deve conter testes de asserção e encadeamento no campo `testScript`:

```javascript
// Validar status HTTP esperado
pw.expect(pw.response.status).toBe(200);

// Validar JSON body e encadear variáveis de ambiente
const data = JSON.parse(pw.response.body);
pw.expect(data).toBeDefined();

if (data.token) {
  pw.env.set("authToken", data.token);
}
if (data.id) {
  pw.env.set("entityId", data.id);
}
```

---

## 📋 Estrutura da Coleção
Gere sempre o bloco JSON na versão de schema `v: 2`.
📖 *Template e Schema de Referência Completo:* [references/hoppscotch-template.json](./references/hoppscotch-template.json)
