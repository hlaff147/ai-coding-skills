# ⚖️ Kubernetes Resource Sizing Guide (Java / Micronaut)

> **Cálculo metódico de requests e limits de CPU e memória para microsserviços Java no Kubernetes, evitando CPU Throttling e OOMKilled.**

---

## 🎯 O Problema

- **OOMKilled da JVM**: Configurar memória no Kubernetes achando que o container só gasta Heap. O Linux cgroup mata o container (Exit Code 137) ao somar Metaspace, threads e buffers diretos.
- **CPU Throttling Silencioso**: `limits.cpu` muito agressivos ativam o limitador de quota CFS do kernel Linux, gerando latências absurdas mesmo quando o cluster está com 80% de CPU livre.
- **Despejos (Evictions)**: Nós sob pressão de memória descartam pods com QoS `Burstable` (onde requests são muito menores que limits).

---

## ✅ A Solução

Esta skill fornece fórmulas matemáticas claras e manifestos prontos para produção:
1. **Fórmula de Headroom da JVM**: Resguardo de 30% para off-heap e Netty I/O.
2. **QoS Anti-Eviction**: Alinhamento de requests e limits de memória.
3. **Bursting Seguro de CPU**: Requests balizados no p95 e limits folgados para startup.

---

## 🔧 Formatos Suportados
- **Antigravity / Gemini:** `SKILL.md`
- **Cursor:** `.cursorrules`
- **GitHub Copilot:** `copilot-instructions.md`
