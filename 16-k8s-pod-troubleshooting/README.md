# ☸️ Kubernetes Pod Troubleshooting Guide

> **Roteiro guiado e sistemático para diagnosticar e mitigar CrashLoopBackOff, OOMKilled, Pending e falhas de probes no Kubernetes com foco em Java/Micronaut.**

---

## 🎯 O Problema

- **Tentativa e erro às cegas**: Reiniciar pods (`rollout restart`) sem verificar o motivo do crash mascara problemas que voltam a acontecer em produção sob carga.
- **Armadilhas de memória JVM vs Container**: A JVM aloca heap, mas também Metaspace, threads e buffers diretos (Netty). Quando o consumo total atinge o `limits.memory` do container, o Linux OOM Killer mata o processo com Exit Code 137.
- **Race conditions de inicialização**: Aplicações que executam migrações de banco ou esperam o sidecar do Istio (`istio-proxy`) frequentemente falham no `livenessProbe` antes de ficarem prontas.

---

## ✅ A Solução

Esta skill atua como um assistente de diagnóstico sênior:
1. **Analisa saídas de CLI**: Interpreta `kubectl describe pod` e `kubectl logs --previous`.
2. **Identifica a causa raiz exata**: Discrimina entre OOM do kernel, erro de inicialização de framework, ou saturação de nós.
3. **Oferece o patch de mitigação**: Gera o YAML corrigido (ajuste de `MaxRAMPercentage`, `startupProbe`, `resources.requests/limits`).

---

## 💬 Exemplo de Uso (Simulação)

### Entrada do Usuário:
```text
Meu pod de pagamentos em Micronaut está reiniciando sem parar.
Segue o trecho do describe:

    State:          Waiting
      Reason:       CrashLoopBackOff
    Last State:     Terminated
      Reason:       OOMKilled
      Exit Code:    137
      Started:      Fri, 12 Sep 2026 01:00:00 -0300
      Finished:     Fri, 12 Sep 2026 01:01:20 -0300
    Limits:
      memory:  512Mi
```

### Resposta Gerada pela Skill:
````markdown
### 🔍 Diagnóstico: OOMKilled (Exit Code 137)
O kernel Linux enviou um `SIGKILL` (128 + 9 = 137) porque o container ultrapassou o teto estrito de **512Mi** definido em `Limits.memory`. 

Em aplicações Java/Micronaut, a memória total é a soma de:
- **Heap Space**
- **Non-Heap:** Metaspace, Thread Stacks, Code Cache e buffers diretos do Netty (I/O).
Se a JVM não tiver um `MaxRAMPercentage` conservador, ela aloca heap próximo ao limite e a memória nativa estoura o cgroup.

---

### 🛠️ Comandos de Investigação
```bash
# 1. Checar se outros pods no namespace sofreram OOM recentemente
kubectl get pods -n pagamentos -o jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.status.containerStatuses[*].lastState.terminated.reason}{"\n"}{end}' | grep OOMKilled

# 2. Inspecionar logs da última execução antes do kill
kubectl logs payment-service-789bf-xzkl -n pagamentos --previous --tail=50
```

---

### 🩹 Solução Recomendada no Deployment

Aumente o `limits.memory` para dar margem à JVM e defina a flag `-XX:MaxRAMPercentage=70.0` para que o Heap utilize no máximo 70% do container, reservando 30% para Metaspace e Netty:

```yaml
spec:
  template:
    spec:
      containers:
        - name: payment-service
          resources:
            requests:
              cpu: "250m"
              memory: "512Mi"
            limits:
              cpu: "1000m"
              memory: "1024Mi" # Elevado para 1Gi
          env:
            - name: JAVA_TOOL_OPTIONS
              value: "-XX:MaxRAMPercentage=70.0 -XX:+ExitOnOutOfMemoryError"
```
````

---

## 🔧 Formatos Suportados
- **Antigravity / Gemini:** `SKILL.md`
- **Cursor:** `.cursorrules`
- **GitHub Copilot:** `copilot-instructions.md`
