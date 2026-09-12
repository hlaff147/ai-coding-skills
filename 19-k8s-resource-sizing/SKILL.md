---
name: k8s-resource-sizing
description: >-
  Calcula e ajusta requests e limits de CPU e Memória para pods no Kubernetes, evitando OOMKilled e CPU Throttling em microsserviços Java/Micronaut. Acione ao pedir dimensionamento de recursos ou tuning de specs K8s.
---

# ⚖️ Kubernetes Resource Sizing Guide (Java / Micronaut)

Guia de dimensionamento e cálculo de `resources.requests` e `resources.limits` no Kubernetes para microsserviços Java e Micronaut, prevenindo CPU Throttling e OOMKilled (Exit 137).

---

## 🚫 Restrições Negativas Críticas

- **NUNCA iguale o `-Xmx` da JVM ao `limits.memory` do container**: A JVM consome memória além do Heap (Metaspace, Thread Stacks, CodeCache e buffers diretos do Netty). Deixar menos de 25-30% de margem resulta em OOMKilled imediato.
- **NUNCA defina `limits.cpu` excessivamente baixo**: O Completely Fair Scheduler (CFS) do Linux aplica throttling severo de CPU em ciclos de 100ms, aumentando latência p99 mesmo com o nó ocioso.
- **NUNCA dimensione apenas pelo consumo médio**: Sempre use como referência o percentil **p95 ou p99** de carga (via New Relic, Datadog ou Prometheus).

---

## 🧮 Fórmula de Cálculo de Memória para JVM

```
Container Memory Limit = Heap + Metaspace + Threads + Off-Heap / Netty + Margem de SO
                       ≈ Heap / 0.70  (Margem de 30% para non-heap)
```

### Exemplo Prático: Microsserviço com Heap de 512Mi
- **Heap Max:** `512Mi`
- **Metaspace + Threads (50 threads x 1Mi) + Netty:** `~200Mi`
- **Container `limits.memory` recomendado:** `768Mi` ou `1024Mi`
- **Configuração JVM:** `-XX:MaxRAMPercentage=70.0 -XX:+ExitOnOutOfMemoryError`

---

## 📋 Padrão de Manifesto Recomendado

```yaml
spec:
  template:
    spec:
      containers:
        - name: app-service
          resources:
            requests:
              cpu: "300m"       # Baseado na média + 20% do New Relic
              memory: "768Mi"   # Igual ao limit para QoS 'Guaranteed' anti-eviction
            limits:
              cpu: "1500m"      # Folga para pikes de CPU e startup rápido
              memory: "768Mi"
          env:
            - name: JAVA_TOOL_OPTIONS
              value: "-XX:MaxRAMPercentage=70.0 -XX:+UseG1GC -XX:+ExitOnOutOfMemoryError"
```

---

## 🔍 Comandos de Verificação em Produção
```bash
# Verificar se há CPU Throttling ativo no container
kubectl top pod <pod-name> -n <namespace>

# Inspecionar métricas de throttling no container
kubectl exec <pod-name> -n <namespace> -- cat /sys/fs/cgroup/cpu.stat
```
