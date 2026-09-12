# 🔍 Java & Micronaut Senior Code Review Checklist

> **Checklist sistemática e bloqueante para code reviews em Java 21+ e Micronaut 4+, avaliando concorrência, AOT, prevenção de N+1 e segurança.**

---

## 🎯 O Problema

- **Revisões Superficiais**: Focar apenas em estilo de código (nomes de variáveis, identação) e deixar passar graves problemas arquiteturais.
- **Armadilhas de Reatividade e Netty**: Bloquear a thread principal do Netty com chamadas JDBC ou HTTP síncronas degrada a aplicação inteira sob carga.
- **Gargalos de Banco Ocultos**: Código com queries N+1 que funciona perfeitamente com 5 registros de teste em banco H2 local, mas derruba o PostgreSQL Aurora em produção.

---

## ✅ A Solução

Esta skill atua como um revisor de código sênior autônomo:
1. **Concorrência**: Valida isolamento de threads e segurança em singletons.
2. **Design de Dados**: Garante imutabilidade com Records e `@Valid`.
3. **Persistência**: Enforça consultas AOT sem N+1 e transações somente-leitura.
4. **Segurança**: Bloqueia vazamentos de credenciais e dados protegidos por LGPD/GDPR.

---

## 🔧 Formatos Suportados
- **Antigravity / Gemini:** `SKILL.md`
- **Cursor:** `.cursorrules`
- **GitHub Copilot:** `copilot-instructions.md`
