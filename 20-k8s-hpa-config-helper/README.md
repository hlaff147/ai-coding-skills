# 📈 Kubernetes HPA Config Helper (HPA v2)

> **Gera manifestos modernos de Horizontal Pod Autoscaler (HPA v2) no Kubernetes, configurando políticas de estabilização para evitar flapping e garantir alta disponibilidade.**

---

## 🎯 O Problema

- **Flapping / Thrashing**: O tráfego sobe rapidamente, o HPA cria pods; o tráfego oscila por 30 segundos, o HPA destrói pods prematuramente, forçando novos cold-starts na JVM.
- **Single Point of Failure**: Configurar `minReplicas: 1` deixa a aplicação sem redundância caso o nó sofra reinício ou drain.
- **Métricas Inválidas para Java**: Tentar usar consumo de memória como gatilho de autoscaling para JVM faz com que o HPA nunca reduza réplicas, pois a JVM não libera memória de Heap imediatamente para o sistema operacional.

---

## ✅ A Solução

Esta skill padroniza a criação de HPAs resilientes:
1. **API `autoscaling/v2`**: Suporte total a múltiplas métricas e blocos `behavior`.
2. **Estabilização de Scale-Down**: Janela de 300 segundos para proteger o cluster contra degradações transitórias.
3. **Escala Rápida (Scale-Up)**: Resposta agressiva em picos de tráfego com `stabilizationWindowSeconds: 0`.

---

## 🔧 Formatos Suportados
- **Antigravity / Gemini:** `SKILL.md`
- **Cursor:** `.cursorrules`
- **GitHub Copilot:** `copilot-instructions.md`
