---
name: k8s-hpa-config-helper
description: >-
  Gera e ajusta manifestos de Horizontal Pod Autoscaler (HPA v2) no Kubernetes com controle de janelas de estabilização e métricas de CPU e customizadas. Acione ao configurar autoscaling ou criar HPA.
---

# 📈 Kubernetes HPA Config Helper (HPA v2)

Gera e refina manifestos de Horizontal Pod Autoscaler (`autoscaling/v2`) no Kubernetes com métricas precisas, janelas de estabilização para evitar flapping e boas práticas de alta disponibilidade.

---

## 🚫 Restrições Negativas Críticas

- **NUNCA use `minReplicas: 1` em microsserviços de produção**: Sempre defina `minReplicas: 2` ou `3` para tolerância a falhas e distribuição entre Availability Zones (AZs).
- **NUNCA use memória como métrica primária isolada de autoscaling para Java**: A JVM retém memória comitada mesmo após GC; usar memória como gatilho de scale-down gera comportamento errático e flapping.
- **NUNCA omita a janela de estabilização de `scaleDown`**: Deixar o default sem janela controlada causa desalocação prematura de pods em flutuações rápidas de carga.
- **NUNCA configure HPA em Deployment sem `resources.requests` definidos**: O HPA calcula percentuais baseado no `requests.cpu`. Sem request, o HPA falhará com status `Unknown`.

---

## 📋 Manifesto Padrão HPA v2 (Produção)

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: order-service-hpa
  namespace: default
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: order-service
  minReplicas: 3
  maxReplicas: 15
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 70
  behavior:
    scaleUp:
      stabilizationWindowSeconds: 0 # Resposta rápida a picos
      policies:
        - type: Percent
          value: 100
          periodSeconds: 15
    scaleDown:
      stabilizationWindowSeconds: 300 # 5 min para evitar flapping
      policies:
        - type: Percent
          value: 20
          periodSeconds: 60
```

---

## 🔍 Comandos de Validação de HPA
```bash
# Inspecionar status de métricas e réplicas do HPA
kubectl get hpa order-service-hpa

# Ver eventos e cálculos de escalonamento detalhados
kubectl describe hpa order-service-hpa
```
