---
name: k8s-pod-troubleshooting
description: >-
  Diagnostica falhas e erros de pods no Kubernetes (CrashLoopBackOff, OOMKilled, Pending, ImagePullBackOff,
  CreateContainerConfigError, falhas de liveness/readiness probes). Acione sempre que o usuário colar saídas de
  kubectl describe pod, kubectl logs, eventos de cluster ou relatar pods em estado de erro ou reinício contínuo.
---

# ☸️ Kubernetes Pod Troubleshooting Guide

Guia especializado e sistemático para identificar, diagnosticar e mitigar problemas de execução de pods no Kubernetes, com foco em microsserviços Java/Micronaut e arquitetura Cloud.

---

## 🚫 Restrições Negativas Críticas

- **NUNCA sugira reiniciar pods às cegas**: Não responda apenas "tente dar rollout restart" sem antes identificar a causa raiz (logs anteriores, eventos do pod ou limites de recursos).
- **NUNCA confunda Exit Code 137 com erro de aplicação**: Exit Code 137 é SIGKILL disparado pelo kernel por OOM (Out Of Memory) no cgroup do container, exigindo ajuste na relação entre `-Xmx` da JVM e `limits.memory` do K8s.
- **NUNCA ignore o container anterior**: Em `CrashLoopBackOff`, sempre verifique os logs do container encerrado com `kubectl logs <pod> --previous`.
- **NUNCA ignore a inicialização do Istio Sidecar**: Se o cluster utilizar Istio/Service Mesh, verifique se a aplicação falhou ao tentar chamar dependências externas (banco/AWS) antes do `istio-proxy` estar pronto (`holdApplicationUntilProxyStarts`).

---

## 🧭 Matriz de Diagnóstico Rápido

| Sintoma / Estado | Causa Mais Provável | Comando de Investigação Primário |
|---|---|---|
| **OOMKilled (Exit 137)** | Consumo total (Heap + Metaspace + Netty direct memory) excedeu `limits.memory`. | `kubectl describe pod <nome> \| grep -E "(Exit Code|OOMKilled|Limits)"` |
| **CrashLoopBackOff (Exit 1)** | Exceção não tratada na inicialização (falha ao conectar no DB Aurora, falta de ENV, erro de parsing). | `kubectl logs <nome> --previous` |
| **CrashLoopBackOff (Exit 143)** | SIGTERM gracioso seguido de timeout de terminação ou probe falhando repetidamente. | `kubectl describe pod <nome> \| grep -A 5 "Liveness"` |
| **Pending** | Falta de recursos no nó (CPU/Memory), `nodeSelector` / `tolerations` incompatíveis ou PVC não anexado. | `kubectl describe pod <nome> \| grep -A 10 "Events:"` |
| **ImagePullBackOff** | Imagem inexistente no registry (ECR), tag errada ou falta de permissão de pull (`imagePullSecrets`). | `kubectl describe pod <nome> \| grep -A 5 "Failed to pull image"` |
| **CreateContainerConfigError** | Secret ou ConfigMap referenciado no `envFrom` ou `volumeMounts` não existe no namespace. | `kubectl get configmap,secret -n <namespace>` |

---

## 📋 Protocolo de Análise e Resposta

Sempre estruture o diagnóstico em 3 blocos:

### 1. 🔍 Causa Raiz Identificada
Identifique o motivo exato com base nos eventos e códigos de saída fornecidos.
*Exemplo: "O pod foi encerrado com Exit Code 137 (OOMKilled). O container atingiu o teto de 512Mi definido em `resources.limits.memory`."*

### 2. 🛠️ Ações Imediatas de Investigação (CLI)
Forneça os comandos exatos para obter mais telemetria:
```bash
# Inspecionar eventos de terminação e limites
kubectl describe pod <pod-name> -n <namespace>

# Ver logs do crash anterior
kubectl logs <pod-name> -n <namespace> -c <container-name> --previous --tail=100

# Verificar uso real de recursos se o pod estiver vivo
kubectl top pod <pod-name> -n <namespace> --containers
```

### 3. 🩹 Solução Recomendada no Manifesto
Apresente o patch em YAML ou configuração da JVM/Micronaut.

#### Caso Clássico: JVM OOMKilled no Kubernetes
```yaml
# spec.template.spec.containers[0]
resources:
  requests:
    cpu: "250m"
    memory: "768Mi"
  limits:
    cpu: "1000m"
    memory: "1024Mi"
env:
  - name: JAVA_TOOL_OPTIONS
    # Reservar margem para Metaspace, threads e Netty buffer: MaxRAMPercentage ~ 70%
    value: "-XX:MaxRAMPercentage=70.0 -XX:+UseG1GC"
```

#### Caso Clássico: Probe Failure durante Inicialização
Se o Micronaut demora a iniciar devido à conexão com banco Aurora ou migrações Flyway:
```yaml
startupProbe:
  httpGet:
    path: /health/liveness
    port: 8080
  initialDelaySeconds: 10
  periodSeconds: 5
  failureThreshold: 12  # Dá até 60s extras para inicialização sem matar o pod
livenessProbe:
  httpGet:
    path: /health/liveness
    port: 8080
  periodSeconds: 10
```
